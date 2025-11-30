import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# --- [서버용 한글 폰트 설정] ---
@st.cache_resource
def font_setup():
    if not os.path.exists("NanumGothic.ttf"):
        os.system("wget https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf")
    fm.fontManager.addfont("NanumGothic.ttf")
    plt.rc('font', family='NanumGothic') 
    plt.rcParams['axes.unicode_minus'] = False 

font_setup()

# --- [데이터 준비] ---
def get_data(keyword):
    chart_df = pd.DataFrame({
        "분야": ["사업화", "R&D", "융자", "수출", "기타"],
        "공고수": [12, 5, 8, 3, 4]
    })
    data = [
        {"제목": f"2025년 {keyword} 초기창업패키지", "기관": "창업진흥원", "지원금": 10000, "상태": "접수중", "요약": "최대 1억원 지원", "경쟁률": "12.5:1"},
        {"제목": "서울시 넥스트 로컬 6기", "기관": "서울시", "지원금": 7000, "상태": "마감임박", "요약": "지역 연계 창업", "경쟁률": "8:1"},
        {"제목": f"{keyword} AI 바우처", "기관": "NIPA", "지원금": 3000, "상태": "접수중", "요약": "솔루션 도입 지원", "경쟁률": "5:1"},
        {"제목": "소상공인 스마트상점", "기관": "소진공", "지원금": 1500, "상태": "접수예정", "요약": "키오스크 도입", "경쟁률": "3:1"},
        {"제목": "중소기업 R&D 역량강화", "기관": "중기부", "지원금": 5000, "상태": "상시모집", "요약": "R&D 전주기 지원", "경쟁률": "6:1"},
        {"제목": "글로벌 점프업", "기관": "KOTRA", "지원금": 2000, "상태": "접수중", "요약": "수출 지원", "경쟁률": "4:1"}
    ]
    return pd.DataFrame(data), chart_df

# --- [화면 구성] ---
st.set_page_config(page_title="비즈내비 Pro", layout="wide", page_icon="🏛️")

with st.sidebar:
    st.title("⚙️ 검색 옵션")
    keyword = st.text_input("키워드", value="AI/빅데이터")
    st.write("---")
    st.link_button("👨‍💼 1:1 컨설팅 신청", "https://open.kakao.com", use_container_width=True)

st.title("📊 정부지원사업 인사이트 대시보드")
st.caption(f"분석 키워드: {keyword}")

df, chart_df = get_data(keyword)

# KPI 지표
c1, c2, c3, c4 = st.columns(4)
c1.metric("수집 공고", "32건", "+5")
c2.metric("평균 지원금", "5,800만", "-200")
c3.metric("매칭 확률", "87%", "+12%")
c4.metric("경쟁률 예측", "4.5:1", "보통")

st.markdown("---")

tab1, tab2 = st.tabs(["📈 시장 분석", "📋 공고 리스트"])

with tab1:
    st.subheader("지원 분야별 분포")
    col_chart, col_text = st.columns([3, 2])
    with col_chart:
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(chart_df['분야'], chart_df['공고수'], color=['#FF9F9F', '#9FDEFF', '#FFF39F', '#9FFFB6', '#D69FFF'])
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, height, f'{int(height)}건', ha='center', va='bottom')
        ax.set_title("분야별 공고 수", fontsize=15)
        st.pyplot(fig)
    with col_text:
        st.success(f"💡 **'{keyword}'** 분야 기회!")
        st.info("사업화 자금 지원이 가장 활발합니다.")

with tab2:
    st.subheader("맞춤형 추천 공고")
    for index, row in df.iterrows():
        with st.expander(f"📌 {row['제목']} ({row['지원금']}만원)"):
            st.write(f"**기관:** {row['기관']} │ **요약:** {row['요약']}")
            st.button("상세 분석", key=f"btn_{index}")
