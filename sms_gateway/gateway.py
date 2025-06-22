import asyncio
import logging
import gammu
from gammu.asyncworker import GammuAsyncWorker
import aiohttp

_LOGGER = logging.getLogger("sms_gateway")

SMS_STATE_UNREAD = "UnRead"

class Gateway:
    def __init__(self, config):
        self._config = config
        self._worker = GammuAsyncWorker(self.sms_pull)
        self._worker.configure({
            "Device": config["GSM_DEVICE"],
            "Connection": config["GSM_CONNECTION"],
        })
        self._first_pull = True

    async def init_async(self):
        await self._worker.init_async()
        _LOGGER.debug("Gateway initialized")

    def sms_pull(self, state_machine):
        state_machine.ReadDevice()
        _LOGGER.debug("Polling modem for SMS...")
        self.sms_read_messages(state_machine, self._first_pull)
        self._first_pull = False

    def sms_read_messages(self, state_machine, force=False):
        entries = self.get_and_delete_all_sms(state_machine, force)
        for entry in entries:
            decoded = gammu.DecodeSMS(entry)
            message = entry[0]
            if message["State"] == SMS_STATE_UNREAD:
                text = "".join([e["Buffer"] for e in decoded.get("Entries", []) if e["Buffer"]])
                event_data = {
                    "phone": message["Number"],
                    "date": str(message["DateTime"]),
                    "message": text or message.get("Text", "")
                }
                asyncio.create_task(self._notify_incoming_webhook(event_data))

    def get_and_delete_all_sms(self, state_machine, force=False):
        entries = []
        try:
            entry = state_machine.GetNextSMS(Folder=0, Start=True)
            while entry:
                entries.append(entry)
                try:
                    state_machine.DeleteSMS(Folder=0, Location=entry[0]["Location"])
                except gammu.ERR_MEMORY_NOT_AVAILABLE:
                    _LOGGER.warning("Could not delete SMS at %s", entry[0]["Location"])
                entry = state_machine.GetNextSMS(Folder=0, Location=entry[0]["Location"])
        except gammu.ERR_EMPTY:
            pass
        return gammu.LinkSMS(entries)

    async def _notify_incoming_webhook(self, payload):
        if not self._config["WEBHOOK_URL"]:
            _LOGGER.debug("No webhook URL configured; skipping.")
            return
        headers = {"Content-Type": "application/json"}
        if self._config["WEBHOOK_TOKEN"]:
            headers["Authorization"] = f"Bearer {self._config['WEBHOOK_TOKEN']}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self._config["WEBHOOK_URL"], json=payload, headers=headers) as resp:
                    if resp.status != 200:
                        _LOGGER.warning("Webhook failed with HTTP %d", resp.status)
            except Exception as e:
                _LOGGER.error("Webhook error: %s", e)

    async def send_sms_async(self, message):
        return await self._worker.send_sms_async(message)

    async def get_info_async(self):
        return {
            "manufacturer": await self._worker.get_manufacturer_async(),
            "model": await self._worker.get_model_async(),
            "firmware": await self._worker.get_firmware_async(),
            "imei": await self._worker.get_imei_async(),
            "signal_quality": await self._worker.get_signal_quality_async(),
            "network_info": await self._worker.get_network_info_async()
        }

    async def terminate_async(self):
        return await self._worker.terminate_async()

