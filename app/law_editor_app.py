import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "processing")))
from law_processor import run_search_logic, run_amendment_logic

st.set_page_config(layout="wide")
st.title("📘 부칙개정 도우미")

with st.expander("ℹ️ 읽어주세요"):
    st.markdown("이 앱은 검색 기능과 개정문 자동생성 기능을 제공합니다.\n- 검색: 법령에서 특정 단어가 포함된 조문을 검색합니다.\n- 개정문 생성: 특정 단어를 다른 단어로 대체하는 부칙 개정문을 생성합니다.")

# 검색 기능 UI
st.header("🔍 검색 기능")
scol1, scol2, scol3 = st.columns([6, 1, 1])
with scol1:
    search_query = st.text_input("검색어 입력", key="search_query")
with scol2:
    do_search = st.button("검색 시작")
with scol3:
    do_reset = st.button("초기화")

search_unit = st.radio("다중검색 단위선택 (미선택시 법률 단위 필터링)", ["법률", "조", "항", "호", "목"], horizontal=True, index=0)
st.caption("※ 예: '행정 & 기본' → 선택된 단위 내에 두 검색어가 모두 포함될 때 결과 출력")

if do_search and search_query:
    with st.spinner("🔍 검색 중..."):
        search_result = run_search_logic(search_query, search_unit)
        st.success("검색 완료")
        for law_name, sections in search_result.items():
            with st.expander(f"📄 {law_name}"):
                for html in sections:
                    st.markdown(html, unsafe_allow_html=True)

# 개정문 생성 UI
st.header("✏️ 타법개정문 생성")
acol1, acol2, acol3 = st.columns([4, 4, 1])
with acol1:
    find_word = st.text_input("찾을 단어", key="find_word")
with acol2:
    replace_word = st.text_input("바꿀 단어", key="replace_word")
with acol3:
    do_amend = st.button("개정문 생성")

if do_amend and find_word and replace_word:
    with st.spinner("🛠 개정문 생성 중..."):
        amend_result = run_amendment_logic(find_word, replace_word)
        st.success("생성 완료")
        for amend in amend_result:
            st.markdown(f"➤ {amend}")