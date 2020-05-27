'''
自底向上 分析器
'''

import copy
from utils import getFirst, getFirstSet
from extract_word import parseString


def get_FirstSet_full(grammar, first,  sigs):
    '''

    :param first:
    :param sigs:
    :return:
    '''
    rr = []
    for s in sigs:
        if not s[0].isupper():
            rr.append(s)
            break
        fs = getFirstSet(grammar, first, s)[0]
        rr += fs
        if 'none' not in fs:
            break
        else:
            rr.remove('none')
    return list(set(rr))

def closeure(I: list, Gramar: list):
    '''
    计算制定项目集的闭包
    :param I:  给定项目集  [[('X',['E'->'A'], a)], ...]
    :param Gramar:  给定文法
    :return:  返回项目集闭包
    '''

    J = I[:] #deep copy
    first = getFirst(Gramar)
    while True:
        fg = False
        for l, r, c in J:
            idx = list(r).index('.')
            if idx < len(r) - 1 and r[idx+1][0].isupper():  # A -> * . B * 形式
                for lg, rg in Gramar:
                    fs = get_FirstSet_full(Gramar, first, r[idx+2:]+[c])   #  求First(后面的* 后接着c）
                    for b in fs:
                        if lg == r[idx+1] and (lg, ['.']+rg, b) not in J:
                            fg = True
                            J.append((lg, ['.']+rg, b))
        if not fg:
            break
    return J

def moveDot(item: tuple, step = 1):
    '''
    点往后移动step格， 默认一格
    :param item: 项目集的一个元素 Turple
    :param step:
    :return:
    '''
    copy_item = copy.deepcopy(item)
    l, r, c = copy_item
    idx = r.index('.')
    if idx < len(r) - step:
        r.remove('.')
        r.insert(idx+1, '.')
        return (l, r, c)
    else:
        print('不能向后移动{} 格！'.format(step))

def get_full_sig(grammar: list):
    '''
    获取文法中所有符号
    :param grammar:  文法 list
    :return:  文法中所有非终结符和终结符
    '''
    l_sigs = [l for l ,r in grammar]  # 文法左侧所有符号
    r_sigs = [] # 文法右侧所有符号
    for _, rs in grammar:
        for rr in rs:
            r_sigs.append(rr)
    res = list(set(l_sigs + r_sigs))

    return res

def goto(I: list, X: str, Grammar: list):
    '''
    计算项目集I 经过X 的后继闭包
    :param I:  给定项目集
    :param X:  给定的后继符号
    :param Grammar:  给定文法
    :return:  返回一个后继项目集闭包
    '''
    J = []
    II = copy.deepcopy(I)
    for l, r, c in II:
        # print(l,r,c)
        idx = r.index('.')
        if idx < len(r) - 1 and r[idx+1] == X: # 找到 A —> * . X *
            # print('移动原点', l, r)
            t = moveDot((l, r, c))
            J.append(t)
    return closeure(J, Grammar)

def createItems(grammar: list):
    '''
    构建LR(1) 自动机的状态集族
    :param grammar:  注意是增广文法， 开始符只存在一个产生式的左部。
    :return:
    '''

    #获取开始符号
    temp_g = copy.deepcopy(grammar[0])
    l, r = temp_g
    r = ['.'] + r
    temp = closeure([(l, r, '#')], grammar)
    # temp.append('none')
    C = [temp]
    Xs = get_full_sig(grammar)
    # print(Xs)
    while True:
        fg = False
        # print(len(C))
        for item in C:
            for l in Xs:
                # item_= item[0:-1]  # 去除最后一个元素吗最后一个元素代表着
                goto_temp = goto(item, l, grammar)
                # print(l, goto_temp )
                # goto_temp.append(l)
                # print(goto_temp)
                if goto_temp and goto_temp not in C:
                    fg = True
                    C.append(goto_temp)
        if not fg:
            break
    return C

def get_index_of_grammar(grammar: list, v):
    '''
    根据 v 返回v在grammar中的序号
    :param gammar:
    :param v:
    :return:
    '''
    # print('GGGGGG', v)
    vv = copy.deepcopy(v)
    l, r = vv
    if '.' in r:
        r.remove('.')
    if vv in grammar:
        return grammar.index(vv)


def createLR_sheeet(items, grammar: list):
    '''
    构造LR（1）分析表
    :param items: LR（1）项集族
    :param grammar:
    :return:
    '''
    sheet ={}
    Vt = get_full_sig(grammar) # 文法所有终结符
    Vt = [v for v in Vt if not v[0].isupper()]
    Vt.append('#')
    copy_items = copy.deepcopy(items)
    for i, item in enumerate(items):
        item_ = copy.deepcopy(item)
        for l, r, c in item:
            for idx in range(len(r) - 1):
                if r[idx] == '.':
                    gt = goto(item_, r[idx + 1], grammar)
                    if not r[idx+1][0].isupper() and gt in items:  # 形如 A—>* .a *
                        j = items.index(gt)
                        sheet[str(i)+'->' + r[idx+1]] = 's'+str(j)
                    elif r[idx+1][0].isupper() and gt in items:  # # 形如 A—>* .B *
                        j = items.index(gt)
                        sheet[str(i) + '->' + r[idx + 1]] = str(j)
            if r[-1] == '.': # 形如 A->* .
                if l == 'S_':
                    sheet[str(i) + '->' + '#'] = 'acc'
                else:
                    # print(l,r)
                    j = get_index_of_grammar(grammar, (l, r))  # 找到规约式在原文法的位置
                    # if not j:
                        # print('yyyy', l,r)
                    sheet[str(i) + '->' + str(c)] = 'r' + str(j)

    return sheet

def LR1_analyse(sheet: dict, grammar, s: str):
    '''

    :param sheet:  创建好的LR1分析表
    :param s:  待分析字符串
    :return:
    '''

    token, errors = parseString(s+'#')
    # 如果有词法错误
    if errors:
        print('词法错误！')
        for e in errors:
            print(e)
            return
    # 定义状态栈， 符号栈
    State = ['0']
    sigs = ['#']
    idx = 0 # token 指针
    while State and idx < len(token):
        current_state = State[-1]
        key = current_state+'->'+ token[idx][0]
        if  key in sheet: #没有错误时
            value = sheet[key]
            if value[0] == 's':
                State.append(value[1:])
                idx += 1
            elif value[0] == 'r':
                # print(value)
                l,r = grammar[int(value[1:])]
                len_ = len(r)
                # len个元素同时出栈
                # print(State)
                State = State[: -len_]
                # print(State)
                # l 符号查表 进栈
                key = State[-1]+'->'+l
                if key in sheet:
                    value = sheet[key]
                    State.append(value)
                else:
                    print('出错')
            elif value == 'acc':
                print('接受成功')
                break
            else:
                print('出错！！')
        else:
            print('出错！！')
            break

