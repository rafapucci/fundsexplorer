class Fund:
    def __init__(self, fund, operation_type, quantity, price, taxes, date):
        self.fund = fund
        self.operation_type = operation_type
        self.quantity = quantity
        self.price = price
        self.taxes = taxes
        self.date = date