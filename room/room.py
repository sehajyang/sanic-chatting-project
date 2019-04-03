from room import redis_pub_sub
from redis_handle import redis_set_get


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
        # FIXME:
        # room_no = str(self.room_no)[:str(self.room_no).find(":")]
        # return await redis_pub_sub.send_message(room_no + ":" + from_id, message)

        return await self.users[from_id].send(str(message))

    async def send_user_list(self, user_id):
        if not self.is_connected:
            await self._connect()

        message = await redis_set_get.get_hash_all_value(self.connection, self.room_no)

        return await redis_pub_sub.send_message(self.room_no + ":" + user_id, message)

    async def receive_message(self):
        if not self.is_connected:
            await self._connect()

        while True:
            try:
                message = await redis_pub_sub.receive_message(self._subscription)
                await redis_pub_sub.send_message(self.room_no, message.value)
            except ConnectionError:
                print('connection error1')
                await redis_pub_sub.unsubscibe_room(self._subscription, self.room_no)
                await redis_set_get.del_hash_keys(self.connection, self.room_no, self.user_id)

    async def users_count(self):
        if not self.is_connected:
            await self._connect()

        return await redis_set_get.get_hash_data_len(self.connection, self.room_no)
