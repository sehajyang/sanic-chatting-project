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
    response.headers["Access-Control-Allow-Credentials"] = "true"
    # response.headers["Access-Control-Allow-Headers"] = "*"


# HTTP
@app.route("/", methods=['GET'])
@jinja.template('main.html')
async def player(request):
    return {'message': 'hello world'}


# XXX: user 정보는 redis가 아니고 rdb에 저장해야됨
@app.route('/login', methods=['GET', 'POST'])
@jinja.template('login.html')
async def login(request):
    message = ''
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')
        name = request.form.get('name')
        print('id', id, 'pwd', password, 'name', name)

        get_password = await redis_set_get.get_hash_value('users', id)
        print('get_password',get_password)

        # TODO: redis get_id and get_pwd
        if password == get_password:
            print(password, get_password)
            user = User(id=id, name=name)
            auth.login_user(request, user)
            return response.redirect('/lobby')
        else:
            return {'message': 'LOGIN FAIL'}
    else:
        return {'message': '로그인 페이지입니다'}


# FIXME: 구린코드 주의
@app.route('/join', methods=['GET', 'POST'])
@jinja.template('join.html')
async def join(request):
    if request.method == 'POST':
        try:
            connection = await redis_pub_sub.get_redis_connection()
            id = request.form.get('id')
            password = request.form.get('password')
            result = await redis_set_get.set_hash_data(connection, 'users', id, password)
            if result is not 0:
                return response.redirect('/login')
            else:
                return {'message': '이미 존재하는 회원입니다'}
        except ConnectionError:
            return {'message': '회원가입에 실패했습니다'}
    else:
        return {'message': '회원가입 페이지입니다'}


@app.route('/logout')
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')


@app.route("/lobby", methods=["GET"])
@auth.login_required(user_keyword='user')
@jinja.template('room_list.html')
async def lobby(request, user):
    room_list = await redis_set_get.get_hash_all_value('rooms')

    return {"room_list": room_list, "user_name": user.name}


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
        await redis_set_get.set_hash_data(connection, 'rooms', room_no, room_title)
        message = '방을 생성했습니다 방 번호: ', room_no
    except Exception:
        message = '방 생성에 실패했습니다'

    return {
        "message": message
    }


@app.route("/rooms/<room_no>/delete", methods=["POST"])
@jinja.template('room_list.html')
async def player(request, room_no):
    await redis_set_get.del_hash_keys('rooms', [room_no])

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
