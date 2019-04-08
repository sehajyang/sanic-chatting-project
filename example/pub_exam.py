import asyncio

from channel import Room

# FIXME:error
if __name__ == '__main__':
    async def main():
        room = Room(10)
        await room.join_channel(ws, user_id)
        await room.send_message('hello!')


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
