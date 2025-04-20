import re

def run_search_logic(query, unit):
    # 실제 법령 API 및 XML 분석 로직은 이후 연결
    # 여기서는 형식 구조와 강조 마크업 예시 구현
    return {
        "공중 등 협박목적 및 대량살상무기확산을 위한 자금조달행위의 금지에 관한 법률": [
            highlight_search_term("① 이 법은 공중 등 협박목적 및 대량살상무기확산을 위한 자금조달행위의 금지에 필요한 사항을 정한다.", query),
            highlight_search_term("② 금융위원회는 제1항에 따라 금융거래등제한대상자를 지정할 수 있다.", query),
        ]
    }

def highlight_search_term(text, query):
    pattern = re.escape(query)
    highlighted = re.sub(pattern, f"<span style='color:red'><strong>{query}</strong></span>", text)
    return f"<div style='padding-left:1em; line-height: 1.8;'>{highlighted}</div>"

def run_amendment_logic(find_word, replace_word):
    # 개정문 자동 생성 예시
    조사 = "을" if has_final_consonant(find_word) else "를"
    return [
        f"① 공중 등 협박목적 및 대량살상무기확산을 위한 자금조달행위의 금지에 관한 법률 일부를 다음과 같이 개정한다. 제2조제1항 및 제4항 중 “{find_word}”{조사} 각각 “{replace_word}”로 한다."
    ]

def has_final_consonant(word):
    if not word: return False
    code = ord(word[-1])
    return (code - 44032) % 28 != 0