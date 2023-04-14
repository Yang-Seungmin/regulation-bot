# regulation-bot
병천의 규ㅣ재 Regulation을 regulate하는 봇

## Commands
- `!규모지`
- `!규타일 랜덤 (x) (y)`
  - x * y가 50을 넘길 경우 `님들 도라이지` 출력
- `!규며듦점수(개발중)`
- `!규택토`
  - 자세한 사용법은 !규택토 도움

## How to run this bot on your machine
bot 폴더 아래에 secrets.py 를 생성하고 다음 필드를 채웁니다.
```Python
regulation_bot_key = 'string' # 디스코드 봇 API Key

opt_regulation_init_message_channel_id = int  # 규재 봇이 실행될때 부활 메시지 날릴 채팅방 id
opt_regulation_message_test_channel_id = int  # 규재 봇 테스트 채널 id, uncaught error 메시지를 추가 출력
opt_regulation_message_gtt_channel_id = int  # 규택토 채널 id, 규택토는 여기서만 가능
```

### Channel ID
봇을 실행하면 봇이 참여하고 있는 모든 디스코드 서버의 모든 채널의 채널 ID와 채널명을 콘솔에 출력합니다. 이를 참고하여 위의 필드를 채울 수 있습니다.

### Gyumoticons
해당 봇을 실행하기 위해서는 봇이 참여하고 있는 서버에 `:*regulation*:`(`regulation`이 포함) 이모티콘 2개 이상, `:transparent:` 이모티콘이 필요합니다.