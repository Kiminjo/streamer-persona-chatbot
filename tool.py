import re
def anno_totext(text,dict):
    #문자열에서 [숫자] 형태의 텍스트를 추출
    p = re.compile('\[([^]]+)\]')
    for idx,wiki in enumerate(text):
        temp=p.findall(wiki)
        for c in temp:
            #[그림해설1] 과 같은 특이한 경우를 제외하기 위한 if문
            if str(c) in dict.keys():
                wiki=wiki.replace('['+str(c)+']',' '+ dict[c])
        text[idx]=wiki
    return text


def cleaning(text_list):
    remove_word=["#","|","\'"]
    for i in range(len(text_list)):
        for word in remove_word:
            text_list[i] = text_list[i].replace(word, "")
    return text_list