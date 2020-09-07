# references:
# https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
import requests
import pandas as pd
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}


def download_free_proxies(to_csv=True):
    print("downloading free proxies...")
    url = "https://free-proxy-list.net/anonymous-proxy.html"
    page = requests.get(url, headers=HEADERS)
    table = pd.read_html(page.text)
    df = table[0]
    df.dropna(inplace=True)
    df = df.groupby(['Https']).get_group('yes')
    df.reset_index(inplace=True)

    if to_csv:
        df.to_csv("../csv/proxies.csv")

if __name__ == '__main__':
    download_free_proxies()