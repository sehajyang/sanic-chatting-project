from redis_handle import redis_set_get, redis_pub_sub
from channel import response_message


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

    async def notify_room_info(self, notify_data_kind):
        if not self.is_connected:
            await self._connect()

        if notify_data_kind is 'room_info':
            user_list = await redis_set_get.get_hash_all_value(self.room_no)
            user_count = await redis_set_get.get_hash_data_len(self.room_no)
            message = response_message.ResponseMessage.make_room_info(user_list, user_count)

        elif notify_data_kind is 'rooms_lobby_data':
            pass

        elif notify_data_kind is 'room_deleted':
            message = response_message.ResponseMessage.make_deleted_sign(self.room_no)

    async def notify_channel_info(self):
        user_count = await redis_set_get.get_hash_all_value(self.room_no)
        user_list = await redis_set_get.get_hash_data_len(self.room_no)
        message = await response_message.ResponseMessage.make_room_info(user_count, user_list)

        await redis_pub_sub.send_message(self.room_no, str(message))
