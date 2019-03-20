from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from sanic.websocket import WebSocketProtocol
from sanic.response import text
import asyncio
from room import Room
from ws_handle import send_ws_channel, receive_ws_channel, send_ws_channel_notify
import sanic_session

app = Sanic()
jinja = SanicJinja2(app, pkg_path='template')
sanic_session.install_middleware(app, 'InMemorySessionInterface')


@app.listener('before_server_start')
async def setup(app, loop):
    pass


@app.middleware('response')
async def allow_cross_site(request, response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
    # response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"


# HTTP
@app.route("/", methods=['GET'])
@jinja.template('main.html')
async def player(request):
    if not request['session'].get('user_session'):
        request['session']['user_session'] = 0

    request['session']['user_session'] += 1

    print(text(request['session']['user_session']))
    return request['session']['user_session']


@app.route("/lobby")
@jinja.template('room_list.html')
async def player(request):
    return {
        "id": "seha",
        "name": "sehajyang",
    }


# WebSocketServer
@app.websocket('/rooms/<room_no>/<user_id>')
async def room_chat(request, ws, room_no, user_id):
    # FIXME: user_id -> get session_id
    room = Room(room_no)
    my_room = Room(room_no + ":" + user_id)

    await room.join_room(ws, user_id)
    await my_room.join_room(ws, user_id)

    # user_session = request['session']['user_session']

    send_task = asyncio.ensure_future(
        send_ws_channel(ws, room, user_id))
    receive_task = asyncio.ensure_future(
        receive_ws_channel(room))
    my_room_receive_task = asyncio.ensure_future(
        receive_ws_channel(my_room))
    done, pending = await asyncio.wait(
        [send_task, receive_task, my_room_receive_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


# send whisper message
@app.websocket('/users/<room_no>/<user_id>')
async def user_chat(request, ws, room_no, user_id):
    # FIXME: user_id
    my_room = Room(room_no + ":" + user_id)

    await my_room.join_room(ws, user_id)
    await send_ws_channel(ws, my_room, user_id)


# user list send
# FIXME: room_chat url의 user_id 삭제시 아래 url /rooms/<room_no>/<users>로 변경
# FIXME: 아래 user_id test용
@app.websocket('/rooms/<room_no>/users/<user_id>')
async def user_list(request, ws, room_no, user_id):
    # FIXME: user_id
    my_room = Room(room_no)

    await my_room.join_room(ws, user_id)
    await send_ws_channel_notify(ws, my_room, user_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, protocol=WebSocketProtocol)
