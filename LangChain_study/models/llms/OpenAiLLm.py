#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from langchain.llms import OpenAI
from LangChain_study.common import ChatParam

os.environ["OPENAI_API_KEY"] = ChatParam.OPENAI_API_KEY
os.environ["OPENAI_API_BASE"] = ChatParam.OPENAI_API_BASE

print(ChatParam.OPENAI_API_BASE)

llm = OpenAI(model_name="text-ada-001", n=2, best_of=2)

# 根据文本生成文本
# print( llm("Tell me a joke") )

# 获取更完整的响应
llm_result = llm.generate(["告诉我一个笑话", "告诉我一首短诗"]*2)
result_len = len(llm_result.generations)
result_first = llm_result.generations[0]
result_last =llm_result.generations[-1]
print(f'返回的文件长度：{result_len}')
print(f'第一个文本的返回内容：{result_first}')
print(f'最后一个文本的返回内容：{result_last}')
print(["告诉我一个笑话", "告诉我一首短诗"]*2)

llm_output_str = llm_result.llm_output
print(f'返回提供商特定信息：{llm_output_str}')
print('请注意，默认情况下，令牌是使用tiktoken估算的token')