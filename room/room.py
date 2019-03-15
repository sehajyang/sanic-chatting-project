from room import redis_pub_sub
import json


class Room:
    def __init__(self, room_no):
        self.room_no = room_no
        self.is_connected = False
        self.connection = None
        self._subscription = None
        self.users = {}

    async def _connect(self):
        self.connection = await redis_pub_sub.get_redis_connection()
        self.is_connected = True

    async def join_room(self, ws, user_id):
        if not self.is_connected:
            await self._connect()
        self.users[user_id] = ws
        self._subscription = await redis_pub_sub.subscribe(self.connection, self.room_no)

    async def leave_room(self, user_id):
        if not self.is_connected:
            await self._connect()
        del self.users[user_id]
        await redis_pub_sub.unsubscibe(self._subscription, self.room_no)

    async def send_message(self, message):
        if not self.is_connected:
            await self._connect()

        return await redis_pub_sub.send_message(self.room_no, message)

    async def receive_message(self):
        if not self.is_connected:
            await self._connect()

        message = await redis_pub_sub.receive_message(self._subscription)
        message_to_json = json.loads(message.value)
        #
        # if message_to_json['method'] == 'WIS':
        #     try:
        #         print(self.users)
        #         print(self.users[message_to_json['receiver_id']])
        #         await self.users[message_to_json['receiver_id']].send(str(message.value))
        #     except ConnectionError:
        #         await self.leave_room(message_to_json['receiver_id'])

        for user_id, ws in self.users.items():
            # TODO: WIS, ALL 함수 따로 뺄 것
            try:
                await ws.send(str(message.value))
                print(user_id)
            except ConnectionError:
                await self.leave_room(user_id)

    async def users_count(self):
        return json.dumps({'room_no': self.room_no, 'count': len(self.users)})
