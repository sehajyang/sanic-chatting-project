

async def set_hash_data(conn, hash_title, key, value):
    return await conn.hset(hash_title, key, value)


async def get_hash_data_len(conn, hash_title):
    return await conn.hlen(hash_title)


async def get_all_hash_title(conn, hash_title):
    return await conn.hkeys(hash_title)


async def get_hash_value_by_key(conn, hash_title, key):
    return await conn.hget(hash_title, key)


async def get_hash_all_value(conn, hash_title):
    return await conn.hgetall_asdict(hash_title)


async def get_hash_value(conn, hash_title, key):
    return await conn.hget(hash_title, key)


async def del_hash_keys(conn, hash_title, keys):
    return await conn.hdel(hash_title, keys)


async def del_hash_title(conn, hash_title):
    return await conn.delete([hash_title])
