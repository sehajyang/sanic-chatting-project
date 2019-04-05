from redis_handle import redis_set_get, redis_pub_sub
from room import ResponseMessage
from channel import Channel

import json


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
        await Room.notify_room_info(self, 'room_info')

    async def leave_room(self, user_id):
        print('leave room')
        if not self.is_connected:
            await self._connect()

        await redis_pub_sub.unsubscibe_room(self._subscription, self.room_no)
        await redis_set_get.del_hash_keys(self.connection, self.room_no, user_id)
        await Room.notify_room_info(self, 'room_info')

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
                await redis_pub_sub.unsubscibe_room(self._subscription, self.room_no)
                await redis_set_get.del_hash_keys(self.connection, self.room_no, self.user_id)

    async def notify_room_info(self, notify_data_kind):
        if not self.is_connected:
            await self._connect()

        message = ""

        if notify_data_kind is 'room_info':
            user_list = await Channel.send_channel_key_list(self.connection)
            user_count = await Channel.send_channel_key_count(self.connection)
            message = ResponseMessage.make_room_info(user_list, user_count)

        elif notify_data_kind is 'rooms_lobby_data':
            pass
        # Room 이름 Channel로 바꿔야 될 것 같은데

        elif notify_data_kind is 'room_deleted':
            message = ResponseMessage.make_deleted_sign(self.room_no)

        await redis_pub_sub.send_message(self.room_no, str(message))
