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