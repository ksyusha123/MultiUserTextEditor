from abc import ABCMeta, abstractmethod, ABC


class Operation:
    __metaclass__ = ABCMeta

    @abstractmethod
    def do(self):
        pass

    @abstractmethod
    def redo(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass


class InsertOperation(Operation):
    def __init__(self, index, symbol):
        self.symbol = symbol
        self.index = index

    def do(self):
        pass

    def redo(self):
        pass


class CreateServerOperation(Operation):
    def __init__(self, file):
        self.file = file

    def do(self):
        pass

    def redo(self):
        pass


class DeleteOperation(Operation):
    def __init__(self, index):
        self.index = index

    def redo(self):
        raise NotImplementedError

    def do(self):
        pass


class StyleOperation(Operation):
    def redo(self):
        pass

    def do(self):
        pass
