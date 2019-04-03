async def set_hash_data(connection, hash_title, key, value):
    return await connection.hset(hash_title, key, value)


async def get_hash_data_len(connection, hash_title):
    return await connection.hlen(hash_title)


async def get_all_hash_title(connection, hash_title):
    return await connection.hkeys(hash_title)


async def get_hash_value_by_key(connection, hash_title, key):
    return await connection.hget(hash_title, key)


async def get_hash_all_value(connection, hash_title):
    return await connection.hgetall(hash_title)


async def del_hash_keys(connection, hash_title, key):
    return await connection.hdel(hash_title, key)
