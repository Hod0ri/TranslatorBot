"""한국어 ↔ 일본어 디스코드 번역 봇.

번역이 켜진 채널에서 한국어/일본어 메시지에 상대 언어 번역을 답글로 단다.
- AI 번역(OpenAI): 대화 문맥, 참가자 닉네임, 채널 주제(예: 원신)를 참고한다.
  실패하거나 AI_TIMEOUT 을 넘기면 Google 번역으로 대체한다.
- Google 번역: 비공식 무료 엔드포인트. 막히면(429 등) AI 로 대체한다.

슬래시 커맨드
  /tr on | off | status       채널 번역 켜기/끄기/상태 (켜면 AI 번역)
  /tr ai on | off             AI 번역 ↔ Google 번역 전환
  /tr topic [주제]             채널 주제. AI 가 그 게임의 공식 명칭으로 번역한다
  /tr summary                 최근 메시지 요약
  /tr math <수식>              LaTeX 수식을 이미지로
  /tr credits                 이번 실행의 OpenAI 사용량과 예상 비용
  /genshin                    원신 채널 역할 받기/빼기
  메시지 우클릭 → 앱 → ふりがな   한자에 후리가나 달기

모듈
  config      .env 와 상수            state       채널 설정 (state.json)
  language    언어 감지, 번역 제외 구간   memory      채널별 대화 문맥과 참가자
  ai          OpenAI 호출과 사용량      translate   번역 (AI / Google)
  furigana    후리가나                 mathrender  수식 이미지
  ui          임베드, 봇 상태 표시       handler     메시지 번역 처리
  client      봇 본체                  commands/   슬래시 커맨드
"""
