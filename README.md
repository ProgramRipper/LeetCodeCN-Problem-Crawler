# 爬取 LeetCode中国 题目

## 简介

爬取 LeetCode 题目描述，并存储为 markdown 或 txt 文件。支持指定状态、难度和语言的题目描述。（后续还会更新对爬取指定标签的题目的支持，以及题目点赞、通过人数等数据的爬取）

## 环境

基于 Python3 运行，依赖库：

> requests
> html2text
> argparse

可以通过执行以下指令来安装所需模块。
```shell
pip install -r requirement.txt
```

## 说明

```shell
python main.py [-h] [-d {1,2,3}] [-l {zh-CN,en}] [-s {ac,notac,null}] [-f {md,txt}] path
```
```
必选参数:
  path                  输出文件夹

可选参数:
  -h, --help            显示此帮助并退出
  -d {1,2,3}, --difficulty {1,2,3}
                        选择题目的难度, 否则所有难度的题目都会被爬取,
                        "1"为简单难度, "2"为中等难度 以及"3"为困难难度.
  -l {zh-CN,en}, --language {zh-CN,en}
                        选择题目描述的语言, 否则未被翻译的(英语)描述会被爬取.
  -s {ac,notac,null}, --status {ac,notac,null}
                        选择题目的状态, 否则所有状态的题目都会被爬取.
                        您需要先登录LeetCode中国账号后才可以读取题目状态.
                        "ac"为您已解决的题目.
                        "notac"为您曾经尝试过解决的题目.
                        "null"为您从未尝试过的题目.
  -f {md,txt}, --format {md,txt}
                        选择存储题目描述的文件格式, 否则.md格式的文件将会被生成.
```

参数说明

| Name | Full Name  | Type | Description                                  |
| ---- | ---------- | ---- | -------------------------------------------- |
| d    | difficulty | int  | 难度：1:简单，2:中等，3:困难                 |
| l    | language   | str  | 语言：zh-CN:简体中文，en:英文                |
| s    | status     | str  | 题目状态：ac:通过，notac:未通过，null:未尝试 |
| f    | format     | str  | 文件格式：md:Markdown文件，txt:Text文件      |

登录说明

- 配置[config.json](config.json)
```json
{
  "account": "填写你的LeetCode中国账号.",
  "password": "填写你的密码."
}
```