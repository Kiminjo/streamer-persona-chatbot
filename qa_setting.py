import streamlit as st
import time

def main():
    save_path = "data/qa.txt"
    st.title('📜 맞춤형 질문 & 대답 작성')

    # 현재 열려 있는 아코디언의 인덱스를 저장하기 위한 변수
    current_accordion_index = 0

    # 10개의 아코디언 생성
    for i in range(1, 11):
        with st.expander(f'질문 {i}', expanded=(i == 1)):  # 초기에는 첫 번째 아코디언이 열려 있도록 설정
            question = st.text_input(f'질문', key=f'question_{i}')
            answer = st.text_area(f'대답', key=f'answer_{i}', height=150)

            # 현재 아코디언의 인덱스를 저장
            current_accordion_index = i

            # 확인 버튼 생성
            if i < 10:
                if st.button(f'확인', key=f'confirm_button_{i}'):
                    st.success("저장되었습니다")
                    time.sleep(0.2)
                    st.empty()

    # 마지막 아코디언의 확인 버튼 생성
    if current_accordion_index == 10:
        if st.button('저장하기'):
            save_to_txt(save_path)
            st.success(f"질의 내용이 {save_path}에 저장되었습니다.")
            time.sleep(0.2)
            st.empty()

def save_to_txt(filename: str):
    with open(filename, 'w', encoding='utf-8') as file:
        for i in range(1, 11):
            question = st.session_state[f'question_{i}']
            answer = st.session_state[f'answer_{i}']
            if question.strip() and answer.strip():  # 질문과 대답이 모두 입력되었을 때만 파일에 쓰기
                file.write(f'{question} {answer}\n\n')

if __name__ == "__main__":
    main()
