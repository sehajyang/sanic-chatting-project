import asyncio_redis
import asyncio_redis.connection
import asyncio_redis.protocol
import dotenv
import os

dotenv.load_dotenv()


async def create_connection_pool():
    return await asyncio_redis.Pool.create(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']),
                                           poolsize=int(os.environ['REDIS_POOL_SIZE']))


async def subscribe_channel(connection, channel):
    subscription = await connection.start_subscribe()
    await subscription.subscribe(['Channel:{}'.format(channel)])
    return subscription


async def unsubscibe_channel(subscription: asyncio_redis.protocol.Subscription, channel):
    await subscription.unsubscribe(['Channel:{}'.format(channel)])


async def receive_message(subscription: asyncio_redis.protocol.Subscription):
    return await subscription.next_published()


async def send_message(channel, message):
    connection = await create_connection_pool()
    await connection.publish('Channel:{}'.format(channel), str(message))
    connection.close()
