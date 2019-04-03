from sanic.websocket import ConnectionClosed
from room.message import Message
from redis_handle import redis_set_get
import json


async def ws_room_send_chat(ws, room, my_room, user_id):
    while True:
        try:
            receive_data = json.loads(await ws.recv())

        except ConnectionClosed:
            await room.leave_room(user_id)
            await my_room.leave_room(user_id)
            await redis_set_get.del_hash_keys(room.connection, room.room_no, user_id)
            await redis_set_get.del_hash_keys(room.connection, my_room.room_no, user_id)
            break

        else:
            if 'from_id' in receive_data:
                print('wispher chat')
                msg = Message(receive_data)
                data_set_from_id = msg.message_json_for_whisper(user_id)
                await my_room.send_message_to_user(receive_data['from_id'], data_set_from_id)

            elif 'query' in receive_data:
                print('noti chat')
                if receive_data['query'] == 'user_list':
                    await room.send_user_list()
                if receive_data['query'] == 'user_count':
                    await room.send_user_count()

            else:
                print('room chat')
                await room.send_message(receive_data)


async def receive_ws_channel(room, ws):
    while True:
        await room.receive_message(ws)
