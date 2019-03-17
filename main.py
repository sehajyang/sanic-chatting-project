from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from sanic.websocket import WebSocketProtocol
from sanic.response import text
import asyncio
from room import Room
from ws_handle import send_ws_channel, receive_ws_channel
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
@app.route("/main", methods=['GET'])
@jinja.template('main.html')
async def player(request):
    if not request['session'].get('user_session'):
        request['session']['user_session'] = 0

    request['session']['user_session'] += 1

    print(text(request['session']['user_session']))
    return text(request['session']['user_session'])


@app.route("/lobby")
@jinja.template('room_list.html')
async def player(request):
    return {
        "id": "seha",
        "name": "sehajyang",
    }


# WebSocketServer
@app.websocket('/room/<room_no>/')
async def chat(request, ws, room_no):
    # FIXME: user_id
    user_id = '1'
    room = Room(room_no)
    await room.join_room(ws, user_id)

    send_task = asyncio.ensure_future(
        send_ws_channel(ws, room, user_id))
    receive_task = asyncio.ensure_future(
        receive_ws_channel(room))
    done, pending = await asyncio.wait(
        [send_task, receive_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, protocol=WebSocketProtocol)
