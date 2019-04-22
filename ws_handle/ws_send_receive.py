import json

from websockets import ConnectionClosed

from channel.response_message import ResponseMessage
from db_driver import redis_set_get


async def ws_room_send_chat(app, ws, room, my_room, user_id):
    while True:
        try:
            receive_data = json.loads(await ws.recv())

        except ConnectionClosed:
            await my_room.leave_channel(app, user_id)
            await redis_set_get.del_hash_keys(app, room.room_no, [user_id])
            await redis_set_get.del_hash_keys(app, my_room.room_no, [user_id])
            break

        except json.JSONDecodeError:
            await room.notify_channel_info(app, ws, 'data_not_json')

        else:
            if 'from_id' in receive_data:
                print('wispher chat')

                msg = ResponseMessage(receive_data)
                data_set_from_id = msg.make_whisper_message(user_id)
                await my_room.send_message_to_user(receive_data['from_id'], data_set_from_id)

            elif 'query' in receive_data:
                print('noti chat')
                await room.notify_channel_info(app, ws, 'room_info')

            else:
                print('room chat')
                await room.send_message(receive_data)


async def receive_ws_channel(room, app, ws):
    while True:
        try:
            await room.receive_message(app, ws)

        except ConnectionClosed:
            break
