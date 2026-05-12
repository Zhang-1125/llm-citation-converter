import os
import re
from jinja2 import Environment, FileSystemLoader


def regex_search(val, pattern):
    """自定义 Jinja2 过滤器：用于正则匹配"""
    if not val:
        return False
    return bool(re.search(pattern, str(val)))


def format_citation(citation_data: dict, style: str) -> str:
    """
    根据给定的样式（模板文件名），将结构化数据拼装成标准格式的字符串
    """
    if not citation_data:
        return "错误：没有可格式化的数据。"

    # 设置 Jinja2 模板目录为当前文件同级的 templates 文件夹
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))

    # 自定义的正则提取函数注册为 Jinja2 的过滤器
    env.filters['regex_search'] = regex_search

    template_name = f"{style}.j2"

    try:
        template = env.get_template(template_name)
        # 渲染模板并去除首尾多余空格
        formatted_text = template.render(**citation_data).strip()
        return formatted_text
    except Exception as e:
        return f"模板渲染失败，请检查样式名称 '{style}' 是否正确存在。详细错误: {e}"