import asyncio
import asyncio_redis


async def Models():
    connection = await asyncio_redis.Connection.create(host='192.168.99.100:32768', port=6379)

    # observer
    observer = await connection.start_subscribe()

    # observer subscribe subject
    await observer.subscribe(['our-channel'])

    while True:
        reply = await observer.next_published()
        print('Received: ', repr(reply.value), 'on channel', reply.channel)

    connection.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Models())
