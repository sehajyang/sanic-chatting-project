from room import redis_pub_sub
import asyncio_redis.replies
import json


class Room:
    def __init__(self, room_no):
        self.room_no = room_no
        self.is_connected = False
        self.connection = None
        self._subscription = None
        self.users = []

    async def _connect(self):
        self.connection = await redis_pub_sub.get_redis_connection()
        self.is_connected = True

    async def join_room(self, user):
        if not self.is_connected:
            await self._connect()
        self.users.append(user)
        self._subscription = await redis_pub_sub.subscribe(self.connection, self.room_no)

    async def leave_room(self, user):
        if not self.is_connected:
            await self._connect()
        self.users.remove(user)
        await redis_pub_sub.unsubscibe(self._subscription, self.room_no)

    async def send_message(self, message):
        if not self.is_connected:
            await self._connect()

        return await redis_pub_sub.send_message(self.room_no, message)

    async def receive_message(self):
        if not self.is_connected:
            await self._connect()

        for receiver in self.users:
            try:
                message = await redis_pub_sub.receive_message(self._subscription)
                await receiver.send(str(message))
            except ConnectionError:
                await self.leave_room(receiver)

    async def users_count(self):
        return json.dumps({'room_no': self.room_no, 'count': len(self.users)})
