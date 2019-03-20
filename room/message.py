import json


class Message:

    def __init__(self, receive_data):
        self.seq = receive_data['seq']
        self.message = receive_data['message']

    def message_json(self):
        message_to_json = {
            'seq': self.seq,
            'message': self.message
        }

        return json.dumps(message_to_json)

    def message_json_for_whisper(self, from_id):
        message_to_json = {
            'from_id': from_id,
            'seq': self.seq,
            'message': self.message
        }

        return json.dumps(message_to_json)
