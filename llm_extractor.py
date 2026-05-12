import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化客户端，读取 .env 中的 DEEPSEEK 配置
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
)


def extract_citation(raw_text: str) -> dict:
    """
    调用大模型，将生肉文献字符串解析为结构化的 JSON 字典
    """
    model_name = os.getenv("MODEL_NAME", "deepseek-v4-pro")

    # 包含了所有 GB7714-2025 必须字段的 Prompt
    system_prompt = """
        你是一个专业的学术文献解析专家。请从用户输入的文献字符串中提取关键信息，并严格以纯 JSON 格式输出。
        请提取以下字段，如果某字段在原文中不存在或无法推断，请将其值设为 null：

        - "authors": 作者列表 (List[str])。英文姓名格式：“姓(全拼) + 空格 + 名(缩写)”，不加缩写点。例如 "Tuskan G A"。

        - "title": 题名/文章名 (str)。
          关键格式要求：
          1. 必须符合 Sentence Case 规范：整句仅首字母大写，其余部分除专有名词和缩写外一律小写。
          2. 保持专有缩写的大写状态，如 "IEEE", "WLAN", "RF", "5G", "AI", "DOI" 等。
          例如：将 "Time Division Coexistence of Wireless Communication" 
          转换为 "Time division coexistence of wireless communication"。

        - "doc_type": 文献标识符 ("J", "C", "M", "D", "R", "P", "EB/OL")
        - "venue": 期刊/会议名称 (str)。注意：期刊/会议名称通常保持每个实词首字母大写。
        - "year": 年份/发布日期 (str)
        - "volume": 卷号 (str)
        - "issue": 期号 (str)
        - "pages": 页码范围 (str)
        - "location": 出版地/国别 (str)
        - "publisher": 出版者/单位 (str)
        - "doi": DOI号 (str)
        - "url": 访问链接 (str)

        注意：只返回纯 JSON，不要包含任何额外说明。
        """

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_text}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,  # 保持低温度，确保提取的稳定性
            # --- 以下为 DeepSeek v4 pro 专属高级配置 ---
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}}
        )

        # 解析返回的 JSON 字符串为 Python 字典
        result_content = response.choices[0].message.content
        citation_data = json.loads(result_content)
        return citation_data

    except json.JSONDecodeError:
        print("JSON 解析失败，大模型返回的可能不是纯 JSON 格式。")
        return {}
    except Exception as e:
        print(f"LLM 提取失败: {e}")
        return {}