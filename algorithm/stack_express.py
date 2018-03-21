#! /usr/bin/python
# -*- coding:utf-8 -*-

# 学习地址：https://facert.gitbooks.io/python-data-structure-cn/3.%E5%9F%BA%E6%9C%AC%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/3.9.%E4%B8%AD%E7%BC%80%E5%89%8D%E7%BC%80%E5%92%8C%E5%90%8E%E7%BC%80%E8%A1%A8%E8%BE%BE%E5%BC%8F/

from pythonds.basic.stack import Stack


def infix2postfix(infixexpr):
    """
    栈的使用：算术表达式中缀表达式转后缀表达式
    :param infixexpr: 完全括号算术表达式
    :return: 后缀表达式
    """
    prec = dict()
    prec['*'] = 3
    prec['/'] = 3
    prec['+'] = 2
    prec['-'] = 2
    prec['('] = 1
    op_stack = Stack()
    postfix_list = []
    token_list = infixexpr.split()

    for token in token_list:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfix_list.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            top_token = op_stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = op_stack.pop()
        else:
            while (not op_stack.isEmpty()) and (prec[op_stack.peek()] >= prec[token]):
                  postfix_list.append(op_stack.pop())
            op_stack.push(token)
    while not op_stack.isEmpty():
        postfix_list.append(op_stack.pop())
    return " ".join(postfix_list)


print(infix2postfix("A * B + C * D"))
print(infix2postfix("( A + B ) * C - ( D - E ) * ( F + G )"))
