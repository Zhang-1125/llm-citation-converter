**特别声明：本项目为AIGC。生成的文献引用结果亦属于AIGC。尽管系统内嵌了本地模板进行后置排版校验，大语言模型仍可能在提取字段时产生幻觉或解析误差。请务必在正式使用前对输出结果进行人工审慎核对。**

---

# 学术文献格式化工具

本项目结合了大语言模型（LLM）的非结构化文本解析能力与 Jinja2 本地模板引擎的精确排版能力，用于将任意格式的原始文献字符串自动转换为标准学术引用格式（如 GB/T 7714-2025、IEEE）。

## 项目构成

* `main.py`：主程序入口，提供交互式命令行界面，支持多行文本连续输入，并将转换结果自动追加保存到本地文件。
* `llm_extractor.py`：大模型交互模块。负责通过 OpenAI SDK 兼容接口（默认指向 DeepSeek-v4-pro）将杂乱的文本提取并格式化为标准 JSON 数据结构。
* `formatter.py`：本地组装模块。利用 Jinja2 模板引擎和自定义正则过滤器，将结构化数据安全、严格地拼装成最终的目标格式。
* `templates/`：本地样式模板库。包含 `gb7714.j2`（国标格式）和 `ieee.j2`（IEEE格式）等模板文件。
* `.env.example`：环境变量模板文件，说明项目运行所需的配置项。
* `requirements.txt`：项目运行所需的 Python 依赖库清单。

## 安装与配置

1. **环境要求**：确保本地已安装 Python 3.8+ 环境。
2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
3. **配置环境变量**：将根目录下的 .env.example 复制并重命名为 .env。打开 .env 文件，填入您的 API 信息：
   ```bash
   OPENAI_API_KEY=在此填入您的_DEEPSEEK_API_KEY
   OPENAI_BASE_UR=在此填入您的大模型API链接[https://api.deepseek.com]
   MODEL_NAME=在此填入您的大模型型号deepseek-v4-pro
   
## 使用方法
0. **直接运行**：
   ```bash
   python main.py
