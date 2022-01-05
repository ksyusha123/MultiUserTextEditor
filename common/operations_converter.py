from common.operations import *


def _insert_insert(insert1: InsertOperation, insert2: InsertOperation) -> InsertOperation:
    if insert1.index < insert2.index:
        return insert1
    return InsertOperation(insert1.index + len(insert1.text_to_insert), insert1.text_to_insert)


def _insert_delete(insert: InsertOperation, delete: DeleteOperation) -> DeleteOperation:
    if insert.index > delete.index:
        return delete
    return DeleteOperation(delete.index + len(insert.text_to_insert))


def _delete_insert(delete: DeleteOperation, insert: InsertOperation) -> InsertOperation:
    if delete.index < insert.index:
        return InsertOperation(insert.index - len(insert.text_to_insert), insert.text_to_insert)
    return insert


def _delete_delete(delete1, delete2):
    if delete1.index < delete2.index:
        return delete1
    elif delete1.index > delete2.index:
        return DeleteOperation(delete1.index - 1)
    return None


def convert_operation(operation, previous_operation):
    if not previous_operation or type(previous_operation) is CreateServerOperation:
        return operation
    if type(previous_operation) is InsertOperation:
        if type(operation) is InsertOperation:
            operation_to_perform = _insert_insert(previous_operation,
                                                  operation)
        elif type(operation) is DeleteOperation:
            operation_to_perform = _insert_delete(previous_operation,
                                                  operation)
    elif type(previous_operation) is DeleteOperation:
        if type(operation) is InsertOperation:
            operation_to_perform = _delete_insert(previous_operation,
                                                  operation)
        elif type(operation) is DeleteOperation:
            operation_to_perform = _delete_delete(previous_operation,
                                                  operation)
    return operation_to_perform
