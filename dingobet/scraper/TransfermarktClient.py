import requests
from bs4 import BeautifulSoup

class TransfermarktClient:
    def __init__(self):
        self._hostUrl = "https://www.transfermarkt.com/"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

    def getSoup(self, url: str):
        r = requests.get(url=url, headers=self.headers)
        return BeautifulSoup(r.content, "html.parser")

    def getLiveSoup(self):
        url = self._hostUrl + "ticker/index/live"
        return self.getSoup(url)