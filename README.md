# StreamAssist-Bot

본 레포지토리는 스트리머의 개인정보에 대한 답변을 대신 해주는 챗봇을 만드는 프로젝트입니다. 

인터넷 개인 방송은 스트리머와 시청자가 실시간 쌍방향 소통하는 플랫폼입니다. 실시간 쌍방향 소통은 기존 방송 시스템과 차별화 되는 인터넷 방송만의 특징으로 이러한 점으로 인해 여러 장단이 생기게 됩니다. 

본 프로젝트는 대표적인 실시간 쌍방향 소통의 문제점인 `지속적이고 수준 낮은 질문으로 인한 방송 흐름 끊김` 문제를 해결하는 것을 목표로 시작되었습니다. 

<br>

## 실행 예시 
![qa](image/qa.png)
위 질문은 스트리머 침착맨이 방송에서 받은 질문과 그에 대한 대답을 스크립트로 옮긴 내용입니다. 

읿반적인 챗봇에 동일한 내용을 질문하면 아래 표의 좌측과 같이 통상적인 대답을 하거나 할루시네이션 증상으로 인해 이상한 답변을 생성합니다. 

본 레포지토리는 특수하고 개인적인 내용을 반영한 챗봇을 만드는 것을 목표로 `데이터 수집`, `전처리`, `튜닝 프로세스`를 구축하였습니다. 


|튜닝 전 응답|튜닝 후 응답| 
|---|---|
|![before_tuning](image/before_tuning.png)|![after_tuning](image/after_tuning.png)|

<br>

### 실행 방법 
1. 환경 만들기
```
conda create -n assist_bot python=3.10.9
```

이 버전은 파이썬 3.10 버전을 필요로 합니다.    
그 이하 버전의 파이썬 사용 시, 특정 기능에 제한이 있을 수 있습니다. 


2. requirement 설치 

```
pip install -r requirements.txt
```

3. 스트리머 정보 구축 
```
python constuct_db.py
```

위 코드를 실행하면 스트리머의 정보를 담은 vectore DB가 생성됩니다. 


4. 채팅 화면 접속 
```
chainlit run main.py
```

5. 실행 종료 
```
control + c (in terminal)
```
<br>

## Error 발생 시 해결 방법 
```
ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): address already in use
```

- 원인: chainlit 접속에 필요한 8000번 포트를 이미 사용 중인 경우 발생하는 에러 

<br>

### 해결 방법 
1. 8000 포트를 사용중인 프로세스 확인
```
sudo lsof -i:8000
```

2. 프로세스 죽이기 
```
kill $PID

kill -9 $PID  //to forcefully kill the port
```

<br>

## 개발 계획 
- [x] 채팅 GUI 추가
- [x] requirements 추가 
- [ ] 커스텀 데이터 입력 GUI 화면 추가 
- [ ] 학습용 데이터 DB화 
- [ ] 데이터 증강 기능 추가 
- [ ] 답변 말투 변경 
- [ ] 추론용 API 서버 구축 
