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
    def to_dict(self):
        pass

    def __init__(self, index, text):
        self.name = 'Insert'
        self.text = text
        self.index = index

    def do(self):
        pass

    def redo(self):
        pass


class CreateServerOperation(Operation):

    def to_dict(self):
        return {
            'name': self.name,
            'file': self.file
        }

    def __init__(self, file):
        self.file = file
        self.name = 'Create'

    def do(self):
        pass

    def redo(self):
        pass


class DeleteOperation(Operation):
    def to_dict(self):
        return {
            'name': self.name,
            'index': self.index
        }

    def __init__(self, index):
        self.index = index
        self.name = 'Delete'

    def redo(self):
        raise NotImplementedError

    def do(self):
        pass


# class StyleOperation(Operation):
#     def redo(self):
#         pass
#
#     def do(self):
#         pass


def operation_from_json(dict):
    if dict['name'] == 'Insert':
        return InsertOperation(dict['text'], dict['index'])
    if dict['name'] == 'Delete':
        return DeleteOperation(dict['index'])
    if dict['name'] == 'Create':
        return CreateServerOperation(dict['file'])
