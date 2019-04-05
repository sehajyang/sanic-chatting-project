from redis_handle import redis_set_get, redis_pub_sub


class Channel:

    async def send_channel_key_list(channel):
        dict_reply = await redis_set_get.get_hash_all_value(channel)

        return await redis_pub_sub.send_message(channel, dict_reply)

    async def send_channel_key_count(channel):
        message = await redis_set_get.get_hash_data_len(channel)

        return await redis_pub_sub.send_message(channel, str(message))
