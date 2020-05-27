'''
递归下降法 分析
'''
from extract_word import parseString
class Tokens():
    '''
    这是一个对词法分析器的结果进行处理的类
    '''
    def __init__(self, tokens):
        '''
        :param tokens:  词法分析器的结果 List（Tuple（word, type, row, col)
        '''
        self.tokens = tokens
        self.idx = 0    # 当前指针
        self.len = len(tokens)
    def get_nextToken(self):
        '''
        获取当前指针的token值，并让指针往后移动
        :return: token
        '''
        if self.idx < self.len:
            token = self.tokens[self.idx]
            self.idx += 1
            return token
        else:
            self.idx += 1
            return None
    def get(self, idx):
        return self.tokens[idx]

    def isFull(self):
        return self.len <= self.idx



class Anlyse():
    '''
    分析类
    '''

    def __init__(self, token):
        self.tk = Tokens(token)
        self.res = True
        self.log = []
        self.const_sheet = []
    
    
    def insert_to_const(self, name, attribute = None, value = None):
        for sig in self.const_sheet:
            if name in sig.values():
                sig[attribute] = value
                return
        # name 还没有添加
        dic = {'name': name, attribute: value}
        self.const_sheet.append(dic)
        

    def D2(self):
        '''
        处理常量声明
        :return:
        '''
        if self.tk.isFull():
            self.res = False
            return
        token = self.tk.get_nextToken()
        if token[0] == 'const':
            pass
        else:
            self.tk.idx -=1
        self.T()
        self.CL()

    def T(self):
        '''
        处理 变量类型
        :return:
        '''
        if self.tk.isFull():
            self.res = False
            return
        token = self.tk.get_nextToken()
        if token[0] in ['int', 'float', 'char']:
            return
        else:
            self.res = False
            info = 'Row: '+str(token[2]) +' Col: '+str(token[3]) + ':::  '+str(token[0])+'不是类型！'
            self.log.append(info)

    def I(self):
        if self.tk.isFull():
            self.res = False
            return
        token = self.tk.get_nextToken()
        if token[1] == 'IDT':
            return
        else:
            self.res = False
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是标识符！'
            self.log.append(info)
            # print(str(token[0]) + '不是标识符！')

    # def FP4(self):

    def CL(self):
        if self.tk.isFull():
            self.res = False
            info = '末尾缺少元素！'
            self.log.append(info)
            return
        self.I()
        token = self.tk.get_nextToken()
        if token and token[0] == '=':
            self.C()
            self.X5()
        # elif token[0] in [',', ';']:
        #     self.tk.idx -= 2
        #     self.FP4()
        else:
            # self.res = False
            # if token:
            #     print(str(token[0]) + '不是 = ！')
            self.C()
            self.X5()

    def C(self):
        if self.tk.isFull():
            self.res = False
            print('末尾缺少元素')
            return
        token = self.tk.get_nextToken()
        if token[1] == 'CONST':
            return
        else:
            self.tk.idx -= 1
            self.res = False
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是 常量'
            self.log.append(info)
            # print(str(token[0]) + '不是 常量')
    def X5(self):
        if self.tk.isFull():
            self.res = False
            print('末尾缺少元素')
            return
        token = self.tk.get_nextToken()
        if token[0] == ';':
            return
        elif token[0] == ',':
            self.CL()
        else:
            self.res = False
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是 ; 或 ,'
            self.log.append(info)
            return

    def D1(self):
        '''
        处理函数声明
        :return:
        '''
        if self.tk.isFull():
            self.res = False
            print('末尾缺少元素')
            return
        self.T1()
        self.I()
        token = self.tk.get_nextToken()
        if token[0] == '(':
            self.FP()
            token = self.tk.get_nextToken()
            if token[0] == ')':
                token = self.tk.get_nextToken()
                if token and token[0] == ';':
                    return
                else:
                    self.res = False
                    if token:
                        info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '后面缺少 ；'
                        self.log.append(info)
                        # print(str(token[0] +' 不是 ;'))
            else:
                self.res = False
                info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '后面缺少 ）'
                self.log.append(info)
                # print(str(token[0] + ' 不是 )'))
        else:
            self.res = False
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '后面缺少 ('
            self.log.append(info)
            # print(str(token[0] + ' 不是 ('))

    def FD(self):
        '''
        函数定义
        :return:
        '''
        self.T1()
        self.I()
        token = self.tk.get_nextToken()
        if token[0] == '(':
            self.FDT()
            token = self.tk.get_nextToken()
            if token[0] == ')':
                self.S5()
            else:
                self.res = False
                info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '后面缺少 )'
                self.log.append(info)
                # print(str(token[0] +' 后面缺少）'))
        else:
            self.res = False
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '后面缺少 ('
            self.log.append(info)
            # print(' 未发现 (')

    def FDT(self):
        token = self.tk.get_nextToken()
        if token[0] in ['int', 'float', 'char']:
            self.I()
            self.X15()
        else:
            self.tk.idx -= 1

    def X15(self):
        token = self.tk.get_nextToken()
        if token[0] == ',':
            self.FDT()
        else:
            self.tk.idx -= 1

    def T1(self):
        '''
        处理 函数类型
        :return:
        '''
        if self.tk.isFull():
            self.res = False
            return
        token = self.tk.get_nextToken()
        if token[0] in ['int', 'float', 'char', 'void']:
            return
        else:
            self.res = False
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是类型！'
            self.log.append(info)
            # print(str(token[0]) + '不是类型！')

    def FP(self):
        if self.tk.isFull():
            self.res = False
            print('末尾缺少元素')
            return
        idx = self.tk.idx
        self.FP1()
        if not self.fp1:
            self.tk.idx = idx

    def FP1(self):
        '''
        函数声明参数列表
        :return:
        '''
        if self.tk.isFull():
            self.res = False
            print('末尾缺少元素')
            return
        token = self.tk.get_nextToken()
        if token[0] in ['int', 'float', 'char']:
            self.fp1 = True
            self.X8()
        else:
            self.fp1 = False

    def X8(self):

        token = self.tk.get_nextToken()
        if token and token[0] == ',':
            self.FP1()
        else:
            self.tk.idx -= 1

    def X9(self):
        token = self.tk.get_nextToken()
        if token and (token[1] in ['IDT', 'KEYWORD'] or token[0] == '{'):
            self.tk.idx -= 1
            self.SL()
        else:
            self.tk.idx -= 1



    def E1(self):
        '''
        表达式， 包含算术表达式、布尔表达式
        :return:
        '''
        token = self.tk.get_nextToken()
        if token and token[1] == 'IDT':
            token = self.tk.get_nextToken()
            if token[0] == '=':
                # 赋值表达式
                self.E()
            else:
                self.tk.idx -= 2
                self.E()
        elif token and token[1] == 'CONST':
            self.tk.idx -= 1
            self.E()
        elif token and token[0] == '(':
            self.tk.idx -= 1
            self.E()
        else:
            self.tk.idx -= 1
            # self.res = False
            # print('匹配表达式失败')

    def X12(self):

        token = self.tk.get_nextToken()
        if token[0] == ';':
            return
        else:
            self.tk.idx -= 1
            self.E1()
            token = self.tk.get_nextToken()
            if token and token[0] ==';':
                return
            else:
                self.res = False
                if token:
                    info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) +' 后面缺少 ;'
                    self.log.append(info)
                    # print(str(token[0]) +' 后面缺少 ;')
    def S(self):
        '''
        语句
        :return:
        '''
        token = self.tk.get_nextToken()
        if token[0] in ['int', 'void', 'float', 'const', 'char']:
            self.tk.idx -= 1
            self.S1()
        elif token[0] == 'if':
            self.tk.idx -= 1
            # 调用 if语句函数
            self.S8()
        elif token[0] == 'for':
            self.tk.idx -= 1
            # 调用 for语句函数
            self.S9()
        elif token[0] == 'while':
            self.tk.idx -= 1
            # 调用 while语句函数
            self.S10()
        elif token[0] == 'do':
            self.tk.idx -= 1
            # 调用 do while语句函数
            self.S11()
        elif token[0] == '{':
            self.tk.idx -= 1
            self.S5()
        elif token[0] == 'return':
            # print('sss')
            self.X12()
        elif token[0] in ['break', 'continue']:
            token = self.tk.get_nextToken()
            if token and token[0] == ';':
                return
            else:
                self.res = False
                t = self.tk.get(self.tk.idx  -2)
                info = 'Row: ' + str(t[2]) + ' Col: ' + str(t[3]) + ':::  ' + str(t[0]) +' 后面缺少 ;'
                self.log.append(info)
                # print(str(token[0]) +' 后面缺少 ;')
        elif token[1] == 'IDT' or token[0] == '(':
            self.tk.idx -= 1
            self.E1()
            token = self.tk.get_nextToken()
            if token and token[0] == ';':
                return
            else:
                # self.tk.idx -= 1
                self.S()
                self.res = False
                t = self.tk.get(self.tk.idx - 2)
                info = 'Row: ' + str(t[2]) + ' Col: ' + str(t[3]) + ':::  ' + str(t[0]) + ' 后面缺少 ;'
                self.log.append(info)
                # print(str(self.tk.get(self.tk.idx - 2)[0]) + ' 后面缺少 ;')

        else:
            self.res = False
            self.sfg = False
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + '未匹配： '+ str(token[0])
            self.log.append(info)
            # self.S()

    def S1(self):
        '''
        函数声明语句、 常量、变量定义
        :return:
        '''
        token = self.tk.get_nextToken()
        if token and token[0] == 'const':
            self.tk.idx -= 1
            self.D2()
        elif token and token[0] == 'void':
            self.tk.idx -= 1
            self.D1()
        elif token and token[0] in ['int', 'char', 'float']:
            if self.tk.get(self.tk.idx + 1)[0] == '(':
                self.tk.idx -= 1
                self.D1()
            else:
                self.tk.idx -= 1
                self.D2()
        else:
            self.res = False
            # self.tk.idx -= 1
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + '匹配函数声明语句，常/变量声明语句出错'
            self.log.append(info)
            # print('匹配函数声明语句，常/变量声明语句出错')

    def S5(self):
        '''
        复合语句
        :return:
        '''

        token = self.tk.get_nextToken()
        if token[0] == '{':
            self.SL()
            token = self.tk.get_nextToken()
            # print('S5 ;', str(token))
            if token and token[0] == '}':
                return
            else:
                self.res = False
                if token:
                    info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '后面缺少 }'
                    self.log.append(info)
                    # print(str(token[0]) + '后面缺少 } ')
        elif token[1] in ['CONST', 'KEYWORD', 'IDT']:
            self.tk.idx -= 1
            self.SL()


    def SL(self):
        self.S()
        self.X9()

    def S8(self):
        '''
        if 语句
        :return:
        '''
        if self.tk.isFull():
            self.res = False
            print('末尾缺少元素')
            return
        token = self.tk.get_nextToken()
        if token[0] == 'if':
            token = self.tk.get_nextToken()
            if token[0] == '(':
                self.E()
                token = self.tk.get_nextToken()
                if token[0] == ')':
                    token = self.tk.get_nextToken()
                    if token[1] == 'IDT' or token[0] in ['{', 'int', 'float', 'char']:
                        self.tk.idx -= 1
                        self.S()
                    else:
                        self.res = False
                        info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '多余字符'
                        self.log.append(info)
                    token = self.tk.get_nextToken()
                    if token and token[0] == 'else':
                        # print('tttttttttt')
                        self.S()
                        # self.E1()
                    else:
                        self.tk.idx -= 1
                else:
                    self.res = False
                    info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是 )'
                    self.log.append(info)
                    # print(str(token[0]) + '不是 )')
            else:
                self.res = False
                info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是 ('
                self.log.append(info)
                # print(str(token[0]) + '不是 (')
        else:
            self.res = False
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是 if'
            self.log.append(info)

            # print(str(token[0]) + '不是 if')

    def S9(self):
        '''
        for 语句
        :return:
        '''
        token = self.tk.get_nextToken()
        if token and token[0] == 'for':
            token = self.tk.get_nextToken()
            if token and token[0] == '(':
                self.E1()
                token = self.tk.get_nextToken()
                if token and token[0] == ';':
                    self.E1()
                    token = self.tk.get_nextToken()
                    if token and token[0] == ';':
                        self.E1()
                        token = self.tk.get_nextToken()
                        if token and token[0] == ')':
                            # print(self.tk.get(self.tk.idx)[0] +' ppp')
                            if self.tk.get(self.tk.idx)[0] == '{':

                                self.S5()
                            else:
                                self.S()

                        else:
                            self.res = False
                            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是 ）'
                            self.log.append(info)
                            # print(str(token[0]) + '不是 ）')
                    else:
                        self.res = False
                        info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是 ;'
                        self.log.append(info)
                        # print(str(token[0]) + '不是 ;')
                else:
                    self.res = False
                    info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是 ;'
                    self.log.append(info)
                    # print(str(token[0]) + '不是 ;')
            else:
                self.res = False
                info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是 （'
                self.log.append(info)
                # print(str(token[0]) + '不是 （')
        else:
            self.res = False
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + '未发现 for '
            self.log.append(info)
            # print('未发现 for ')

    def S10(self):
        token = self.tk.get_nextToken()
        if token[0] == 'while':
            token = self.tk.get_nextToken()
            if token and token[0] == '(':
                self.E1()
                token = self.tk.get_nextToken()
                if token and token[0] == ')':
                    # print(self.tk.get(self.tk.idx))
                    if self.tk.get(self.tk.idx) == '{':
                        # print('yyyy')
                        self.S5()
                    else:
                        self.S()
                else:
                    self.res = False
                    t = self.tk.get(self.tk.idx - 2)
                    info = 'Row: ' + str(t[2]) + ' Col: ' + str(t[3]) + ':::  ' + str(t[0]) + '后缺少 ） '
                    self.log.append(info)
                    # print(str(self.tk.get(self.tk.idx - 2)) + '后缺少 ） ')
            else:
                self.res = False
                info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(
                    token[0]) + '未发现 （ '
                self.log.append(info)
                # print('未发现 （ ')
        pass

    def S11(self):
        token = self.tk.get_nextToken()
        if token[0] == 'do':
            self.SL()
            # token = self.tk.get_nextToken()
            # if token and token[0] == 'while':
            #     token = self.tk.get_nextToken()
            #     if token and token[0] == '(':
            #         self.E1()
            #         token = self.tk.get_nextToken()
            #         if token and token[0] == ')':
            #             token = self.tk.get_nextToken()
            #             if token and token[0] == ';':
            #                 return
            #             else:
            #                 self.res = False
            #                 print(str(self.tk.get(self.tk.idx - 2)) + '后缺少 ; ')
            #         else:
            #             self.res = False
            #             print(str(self.tk.get(self.tk.idx - 2)) + '后缺少 )')
            #     else:
            #         self.res = False
            #         print(str(self.tk.get(self.tk.idx - 2)) + '后缺少 ( ')
            # else:
            #     self.res = False
            #     # print(token[0])
            #     print('未发现 while ')
        pass



    def EE(self):
        self.E()
        if not self.tk.isFull():
            self.res = False
            print('尾部含多余缺少符号')

    def E(self):
        '''
        :return:
        '''
        if self.tk.isFull():
            self.res = False
            print('末尾缺少元素')
            return
        self.IT()
        self.X1()


    def X1(self):
        token = self.tk.get_nextToken()
        if token and token[0] in ['+', '-', '|', '&', '>', '<']:
            self.E()
        else:
            self.tk.idx -= 1

    def IT(self):
        if self.tk.isFull():
            self.res = False
            print('末尾缺少元素')
            return
        self.F()
        self.X2()

    def X2(self):
        token = self.tk.get_nextToken()
        if token and token[0] in ['*', '/', '%', '||', '&&', '==', '!=']:
            self.IT()
        else:
            self.tk.idx -= 1

    def F(self):
        if self.tk.isFull():
            self.res = False
            print('末尾缺少元素')
            return
        token = self.tk.get_nextToken()
        if token[0] == '(':
            self.E()
            token = self.tk.get_nextToken()
            if token and token[0] == ')':
                return
            else:
                self.res = False
                if token:
                    info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  '  + str(token[0]) +'不是 )'
                    self.log.append(info)
                    # print(str(token[0]) +'不是 )')
                else:
                    info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  '  + str(token[0]) + '缺少 ）'
                    self.log.append(info)
                    # print('缺少 ）')
        elif token[1] == 'IDT':

            if not self.tk.isFull() and self.tk.get(self.tk.idx)[0] == '(':
                # 进入函数调用语句
                self.FC()
            else:
                self.tk.idx -= 1
                self.I()
        elif token[1] == 'CONST':
            return
        else:
            self.res = False
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '匹配出错 '
            self.log.append(info)
            # print(str(token[0]) + '匹配出错 ')

    def FC(self):
        token = self.tk.get_nextToken()
        if token[0] == '(':
            self.FP2()
            token = self.tk.get_nextToken()
            if token and token[0] == ')':
                return
            else:
                self.res = False
                if token:
                    info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0]) + '不是 )'
                    self.log.append(info)
                    # print(str(token[0]) + '不是 )')
        else:
            self.res = False
            info = 'Row: ' + str(token[2]) + ' Col: ' + str(token[3]) + ':::  ' + str(token[0])  + '不是 ('
            self.log.append(info)
            # print(str(token[0]) + '不是 (')

    def FP2(self):
        self.E()
        idx = self.tk.idx
        self.X3()
        if not self.fp3:
            self.fp3 = True
            self.tk.idx = idx


    def FP3(self):
        self.E()
        idx = self.tk.idx
        self.X3()
        if not self.fp3:
            self.fp3 = True
            self.tk.idx = idx

    def X3(self):
        token = self.tk.get_nextToken()
        if token and token[0] == ',':
            self.fp3 = True
            self.FP3()
        else:
            self.fp3 = False


    def anlyseP(self):
        '''
        总控程序
        :return:
        '''

        while not self.tk.isFull():
            token = self.tk.get_nextToken()
            if token[0] == 'const':
                self.D2()
            elif token[0] == 'main':
                token = self.tk.get_nextToken()
                if token[0] == '(':
                    token = self.tk.get_nextToken()
                    if token[0] == ')':
                        print('hhhh')
                        print(len(self.log))
                        self.S5()
                        print(len(self.log))
                        while not self.tk.isFull():
                            token = self.tk.get_nextToken()
                            if token[0] in ['int', 'void', 'float', 'char']:
                                self.tk.idx -= 1
                                self.FD()

            elif token[0] in ['int', 'float', 'char', 'void']:
                token = self.tk.get_nextToken()
                if token[1] == 'IDT':
                    token = self.tk.get_nextToken()
                    if token[0] in ['=', ',']:
                        self.tk.idx -= 3
                        self.D2()
                    elif token[0] =='(':
                        self.tk.idx -= 3
                        self.D1()





s = '''
//语法分析测试代码
r = b-(c*3) + c*3;
if(d<(c+1)&(c+1)>b)
{
    e = b;
}
else
{
    e = d;
}
d = sum(b,d);
for(i=2;i<n;i=i+1)
{
    while (jj<i)
   {
     if(i%j==0)
     {break;}
    }
}

'''
tokens, errors = parseString(s)

print(len(tokens))
print(len(errors))
print(tokens)
an  = Anlyse(tokens)
an.S5()
print(an.res, an.tk.idx, an.tk.len)

print(an.log)
with open ('log.txt', 'w') as f:
    for l in an.log:
        print(l)
        f.write(l + '\n')