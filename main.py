from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from sanic.websocket import WebSocketProtocol, ConnectionClosed
import asyncio
from room import Room

app = Sanic()
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


@app.websocket("/room/create/<room_no>")
async def room_create(request, ws, room_no):
    room = Room(room_no)
    await room.join_room(ws)
    print('create room')


# WebSocketServer
@app.websocket('/room/<room_no>')
async def chat(request, ws, room_no):
    room = Room(room_no)
    await room.join_room(ws)

    send_task = asyncio.ensure_future(
        send(ws, room))
    receive_task = asyncio.ensure_future(
        receive(room))
    done, pending = await asyncio.wait(
        [send_task, receive_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


async def send(ws, room):
    while True:
        try:
            message = await ws.recv()
        except ConnectionClosed:
            await room.leave_room(ws)
            break
        else:
            await room.send_message(message)


async def receive(room):
    while True:
        await room.receive_message()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, protocol=WebSocketProtocol)
