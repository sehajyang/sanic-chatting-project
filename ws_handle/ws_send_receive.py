from sanic.websocket import ConnectionClosed


async def send_ws_channel(ws, room):
    while True:
        try:
            message = await ws.recv()
        except ConnectionClosed:
            await room.leave_room(ws)
            break
        else:
            await room.send_message(message)


async def receive_ws_channel(room):
    while True:
        await room.receive_message()
