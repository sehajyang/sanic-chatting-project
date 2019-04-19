

async def set_hash_data(app, hash_title, key, value):
    return await app.conn.hset(hash_title, key, value)


async def get_hash_data_len(app, hash_title):
    return await app.conn.hlen(hash_title)


async def get_all_hash_title(app, hash_title):
    return await app.conn.hkeys(hash_title)


async def get_hash_value_by_key(app, hash_title, key):
    return await app.conn.hget(hash_title, key)


async def get_hash_all_value(app, hash_title):
    return await app.conn.hgetall_asdict(hash_title)


async def get_hash_value(app, hash_title, key):
    return await app.conn.hget(hash_title, key)


async def del_hash_keys(app, hash_title, keys):
    return await app.conn.hdel(hash_title, keys)


async def del_hash_title(app, hash_title):
    return await app.conn.delete([hash_title])
