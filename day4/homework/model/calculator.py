#!/usr/bin/env python3
# coding:utf-8

import re
class calculator(object):

    def __init__(self):
        '''
        构造方法，用来初始化所有用到的正则表达式
        :return:
        '''
        self.__one_parentheses_ex = '\([^\(\)]+\)' # 匹配有一个括号的，用来提取括号内的子串
        #self.__no_parentheses = '^[^\(\)]+$'
        self.__check_no_parentheses_ex = '^[\+\-]{0,1}\d+[\.]{0,1}\d*([\+\-\*\/]{1}[\+\-]{0,1}\d+[\.]{0,1}\d*)+$' # 检查不加括号的表达式是否合法
        #self.__multiplication_division = '[\+\-]*\d+[.]{0,1}\d+[\*\/]{1}[\+\-]*\d+[.]*\d+' # 匹配乘除法表达式
        self.__multiplication_division_ex = '[\+\-]{0,1}\d+[\.]{0,1}\d*[\*\/]{1}[\+\-]*\d+[\.]{0,1}\d*' # 匹配乘除法表达式
        #self.__add_sub = '[\+\-]*\d+[.]*\d*[\+\-]{1}[\+\-]*\d+[.]*\d*' # 匹配加法
        self.__add_sub_ex = '[\+\-]{0,1}\d+[\.]*\d*[\+\-]+\d+[\.]*\d*' #匹配加减法表达式
        self.__is_num = '^[\+\-]{0,1}\d+[\.]{0,1}\d*$' # 匹配单个数字，用于括号内只有一个数字的情况下，例如(-1.0)
        self.__mult_sign = '[\+\-]{2,}' # 匹配多个连续正负号的情况，用于替换多个符号


    def __replace_sign(self, expression):
        '''
        替换多个连续+-符号的问题，例如+-----，遵循奇数个负号等于正否则为负的原则进行替换
        :param expression: 表达式，包括有括号的情况
        :return: 返回经过处理的表达式
        '''
        signs = re.findall(self.__mult_sign, expression) # 找出多个连续的正负号
        #print(signs)
        if signs: # 判断是否存在
            # 存在则逐一替换
            for sign in signs:
                if sign.count('-')%2 ==1:
                    expression = expression.replace(sign, '-', 1)
                else:
                    expression = expression.replace(sign, '+', 1)
        return expression

    def __multiplication_division(self, expression):
        '''
        逐一找出乘除法表达式，并计算出所有表达式的结果
        :param expression: 四则运算表达式
        :return: 返回不包含乘除法的四则运算表达式，也就是说只有加减法
        '''
        expression = self.__replace_sign(expression)
        res = re.search(self.__multiplication_division_ex, expression) # 查找最基本的乘除法表达式，只包含两个数和运算符号
        #result = ''
        #print(res)
        if res: # 是否包含乘除法
            # 包含
            res = res.group()
            #tmp_list = re.split()
            #num1,num2  = re.split('[\*\/]', res)
            num1, num2 = re.findall('[\+\-]{0,1}\d+[\.]{0,1}\d*', res) # 获得表达式的两个数
            #print(num1,num2)
            operate = re.search('[\*\/]', res).group() # 获得符号
            #print(re.split('[\*\/]', res))
            result = self.__base_arithmetic(num1, operate, num2) # 进行计算
            #print(result)
            #print(expression)
            #print(expression.replace(res, result))
            expression = expression.replace(res, result) # 将结果替换到表达式中
            return self.__multiplication_division(expression) # 进行递归，继续查找并计算基本乘除法表达式
        else:
            #print(result)
            # 如果不包含最基本表达式，说明乘除法计算版完毕，返回表达式，结束递归
            return expression

    def __add_subtraction(self, expression):
        '''
        将只包含加减法的表达式进行计算，并返回结果
        :param expression: 加减法运算表达式
        :return: 返回计算结果
        '''
        expression = self.__replace_sign(expression)
        #expression = expression.replace('++','+').replace('+-','-').replace('--',"+").replace('-+','-')
        res = re.search(self.__add_sub_ex, expression)

        #result = ''
        #print(res)
        if res:
            #res = res.group().replace('++','+').replace('+-','-').replace('--',"+").replace('-+','-')
            res = res.group()
            #tmp_list = re.split()
            #num1,num2  = re.split('[\+\-]', res)
            #print(re.split('[\+\-]', res))
            #num1, num2 = re.split('[\+\-]', res)[1:]
            #num1, num2 = re.search('[\+\-]\d+[.]*\d*', res).group()
            #print(re.findall('[\+\-]*\d+[.]*\d*', res))
            num1, num2 = re.findall('[\+\-]{0,1}\d+[\.]{0,1}\d*', res)
            operate = '+'
            # 说明这里的为什么符号都用加号，因为所谓的减法其实就是加法，例如2-1等于2+(-1)

            #print(re.split('[\*\/]', res))
            result = self.__base_arithmetic(num1, operate, num2) # 计算最基本的加减法表达式的值
            #print(result)
            #print(expression)
            #print(expression.replace(res, result))
            expression = expression.replace(res, result)
            return self.__add_subtraction(expression) # 进行递归，继续查找并计算基本加减法表达式
        else:
            #print(result)
            #
            # 如果查找不到最基本的加减法表达式，说明只剩下结果，返回结果
            return expression


    def __four_arithmetic_operation(self, expression):
        '''
        进行没有括号的四则运算，按照先乘除后加减的原则进行计算
        :param expression: 四则运算表达式
        :return: 运算结果
        '''
        expression = self.__replace_sign(expression) # 先计算乘除法
        #expression = expression.replace('++','+').replace('+-','-').replace('--',"+").replace('-+','-')
        expression = self.__multiplication_division(expression) # 先计算乘除法
        #print(expression)
        return self.__add_subtraction(expression) # 后计算加减法

    def __base_arithmetic(self, num1, operate, num2):
        '''
        基础运算方法，计算两个数的加减乘除结果
        :param num1: 第一个数
        :param operate: 计算符号
        :param num2: 第二个数
        :return: 计算结果
        '''

        try:
            num1 = float(num1)
            num2 = float(num2)
        except Exception:
            #print('fff')
            return None
        if operate == '+':
            result = num1 + num2
        elif operate == '-':
            result = num1 - num2
        elif operate == '*':
            result = num1 * num2
        elif operate == '/':
            result = num1 / num2
        else:
            return None
        if result >= 0:
            # 如果最后的值大于0返回的值前面加一正好，避免 1-2*-3，-2*3被乘法表达时候-2*-3 = 6 最后替换回去后出现 1-2*-3 = 16的情况
            return '%s%s' %('+', result)
        else:
            return str(result)


    def __parentheses(self, expression):
        '''
        逐一将括号内的表达式取出来，如果取出来的四则运算表达式合法，进行四则运算，如果不合法返回False
        :param expression: 带括号的四则运算表达式
        :return: 不带括号的四则运算表达式或者false
        '''
        # flag = True
        res = re.search(self.__one_parentheses_ex, expression)
        while res:
            #res = re.search(self.__one_parentheses_ex, expression) # 搜索括号的表达式
            res = res.group()
            res_tmp = res.replace('(','').replace(')', '')
            #print(expression)
            # if re.match(self.__check_no_parentheses_ex, res_tmp):
            #     print(res_tmp)
            # else:
            #     print(res_tmp, '不合法')
            #     return None

            if re.match(self.__is_num, res_tmp): # 判断括号是否只是一个数

                result = res_tmp # 是的话结果就是那个数
                #print(result)
            else:
                # 否则进行四则运算表达式
                if not self.__check_expression(res_tmp): # 判断四则运算表达式是否合法
                    return False
                result = self.__four_arithmetic_operation(res_tmp) # 继续你四则运算
            expression = expression.replace(res, result) # 替换结果
            # if not re.search(self.__one_parentheses_ex, expression): # 判断是否还包含带括号的表达式
            #     # 包含的话输出去掉括号后的结果
            #     flag = False # 不包含退出循环
            res = re.search(self.__one_parentheses_ex, expression)
        return  expression # 返回不带括号的表达式

    # def __parentheses(self, expression):
    #     '''
    #     带括号的四则运算
    #     :param expression: 带括号的四则运算表达式
    #     :return: 返回不包含括号的四则运算表达式
    #     '''
    #     res = re.search(self.__one_parentheses_ex, expression)
    #     if res:
    #         res = res.group()
    #         #print(expression)
    #         res_tmp = res.replace('(','').replace(')', '')
    #         result = self.__four_arithmetic_operation(res_tmp)
    #         # print(res)
    #         # print(eval(res))
    #         # print(result)
    #         # print(expression)
    #         expression = expression.replace(res, result)
    #         print(expression)
    #         return self.__parentheses(expression)
    #     else:
    #         return expression

    def __check_expression(self, expression):
        '''
        判断不带括号的四则运算表达式是否合法
        :param expression: 不带括号的四则运算表达式
        :return: 合法返回True，不合法返回False
        '''
        if re.match(self.__check_no_parentheses_ex, expression):
            return True
        else:
            #print(expression)
            return False

        #'^[\+\-]{0,1}\d+[.]{0,1}\d*([\+\-\*\/]{1}[\+\-]{0,1}\d+[.]{0,1}\d*)+$'

    def getResult(self, expression):
        '''
        计算带括号的四则运算的值
        :param expression: 带括号的四则运算表达式
        :return: 最终的结果
        '''
        #print(expression)
        expression = self.__replace_sign(expression)
        #print(expression)
        expression = self.__parentheses(expression)
        expression = self.__replace_sign(expression)
        if not expression:
            return False
        else:
            # expression = self.__replace_sign(expression)
            if self.__check_expression(expression):
                return self.__four_arithmetic_operation(expression)
            else:
                return False