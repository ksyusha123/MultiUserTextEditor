from client.operations import InsertOperation, DeleteOperation


def insert_insert(insert1, insert2):
    if insert1.index < insert2.index:
        return insert1
    return InsertOperation(insert1.index + 1, insert1.symbol)


def insert_delete(insert, delete):
    if insert.index <= delete.index:
        return insert
    return InsertOperation(insert.index - 1, insert.symbol)


def delete_insert(delete, insert):
    if delete.index < insert.index:
        return InsertOperation(insert.index - 1, insert.symbol)
    return insert


def delete_delete(delete1, delete2):
    if delete1.index < delete2.index:
        return delete1
    elif delete1.index > delete2.index:
        return DeleteOperation(delete1.index - 1)
    return None
