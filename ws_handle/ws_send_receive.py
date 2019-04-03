from sanic.websocket import ConnectionClosed
from room.message import Message
import json


async def ws_room_send_chat(ws, room, my_room, user_id):
    while True:
        try:
            receive_data = json.loads(await ws.recv())

        except ConnectionClosed:
            await room.leave_room(user_id)
            await my_room.leave_room(user_id)
            break

        else:
            if 'from_id' in receive_data:
                print('wispher chat')
                msg = Message(receive_data)
                data_set_from_id = msg.message_json_for_whisper(user_id)
                await my_room.send_message_to_user(receive_data['from_id'], data_set_from_id)

            elif 'query' in receive_data:
                print('noti chat')
                await room.send_info(user_id)

            else:
                print('room chat')
                await room.send_message(receive_data)


async def receive_ws_channel(room, ws):
    while True:
        await room.receive_message(ws)
