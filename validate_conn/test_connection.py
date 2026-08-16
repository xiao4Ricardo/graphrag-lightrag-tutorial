import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1")
model_name = os.getenv("LLM_MODEL", "deepseek-ai/DeepSeek-V3")

def test_api_connection():
    print(f"测试 API 连接中... (Base URL: {base_url}, Model: {model_name})")
    client = OpenAI(api_key=api_key, base_url=base_url)
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": "你好，请确认 API 连接是否正确！"}
            ]
        )
        print("API 连接正常，收到响应:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"API 连接失败: {e}")

if __name__ == "__main__":
    test_api_connection()
