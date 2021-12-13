from abc import ABCMeta, abstractmethod


class Operation:
    __metaclass__ = ABCMeta

    @abstractmethod
    def do(self):
        pass

    @abstractmethod
    def redo(self):
        pass


class InsertOperation(Operation):
    def __init__(self, index, symbol):
        self.symbol = symbol
        self.index = index

    def do(self):
        pass

    def redo(self):
        pass


class DeleteOperation(Operation):
    def __init__(self, index):
        self.index = index

    def redo(self):
        pass

    def do(self):
        pass


class StyleOperation(Operation):
    def redo(self):
        pass

    def do(self):
        pass
