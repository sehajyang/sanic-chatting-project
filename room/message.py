import json


class Message:

    def __init__(self, receiver, seq, message):
        self.receiver_id = receiver
        self.seq = seq
        self.message = message

    def message_json(self):
        message_to_json = {
            'receiver_id': self.receiver_id,
            'seq': self.seq,
            'message': self.message
        }

        return json.dumps(message_to_json)
