from sanic.websocket import ConnectionClosed
from room.message import Message
import json


async def send_ws_channel(ws, room, user_id):
    while True:
        try:
            data_dict = json.loads(await ws.recv())
            msg = Message(data_dict['receiver_id'], data_dict['seq'], data_dict['method'], data_dict['message'])
            data = msg.message_json()
        except ConnectionClosed:
            await room.leave_room(user_id)
            break
        else:
            await room.send_message(data)


async def receive_ws_channel(room):
    while True:
        await room.receive_message()
