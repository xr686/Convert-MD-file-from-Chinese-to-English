import tkinter as tk
from tkinter import filedialog, messagebox
import re
from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_alimt20181012 import models as alimt_20181012_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

from alibabacloud_credentials.credentials import AccessKeyCredential

def create_client():
    # 使用 AccessKey 初始化凭证
    credential = AccessKeyCredential(
        "xxxxxxxx",   # 你的 AccessKey ID
        "xxxxxxxx"  # 你的 AccessKey Secret
    )
    config = open_api_models.Config(credential=credential)
    config.endpoint = "mt.cn-hangzhou.aliyuncs.com"  # 阿里云机器翻译服务地址
    return AlimtClient(config)


client = create_client()

def translate_text(text):
    if not text.strip():
        return text
    request = alimt_20181012_models.TranslateGeneralRequest(
        format_type='text',
        source_language='zh',
        target_language='en',
        source_text=text
    )
    runtime = util_models.RuntimeOptions()
    try:
        response = client.translate_general_with_options(request, runtime)
        return response.body.data.translated
    except Exception as e:
        print("翻译错误:", e)
        return text

# ------------------- Markdown 翻译处理 -------------------
def translate_markdown_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    translated_lines = []
    in_code_block = False

    code_block_pattern = re.compile(r'^```')
    for line in lines:
        if code_block_pattern.match(line.strip()):
            in_code_block = not in_code_block
            translated_lines.append(line)
            continue

        if in_code_block or line.strip().startswith('![') or line.strip().startswith('['):
            # 保留代码块和图片、链接不翻译
            translated_lines.append(line)
        else:
            # 翻译中文文本
            translated_line = translate_text(line)
            translated_lines.append(translated_line + '\n')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)

# ------------------- Tkinter 界面 -------------------
class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown 中文翻译器")
        self.root.geometry("400x200")

        self.input_file = ''
        self.output_file = ''

        tk.Button(root, text="导入文件", command=self.select_input_file).pack(pady=10)
        tk.Button(root, text="保存路径", command=self.select_output_file).pack(pady=10)
        tk.Button(root, text="开始翻译", command=self.start_translation).pack(pady=10)
        tk.Button(root, text="退出", command=root.quit).pack(pady=10)

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
        if self.input_file:
            messagebox.showinfo("提示", f"已选择文件: {self.input_file}")

    def select_output_file(self):
        self.output_file = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
        if self.output_file:
            messagebox.showinfo("提示", f"保存路径: {self.output_file}")

    def start_translation(self):
        if not self.input_file or not self.output_file:
            messagebox.showwarning("警告", "请先选择输入文件和保存路径")
            return
        translate_markdown_file(self.input_file, self.output_file)
        messagebox.showinfo("完成", "翻译完成！")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
