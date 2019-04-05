from sanic.websocket import ConnectionClosed
from room.response_message import ResponseMessage
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
                msg = ResponseMessage(receive_data)
                data_set_from_id = msg.make_whisper_message(user_id)
                await my_room.send_message_to_user(receive_data['from_id'], data_set_from_id)

            elif 'query' in receive_data:
                print('noti chat')
                await room.notify_room_info('room_info')

            else:
                print('room chat')
                await room.send_message(receive_data)


async def receive_ws_channel(room, ws):
    while True:
        await room.receive_message(ws)
