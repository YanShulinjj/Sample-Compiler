from LR1 import createItems, createLR_sheeet
from utils import getFirst, getFirstSet, getFollow, getFollowSet
from extract_word import parseString
import  pickle

all_g, all_sheet = pickle.load(open('data/all_sheetLR14.pkl', 'rb'))
all_item = pickle.load(open('data/all_LR1_items4.pkl', 'rb'))
follow = getFollow(all_g)

def transfer(ls):
    '''
    列表转字典， key 为其下标
    :param ls:
    :return:
    '''
    r = {}
    for i,l in enumerate(ls):
        r[i] = l
    return r

def get_final_sigs(grammar):
    '''
    获取 文法中的全部终结符
    :param grammar:
    :return:
    '''

    res = []
    for l, r in grammar:
        for rr in r:
            if not rr[0].isupper():
                res.append(rr)
    return list(set(res))

def isexist_goto(sheet, state):
    '''
    判断状态state 是否有goto选项
    :param sheet:  LR1分析表
    :param state:  state状态
    :return:
    '''

    for key in sheet.keys():
        # print(key)
        s = key.split('->')
        # print('S', s)
        if s[0] == state and s[1][0].isupper():
            return True, s[1]
    return False, None


class LR1_G():

    def __init__(self):
        self.idx = 0
        self.codes = []
        self.NXQ = 1
        # 定义符号表
        self.const_attri_sheet = []
        self.variable_attri_sheet = []
        self.func_attr_sheet = []
        pass

    def doentry(self, token: list):
        '''
        翻译入口
        :param token:
        :return:
        '''
        token.append(('#', 'BOUND', token[-1][2], token[-1][3] + 1))
        # 定义状态栈， 符号栈
        State = ['0']
        sigs = ['#']
        infos = []
        ############ 属性定义区域 ###########

        ######################### ###########
        fg = True
        fg_s = False
        idx = 0  # token 指针

        while State and idx < len(token):
            if len(list(set(infos))) != len(infos):
                infos.pop()
                break
            current_state = State[-1]

            if token[idx][1] in ['CONST']:
                key = current_state + '->' + 'c'
                # self.e.append(token[idx][0])
            elif token[idx][1] in ['IDT']:
                key = current_state + '->' + 'id'
                # self.e.append(token[idx][0])
            elif token[idx][0] in ['>', '<', '>=', '<=', '==', '!=']:
                key = current_state + '->' + 'rop'
                # t = self.AE[-1].PLACE
                # if t not in self.e:
                #     self.e.append(t)

            elif token[idx][0] in get_final_sigs(all_g) + ['#']:
                key = current_state + '->' + token[idx][0]
                if key not in all_sheet:  # 没有错误时
                    fg_s = True  # 此时下次的移动， idx 不用加一
                    key = current_state + '->' + 'none'
            else:
                # print(token[idx][0])
                key = current_state + '->' + 'none'
            if key in all_sheet:  # 没有错误时
                value = all_sheet[key]
                if value[0] == 's':
                    State.append(value[1:])
                    sigs.append(token[idx][0])
                    if fg_s:
                        fg_s = False
                    else:
                        idx += 1
                elif value[0] == 'r':
                    # 获取产生式
                    j = int(value[1:])
                    l, r = all_g[j]
                    len_ = len(r)
                    # len个元素同时出栈
                    State = State[: -len_]
                    sigs = sigs[: -len_]

                    # print(State)
                    # l 符号查表 进栈
                    key = State[-1] + '->' + l
                    if key in all_sheet:
                        value = all_sheet[key]
                        State.append(value)
                        sigs.append(l)
                    else:
                        info = token[idx][0] + '附近出现语法错误！' + ':: row: '+str(token[idx][2]) + '  col: '+ str(token[idx][3])
                        infos.append(info)
                        # print(key, token[idx], '不在字典中')
                        idx = self.error_process(State, sigs, token, idx)
                        fg = False
                        # break
                elif value == 'acc':
                    # print('接受成功')
                    info = ''
                    fg = True
                    break
                elif str(value).isdigit():
                    info = token[idx] + '异常！'
                    infos.append(info)
                    # print('异常！')
                else:
                    info = token[idx][0] + '附近出现语法错误！' + ':: row: '+str(token[idx][2]) + '  col: '+ str(token[idx][3])
                    infos.append(info)
                    # print(key, token[idx], '不在字典中')
                    idx = self.error_process(State, sigs, token, idx)
                    fg = False
                    # break
            else:
                info = token[idx][0] + '附近出现语法错误！' + ':: row: '+str(token[idx][2]) + '  col: '+ str(token[idx][3])
                infos.append(info)
                # print(key, token[idx], '不在字典中')
                idx = self.error_process(State, sigs, token, idx)
                fg = False
                # break
        # print(current_state)
        return fg, infos

    def entry(self, s):
        token, errors = parseString(s)
        if errors:
            # print('词法分析不通过！')
            return
        else:
            return self.doentry(token)

    def error_process(self, State, sigs, token, idx):
        '''
        采用恐慌模式
        进行错误处理
        :return:
        '''
        # print('SSSS', sigs)
        while State:
            fg, v = isexist_goto(all_sheet, State[-1])
            if fg:
                fw = getFollowSet(follow, v)[0]
                # print(fw)
                # 找到 state 存在 goto目标，认为 从 v推导处的串中包含错误
                while idx < len(token):
                    if token[idx][0] in fw:
                        value = all_sheet[State[-1] + '->' + v]
                        State.append(value)
                        # idx += 1
                        return idx
                    else:
                        idx += 1
            State.pop()
        return idx



