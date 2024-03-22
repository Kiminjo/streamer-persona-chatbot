import streamlit as st

def main():
    st.title('질문 및 답변 웹앱')

    # 초기 데이터
    questions = ['질문1', '질문2', '질문3', '질문4', '질문5', '질문6', '질문7', '질문8', '질문9', '질문10']
    current_question_index = 0

    # 질문 선택 드롭다운
    selected_question_index = st.selectbox('질문 선택', options=list(range(1, len(questions) + 1)), index=current_question_index)

    # 현재 선택된 질문에 대한 입력 필드 생성
    current_question = questions[selected_question_index - 1]
    st.subheader(f'질문 {selected_question_index}')

    # 작은 입력 필드와 큰 입력 필드 생성
    answer_small = st.text_input('대답 (작은 입력 필드)')
    answer_large = st.text_area('대답 (큰 입력 필드)')

    # 확인 버튼
    if st.button('확인'):
        st.success('저장되었습니다.')

    # 저장하기 버튼
    if st.button('저장하기'):
        save_answers(current_question, answer_small, answer_large)

    # 페이지 재로드
    st.experimental_rerun()

def save_answers(question, answer_small, answer_large):
    with open('answers.txt', 'a') as f:
        f.write(f'{question}: \n')
        f.write(f'작은 입력 필드: {answer_small}\n')
        f.write(f'큰 입력 필드: {answer_large}\n\n')
    st.success('질문과 답변이 저장되었습니다.')

if __name__ == "__main__":
    main()
