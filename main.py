import requests
from bs4 import BeautifulSoup
import json
import traceback

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def safe_req(url, timeout=10):
    try:
        return requests.get(url, headers=HEADERS, timeout=timeout)
    except Exception:
        return None

# 英译中简易容错翻译
def translate_text(text):
    if not text:
        return text
    try:
        res = requests.get(f"https://translate.argosopentech.com/translate",
            json={"q":text,"source":"en","target":"zh"}).json()
        return res.get("translatedText",text)
    except:
        return text

# —— 稳定源：路透 RSS ——
def crawl_reuters():
    try:
        res = safe_req("https://feeds.reuters.com/reuters/businessNews")
        if not res:
            return []
        soup = BeautifulSoup(res.text, "xml")
        items = soup.find_all("item")[:5]
        lst = []
        for item in items:
            title_en = item.find("title").text
            title_cn = translate_text(title_en)
            link = item.find("link").text
            lst.append({"c":title_cn,"e":title_en,"u":link,"s":"路透社"})
        return lst
    except:
        return []

# —— 水利系统 3 个官网（国内 100%稳定）——
def crawl_mwr():
    try:
        res = safe_req("http://www.mwr.gov.cn/xw/")
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text,"html.parser")
        lst = []
        for a in soup.select("ul.list li a")[:5]:
            lst.append({"c":a.get_text(strip=True),"e":"","u":a["href"],"s":"国家水利部"})
        return lst
    except:
        return []

def crawl_gsl():
    try:
        res = safe_req("http://slt.gansu.gov.cn/")
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text,"html.parser")
        lst = []
        for a in soup.select(".news_list li a")[:5]:
            lst.append({"c":a.get_text(strip=True),"e":"","u":a["href"],"s":"甘肃省水利厅"})
        return lst
    except:
        return []

def crawl_tswj():
    try:
        res = safe_req("http://slj.tianshui.gov.cn/")
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text,"html.parser")
        lst = []
        for a in soup.select("li a")[:5]:
            href = a.get("href","")
            lst.append({"c":a.get_text(strip=True),"e":"","u":href,"s":"天水市水务局"})
        return lst
    except:
        return []

def main():
    all_news = []
    all_news.extend(crawl_reuters())
    all_news.extend(crawl_mwr())
    all_news.extend(crawl_gsl())
    all_news.extend(crawl_tswj())

    # 写入文件，强制覆盖，一定生成合法json
    with open("news.json","w",encoding="utf-8") as f:
        json.dump(all_news, ensure_ascii=False, indent=2, fp=f)

    print(f"执行完成，共获取资讯 {len(all_news)} 条")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        # 即便全局报错，也要生成空合法json，保证网页不崩
        with open("news.json","w",encoding="utf-8") as f:
            json.dump([], f)
