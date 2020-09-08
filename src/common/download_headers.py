import requests
import pandas as pd

HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}


def download_agent_headers(to_csv=True):
    print("downloading free agent-headers....")
    browers = ['firefox']
    url = "https://developers.whatismybrowser.com/useragents/explore/software_name/"

    dfs = []
    for b in browers:
        endpoint = "".join([url, b])
        page = requests.get(endpoint, headers=HEADERS)
        table = pd.read_html(page.text)
        df = table[0]
        df.columns = df.columns.str.strip()
        dfs.append(df)

    results = pd.concat(dfs)
    if to_csv:
        results.to_csv("./src/csv/user_agents.csv")