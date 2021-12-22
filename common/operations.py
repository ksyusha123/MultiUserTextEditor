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
    def to_json(self):
        pass

    def __init__(self, name, index, text):
        self.name = name
        self.text = text
        self.index = index

    def do(self):
        pass

    def redo(self):
        pass


class CreateServerOperation(Operation):
    def to_json(self):
        pass

    def __init__(self, file):
        self.file = file

    def do(self):
        pass

    def redo(self):
        pass


class DeleteOperation(Operation):
    def to_json(self):
        pass

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


def operation_from_json(dict):
    if dict['name'] == 'Insert':
        return InsertOperation(dict['name'], dict['text'], dict['index'])
