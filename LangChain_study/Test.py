#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

os.environ["OPENAI_API_KEY"] = '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'
# 使用代理访问openai的接口，对于“v1/chat/completions”的api来说，需要在代理后面加一个v1才能构成一个完整的地址
os.environ["OPENAI_API_BASE"] = 'https://service-n5tgsaik-1254280433.usw.apigw.tencentcs.com/release/v1'

chat  = ChatOpenAI(model_name="gpt-3.5-turbo"
                   ,max_tokens=2048)

print(os.environ.get("OPENAI_API_BASE"))
messages = [
    SystemMessage(content="你现在是一个熟读唐诗宋词的诗人，当我说出作诗时,你要写七言绝句。当我说出作词时，你要写宋词，注意输出格式要符合规范。"),
    HumanMessage(content="作词，题目：春柳！")
]
result = chat(messages)
print(result)