from redis_handle import redis_set_get, redis_pub_sub
from channel import ResponseMessage


class Channel:
    def __init__(self, room_no):
        self.room_no = room_no
        self.is_connected = False
        self.connection = None
        self.protocol = None
        self._subscription = None
        self.user_id = ""

    async def _connect(self):
        self.connection = await redis_pub_sub.get_redis_connection()
        self.is_connected = True

    async def join_channel(self, user_id, user_name):
        if not self.is_connected:
            await self._connect()

        self.user_id = user_id
        await redis_set_get.set_hash_data(self.connection, self.room_no, user_id, user_name)
        self._subscription = await redis_pub_sub.subscribe_channel(self.connection, self.room_no)

    async def leave_channel(self, user_id):
        print('leave room')
        if not self.is_connected:
            await self._connect()

        await redis_pub_sub.unsubscibe_channel(self._subscription, self.room_no)
        await redis_set_get.del_hash_keys(self.connection, self.room_no, user_id)

    async def send_message(self, message):
        if not self.is_connected:
            await self._connect()

        return await redis_pub_sub.send_message(self.room_no, message)

    async def send_message_to_user(self, from_id, message):
        if not self.is_connected:
            await self._connect()

        room_no = str(self.room_no)[:str(self.room_no).find(":")]
        return await redis_pub_sub.send_message(room_no + ":" + from_id, message)

    async def send_user_list(self):
        if not self.is_connected:
            await self._connect()

        dict_reply = await redis_set_get.get_hash_all_value(self.room_no)

        return await redis_pub_sub.send_message(self.room_no, dict_reply)

    async def send_user_count(self):
        if not self.is_connected:
            await self._connect()

        message = await redis_set_get.get_hash_data_len(self.room_no)

        return await redis_pub_sub.send_message(self.room_no, str(message))

    async def receive_message(self, ws):
        if not self.is_connected:
            await self._connect()

        while True:
            try:
                message = await redis_pub_sub.receive_message(self._subscription)
                await ws.send(str(message.value))
            except ConnectionError:
                await redis_pub_sub.unsubscibe_channel(self._subscription, self.room_no)
                await redis_set_get.del_hash_keys(self.connection, self.room_no, self.user_id)

    async def notify_channel_info(self):
        user_count = await self.send_user_count()
        user_list = await self.send_user_list()
        ResponseMessage.make_room_info(user_count, user_list)

