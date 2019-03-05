from sanic import Sanic
from sanic.log import logger
from sanic.response import json, text, html
from sanic_jinja2 import SanicJinja2

app = Sanic()

jinja = SanicJinja2(app,pkg_path='template')


@app.route("/")
async def test(request):
    logger.info('main.py')
    return json({"hello": "world"})


@app.route("/player")
@jinja.template('player.html')
async def player(request):
    return {
        "Player": "CR7",
        "Category": "Soccer",
    }


app.static('/home', 'static/index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
