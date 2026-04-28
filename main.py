import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def trans(text):
    try:
        url = f"https://api.aa1.cn/api/translator?msg={requests.utils.quote(text)}"
        res = requests.get(url, timeout=8)
        data = res.json()
        return data.get("result", text)
    except:
        return text

def safe_get(url, encoding=None):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if encoding:
            r.encoding = encoding
        return r.text
    except:
        return ""

# 外媒
def reuters():
    html = safe_get("https://www.reuters.com/business")
    if not html: return []
    s = BeautifulSoup(html, "html.parser")
    arr = []
    for a in s.select("h3 a")[:5]:
        t = a.get_text(strip=True)
        arr.append({"c":trans(t), "e":t, "u":"https://www.reuters.com"+a["href"], "s":"路透社"})
    return arr

def bloomberg():
    html = safe_get("https://www.bloomberg.com/economics")
    if not html: return []
    s = BeautifulSoup(html, "html.parser")
    arr = []
    for a in s.select("article a")[:5]:
        t = a.get_text(strip=True)
        if not t: continue
        u = a["href"]
        if not u.startswith("http"):
            u = "https://www.bloomberg.com" + u
        arr.append({"c":trans(t), "e":t, "u":u, "s":"彭博社"})
    return arr

def economist():
    html = safe_get("https://www.economist.com/finance-and-economics")
    if not html: return []
    s = BeautifulSoup(html, "html.parser")
    arr = []
    for a in s.select("h3 a")[:5]:
        t = a.get_text(strip=True)
        arr.append({"c":trans(t), "e":t, "u":"https://www.economist.com"+a["href"], "s":"经济学人"})
    return arr

def wsj():
    return []

def fortune():
    html = safe_get("https://fortune.com/economy/")
    if not html: return []
    s = BeautifulSoup(html, "html.parser")
    arr = []
    for a in s.select("h3 a")[:5]:
        t = a.get_text(strip=True)
        arr.append({"c":trans(t), "e":t, "u":a["href"], "s":"财富"})
    return arr

# 国内水利
def mwr():
    html = safe_get("http://www.mwr.gov.cn/xw/", "utf-8")
    if not html: return []
    s = BeautifulSoup(html, "html.parser")
    arr = []
    for a in s.select("ul.list li a")[:5]:
        t = a.get_text(strip=True)
        arr.append({"c":t, "e":"", "u":a["href"], "s":"国家水利部"})
    return arr

def gswater():
    html = safe_get("http://slt.gansu.gov.cn/", "utf-8")
    if not html: return []
    s = BeautifulSoup(html, "html.parser")
    arr = []
    for a in s.select(".news_list li a")[:5]:
        t = a.get_text(strip=True)
        arr.append({"c":t, "e":"", "u":a["href"], "s":"甘肃省水利厅"})
    return arr

def tsshuiwu():
    html = safe_get("http://slj.tianshui.gov.cn/", "utf-8")
    if not html: return []
    s = BeautifulSoup(html, "html.parser")
    arr = []
    for a in s.select("li a")[:5]:
        t = a.get_text(strip=True)
        arr.append({"c":t, "e":"", "u":a["href"], "s":"天水市水务局"})
    return arr

if __name__ == "__main__":
    data = []
    data += reuters()
    data += bloomberg()
    data += economist()
    data += fortune()
    data += mwr()
    data += gswater()
    data += tsshuiwu()

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ 成功抓取新闻：", len(data), "条")
