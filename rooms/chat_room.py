from sanic.websocket import ConnectionClosed


class Room:

    def __init__(self):
        # self.sub = Subject()
        self.clients = []

    def join(self, client):
        self.clients.append(client)
        # self.sub.register_observer(client)

    def leave(self, client):
        try:
            self.clients.remove(client)
            # self.sub.remove_observer(client)
        except ValueError:
            pass

    async def send_massage(self, message):
        for receiver in self.clients:
            try:
                await receiver.send(message)
            except ConnectionClosed:
                self.leave(receiver)

    # 몇 명 들어가있는 방인지 알기위함
    def __len__(self):
        return len(self.clients)
