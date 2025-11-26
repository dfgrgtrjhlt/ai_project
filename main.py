import streamlit as st 
st.title('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름을 입력하셈') 
st.selectbox('니가 좋아하는 걸 말해보세여',['떡볶이'])
if st.button('인사말 생성'): 
  st.info(a+'님, 안녕하세요 반가워용!!><')
st.warning(b+'를 좋아하시는구먼?')
st.error('반갑웡')
st.balloons()
