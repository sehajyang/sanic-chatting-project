import asyncio

from room import Room

# FIXME:error
if __name__ == '__main__':
    async def main():
        room = Room(10)
        await room.join_room(ws,user_id)
        print('join')
        while True:
            reply = await room.receive_message()
            print(reply.value)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
