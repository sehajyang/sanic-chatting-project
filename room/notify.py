import json


class Notify:

    def __init__(self, seq):
        self.seq = seq
        self.query = ""

    def notify_json_for_user_list(self, query):
        notify_to_json = {
            'seq': self.seq,
            'query': query
        }

        return json.dumps(notify_to_json)
