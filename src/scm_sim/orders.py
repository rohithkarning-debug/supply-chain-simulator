from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict
from scm_sim.inventory import Inventory, InsufficientStockError

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    FULFILLED = "FULFILLED"
    BACKORDERED = "BACKORDERED"
    CANCELLED = "CANCELLED"

@dataclass
class Order:
    order_id: str
    customer_id: str
    warehouse_id: str
    sku: str
    quantity: int
    created_day: int
    status: OrderStatus = OrderStatus.PENDING
    fulfilled_day: Optional[int] = None

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Order quantity must be greater than 0.")

class OrderManager:
    """Manages creation, fulfillment and cancellation of orders."""
    
    def __init__(self, inventory: Inventory):
        self.inventory = inventory
        self._orders: Dict[str, Order] = {}
        self._next_id = 1
        
    def create(self, customer_id: str, warehouse_id: str, sku: str, quantity: int, day: int) -> Order:
        """Creates a new order and assigns it an ID."""
        order_id = f"ORD-{self._next_id:04d}"
        self._next_id += 1
        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            warehouse_id=warehouse_id,
            sku=sku,
            quantity=quantity,
            created_day=day
        )
        self._orders[order_id] = order
        return order
        
    def get(self, order_id: str) -> Order:
        """Retrieves an order by its ID."""
        if order_id not in self._orders:
            raise KeyError(f"Order {order_id} not found.")
        return self._orders[order_id]
        
    def try_fulfil(self, order: Order, day: int) -> bool:
        """
        Attempts to fulfill the given order.
        If stock is sufficient, removes the stock and marks as FULFILLED.
        If stock is insufficient, marks as BACKORDERED.
        Returns True if fulfilled, False otherwise.
        """
        if order.status in (OrderStatus.FULFILLED, OrderStatus.CANCELLED):
            return False
            
        current_stock = self.inventory.level(order.warehouse_id, order.sku)
        if current_stock >= order.quantity:
            self.inventory.remove(order.warehouse_id, order.sku, order.quantity)
            order.status = OrderStatus.FULFILLED
            order.fulfilled_day = day
            return True
        else:
            order.status = OrderStatus.BACKORDERED
            return False
            
    def process_open(self, day: int) -> List[Order]:
        """
        Retries all PENDING and BACKORDERED orders.
        Oldest orders are processed first (sorted by created_day, then order_id).
        Returns a list of orders that were successfully fulfilled.
        """
        open_orders = [
            order for order in self._orders.values() 
            if order.status in (OrderStatus.PENDING, OrderStatus.BACKORDERED)
        ]
        open_orders.sort(key=lambda o: (o.created_day, o.order_id))
        
        newly_fulfilled = []
        for order in open_orders:
            if self.try_fulfil(order, day):
                newly_fulfilled.append(order)
                
        return newly_fulfilled
        
    def cancel(self, order_id: str) -> Order:
        """
        Cancels the specified order.
        Raises ValueError if the order is already fulfilled.
        """
        order = self.get(order_id)
        if order.status == OrderStatus.FULFILLED:
            raise ValueError("Cannot cancel an already fulfilled order.")
        order.status = OrderStatus.CANCELLED
        return order
        
    def by_status(self, status: OrderStatus) -> List[Order]:
        """Returns all orders with the given status."""
        return [order for order in self._orders.values() if order.status == status]
