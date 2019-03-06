from sanic import Sanic, response
from sanic_jinja2 import SanicJinja2
from sanic.websocket import WebSocketProtocol, ConnectionClosed
import json

from chat_room import Room

app = Sanic()
room = Room()

jinja = SanicJinja2(app, pkg_path='template')


@app.middleware('response')
async def allow_cross_site(request, response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
    # response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"


# WebSocketServer
@app.websocket('/')
async def feed(request, ws):
    return await response.file('static/index.html')


@app.websocket('/chat')
async def chat(request, ws):
    room.join(ws)
    while True:
        try:
            message = await ws.recv()
        except ConnectionClosed:
            room.leave(ws)
            break
        else:
            await room.send_massage(message)


@app.route("/player")
@jinja.template('player.html')
async def player(request):
    return {
        "Player": "CR7",
        "Category": "Soccer",
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, protocol=WebSocketProtocol)
