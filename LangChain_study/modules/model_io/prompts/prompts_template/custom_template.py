#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# -------- 3、自定义提示模板（以您想要的任何方式格式化提示） ----------------
# 当前自定义模板的需求描述：给定函数名称和源代码，生成该函数的英语解释。
# 当前自定义模板，是一个文本自定义模板，而非聊天自定义模板
# 为什么需要：当模板的内容含有“一些逻辑代码/特殊指令执行后的结果”时
#    为什么不将这部分内容作为模板的参数呢，为了形成一个友好通用的模板所以将通用的东西都放到一起，即模板里。
################################################################################


# ------------------{{1、创建一个函数用于作为参数来演示案例}} -----------
import inspect

def get_source_code(function_name):
    # 获取给定函数名的源代码
    return inspect.getsource(function_name)

# ------------------{{2、将创建一个自定义提示模板，它将函数名称作为输入，并格式化提示模板以提供函数的源代码。}} -----------
from langchain.prompts import StringPromptTemplate
from pydantic import BaseModel, validator


class FunctionExplainerPromptTemplate(StringPromptTemplate, BaseModel):
    """自定义提示模板，将函数名称作为输入，并格式化提示模板以提供函数的源代码。"""

    @validator("input_variables")
    def validate_input_variables(cls, v):
        """验证输入变量是否正确。"""
        if len(v) != 1 or "function_name" not in v:
            raise ValueError("function_name must be the only input_variable.")
        return v

    def format(self, **kwargs) -> str:
        # 获取函数的源码
        source_code = get_source_code(kwargs["function_name"])

        # 生成要发送到语言模型的提示
        prompt = f"""
        Given the function name and source code, generate an English language explanation of the function.
        Function Name: {kwargs["function_name"].__name__}
        Source Code:
        {source_code}
        Explanation:
        """
        return prompt

    def _prompt_type(self):
        return "function-explainer"


# ------------------{{3、使用自定义提示}} -----------

fn_explainer = FunctionExplainerPromptTemplate(input_variables=["function_name"])

# 生成函数“get_source_code”的提示
prompt = fn_explainer.format(function_name=get_source_code)
print(prompt)