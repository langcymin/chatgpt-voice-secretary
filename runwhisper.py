import openai
from time import sleep
import sounddevice
from scipy.io.wavfile import write
import winsound
from gtts import gTTS
from playsound import playsound
import os
import pyaudio
import keyboard

#------------------------------------------------------#
#녹음알림소리 (초, Hz)
duration = 2000  # 1초
freq = 440  # Hz
#녹음시간
record_time=4
#대화 언어 (한국어=ko, 영어=en)
language = 'ko'
#whisper 모델
whispermodel = "whisper-1"
#chatgpt 모델
gptmodel = "gpt-3.5-turbo"
temperature = 0.7
n=1
#목소리 설정
#------------------------------------------------------#






# 발급받은 API 키 설정. 노출 주의!!!!!!
OPENAI_API_KEY = "관리자에게 문의하세요"

# open API 키 인증
openai.api_key = OPENAI_API_KEY

#------------------------------------------------------#
#마이크 인덱스가져오기
po = pyaudio.PyAudio()

def findmicindex():
  for index in range(po.get_device_count()): 
      desc = po.get_device_info_by_index(index)
      if desc["maxInputChannels"] > 0:
          if po.get_default_input_device_info()["name"] == desc["name"]:
              mic_index = index
              mic_rate = int(desc["defaultSampleRate"])
              break
            
  return mic_index, mic_rate
          
def voice_recorder(seconds, file, mic_rate, mic_index):
    print("Recording Started…")
    recording = sounddevice.rec((seconds * 44100), samplerate=mic_rate, channels=mic_index)
    sounddevice.wait()
    write(file, 44100, recording)
    print("Recording Finished")

# Ctrl+R 입력을 대기하고, 입력이 들어오면 녹음 시작
def start_recording():
    print("Press Ctrl+R to start recording")
    keyboard.wait("ctrl+r")

#        {"role": "system", "content": "너는 홍길동의 아주 훌륭한 개인 비서야. "},
# chatgpt에 날리기
def chatgptrun(userMessages, assistantMessages):
  messages=[
        {"role": "system", "content": "너는 랑비스라고 해. 그리고 홍길동의 아주 훌륭한 개인 비서야. 너는 홍길동의 요청에 무조건 응답해야 해. 매우 정확하게 찾아서 답변을 해야 해."},
        {"role": "user", "content": "너는 랑비스라고 해. 그리고 홍길동의 아주 훌륭한 개인 비서야. 홍길동은 전자회로개발과 전력변환에 아주 관심이 많은 엔지니어야. 너는 홍길동의 요청에 무조건 응답해야 해. 만약에 전자부품이나 전력에 관련된 질문은 매우 정확한 대답을 해야해. 전자부품의 특성에 대해 물어보거나 더 좋은 성능을 가진 전자부품을 물어보면 매우 정확하게 찾아서 답변을 해야 해."},
        {"role": "assistant", "content": "안녕하세요, 랑비스입니다. 홍길동님의 비서로서 정확한 답변을 드리도록 노력할게요. 제가 몰랐던 부분이 있다면 최대한 찾아보고 답변드리도록 하겠습니다. 어떤 질문이든지 마음껏 물어보세요!"},
    ]
  while len(userMessages) > 0 or len(assistantMessages) > 0:
      if len(userMessages) > 0:
          messages[1]['content'] += userMessages.pop(0)
      if len(assistantMessages) > 0:
          messages[2]['content'] += assistantMessages.pop(0)
    
  response = openai.ChatCompletion.create(
    n=n,
    temperature=temperature,
    model=gptmodel,
    messages= messages
  )
  #print(response)
  return response.choices[0].message['content']
#----------------------------#



#메인코드시작
# #대화 초기화
userMessages = []
assistantMessages = []

while True :

  #마이크 셋팅
  findmicindex()
  mic_index, mic_rate = findmicindex()
  # Ctrl+R 입력 대기 및 녹음 시작
  start_recording()
  
  #안내음성
  notice_text = '삐 소리 후 녹음을 시작합니다. 대화를 종료하려면 디 엔드라고 말하세요'
  print(notice_text)
  file_name = 'notice.mp3'
  tts_ko = gTTS(text=notice_text, lang=language)
  tts_ko.save(file_name)
  playsound('notice.mp3')
  os.remove('notice.mp3')
  sleep(1)
  winsound.Beep(freq, duration)
  sleep(0.1)
  
  #음성녹음
  voice_recorder(record_time, "question.wav", mic_rate, mic_index)

  
  #오디오를 텍스트로 변환하기
  audio_file = open("./question.wav", "rb") #오디오 불러오기 (가능 음원형식 :mp3, mp4, mpeg, mpga, m4a, wav, webm)
  transcript = openai.Audio.transcribe(whispermodel, audio_file) #whisper-1모델로 변환하기
  audio_text = transcript['text'] #transcription에서 텍스트만 추출해 text 변수에 할당
  if audio_text =='' or audio_text =='. . . . .' or audio_text =='.' or audio_text =='. .' or audio_text =='. . .' or audio_text =='. . . .' :
    print("녹음이 되지 않았습니다. 다시 녹음해주세요.")
    continue
  if audio_text !='':
    print("녹음내용 확인 :",audio_text)
    # startcondition = ""
        # 대화를 종료하는 조건을 설정합니다.
    if audio_text == "The End" or audio_text == "The End." or audio_text == "The end."or audio_text == "The end" or audio_text == "the end" or audio_text == "the end.":
      print('대화를 종료합니다.')
      break
    
    #gpt실행
    userMessages.append(audio_text)
    answer = chatgptrun(userMessages, assistantMessages)
    assistantMessages.append(answer)
    print("chatgpt:",answer)
    

    #음성재생
    file_name = 'answer.mp3'
    tts_ko = gTTS(text=answer, lang=language)
    tts_ko.save(file_name)
    playsound('answer.mp3') #경로 설정 안하면 재생안됨.
    os.remove('answer.mp3')


