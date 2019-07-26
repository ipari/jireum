# 지름 크롤러
여러 사이트의 알뜰구매 게시판의 글을 크롤링하여 Slack Webhook 으로 쏘아줍니다.

## 사용법
의존성 있는 패키지를 설치합니다.

```
$ pip install -r requirements.txt
```

`webhooks.json` 을 만들고, 그 안에 Webhook URL을 넣어줍니다.

```
["<url1>", "<url2>", ...]
```

실행합니다.

```
$ python run.py
```
