import streamlit as st
import time

# 세션 상태 초기화
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'time_left' not in st.session_state:
    st.session_state.time_left = 0
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = 'Work'
if 'work_duration' not in st.session_state:
    st.session_state.work_duration = 25 * 60 # 기본 작업 시간 25분
if 'break_duration' not in st.session_state:
    st.session_state.break_duration = 5 * 60 # 기본 휴식 시간 5분

st.title("🍅 스트림릿 뽀모도로 타이머")

# 시간 설정 입력
with st.sidebar:
    st.markdown("### 시간 설정 (분)") # st.h3 대신 st.markdown 사용
    work_minutes = st.number_input("작업 시간", min_value=1, value=st.session_state.work_duration // 60)
    break_minutes = st.number_input("휴식 시간", min_value=1, value=st.session_state.break_duration // 60)

    if st.button("설정 적용"):
        st.session_state.work_duration = work_minutes * 60
        st.session_state.break_duration = break_minutes * 60
        st.session_state.time_left = st.session_state.work_duration # 설정 변경 시 작업 시간으로 초기화
        st.session_state.current_mode = 'Work'
        st.session_state.timer_running = False
        st.rerun()

# 타이머 디스플레이 영역
timer_display = st.empty()

# 타이머 제어 버튼
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("시작"):
        st.session_state.timer_running = True
        if st.session_state.time_left == 0: # 타이머가 0이면 현재 모드의 시간으로 설정
             if st.session_state.current_mode == 'Work':
                 st.session_state.time_left = st.session_state.work_duration
             else:
                 st.session_state.time_left = st.session_state.break_duration

with col2:
    if st.button("일시 정지"):
        st.session_state.timer_running = False

with col3:
    if st.button("재설정"):
        st.session_state.timer_running = False
        st.session_state.time_left = st.session_state.work_duration
        st.session_state.current_mode = 'Work'

# 타이머 실행 로직
if st.session_state.timer_running:
    if st.session_state.time_left > 0:
        # 시간 표시 업데이트
        minutes, seconds = divmod(st.session_state.time_left, 60)
        timer_text = f"## {st.session_state.current_mode} 모드: {minutes:02d}:{seconds:02d}"
        timer_display.markdown(timer_text)

        # 1초 대기 후 시간 감소 및 새로고침
        time.sleep(1)
        st.session_state.time_left -= 1
        st.rerun()
    else:
        # 타이머 종료 시 모드 전환
        if st.session_state.current_mode == 'Work':
            st.session_state.current_mode = 'Break'
            st.session_state.time_left = st.session_state.break_duration
            st.balloons() # 작업 시간 종료 알림
            st.warning("휴식 시간입니다!")
        else:
            st.session_state.current_mode = 'Work'
            st.session_state.time_left = st.session_state.work_duration
            st.balloons() # 휴식 시간 종료 알림
            st.success("작업 시간입니다!")
        st.session_state.timer_running = False
        st.rerun()
else:
    # 타이머가 멈춰있을 때 마지막 시간 표시
    minutes, seconds = divmod(st.session_state.time_left, 60)
    timer_text = f"## {st.session_state.current_mode} 모드: {minutes:02d}:{seconds:02d}"
    timer_display.markdown(timer_text)

# 초기 로드 시 시간 표시
if st.session_state.time_left == 0 and not st.session_state.timer_running:
     minutes, seconds = divmod(st.session_state.work_duration, 60)
     timer_text = f"## Work 모드: {minutes:02d}:{seconds:02d}"
     timer_display.markdown(timer_text)
