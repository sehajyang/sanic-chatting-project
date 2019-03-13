from room import redis_pub_sub
import asyncio_redis.replies


class Room:
    def __init__(self, room_no):
        self.room_no = room_no
        self.is_connected = False
        self.connection = None
        self._subscription = None

    async def _connect(self):
        self.connection = await redis_pub_sub.get_redis_connection()
        self.is_connected = True

    async def join_room(self):
        if not self.is_connected:
            await self._connect()

        self._subscription = await redis_pub_sub.subscribe(self.connection, self.room_no)

    async def leave_room(self):
        if not self.is_connected:
            await self._connect()
        await redis_pub_sub.unsubscibe(self._subscription, self.room_no)

    async def send_message(self, message):
        if not self.is_connected:
            await self._connect()
        return await redis_pub_sub.send_message(self.room_no, message)

    async def receive_message(self) -> asyncio_redis.replies.PubSubReply:
        if not self.is_connected:
            await self._connect()
        return await redis_pub_sub.receive_message(self._subscription)
