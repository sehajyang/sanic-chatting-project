from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from sanic.websocket import WebSocketProtocol
from sanic.response import text
import asyncio
from channel import Room
from ws_handle import receive_ws_channel, ws_room_send_chat
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
@app.websocket('/rooms/<room_no>/<user_id>/<user_name>')
async def room_chat(request, ws, room_no, user_id, user_name):
    # FIXME: user_id -> get session_id
    room = Room(room_no)
    my_room = Room(room_no + ":" + user_id)

    await room.join_channel(user_id, user_name)
    await my_room.join_channel(user_id, user_name)

    # user_session = request['session']['user_session']

    send_task = asyncio.create_task(ws_room_send_chat(ws, room, my_room, user_id))
    receive_task = asyncio.create_task(receive_ws_channel(room, ws))
    my_room_receive_task = asyncio.create_task(receive_ws_channel(my_room, ws))
    done, pending = await asyncio.wait(
        [send_task, receive_task, my_room_receive_task],
        return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, protocol=WebSocketProtocol)
