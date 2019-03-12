from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from sanic.websocket import WebSocketProtocol, ConnectionClosed

from rooms.chat_room import Room

app = Sanic()
chat_room = Room()
jinja = SanicJinja2(app, pkg_path='template')


@app.middleware('response')
async def allow_cross_site(request, response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
    # response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"


# HTTP
@app.route("/main", methods=['GET'])
@jinja.template('main.html')
async def player(request):
    return {
        "id": "seha",
        "name": "sehajyang",
    }


@app.route("/lobby")
@jinja.template('room_list.html')
async def player(request):
    return {
        "id": "seha",
        "name": "sehajyang",
    }


# WebSocketServer
@app.websocket('/room')
async def chat(request, ws):
    chat_room.join(ws)
    while True:
        try:
            message = await ws.recv()
        except ConnectionClosed:
            chat_room.leave(ws)
            break
        else:
            await chat_room.send_massage(message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, protocol=WebSocketProtocol)
