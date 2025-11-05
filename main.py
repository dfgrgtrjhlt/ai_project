import streamlit as st 
st.title('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름을 입력하셈') 
st.selectbox('니가 좋아하는 걸 처 말해보시긬ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ',['난김연희','손민지','김린유','함승현황은서','떡볶이','이채민'])
if st.button('인사말 생성'): 
  st.info(a+'님, 안녕하시긔!!!!!!!!!!!!!!!!!!!!! 반갑지않긔윤!!><')
st.warning(b+'를 꼴에z좋아하시는구먼?')
st.error('반갑노')
st.balloons()
