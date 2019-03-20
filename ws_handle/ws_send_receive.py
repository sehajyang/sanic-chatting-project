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
            if 'from_id' in receive_data:
                data_set_from_id = msg.message_json_for_whisper(user_id)
                await room.send_message_to_user(receive_data['from_id'], data_set_from_id)
            else:
                await room.send_message(data)


async def receive_ws_channel(room):
    while True:
        await room.receive_message()


# TODO : 분기 나눌 것 (그러기 위한 query key)
async def send_ws_channel_notify(ws, room, user_id):
    try:
        # receive_data = json.loads(await ws.recv())
        user_list = await room.user_list()
        print(f'userlist {user_list}')
    except ConnectionClosed:
        await room.leave_room(user_id)
    else:
        await room.send_notify(user_id, user_list)
