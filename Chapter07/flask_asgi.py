import asyncio
from threading import current_thread
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, jsonify
from aiohttp import ClientSession


app = Flask(__name__)
LOGGING_URL = "https://postman-echo.com/post"

async def post_url(data):
    async with ClientSession() as session:
        response = await session.post(LOGGING_URL, data=data)
        j = await response.json()
    return {'url': str(response.url), 'status': response.status, 'data':await response.json()}

@app.before_request
async def app_before_request():
    print(f'Sending message before request: {current_thread().name}')
    await post_url({'message': f'Inside app_before_request(): {current_thread().name}'})

@app.after_request
async def app_after_request(response):
    print(f'Posting message after response: {response.status}')
    await post_url({'message': f'Returning response status: {response.status}'})
    return response

@app.errorhandler(404)
async def page_not_found(e):
    print(f'Error caught: {e} in {current_thread().name}')
    results = await post_url(f'Error caught: {e}')
    return jsonify(results), 404

@app.route('/')
async def index():
    print(f'Inside route index(): {current_thread().name}')
    await asyncio.sleep(1)
    return jsonify({"message":"ok"})

asgi_app = WsgiToAsgi(app)
if __name__ == '__main__':
    app.run()
