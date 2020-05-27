'''
预测分析表语法分析
作者: yan
创建时间： 2020/4/11
最近修改时间： 2020/5/11
'''

import copy
import sys
from utils import getFirst, getFirstSet, getFollow, getFollowSet
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

def get_NVT(grammar):
    '''
    获取 文法中的全部非终结符
    :param grammar:
    :return:
    '''

    res = []
    for l, r in grammar:
        if l not in res:
            res.append(l)

    return res

def deduce(grammar: list, N):
    '''
    判断某非终结符能否推出空
    :param grammar:  语法
    :param N: 非终结符
    :return:  Bool
    '''

    if N not in [g[0] for g in grammar]:
        return False
    if ['none'] not in [g[1] for g in grammar]:
        return False
    Ncan = [N]
    for g in grammar:
        if g[0] in Ncan:
            if g[1] == ['none']:
                return True
            elif ''.join([c[0] for c in g[1]]).isupper():
                ls = []
                for c in g[1]:
                    if c not in ls:
                        ls.append(c)
                Ncan.append(ls)
    endcan = [g[0] for g in grammar if g[1] == ['none']]

    for n in Ncan:
        if len(n) == 1 and n in endcan:
            return True
        else:
            fg = True
            for c in n:
                if c not in endcan:
                    fg = False
            if fg:
                return True

    return False

def deduce_muti(grammar: list, S):
    '''
    判断多个非终结符是否能推出空
    :param grammar:
    :param S:
    :return:
    '''

    for i in range(len(S)-1, -1, -1):
        if not deduce(grammar, S[i]):
            return i
    return 0


def isequal(A, B):
    '''
    判断两字典内容是否一样
    :param A:
    :param B:
    :return:
    '''
    if A.keys() != B.keys():
        return False
    else:
        for key in A.keys():
            if sorted(A[key]) != sorted(B[key]):
                return False
        return True

def clear(A: list):
    '''
    :param A:  [[]]
    :return:
    '''
    res = []
    for a in A:
        if a not in res:
            res.append(a)
    return res
def append(A, B):
    '''

    :param A:  []
    :param B: [[]]
    :return:
    '''
    fg = False
    for b in B:
        if b not in A:
            A.append(b)
        else: #  B,A 有交集
            fg = True
    return fg

def isLL1(grammar):
    '''
    判断grammar是不是以S_开头的LL1文法
    :param grammar:
    :return:
    '''
    #判断是不是以S_开头的
    if grammar[0][0] != 'S_':
        return False

    # 判断是否左递归
    for l, r in grammar:
        if l == r[0]:
            return False

    #判断First相交
    first = getFirst(grammar)
    Vt = get_NVT(grammar)   #获取全部非终结符
    follow = getFollow(grammar)
    for v in Vt:
        res_v = []
        for l, r in grammar:
            if l == v:
                fg = append(res_v, first[l + '->' + ''.join(r)])
                if fg:  #有交集
                    return False
        if 'none' in res_v:
            follow_v = getFollowSet(follow, v)
            for f in follow_v:
                if f in res_v:  # 某非终结符含空的First集和其follow其有交集
                    return False
    return True


def createPreAnalySheet(gramar: list):
    '''
    
    :param gramar:  文法
    :return:  预测分析表 字典 key（非终结者符，终结者） value（预测替换的式子）
    '''
    # 获取所有非终结符
    res={}
    follow = getFollow(gramar)
    first = getFirst(gramar)
    for l, r in gramar:
        # #print(l, r, 'yyy')
        key = l + '->'+''.join(r)
        fst = getFirstSet(gramar, first, key)[0]

        if 'none' in fst:
            follow_ = getFollowSet(follow, l)[0]
            append(fst, follow_)
        for s in fst:
            if s != 'none':
                key_ = l + '->' + s
                res[key_] = r
                # if key_ in res:
                #     res[key_].append(r)
                # else:
                #     res[key_] = [r]

    return res

class Predict_Analyse():
    '''
    预测分析类
    '''

    def __init__(self, grammar, sheet = None):
        if not isLL1(grammar):
            print('该文法不是LL1文法！')    #UI进行提醒
            self.enable = False
        else:
            self.enable = True
            if not sheet:
                self.sheet = createPreAnalySheet(grammar)
            else:
                self.sheet = sheet
    def run(self, s):
        '''
        使用预测分析法 匹配s
        :param sheet: 预测分析表
        :param gramar:
        :param s:  源代码
        :return: 是否符合文法
        '''
        self.token, errors = parseString(s + '#')
        self.stack = ['#', 'S_']  # 辅助栈， A 表示开始符
        self.idx = 0
        self.step_fg = True
        # doPreAnaly(self.sheet, token)



    def doPreAnly_by_step(self):
        if self.idx >= len(self.token) or not self.stack:
            self.step_fg = False
            return None, None, None
        self.X = self.stack.pop()
        # print('Stack:', self.stack, 'X:', self.X, '__: ', self.token[self.idx][0])
        if self.X:
            if self.X != '#' and not self.X[0][0].isupper():  # 终结符号
                if self.token[self.idx][0] == self.X:
                    self.idx += 1
                    info = "匹配"+str(self.X)
                else:
                    info = '匹配失败'
                    # return str(self.X) + ' 与 ' + str(self.token[self.idx][0]) + ' 匹配失败', '-'
            elif self.X == '#':
                if self.X == self.token[self.idx][0]:
                    info = '匹配成功'
                else:
                    info = '匹配失败'
                    # return str(self.X) + ' 与 ' + str(self.token[self.idx][0]) + ' 匹配失败', '-'
            else:  # 非终结者符

                key = self.X + '->' + self.token[self.idx][0]
                if key in self.sheet:
                    if self.sheet[key] != 'none':
                        lst = self.sheet[key]
                        info = str(self.X) + '替换' + ''.join(lst)
                        # print('替换：', lst)
                        self.stack += [item for item in lst[::-1] if item != 'none']
                else:
                    info = '匹配失败'
        return ''.join(self.stack), ''.join([l[0] for l in self.token[self.idx:]]), info


    def doPreAnaly(self):
        stack = ['#', 'S_']  # 辅助栈， A 表示开始符
        token = copy.deepcopy(self.token)
        idx = 0
        while idx < len(token) and stack:
            X = stack.pop()
            print('Stack:', stack, 'X:', X, '__: ',token[idx][0])
            if X:
                if X != '#' and not X[0][0].isupper():  # 终结符号
                    if token[idx][0] == X:
                        idx += 1
                    else:
                        print('匹配失败')
                        return False
                elif X == '#':
                    if X == token[idx][0]:
                        return True
                    else:
                        return  False
                else: #非终结者符

                    key = X + '->' + token[idx][0]
                    print(key)
                    if key in self.sheet:
                        if self.sheet[key] != 'none':
                            lst = self.sheet[key]
                            print('替换：',lst)
                            stack += [item for item in lst[::-1] if item != 'none']
                    else:
                        return False


def split_r(r):
    '''
    分割右侧符号
    如果某符号为 ', 则分给前者， 其他符号都单独存在
    :param r:
    :return:
    '''

    rr = list(r)
    for i in range(len(rr)):
        if rr[i] == "\'":
            rr[i-1] += '\''
        if rr[i] == 'ε':
            rr[i] = 'none'

    while '\'' in rr:
        rr.remove('\'')
    return rr


def transfer(s):
    '''
    将用户输入的字符串转换成格式化的文法
    :param s:
    :return:
    '''

    grammar = []
    s = s.strip()
    lines = s.split('\n')
    print(lines)
    for line in lines:
        print(line)
        if line != '':
            line = line.strip()
            l, r = line.split('->')
            if l[0].isupper():
                grammar.append((l.strip(), split_r(r)))

    return grammar
