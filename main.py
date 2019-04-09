from sanic import Sanic, response
from sanic_jinja2 import SanicJinja2
from sanic.websocket import WebSocketProtocol
from sanic.response import text
import asyncio
from channel import Channel
from ws_handle import receive_ws_channel, ws_room_send_chat
from redis_handle import redis_set_get, redis_pub_sub
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


@app.route("/lobby", methods=["GET"])
@jinja.template('room_list.html')
async def player(request):
    room_list = await redis_set_get.get_hash_all_value('lobby')

    return response.json({'room_list': room_list})


# HTTP POST
@app.route("/rooms/<room_no>", methods=["POST"])
@jinja.template('room_list.html')
async def player(request, room_no):
    connection = await redis_pub_sub.get_redis_connection()
    room_title = request.form.get('room_title')
    room_password = request.form.get('room_password')
    await redis_set_get.set_hash_data(connection, room_no, room_password, room_title)

    return {
        "id": "seha",
        "name": "sehajyang",
    }


@app.route("/rooms/<room_no>", methods=["DETELE"])
@jinja.template('room_list.html')
async def player(request, room_no):
    connection = await redis_pub_sub.get_redis_connection()
    user_list = await redis_set_get.get_hash_all_value(room_no)
    await redis_set_get.del_hash_keys(connection, room_no, user_list)

    return {
        "id": "seha",
        "name": "sehajyang",
    }


# WebSocketServer
@app.websocket('/rooms/<room_no>/<user_id>/<user_name>')
async def room_chat(request, ws, room_no, user_id, user_name):
    # FIXME: user_id -> get session_id
    room = Channel(room_no)
    my_room = Channel(room_no + ":" + user_id)

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
