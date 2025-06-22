from .app import init_app
from aiohttp import web

def main():
    web.run_app(init_app(), port=3000)

if __name__ == "__main__":
    main()

