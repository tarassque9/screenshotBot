import imgkit
import time


def take_screenshot(url, filename):
    try:
        imgkit.from_url(url, f'screenshots/{filename}.jpg')
        return True
    except Exception:
        return False
