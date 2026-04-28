import requests
from bs4 import BeautifulSoup
import json

HEADERS = {"User-Agent": "Mozilla/5.0"}

def safe_get(url, encoding="utf-8"):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.encoding = encoding
        return res.text
    except:
        return ""

# 1. 路透社 稳定
def reuters():
    html = safe_get("https://www.reuters.com/business", "utf-8")
    soup = BeautifulSoup(html, "html.parser")
    arr = []
    for a in soup.select("h3 a")[:6]:
        t = a.get_text(strip=True)
        arr.append({"c":t,"e":"","u":"https://www.reuters.com"+a["href"],"s":"路透社"})
    return arr

# 2. 水利部
def mwr():
    html = safe_get("http://www.mwr.gov.cn/xw/")
    soup = BeautifulSoup(html, "html.parser")
    arr = []
    for a in soup.select("ul.list li a")[:6]:
        arr.append({"c":a.get_text(strip=True),"e":"","u":a["href"],"s":"国家水利部"})
    return arr

# 3. 甘肃水利厅
def gswater():
    html = safe_get("http://slt.gansu.gov.cn/")
    soup = BeautifulSoup(html, "html.parser")
    arr = []
    for a in soup.select(".news_list li a")[:6]:
        arr.append({"c":a.get_text(strip=True),"e":"","u":a["href"],"s":"甘肃省水利厅"})
    return arr

# 4. 天水市水务局
def tsshuiwu():
    html = safe_get("http://slj.tianshui.gov.cn/")
    soup = BeautifulSoup(html, "html.parser")
    arr = []
    for a in soup.select("li a")[:6]:
        txt = a.get_text(strip=True)
        href = a.get("href","")
        arr.append({"c":txt,"e":"","u":href,"s":"天水市水务局"})
    return arr

if __name__=="__main__":
    data = []
    data.extend(reuters())
    data.extend(mwr())
    data.extend(gswater())
    data.extend(tsshuiwu())

    # 强制写入文件
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("OK，本次采集数量：", len(data))
