from common.operations import InsertOperation, DeleteOperation


def insert_insert(insert1: InsertOperation, insert2: InsertOperation) -> InsertOperation:
    if insert1.index < insert2.index:
        return insert1
    return InsertOperation(insert1.index + 1, insert1.symbol)


def insert_delete(insert: InsertOperation, delete: DeleteOperation) -> DeleteOperation:
    if insert.index > delete.index:
        return delete
    return DeleteOperation(delete.index + 1)


def delete_insert(delete: DeleteOperation, insert: InsertOperation) -> InsertOperation:
    if delete.index < insert.index:
        return InsertOperation(insert.index - 1, insert.symbol)
    return insert


def delete_delete(delete1, delete2):
    if delete1.index < delete2.index:
        return delete1
    elif delete1.index > delete2.index:
        return DeleteOperation(delete1.index - 1)
    return None
