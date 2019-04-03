import asyncio_redis
import asyncio_redis.connection
import asyncio_redis.protocol
import dotenv
import os

dotenv.load_dotenv()


async def get_redis_connection():
    return await asyncio_redis.Connection.create(host=os.environ['REDIS_HOST'],
                                                 port=int(os.environ['REDIS_PORT']))


async def subscribe_room(connection, channel):
    subscription = await connection.start_subscribe()
    await subscription.subscribe(['Channel:{}'.format(channel)])
    return subscription


async def unsubscibe_room(subscription: asyncio_redis.protocol.Subscription, channel):
    await subscription.unsubscribe(['Channel:{}'.format(channel)])


async def receive_message(subscription: asyncio_redis.protocol.Subscription):
    return await subscription.next_published()


async def send_message(channel, message):
    connection = await get_redis_connection()
    await connection.publish('Channel:{}'.format(channel), str(message))
    connection.close()
