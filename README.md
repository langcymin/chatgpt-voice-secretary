# javis_chatgpt
윈도우 터미널로 사용하는 자비스

0. *****API 키는 절대 노출되어서는 안되는 값입니다. 노출에 주의해주세요.******

    1) API 키 발급 : https://platform.openai.com/account/api-keys   
    2) Payment정보 입력 : https://platform.openai.com/account/billing/overview   
    3) 과금정보(토큰당 과금구조) : https://openai.com/pricing#language-models    
    - 토큰? : 문장을 텍스트로 나눌 수 있는 가장 작은 단위
    - 오늘은 날씨가 너무 춥다 : "오늘은" +"날씨가"+"너무"+"춥다" -> 5개 토큰
    - Hello! How are you today? : "Hello!" + "How"+"are"+"you"+"today?" -> 5개 토큰

1. Window환경에서만 사용 가능합니다.

2. python 버전은 아래로 들어가 최신버전을 설치해주세요.
https://www.python.org/downloads/

3. 아래는 설치해야 하는 python 모듈의 모음입니다. 터미널에서 입력해주세요.   
pip3 install -r requirements.txt

4. 파일 실행은 다음과 같이 합니다.
    1) 터미널을 엽니다.
    2) 파일이 있는 폴더로 이동합니다.
    - 상위폴더 이동 : cd.. 
    - 하위폴더 이동 : cd 폴더이름
    3) 다음명령어를 입력합니다 : py -3.11 runwhisper.py 

5. 실행 중에 마이크 설정에 문제가 생겼을 경우, findmicindex.py로 index와 샘플레이트를 확인합니다.
