from aiohttp import web
from sms_gateway.gateway import Gateway
from sms_gateway.api import send_sms, get_info
from sms_gateway.config import load_config
import logging

_LOGGER = logging.getLogger("sms_gateway.app")

async def init_app():
    config = load_config()
    app = web.Application()
    gateway = Gateway(config)
    await gateway.init_async()
    app["gateway"] = gateway

    app.add_routes([
        web.post("/api/sms/send", send_sms),
        web.get("/api/sms/info", get_info)
    ])
    
    _LOGGER.info("App initialized and routes registered.")
    return app

