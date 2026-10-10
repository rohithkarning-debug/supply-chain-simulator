class InsufficientStockError(Exception):
    pass

class Inventory:
    def __init__(self):
        self._stock = {}

    def level(self, warehouse, sku):
        return self._stock.get((warehouse, sku), 0)

    def add(self, warehouse, sku, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._stock[(warehouse, sku)] = self.level(warehouse, sku) + qty
        return self.level(warehouse, sku)

    def remove(self, warehouse, sku, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        if qty > self.level(warehouse, sku):
            raise InsufficientStockError(f"not enough {sku} at {warehouse}")
        self._stock[(warehouse, sku)] -= qty
        return self.level(warehouse, sku)

    def is_stockout(self, warehouse, sku):
        return self.level(warehouse, sku) == 0
