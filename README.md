# Многопользовательский текстовый редактор  

Авторы: Астахова Ксения, Жданов Илья  

## Описание протокола:  
```
{
    "server_id": server_guid,
    "user_id": user_guid,
    "operation": 
    {
        "name": operation.name,
        "text": operation.text (не указывается для DeleteOperation),
        "index": operation.index
    },
    "revision": revision
}
