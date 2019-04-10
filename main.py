import asyncio

from sanic import Sanic, response
from sanic.response import text
from sanic.websocket import WebSocketProtocol
from sanic_auth import Auth, User
from sanic_jinja2 import SanicJinja2

from channel import Channel
from redis_handle import redis_set_get, redis_pub_sub
from ws_handle import receive_ws_channel, ws_room_send_chat

session = {}
app = Sanic(__name__)
app.config.AUTH_LOGIN_ENDPOINT = 'login'
auth = Auth(app)
jinja = SanicJinja2(app, pkg_path='template')


@app.listener('before_server_start')
async def setup(app, loop):
    pass


@app.middleware('request')
async def add_session(request):
    request['session'] = session


@app.middleware('response')
async def allow_cross_site(request, response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
    # response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"


# HTTP
@app.route("/", methods=['GET'])
@jinja.template('main.html')
async def player(request):
    return text('hello world')


@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    message = ''
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')
        # TODO: redis get_id and get_pwd
        if id == 'seha' and password == '1234':
            user = User(id='seha', name='세하쟝')
            auth.login_user(request, user)
            return response.redirect('/')
        message = 'LOGIN FAIL'
    return response.json({'message': message})


@app.route('/logout')
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')


@app.route("/lobby", methods=["GET"])
@auth.login_required(user_keyword='user')
@jinja.template('room_list.html')
async def lobby(request, user):
    room_list = await redis_set_get.get_hash_all_value('lobby')

    return response.json({"room_list": room_list, "user_name": user.name})


def handle_no_auth(request):
    return response.json(dict(message='unauthorized'), status=401)


# HTTP POST
@app.route("/rooms/<room_no>", methods=["POST"])
@jinja.template('room_list.html')
async def player(request, room_no):
    connection = await redis_pub_sub.get_redis_connection()
    room_title = request.form.get('room_title')
    room_password = request.form.get('room_password')

    try:
        message = await redis_set_get.set_hash_data(connection, room_no, room_password, room_title)
    except Exception:
        message = '방 생성에 실패했습니다'

    return {
        "message": message
    }


@app.route("/rooms/<room_no>/delete", methods=["POST"])
@jinja.template('room_list.html')
async def player(request, room_no):
    connection = await redis_pub_sub.get_redis_connection()
    user_list = await redis_set_get.get_hash_all_value(room_no)
    await redis_set_get.del_hash_keys(connection, room_no, user_list)

    return {
        "message": "방을 삭제했습니다"
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
