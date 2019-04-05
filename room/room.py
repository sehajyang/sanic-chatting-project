from redis_handle import redis_set_get, redis_pub_sub


class Room:
    def __init__(self, room_no):
        self.room_no = room_no
        self.is_connected = False
        self.connection = None
        self.protocol = None
        self._subscription = None
        # FIXME: users redis에 넣기
        self.user_id = ""

    async def _connect(self):
        self.connection = await redis_pub_sub.get_redis_connection()
        self.is_connected = True

    async def join_room(self, user_id, user_name):
        if not self.is_connected:
            await self._connect()

        self.user_id = user_id
        await redis_set_get.set_hash_data(self.connection, self.room_no, user_id, user_name)
        self._subscription = await redis_pub_sub.subscribe_room(self.connection, self.room_no)

    async def leave_room(self, user_id):
        print('leave room')
        if not self.is_connected:
            await self._connect()

        await redis_pub_sub.unsubscibe_room(self._subscription, self.room_no)
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
                await redis_pub_sub.unsubscibe_room(self._subscription, self.room_no)
                await redis_set_get.del_hash_keys(self.connection, self.room_no, self.user_id)

    async def notify_room_info(self):
        pass

