import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup

from _db import database
from settings import CONFIG


class Helper:
    def get_header(self):
        header = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E150",  # noqa: E501
            "Accept-Encoding": "gzip, deflate",
            # "Cookie": CONFIG.COOKIE,
            "Cache-Control": "max-age=0",
            "Accept-Language": "vi-VN",
            # "Referer": "https://mangabuddy.com/",
        }
        return header

    def download_url(self, url):
        return requests.get(url, headers=self.get_header())

    def log(self, log_msg, log_file: str, is_error_log: bool = True) -> None:
        Path(CONFIG.LOG_FOLDER).mkdir(parents=True, exist_ok=True)
        Path(CONFIG.TMP_FOLDER).mkdir(parents=True, exist_ok=True)
        with open(CONFIG.TMP_FILE, "w") as f:
            f.write(f"{time.asctime()} LOG: {log_msg}\n")

        cmd = f"cat {CONFIG.TMP_FILE} >> {log_file}"
        if is_error_log:
            cmd = f"""grep -q "{log_msg}" {log_file} || {cmd}"""
        os.system(cmd)


helper = Helper()
