from sms_gateway.app import init_app
from aiohttp import web

if __name__ == "__main__":
    web.run_app(init_app(), port=3000)

