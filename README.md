# Amazon Bedrock에서 OpenAI 모델 사용하기


여기에서는 AWS 환경에서 OpenAI 모델을 활용하는것을 설명합니다. OpenAI에서 제공하는 [BedrockOpenAI](https://developers.openai.com/api/docs/guides/amazon-bedrock#make-responses-api-requests)을 이용하여 OpenAI의 Responses API를 활용할 수 있습니다. 이를 통해 AWS의 다른 서비스처럼 인증, 결제, 보안을 이용할 수 있습니다.

## OpenAI 모델 활용하기

### Bedrock을 사용해야 하는 경우
- AWS 기반 인증, 과금이 필요할 때
- AWS 기반 ID, 접근 권한, 계정 관리가 필요할 때
- 특정 AWS 리전에 배포해야 하는 규정 준수 요건이 있을 때


### Hello World

필요한 패키지를 설치합니다.

```bash
pip install -U "openai>=2.40.0"
```


아래와 같이 Bedrock Key를 등록합니다.

```baseh
export AWS_BEARER_TOKEN_BEDROCK="YOUR_BEDROCK_API_KEY"
```

이후 [hello.py](./hello.py)를 실행합니다.

```python
from openai import BedrockOpenAI

client = BedrockOpenAI(aws_region="us-east-2")

response = client.responses.create(
    model="openai.gpt-5.5",
    input="AWS에서 OpenAI API를 사용하는 방법을 설명해주세요.",
)

print(response.output_text)
```

이때의 배포 모델은 `openai.gpt-5.5` (us-east-2 리전)이고, API URL은 `https://bedrock-mantle.us-east-2.api.aws/openai/v1`입니다.


### AWS Credential

`aws-bedrock-token-generator` 패키지를 설치하면 토큰 자동 갱신이 가능합니다.

```bash
pip install aws-bedrock-token-generator
```

이후 [basic.py](./basic.py)를 실행하면 AWS Credential을 이용해 인증하고 결과를 streaming으로 전달합니다.

```python
from openai import BedrockOpenAI
from aws_bedrock_token_generator import provide_token

AWS_REGION = "us-east-2"

client = BedrockOpenAI(
    aws_region=AWS_REGION,
    bedrock_token_provider=lambda: provide_token(region=AWS_REGION),
)

stream = client.responses.create(
    model="openai.gpt-5.5",
    input="Amazon S3에 파일을 업로드하는 방법을 설명해주세요.",
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)

print()
```

### 기능 지원 현황 (2026년 6월 1일 기준)

| 기능 | OpenAI API | Amazon Bedrock |
|---|---|---|
| 텍스트 생성 | ✅ | ✅ |
| 이미지 입력 | ✅ | ✅ |
| 파일 입력 | ✅ | ✅ (지원 파일 형식 한정) |
| 구조화된 출력 | ✅ | ✅ |
| 함수 호출 | ✅ | ✅ |
| 스트리밍 응답 | ✅ | ✅ |
| 추론(Reasoning) | ✅ | ✅ |
| 프롬프트 캐싱 | ✅ | ✅ |
| 커스텀 도구 | ✅ | ✅ |
| 오디오 입력 | ✅ | ❌ |
| WebSocket 연결 | ✅ | ❌ |
| 웹 검색 도구 | ✅ | ❌ |
| 파일 검색 도구 | ✅ | ❌ |
| Computer Use | ✅ | ❌ |
| Shell 도구 | ✅ | ❌ |
| 이미지 생성 도구 | ✅ | ❌ |
| Remote MCP 서버 | ✅ | ❌ |
| 서비스 티어 | ✅ | On-demand 전용 |


## 실행하기

아래와 같이 실행합니다. 

```bash
python basic.py
```

이때의 결과는 아래와 같습니다.

<img width="790" height="552" alt="image" src="https://github.com/user-attachments/assets/2bfba1db-e645-41cd-8cbc-1450542d3708" />




## Reference

[OpenAI models in Amazon Bedrock](https://developers.openai.com/api/docs/guides/amazon-bedrock)
