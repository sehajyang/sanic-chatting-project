import asyncio_redis
import asyncio_redis.connection
import dotenv
import os
import json

dotenv.load_dotenv()


async def get_redis_connection():
    return await asyncio_redis.Connection.create(host=os.environ['REDIS_HOST'],
                                                 port=int(os.environ['REDIS_PORT']))


async def subscribe(connection, room_no):
    subscription = await connection.start_subscribe()
    await subscription.subscribe(['Room:{}'.format(room_no)])
    return subscription


async def unsubscibe(subscription: asyncio_redis.protocol.Subscription, room_no):
    await subscription.unsubscribe(['Room:{}'.format(room_no)])


async def receive_message(subscription: asyncio_redis.protocol.Subscription):
    return await subscription.next_published()


async def send_message(room_no, message):
    connection = await get_redis_connection()
    json_values = json.dumps({'message': message})
    await connection.publish('Room:{}'.format(room_no), str(json_values))
    connection.close()
