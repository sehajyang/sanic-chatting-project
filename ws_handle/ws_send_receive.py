from sanic.websocket import ConnectionClosed
from room.message import Message
import json


async def send_ws_channel(ws, room, user_id):
    while True:
        try:
            receive_data = json.loads(await ws.recv())
            msg = Message(receive_data)
            data = msg.message_json()
        except ConnectionClosed:
            await room.leave_room(user_id)
            break
        else:
            if receive_data['from_id'] is not "":
                print('exist from_id')
                data_set_from_id = msg.message_json_set_from_id(user_id)
                await room.send_message_to_user(receive_data['from_id'], data_set_from_id)
            else:
                print('not exist from_id')
                await room.send_message(data)


async def receive_ws_channel(room):
    while True:
        await room.receive_message()
