from sanic.websocket import ConnectionClosed
import json


async def send_ws_channel(ws, room):
    while True:
        try:
            data = await ws.recv()
        except ConnectionClosed:
            await room.leave_room(ws)
            break
        else:
            await room.send_message(json.dumps({'message': data}))


async def receive_ws_channel(room):
    while True:
        await room.receive_message()
