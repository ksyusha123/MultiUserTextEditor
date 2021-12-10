class Operation:
    def __init__(self, type, symbol, index):
        self.type = type
        self.symbol = symbol
        self.index = index

    def do(self):
        pass

    def redo(self):
        pass


class InsertOperation(Operation):
    pass


class RemoveOperation(Operation):
    pass


class StyleOperation(Operation):
    pass
