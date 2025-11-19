# Convert-MD-file-from-Chinese-to-English
这个项目可以将你写的中文内容的.md格式的文件自动转译为英文的.md文件，自动调用阿里云翻译的API进行翻译操作。This project can automatically convert the .md format files of your written Chinese content into English .md files, and automatically invoke the API of Alibaba Cloud Translation for the translation process.




需要先在“阿里云”平台购买翻译包：https://www.aliyun.com/product/ai/alimt?spm=5176.19720258.J_8058803260.278.e9392c4a5eczxp

我买的是“文本&文档翻译”中的“语种识别”，买了100万字符，一年的，一天转3000字也能用一年

然后在顶部搜索“创建AccessKey”，跟着官方教程操作

请记下你自己的AccessKey lD和AccessKey Secret

然后代码中的14、15行分别填入你的AccessKey lD和AccessKey Secret：

    credential = AccessKeyCredential(
        "xxxxxxxx",   # 你的 AccessKey ID
        "xxxxxxxx"  # 你的 AccessKey Secret
    )

此时即可直接运行，若你想打包为.exe方便使用，请执行
pyinstaller --onefile --windowed translator.py
