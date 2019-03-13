from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from sanic.websocket import WebSocketProtocol, ConnectionClosed

from rooms.room import Room

app = Sanic()
room = Room()
jinja = SanicJinja2(app, pkg_path='template')


@app.listener('before_server_start')
async def setup(app, loop):
    pass


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
@app.websocket('/room/<room_no>')
async def chat(request, ws, room_no):
    print(room_no)
    sub = Room()
    room.join(ws)
    while True:
        obs = Observer()
        obs.register_subject(sub)
        try:
            message = await ws.recv()
        except ConnectionClosed:
            room.leave(ws)
            obs.unregister_subject(ws)
            break
        else:
            await room.send_massage(message)
            sub.set_msg('broadcast: ', message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, protocol=WebSocketProtocol)
