import os

def get_env(key, default=None, required=False):
    value = os.getenv(key, default)
    if required and not value:
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return value

def load_config():
    return {
        "WEBHOOK_URL": get_env("WEBHOOK_URL", "http://localhost:8123/webhook/sms"),
        "WEBHOOK_TOKEN": get_env("WEBHOOK_TOKEN"),
        "GSM_DEVICE": get_env("GSM_DEVICE", "/dev/ttyUSB0"),
        "GSM_CONNECTION": get_env("GSM_CONNECTION", "at115200"),
        "POLL_INTERVAL": int(get_env("POLL_INTERVAL", "10"))
    }

