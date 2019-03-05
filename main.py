from sanic import Sanic, response
from sanic.log import logger
from sanic_jinja2 import SanicJinja2
from sanic.websocket import WebSocketProtocol
import json

app = Sanic()

jinja = SanicJinja2(app, pkg_path='template')


@app.middleware('response')
async def allow_cross_site(request, response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
    # response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"


# @app.route("/")
# async def test(request):
#     logger.info('main.py')
#     return json({"hello": "world"})


@app.route("/player")
@jinja.template('player.html')
async def player(request):
    return {
        "Player": "CR7",
        "Category": "Soccer",
    }


@app.websocket('/')
async def feed(request, ws):
    send_dic = {'id':'seha','msg': 'hello!'}
    print('Sending: ' + json.dumps(send_dic))
    await ws.send(json.dumps(send_dic))
    data = await ws.recv()
    resonse_dic = {'id':'mc','msg': data}
    print('Received: ' + str(resonse_dic))



app.static('/home', 'static/index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, protocol=WebSocketProtocol)
