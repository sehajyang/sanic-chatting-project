import json
from channel import room_constants


class ResponseMessage:

    def __init__(self, receive_data):
        self.seq = receive_data['seq']
        self.message = receive_data['message']

    def make_chat_message(self):
        message_to_json = {
            'seq': self.seq,
            'message': self.message
        }
        return json.dumps(message_to_json)

    def make_whisper_message(self, from_id):
        message_to_json = {
            'from_id': from_id,
            'seq': self.seq,
            'message': self.message
        }
        return json.dumps(message_to_json)

    def make_lobby_info(self, room_list, room_count):
        message_to_json = {
            'seq': self.seq,
            'room_list': room_list,  # k: room_no, v: title
            'user_count': room_count
        }
        return json.dumps(message_to_json)

    @staticmethod
    def make_room_info(user_list, user_count):
        message_to_json = {
            'user_list': user_list,
            'user_count': user_count
        }
        return json.dumps(message_to_json)

    @staticmethod
    def make_deleted_sign(room_no):
        message_to_json = {
            'room_no': room_no,
            'room_status': room_constants.ROOM_DEL_STATUS,
            'alter': room_constants.ROOM_DEL_ALTER,
            'redirect': room_constants.ROOM_DEL_REDIRECT
        }
        return json.dumps(message_to_json)

    @staticmethod
    def make_alter_sign(room_no, alter_message):
        message_to_json = {
            'room_no': room_no,
            'alter': alter_message,
        }
        return json.dumps(message_to_json)
