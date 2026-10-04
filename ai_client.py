import os

from dotenv import load_dotenv
from openai import OpenAI

from config import BASE_URL, MODEL_NAME


# 读取项目中的 .env 文件
load_dotenv()

# 从 .env 中获取 SiliconFlow API Key
api_key = os.getenv("SILICONFLOW_API_KEY")

if not api_key:
    raise ValueError(
        "没有找到 SILICONFLOW_API_KEY，请检查 .env 文件。"
    )


# 创建 SiliconFlow 客户端
client = OpenAI(
    api_key=api_key,
    base_url=BASE_URL
)


def ask_ai(prompt):
    """
    向大模型发送问题，并返回模型生成的回答。
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "你是一名专业、严谨、可靠的AI助手。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI调用失败：{e}"