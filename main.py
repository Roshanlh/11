import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def trans(text):
    try:
        url = f"https://api.aa1.cn/api/translator?msg={requests.utils.quote(text)}"
        res = requests.get(url, timeout=8)
        return res.json().get("result", text)
    except:
        return text

def reuters():
    s = BeautifulSoup(requests.get("https://www.reuters.com/business",headers=HEADERS).text,"html.parser")
    arr=[]
    for a in s.select("h3 a")[:6]:
        t=a.get_text(strip=True)
        arr.append({"c":trans(t),"e":t,"u":"https://www.reuters.com"+a["href"],"s":"路透社"})
    return arr

def bloomberg():
    s = BeautifulSoup(requests.get("https://www.bloomberg.com/economics",headers=HEADERS).text,"html.parser")
    arr=[]
    for a in s.select("article h3 a")[:6]:
        t=a.get_text(strip=True)
        u=a["href"]
        if not u.startswith("http"):u="https://www.bloomberg.com"+u
        arr.append({"c":trans(t),"e":t,"u":u,"s":"彭博社"})
    return arr

def economist():
    s = BeautifulSoup(requests.get("https://www.economist.com/finance-and-economics",headers=HEADERS).text,"html.parser")
    arr=[]
    for a in s.select("h3 a")[:6]:
        t=a.get_text(strip=True)
        arr.append({"c":trans(t),"e":t,"u":"https://www.economist.com"+a["href"],"s":"经济学人"})
    return arr

def wsj():
    s = BeautifulSoup(requests.get("https://www.wsj.com/economy",headers=HEADERS).text,"html.parser")
    arr=[]
    for a in s.select("h2 a")[:6]:
        t=a.get_text(strip=True)
        arr.append({"c":trans(t),"e":t,"u":a["href"],"s":"华尔街日报"})
    return arr

def fortune():
    s = BeautifulSoup(requests.get("https://fortune.com/economy/",headers=HEADERS).text,"html.parser")
    arr=[]
    for a in s.select("h3 a")[:6]:
        t=a.get_text(strip=True)
        arr.append({"c":trans(t),"e":t,"u":a["href"],"s":"财富"})
    return arr

def mwr():
    res = requests.get("http://www.mwr.gov.cn/xw/",headers=HEADERS)
    res.encoding="utf-8"
    s=BeautifulSoup(res.text,"html.parser")
    arr=[]
    for a in s.select("ul.list li a")[:6]:
        arr.append({"c":a.get_text(strip=True),"e":"","u":a["href"],"s":"国家水利部"})
    return arr

def gswater():
    res = requests.get("http://slt.gansu.gov.cn/",headers=HEADERS)
    res.encoding="utf-8"
    s=BeautifulSoup(res.text,"html.parser")
    arr=[]
    for a in s.select(".news_list li a")[:6]:
        arr.append({"c":a.get_text(strip=True),"e":"","u":a["href"],"s":"甘肃省水利厅"})
    return arr

def tsshuiwu():
    res = requests.get("http://slj.tianshui.gov.cn/",headers=HEADERS)
    res.encoding="utf-8"
    s=BeautifulSoup(res.text,"html.parser")
    arr=[]
    for a in s.select("li.clearfix a")[:6]:
        arr.append({"c":a.get_text(strip=True),"e":"","u":a["href"],"s":"天水市水务局"})
    return arr

if __name__=="__main__":
    data = []
    data.extend(reuters())
    data.extend(bloomberg())
    data.extend(economist())
    data.extend(wsj())
    data.extend(fortune())
    data.extend(mwr())
    data.extend(gswater())
    data.extend(tsshuiwu())
    with open("news.json","w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
    print("更新完成")
