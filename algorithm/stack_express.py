#! /usr/bin/python
# -*- coding:utf-8 -*-

# 学习地址：https://facert.gitbooks.io/python-data-structure-cn/3.%E5%9F%BA%E6%9C%AC%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/3.9.%E4%B8%AD%E7%BC%80%E5%89%8D%E7%BC%80%E5%92%8C%E5%90%8E%E7%BC%80%E8%A1%A8%E8%BE%BE%E5%BC%8F/
# 1、创建一个名为 opstack 的空栈以保存运算符。给输出创建一个空列表。
# 2、通过使用字符串方法拆分将输入的中缀字符串转换为标记列表。
# 3、从左到右扫描标记列表。
#    a、如果标记是操作数，将其附加到输出列表的末尾。
#    b、如果标记是左括号，将其压到 opstack 上。
#    c、如果标记是右括号，则弹出 opstack，直到删除相应的左括号。将每个运算符附加到输出列表的末尾。
# 4、如果标记是运算符，*，/，+或 - ，将其压入 opstack。但是，首先删除已经在 opstack 中具有更高或相等优先级的任何运算符，并将它们加到输出列表中。
# 5、当输入表达式被完全处理时，检查 opstack。仍然在栈上的任何运算符都可以删除并加到输出列表的末尾。

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


def postfix_eval(postfixexpr):
    oper_stack = Stack()
    token_list = postfixexpr.split()

    for token in token_list:
        if token in "0123456789":
            oper_stack.push(int(token))
        else:
            operand2 = oper_stack.pop()
            operand1 = oper_stack.pop()
            result = do_math(token, operand1, operand2)
            oper_stack.push(result)
    return oper_stack.pop()


def do_math(op, op1, op2):
    if op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    else:
        return op1 - op2


print(infix2postfix("A * B + C * D"))
print(infix2postfix("( A + B ) * C - ( D - E ) * ( F + G )"))
print(postfix_eval('7 8 + 3 2 + /'))
