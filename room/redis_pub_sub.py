import asyncio
import asyncio_redis
import asyncio_redis.connection
import dotenv
import os

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
    await connection.publish('Room:{}'.format(room_no), message)

    connection.close()


if __name__ == '__main__':
    async def main():
        await send_message(10, 'hi')


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
