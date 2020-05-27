'''
定义 Frist集， Follow 集函数
'''

from extract_word import parseString
import copy
import sys

Start = 'S_'
class Tokens():
    '''
    这是一个对词法分析器的结果进行处理的类
    '''

    def __init__(self, tokens):
        '''
        :param tokens:  词法分析器的结果 List（Tuple（word, type, row, col)
        '''
        self.tokens = tokens
        self.idx = 0  # 当前指针
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

    for i in range(len(S) - 1, -1, -1):
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
    for b in B:
        if b not in A:
            A.append(b)


def getFirst(gramar: list):
    '''

    :param gramar:  文法，list(tuple(文法左部分，文法右部分)), 规定右边不含有|
    :param elements:   获取element 的First集
    :return: List
    '''
    res = {}
    while True:
        res_copy = copy.deepcopy(res)
        for l, r in gramar:

            key = l + '->' + ''.join(r)
            if r != ['none'] and not r[0][0].isupper():  # 形如 A-> a*
                if key not in res:
                    res[key] = []
                if r[0] not in res[key]:
                    res[key].append(r[0])
            elif r == ['none']:  # 形如 A-> 空
                if key not in res:
                    res[key] = []
                if r[0] not in res[key]:
                    res[key] += r
            elif r[0].isupper() and not deduce(gramar, r[0]):  # 形如 A-> X*

                if key not in res:
                    res[key] = []

                for ll, rr in gramar:
                    if ll == r[0]:
                        key_ = ll + '->' + ''.join(rr)
                        if key_ not in res:
                            res[key_] = []
                        append(res[key], res[key_])

            else:  # 形如 A -> X1X2X3..Xk*
                if key not in res:
                    res[key] = []

                for i, e in enumerate(r):  # 形如 A -> X1X2X3..Xk*
                    if deduce(gramar, e) and i + 1 < len(r) and e[0].isupper():
                        for ll, rr in gramar:
                            if ll == e:
                                key_ = ll + '->' + ''.join(rr)
                                if key_ not in res:
                                    res[key_] = []
                                res[key] += res[key_]
                    else:
                        # print(e)
                        if e[0].isupper():
                            for ll, rr in gramar:
                                if ll == r[0]:
                                    key_ = ll + '->' + ''.join(rr)
                                    if key_ not in res:
                                        res[key_] = []
                                    append(res[key], res[key_])
                        elif e not in res[key]:
                            # print('iiii')
                            res[key].append(r[i])
                        break
                res[key] = clear(res[key])
            # print(l, r, res[key])
        # print(res)
        if isequal(res, res_copy):
            break
    return res


def getFirstSet(gramar, res, *elements):
    rr = []
    for element in elements:
        if '->' not in element:
            res_v = []
            for l, r in gramar:
                if l == element:
                    # res_v += res[l+'->'+r]
                    append(res_v, res[l + '->' + ''.join(r)])
            rr.append(res_v)
        else:
            try:
                res_v = res[element]
                rr.append(res_v)
            except BaseException:
                print('该语法不包含： ', element)
    return rr


def getFollow(gramar: list):
    '''

    :param gramar:  文法，list(tuple(文法左部分，文法右部分)), 规定右边不含有|
    :param elements:   获取element 的Follow集
    :return: List
    '''
    res = {}
    first = getFirst(gramar)
    while True:
        res_copy = copy.deepcopy(res)
        for l, r in gramar:
            # #print(l, r)
            if l == Start:  # A 作为开始符
                if l not in res:
                    res[l] = []
                if '#' not in res[l]:
                    # #print('yyyy')
                    res[l].append('#')

            for i in range(len(r)):
                if i < len(r) - 1 and r[i][0].isupper() and not r[i + 1][0].isupper():  # 形如 A -> * Bb *
                    # 把紧贴着的终结符b加入B的follow集中
                    if r[i] not in res:
                        res[r[i]] = []
                    if r[i + 1] not in res[r[i]]:
                        res[r[i]].append(r[i + 1])
                    # #print(res)
                if i < len(r) - 1 and r[i][0].isupper() and r[i + 1][0].isupper():  # 形如 A -> * BC *
                    # 把紧贴着的非终结符C的First集加入B的follow集中

                    [fs] = getFirstSet(gramar, first, r[i + 1])

                    if 'none' in fs:
                        fs.remove('none')

                    if r[i] not in res:
                        res[r[i]] = []
                    res[r[i]] += fs
                    res[r[i]] = list(set(res[r[i]]))

                i = deduce_muti(gramar, r)
                if r[-1][0].isupper() and l != r[-1]:  # 形如 B -> *A
                    # 把B的follow集 添加到A的follow集里
                    if r[-1] not in res:
                        res[r[-1]] = []
                    if l not in res:
                        res[l] = []
                    res[r[-1]] += res[l]
                    res[r[-1]] = list(set(res[r[-1]]))
                if i != len(r) - 1:  # 形如 B -> *Ap, p->none
                    if r[i] not in res:
                        res[r[i]] = []
                    if l not in res:
                        res[l] = []
                    append(res[r[i]], res[l])

        if isequal(res, res_copy):
            break
    return res


def getFollowSet(res, *elements):
    # print(elements , res)
    res_v = [res[element] for element in elements]
    return res_v

