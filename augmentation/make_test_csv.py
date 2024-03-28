import pandas as pd 

q = ["소영이가 아빠는 왜 집에서 노냐고 물어본 적 없나요?",
     "본인이 봐도 재밌는 침튜브 컨텐츠가 있을까요?",
     "방송을 하면서 가장 뿌듯함을 느낄때가 언제인가요?", 
     "방송에서 만든 요리 중에 진짜 이건 못먹겠다 생각한 요리가 있었나요?",
     "가족들이랑 소풍방송 하는거 어떨까요?"]

a = ["네 그런거 모르던데요.",
     "최근에 꽂힌건 삼괴권이요. 제가 원래 제 영상 잘 안보는 편인데 이건 20번 봤어요.",
     "반응이 좋을 때, 특히 ㅋㅋㅋ로 도배가 될때가 제일 좋아요. '아 너무 재밌어요'는 좀 가짜 리액션이라고 생각해서요.",
     "임세모님이 나왔던 아빠손 볶음밥이요. 기름이 너무 많고 먹기 힘들었어요.",
     "안돼요. 어색할 것 같아요."]

df = pd.DataFrame({"question": q, "answer": a})
df.to_csv("data/test_data.csv", index=False)