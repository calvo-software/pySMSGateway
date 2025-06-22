from aiohttp import web
import logging

_LOGGER = logging.getLogger("sms_gateway.api")

async def send_sms(request):
    gateway = request.app["gateway"]
    try:
        data = await request.json()
        sms = {
            "Text": data["text"],
            "Number": data["number"],
            "SMSC": {"Location": 1}
        }
        await gateway.send_sms_async(sms)
        return web.json_response({"status": "SMS sent"})
    except Exception as e:
        _LOGGER.error("SMS send failed: %s", e)
        return web.json_response({"error": str(e)}, status=500)

async def get_info(request):
    gateway = request.app["gateway"]
    try:
        info = await gateway.get_info_async()
        return web.json_response(info)
    except Exception as e:
        _LOGGER.error("Failed to get modem info: %s", e)
        return web.json_response({"error": str(e)}, status=500)

