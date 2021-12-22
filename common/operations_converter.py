from client.operations import InsertOperation, DeleteOperation


def _insert_insert(insert1: InsertOperation, insert2: InsertOperation) -> InsertOperation:
    if insert1.index < insert2.index:
        return insert1
    return InsertOperation(insert1.index + len(insert1.text), insert1.text)


def _insert_delete(insert: InsertOperation, delete: DeleteOperation) -> DeleteOperation:
    if insert.index > delete.index:
        return delete
    return DeleteOperation(delete.index + len(insert.text))


def _delete_insert(delete: DeleteOperation, insert: InsertOperation) -> InsertOperation:
    if delete.index < insert.index:
        return InsertOperation(insert.index - len(insert.text), insert.text)
    return insert


def _delete_delete(delete1, delete2):
    if delete1.index < delete2.index:
        return delete1
    elif delete1.index > delete2.index:
        return DeleteOperation(delete1.index - 1)
    return None


def convert_operation(self, operation, previous_operation):
    if previous_operation is InsertOperation:
        if operation is InsertOperation:
            operation_to_perform = _insert_insert(previous_operation,
                                                  operation)
        else:
            operation_to_perform = _insert_delete(previous_operation,
                                                  operation)
    else:
        if operation is InsertOperation:
            operation_to_perform = _delete_insert(previous_operation,
                                                  operation)
        else:
            operation_to_perform = _delete_delete(previous_operation,
                                                  operation)
    return operation_to_perform
