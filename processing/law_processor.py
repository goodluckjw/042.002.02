import re
import requests
import xml.etree.ElementTree as ET
import os

OC = os.getenv("OC", "YOUR_OC")
API_KEY = os.getenv("API_KEY", "YOUR_API_KEY")

BASE_URL = "http://www.law.go.kr/DRF"

def run_search_logic(query, unit):
    law_dict = {}
    law_list_url = f"{BASE_URL}/lawSearch.do?OC={OC}&target=law&type=XML&display=100&search=2&knd=A0002&query={query}"
    res = requests.get(law_list_url)
    res.encoding = "utf-8"

    if res.status_code != 200:
        return {"[요청 실패]": [f"법령 목록 요청 실패: {res.status_code}"]}

    root = ET.fromstring(res.content)
    for law in root.findall("law"):
        law_name = law.findtext("법령명한글")
        mst = law.findtext("법령일련번호")
        if not mst:
            continue

        text_list = get_law_text(mst, query, unit)
        if text_list:
            law_dict[law_name] = text_list

    return law_dict

def get_law_text(mst, query, unit):
    law_url = f"{BASE_URL}/lawService.do?OC={OC}&target=law&type=XML&lawType=한글&ID={mst}"
    res = requests.get(law_url)
    res.encoding = "utf-8"

    if res.status_code != 200:
        return [f"법령 본문 요청 실패: {res.status_code}"]

    root = ET.fromstring(res.content)
    result = []

    for article in root.findall(".//조문"):
        jo_text = article.findtext("조문내용") or ""
        matches = []

        for hang in article.findall("항"):
            hang_text = hang.findtext("항내용") or ""
            ho_texts = [ho.findtext("호내용") or "" for ho in hang.findall("호")]
            for ho_text in ho_texts:
                if query in ho_text:
                    matches.append(indent_line(ho_text, 2, query))

            if query in hang_text:
                matches.append(indent_line(hang_text, 1, query))

        if query in jo_text or matches:
            block = []
            if query in jo_text:
                block.append(indent_line(jo_text, 0, query))
            block.extend(matches)
            if block:
                result.append("<br>".join(block))

    return result

def indent_line(text, level, query):
    highlight = f"<span style='color:red'><strong>{query}</strong></span>"
    text = re.sub(re.escape(query), highlight, text)
    indent = "&nbsp;" * (4 * level)
    return f"<div style='line-height: 1.8'>{indent}{text}</div>"

def run_amendment_logic(find_word, replace_word):
    조사 = get_josa(find_word, "을", "를")
    return [
        f"① 공중 등 협박목적 및 대량살상무기확산을 위한 자금조달행위의 금지에 관한 법률 일부를 다음과 같이 개정한다. 제2조제1항 및 제4항 중 “{find_word}”{조사} 각각 “{replace_word}”로 한다."
    ]

def get_josa(word, josa_with_batchim, josa_without_batchim):
    if not word:
        return josa_with_batchim
    last_char = word[-1]
    code = ord(last_char)
    return josa_with_batchim if (code - 44032) % 28 != 0 else josa_without_batchim