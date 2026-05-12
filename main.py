import os
import json
from llm_extractor import extract_citation
from formatter import format_citation


def main():
    # 定义输出文件的名称
    output_file = "formatted_citations.txt"

    print("=" * 60)
    print("学术文献格式化")
    print(f"提示：所有转换成功的文献将自动追加保存到：{output_file}")
    print("=" * 60)

    while True:
        print("\n" + "-" * 60)
        print("请输入原始文献信息 (支持多行粘贴)。")
        print("   -> 粘贴完成后，请【连按两次回车】开始转换。")
        print("   -> 输入 'q', 'quit' 或 'exit' 并按回车退出程序。")
        print("-" * 60)
        print("\n")

        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break

            # 检查是否输入了退出指令（仅在第一行输入有效）
            if len(lines) == 0 and line.strip().lower() in ['q', 'quit', 'exit']:
                print("\n感谢使用，转换记录已保存在本地，程序已退出！")
                return

            # 连续输入两个空行（即用户按了两次回车），结束输入
            if line.strip() == "" and len(lines) > 0:
                break

            lines.append(line)

        # 将多行输入合并为单行文本
        raw_input = " ".join(lines).strip()

        if not raw_input:
            print("未检测到内容，请重新输入。")
            continue

        # 交互：选择输出格式
        style = input("\n请选择目标格式 (直接回车默认 gb7714，输入 ieee 选 IEEE 格式): ").strip().lower()
        if not style:
            style = "gb7714"
        elif style not in ["gb7714", "ieee"]:
            print(f"警告：未知的格式 '{style}'，将回退使用默认的 gb7714 格式。")
            style = "gb7714"

        print(f"\n正在调用大模型解析并转换为 {style.upper()} 格式，请稍候...")

        # 1. 调用大模型提取
        parsed_data = extract_citation(raw_input)

        if parsed_data:
            # 2. 模板拼装
            formatted_citation = format_citation(parsed_data, style=style)

            print("\n[转换成功]:")
            print(formatted_citation)

            # 3. 写入文本文件 (使用 'a' 模式追加)
            try:
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(formatted_citation + "\n")
                print(f"[已保存] 成功追加到 {output_file}")
            except Exception as e:
                print(f"[保存失败] 无法写入文件: {e}")
        else:
            print("[转换失败] 大模型未能成功解析此文献，请检查原文内容或网络连接。")


if __name__ == "__main__":
    # 确保终端能正确显示中文
    import sys

    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    main()