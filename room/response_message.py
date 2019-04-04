import json


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

    def make_room_info(self):
        pass

    def make_deleted_sign(self):
        pass
