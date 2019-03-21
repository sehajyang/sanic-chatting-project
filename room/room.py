from room import redis_pub_sub
import json


class Room:
    def __init__(self, room_no):
        self.room_no = room_no
        self.is_connected = False
        self.connection = None
        self._subscription = None
        # FIXME: users redis에 넣기
        self.users = {}

    async def _connect(self):
        self.connection = await redis_pub_sub.get_redis_connection()
        self.is_connected = True

    async def join_room(self, ws, user_id):
        if not self.is_connected:
            await self._connect()
        self.users[user_id] = ws
        print('join_room : ', self.users)
        self._subscription = await redis_pub_sub.subscribe_room(self.connection, self.room_no)

    # FIXME:27라인 같은 유저 있을경우 동작은 하되 오류임
    async def leave_room(self, user_id):
        print('leave room')
        if not self.is_connected:
            await self._connect()
        del self.users[user_id]
        await redis_pub_sub.unsubscibe_room(self._subscription, self.room_no)

    async def send_message(self, message):
        if not self.is_connected:
            await self._connect()

        return await redis_pub_sub.send_message(self.room_no, message)

    async def send_message_to_user(self, from_id, message):
        if not self.is_connected:
            await self._connect()
        # room_no = str(self.room_no)[:str(self.room_no).find(":")]
        # return await redis_pub_sub.send_message(room_no + ":" + from_id, message)
        print(self.users.keys())
        return await self.users[from_id].send(str(message))

    async def send_info(self, user_id):
        if not self.is_connected:
            await self._connect()
        # XXX: 자기자신만 나오고있음
        for item in self.users.items():
            print(item)

        message = json.dumps({'user_list': str(self.users.keys())})

        return await redis_pub_sub.send_message(self.room_no + ":" + user_id, message)

    async def receive_message(self):
        if not self.is_connected:
            await self._connect()

        message = await redis_pub_sub.receive_message(self._subscription)

        for user_id, ws in self.users.items():
            try:
                await ws.send(str(message.value))
            except ConnectionError:
                await self.leave_room(user_id)

    async def users_count(self):
        if not self.is_connected:
            await self._connect()

        return json.dumps({'room_no': self.room_no, 'count': len(self.users)})

