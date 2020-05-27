from LR1 import createItems, createLR_sheeet
from utils import getFirst, getFirstSet, getFollow, getFollowSet
from extract_word import parseString
import  pickle

all_g, all_sheet = pickle.load(open('data/all_sheetLR14.pkl', 'rb'))
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
        s = key.split('->')
        if s[0] == state and s[1][0].isupper():
            return True, s[1]
    return False, None

class node():
    def __init__(self, key = None):
        self.key = key
        self.id = ''
        self.type = ''
        self.value = 0
        self.PLACE = ''
        self.fg = False
        self.entry_id = ''
        self.TC = ''
        self.FC = ''
        self.CHAIN = 0
        self.HEAD = ''
        self.TEST = ''
        self.RIGHT = ''
        self.INC = ''
        self.BRK = ''

class Translate():

    def __init__(self):
        self.idx = 0
        self.codes = []
        self.NXQ = 1
        # 定义符号表
        self.const_attri_sheet = []
        self.variable_attri_sheet = []
        self.func_attr_sheet = []
        self.define_var()
        self.fg = True
        pass
    def get_temp(self):
        '''
        申请一个临时变量
        :return:
        '''
        self.idx += 1
        return 't'+str(self.idx)

    def get_current_temp(self):
        '''
        获取最近申请得临时变量
        :return:
        '''
        return 't'+str(self.idx)

    def search_attribute_sheet(self, id):
        for i, elem in enumerate(self.const_attri_sheet):
            if elem['name'] == id:
                return id, elem['value']
        for i, elem in enumerate(self.variable_attri_sheet):
            if elem['name'] == id:
                if 'value' in elem:
                    return id, elem['value']
                else:
                    return id, 0
        return 'Undefined {}'.format(id), None

    def search_func_sheet(self, func_id):
        '''
        查询函数属性表
        :param func_id:
        :return:
        '''
        for sheet in self.func_attr_sheet:
            if sheet['name'] == func_id:
                return sheet['entry'], sheet['parList']
        return '未定义函数{}'.format(func_id), None

    def add_new_attribute(self, name, attribute = None, value = None, isconst = True):
        if isconst:
            for sig in self.const_attri_sheet:
                if name in sig.values():
                    sig[attribute] = value
                    return
            # name 还没有添加
            dic = {'name': name, attribute: value}
            self.const_attri_sheet.append(dic)
        else:
            for sig in self.variable_attri_sheet:
                if name in sig.values():
                    sig[attribute] = value
                    return
            # name 还没有添加
            dic = {'name': name, attribute: value}
            self.variable_attri_sheet.append(dic)

    def add_new_attr_for_func(self, name, attribute = None, value = None):
        for sig in self.func_attr_sheet:
            if name in sig.values():
                sig[attribute] = value
                return
        # name 还没有添加
        dic = {'name': name, attribute: value}
        self.func_attr_sheet.append(dic)

    def generate_code(self, op, arg1, arg2, result_t):
        '''
        产生一个四元式, 自动加入程序列里
        :param op: 运算符
        :param arg1:
        :param arg2:
        :param result_t:
        :return:
        '''
        self.codes.append([op, arg1, arg2, result_t])
        self.NXQ += 1

    def backpatch(self, P, t):
        Q = P
        record = []
        if P == 0:
            return
        while Q != 0 and Q not in record:
            record.append(Q)
            print(self.codes[Q - 1])
            m = self.codes[Q - 1][-1]
            if self.codes[Q - 1][-1] == t:
                break
            self.codes[Q - 1][-1] = t
            Q = m


    def merge(self, P1, P2):
        if P1 == 0:
            return P2
        elif P2 == 0:
            return P1
        elif P1 == P2:
            return P1
        else:
            ## P1 P2 都不为空
            P = P2
            while True:
                m = self.codes[P-1][-1]
                if m == 0:
                    self.codes[P - 1][-1] = P1
                    break
                P = m #指针后移
            return P2

    def define_var(self):
        self.VDCL = node()
        self.AE = node()
        self.DCL = node('LCD')
        self.Head = node('Head')
        self.Type = node('Type')
        self.TD = node('TD')
        self.AE = []
        self.IT = []
        self.F = node('F')
        self.P = node('P')
        self.D = node('D')
        self.U = node('U')
        self.BF = node('BF')
        self.BE_or = node('BE_or')
        self.BT_and = node('BT_and')
        self.BE = node('BE')
        self.BT = node('BT')
        self.FDP = []
        self.S = []
        self.SS = node('SS')
        self.C = []
        self.Dw = []
        self.T = node('T')
        self.FF = node('FF')
        self.A = node('A')
        self.B = []
        self.last_s = 0
        self.steam = []
        self.id = []
        self.v = []
        self.e = []
        self.Next = []
        self.FT = node('FT')
        self.FCF = node('FCF')
        self.FC = node('FC')
        self.breakpoints = []
        self.ret = ''
        self.func_ids = []
        self.while_entrance = 0
    def r1(self, sigs):
        self.add_new_attribute(sigs[-1], 'type', self.VDCL.type, False)

    def r2(self, sigs):
        print('r2', sigs)
        self.add_new_attribute(sigs[-3], 'type', self.VDCL.type, False)
        self.add_new_attribute(sigs[-3], 'value', self.AE[-1].value, False)
        self.generate_code('=', self.AE[-1].PLACE, '', sigs[-3])
    def r4(self, sigs):
        self.add_new_attribute(sigs[-1], 'type', self.Type.type, False)
        self.VDCL.type = self.Type.type

    def r5(self, sigs):
        self.add_new_attribute(sigs[-3], 'type', self.Type.type, False)
        self.add_new_attribute(sigs[-3], 'value', self.AE[-1].value, False)
        self.generate_code('=', self.AE[-1].PLACE, '', sigs[-3])
        self.VDCL.type = self.Type.type

    def r6(self):
        self.TD.type = self.Head.type

    def r8(self):
        self.Head.type = self.Type.type
        self.TD.type = self.Head.type

    def r9_11(self, type_):
        self.Type.type = type_


    def r12_13(self):
        self.TD.id = self.id.pop()
        self.TD.value = self.v.pop()
        self.add_new_attribute(self.TD.id, 'value', self.TD.value)
        self.add_new_attribute(self.TD.id, 'type', self.TD.type)

    def r14(self):
        ae = self.AE.pop()
        it = self.IT.pop()
        arg2, arg1 = self.steam.pop(), self.steam.pop()
        ae.value = int(ae.value) + int(it.value)
        self.AE.append(ae)
        t = self.get_temp()
        self.steam.append(t)
        self.generate_code('+', arg1, arg2, t)
        # if self.e:
            # self.e.pop()
        # self.e.append(self.get_current_temp())
        self.AE[-1].PLACE = self.get_current_temp()

    def r15(self):
        ae = self.AE.pop()
        it = self.IT.pop()
        arg2, arg1 = self.steam.pop(), self.steam.pop()
        # print(it.value)
        ae.value = int(ae.value) - int(it.value)
        self.AE.append(ae)
        t = self.get_temp()

        self.steam.append(t)
        self.generate_code('-', arg1, arg2, t)
        # self.e.append(self.get_current_temp())
        self.AE[-1].PLACE = self.get_current_temp()

    def r16(self):
        ae = node()
        t = self.IT[-1].PLACE
        it = self.IT.pop()
        ae.value = int(it.value)
        self.AE.append(ae)
        self.AE[-1].PLACE = t


    def r17(self):
        arg2, arg1 = self.steam.pop(), self.steam.pop()

        it = self.IT.pop()
        it.value = int(it.value) * int(self.F.value)
        self.IT.append(it)
        t = self.get_temp()

        self.steam.append(t)
        self.generate_code('*', arg1, arg2, t)
        self.IT[-1].PLACE = self.get_current_temp()

    def r18(self):
        arg2, arg1 = self.steam.pop(), self.steam.pop()
        it = self.IT.pop()
        it.value = int(it.value) / int(self.F.value)
        self.IT.append(it)
        t = self.get_temp()

        self.steam.append(t)
        self.generate_code('/', arg1, arg2, t)
        self.IT[-1].PLACE = self.get_current_temp()

    def r19(self):
        arg2, arg1 = self.steam.pop(), self.steam.pop()
        it = self.IT.pop()
        it.value = int(it.value) % int(self.F.value)
        self.IT.append(it)
        t = self.get_temp()

        self.generate_code('%', arg1, arg2, t)
        self.steam.append(t)
        self.IT[-1].PLACE = self.get_current_temp()

    def r20(self):
        it = node('IT')
        it.value = int(self.F.value)
        self.IT.append(it)
        self.IT[-1].PLACE = self.F.PLACE


    def r21(self):
        print('PPP', self.P.value)
        self.F.value = int(self.P.value)
        self.F.PLACE = self.P.PLACE

    def r22(self):
        self.F.value = - int(self.P.value)
        t = self.get_temp()

        arg1 = self.steam.pop()
        self.generate_code('@', arg1, '', t)
        self.steam.append(t)
        self.F.PLACE = self.get_current_temp()

    def r23(self):
        ae = self.AE.pop()
        self.P.value = int(ae.value)
        self.P.PLACE = self.AE[-1].PLACE

    def r24(self, sigs):
        # 查找属性表
        _, v = self.search_attribute_sheet(sigs[-1])
        if v:

            self.P.value = int(v)
            self.steam.append(sigs[-1])
            self.P.PLACE = sigs[-1]
        else:
            self.P.value = 1
            self.steam.append(sigs[-1])
            self.P.PLACE = sigs[-1]
            print(_)

    def r25(self, sigs):
        self.P.value = int(sigs[-1])
        # t = self.get_temp()
        # self.generate_code('=', sigs[-1], '', t)
        self.steam.append(sigs[-1])
        self.P.PLACE  = sigs[-1]


    def r26(self):
        self.BE.FC = self.BT.FC
        # print(BE_or.TC, BT.TC)
        self.BE.TC = self.merge(self.BE_or.TC, self.BT.TC)

    def r27(self):
        # print('back F to', BE.FC)
        self.backpatch(self.BE.FC, self.NXQ)
        self.BE_or.TC = self.BE.TC

    def r28(self):
        self.BE.TC, self.BE.FC = self.BT.TC, self.BT.FC

    def r29(self):

        self.BT.TC = self.BF.TC
        # print(BT_and.FC, BF.FC)
        print('yyyyy',self.BT_and.FC, self.BF.FC)
        for i, code in enumerate(self.codes):
            print(i+1, code)
        self.BT.FC = self.merge(self.BT_and.FC, self.BF.FC)

    def r30(self):
        self.backpatch(self.BT.TC, self.NXQ)
        # print('back to ', BT.TC)
        self.BT_and.FC = self.BT.FC

    def r31(self):
        self.BT.TC, self.BT.FC = self.BF.TC, self.BF.FC

    def r32(self):
        self.BF.FC, self.BF.TC = self.BF.TC, self.BF.FC
    def r33(self):
        self.BF.TC = self.BE.TC
        self.BF.FC = self.BE.FC

    def r34(self):
        self.BF.TC = self.NXQ
        self.BF.FC = self.NXQ + 1
        self.e.append(self.AE[-1].PLACE)
        arg2, arg1 = self.e.pop(), self.e.pop()
        self.generate_code('j' + self.op, arg1, arg2, 0)
        # link2 = self.NXQ - 1
        self.generate_code('j', '', '', 0)
        # link = self.NXQ - 1

    def r35(self, sigs):
        self.BF.TC = self.NXQ
        self.BF.FC = self.NXQ + 1
        arg1, op, arg2 = sigs[-3], sigs[-2], sigs[-1]
        self.generate_code('j' + op, arg1, arg2, 0)
        # link2 = self.NXQ - 1
        self.generate_code('j', '', '', 0)
        # link = self.NXQ - 1

    def r36(self):
        self.BF.TC = self.NXQ
        self.BF.FC = self.NXQ
        # self.generate_code('j' + op, self.e.pop(), '', 0)
        # link2 = self.NXQ - 1

        self.generate_code('j', '', '', 0)
        # link = self.NXQ - 1

    def r37(self):
        # print(self.codes)
        c = self.C.pop()
        if not self.S:
            s = node('S')
            self.S.append(s)
        print('pppppp',c.CHAIN, self.S[-1].CHAIN)

        n = node('Next')
        n.CHAIN = c.CHAIN
        n.INC = self.NXQ
        self.Next.append(n)


    def r38(self):
        # print(BE_FC, self.NXQ)
        self.backpatch(int(self.BE.TC), self.NXQ)
        c = node('C"')
        c.CHAIN = int(self.BE.FC)
        self.C.append(c)
        self.last_s = self.BE.FC

    def r39(self):
        print('hhhhhh', self.T.CHAIN, self.SS.CHAIN)
        s = node('S')
        s.CHAIN = self.merge(self.T.CHAIN, self.SS.CHAIN)
        self.S.append(s)

        n = node('Next')
        n.CHAIN = s.CHAIN
        n.INC = self.NXQ
        self.Next.append(n)

        # self.backpatch(self.S.CHAIN, self.NXQ)
        # self.S.CHAIN = 0

    def r40(self):
        q = self.NXQ
        self.generate_code('j', '', '', 0)
        c = self.C.pop()
        print('CCCC', c.CHAIN, q, self.SS.CHAIN)
        self.backpatch(c.CHAIN, self.NXQ)
        print('tggg',self.SS.CHAIN, q)
        self.T.CHAIN = self.merge(self.SS.CHAIN, q)


    def r41(self, sigs):
        self.generate_code('=', self.AE[-1].PLACE, '', sigs[-4])

    def r42(self):
        # s = node('S')
        # s.CHAIN = 0
        # self.S.append(s)
        pass

    def r43(self):
        # s = node('S')
        # s.CHAIN = 0
        # self.S.append(s)
        pass

    def r45(self):
        self.D.HEAD = self.NXQ
    def r44(self):
        # s = node('S')
        # s.CHAIN = 0
        # self.S.append(s)
        pass

    def r46(self):
        self.U.HEAD = self.D.HEAD
        # print('yyyyyyyyy', self.S.CHAIN)
        s = self.S.pop()
        self.backpatch(s.CHAIN, self.NXQ)

    def r47(self):
        self.backpatch(self.BE.TC, self.U.HEAD)
        s = node('S')
        s.CHAIN = self.BE.FC
        self.S.append(s)


    def r50(self, sigs):
        self.generate_code('=', self.AE[-1].PLACE, '', sigs[-3])

    def r51(self):
        # arg = self.AE[-1].PLACE

        self.FF.TEST = self.NXQ

    def r52(self):
        arg = self.AE[-1].PLACE
        self.A.PLACE = self.get_temp()

        self.A.RIGHT = self.BE.TC

        self.A.CHAIN = self.BE.FC

        self.A.INC = self.NXQ
        self.A.TEST = self.FF.TEST

    def r53(self):
        self.generate_code('j', '', '', self.A.TEST)
        print('RRRR', self.A.RIGHT)
        self.backpatch(self.A.RIGHT, self.NXQ)
        # self.backpatch(self.BE.TC, self.NXQ)
        b = node('B')
        b.CHAIN = self.A.CHAIN
        b.INC = self.A.INC
        b.AGAIN = self.NXQ
        b.RIGHT = self.A.RIGHT
        self.B.append(b)
        self.Next.append(b)
        s = node('S')
        s.CHAIN = b.CHAIN
        self.S.append(s)

    def r54(self):

        if self.SS.CHAIN == '':
            self.SS.CHAIN = 0


        print('uuuu', self.NXQ)

        print('BBBBB', self.B[-1].INC, self.BE.FC)
        for i, code in enumerate(self.codes):
            print(i+1, code)
        # self.backpatch(self.S[-1].CHAIN, self.NXQ+1)
        self.generate_code('j', '', '', self.B[-1].INC)


        # self.backpatch(self.BE.FC, self.NXQ)

        s = node('S')
        s.CHAIN = self.merge(self.S[-1].CHAIN, 0)
        self.S.append(s)
        # self.S.CHAIN = self.merge(self.FF.CHAIN, self.S.BRK)

    def r55(self):
        s = node('S')
        s.CHAIN = self.SS.CHAIN
        self.S.append(s)

    def r56(self):

        # s = self.S.pop()

        if self.S:
            print('R56', self.S[-1].CHAIN, self.SS.CHAIN)
            self.SS.CHAIN = self.S[-1].CHAIN
        else:
            self.SS.CHAIN = 0


    def r57(self):
        # s = self.S.pop()


        if self.S:
            print('R57', self.S[-1].CHAIN, self.SS.CHAIN)
            # self.backpatch(self.S[-1].CHAIN, self.NXQ)
            for code in self.codes:
                print(code)

    def r58(self):
        # print(BE_FC, self.NXQ)
        self.backpatch(int(self.BE.TC), self.NXQ)
        dw = node('DW')
        dw.CHAIN = int(self.BE.FC)
        self.Dw.append(dw)
        self.last_s = self.BE.FC




    def r59(self):
        for i, c in enumerate(self.codes):
            print(i + 1, c)
        if self.S:
            if self.Next:
                next_ = self.Next.pop()
                if self.Next:
                    print('yyyyyyyyyy', next_.CHAIN, self.Next[-1].INC)
                    self.backpatch(next_.CHAIN, self.Next[-1].INC)
                    for i, c in enumerate(self.codes):
                        print(i+1, c)
                else:
                    self.backpatch(next_.CHAIN, self.NXQ)
            else:
                print('rr59', self.S[-1].CHAIN, self.NXQ)
                self.backpatch(self.S[-1].CHAIN, self.NXQ)
            self.S[-1].CHAIN = 0
        else:
            print('yyy')
            s = node('S')
            self.S.append(s)
            n = node('Next')
            n.CHAIN = self.NXQ
            n.INC = self.NXQ
            self.Next.append(n)

        # print('r59', self.NXQ, self.BE.FC)
        # self.backpatch(self.BE.FC, self.NXQ)
        #
        # self.backpatch(self.S[-1].CHAIN, self.NXQ)
        # for i, c in enumerate(self.codes):
        #     print(i + 1, c)
        pass
    def r61(self):
        self.generate_code('ret', '', '', 'return_v')
        self.ret = self.AE[-1].PLACE
        current_func_id = self.func_ids.pop()
        for code in self.codes:
            if code[0] == 'call' and code[1] == current_func_id:
                code[-1] = 'return_v'

    def r62_64(self):
        # s = node('S')
        # s.CHAIN = 0
        # self.S.append(s)
        pass

    def r67(self):
        if self.breakpoints:
            breakpoint = self.breakpoints.pop()
        else:
            breakpoint = ''
        self.generate_code('j', '', '', breakpoint)


    def r68_69(self, sigs):
        self.FT.type = self.Type.type
        # 添加到属性表里
        func_id = sigs[-4]
        self.func_ids.append(func_id)
        # self.add_new_attr_for_func(func_id, 'rtype', self.Type.type)
        self.add_new_attr_for_func(func_id, 'entry', self.NXQ)
        print('添加入口', func_id, self.NXQ)
        #添加参数信息
        # self.add_new_attr_for_func(func_id, 'parList', self.FDP)
        ##把之前调用此函数的call代码更新entry
        # for code in self.codes:
        #     if code[0] == 'call' and code[1] == func_id:
        #         code[-1] = self.NXQ
        #清空FDP
        self.FDP = []
        self.generate_code(func_id, '', '', '')

    def r70_71(self, sigs):
        self.FT.type = self.Type.type
        # 添加到属性表里
        func_id = sigs[-5]
        self.add_new_attr_for_func(func_id, 'rtype', self.Type.type)
        # 添加参数信息
        self.add_new_attr_for_func(func_id, 'entry', '待定')
        self.add_new_attr_for_func(func_id, 'parList', self.FDP)
        ##把之前调用此函数的call代码更新entry
        for code in self.codes:
            if code[0] == 'call' and code[1] == func_id:
                code[-1] = self.NXQ
        # 清空FDP
        self.FDP = []

    def r72(self, sigs):
        self.FDP.append({'type': self.Type.type, 'par': sigs[-1]})

    def r75(self):
        # s = node('S')
        # s.CHAIN = 0
        # self.S.append(s)
        pass
    def r79(self, sigs):
        self.op = sigs[-1]
        self.e.append(self.AE[-1].PLACE)

    def r80(self):
        self.generate_code('main', '', '', '')

    def r81(self):
        # self.backpatch(self.S[-1].CHAIN, self.NXQ)
        pass

    def r82(self):
        for i, c in enumerate(self.codes):
            print(i + 1, c)
        if self.S:
            if self.Next:
                next_ = self.Next.pop()
                if self.Next:
                    print('yyyyyyyyyy', next_.CHAIN, self.Next[-1].INC)
                    self.backpatch(next_.CHAIN, self.Next[-1].INC)
                    for i, c in enumerate(self.codes):
                        print(i+1, c)
                else:
                    self.backpatch(next_.CHAIN, self.NXQ)
            else:
                self.backpatch(self.S[-1].CHAIN, self.NXQ)
            self.S[-1].CHAIN = 0
        else:
            print('yyy')
            s = node('S')
            self.S.append(s)
            n = node('Next')
            n.CHAIN = self.NXQ
            n.INC = self.NXQ
            self.Next.append(n)


    def r83(self):

        if self.Next:
            next_ = self.Next.pop()
            print(next_.CHAIN)
            if self.Next:
                print('hhhh',self.Next[-1].INC)
                self.backpatch(next_.CHAIN, self.Next[-1].INC)
            else:
                print('AA', next_.CHAIN)
                self.backpatch(next_.CHAIN, self.NXQ)
        else:
            self.backpatch(self.A.CHAIN, self.NXQ)

    def r84(self):

        self.backpatch(self.A.CHAIN, self.NXQ)

    def r85(self):
        # print(self.codes)
        dw = self.Dw.pop()
        if not self.S:
            s = node('S')
            self.S.append(s)
        print('pppppp', dw.CHAIN, self.S[-1].CHAIN)

        n = node('Next')
        n.CHAIN = dw.CHAIN
        n.INC = self.NXQ
        self.Next.append(n)
        print('r85', self.S[-1].CHAIN)
        self.backpatch(self.S[-1].CHAIN, self.NXQ)
        self.generate_code('j', '', '', self.while_entrance)
    def r86(self, sigs):
        #找到函数入口并保存当前NXQ
        fun_id = sigs[-4]
        entry, parlist = self.search_func_sheet(fun_id)
        self.generate_code('call', fun_id, '', 'return_v')
        #如果该函数有返回值，添加AE.PLACE = 'return_v'

        # 保存断点
        print('断点： ',self.NXQ)
        self.breakpoints.append(self.NXQ)
        self.FC.PLACE = self.FCF.PLACE
    def r89(self):
        self.generate_code('para', self.FCF.PLACE, '', '')

    def r90(self):
        self.generate_code('para', self.FCF.PLACE, '', '')

    def r91(self):
        self.FCF.PLACE = self.AE[-1].PLACE
    def r92(self):
        self.FCF.PLACE = self.FC.PLACE

    def r94(self):
        self.generate_code('sys', '', '', '')

    def r95(self):
        self.P.PLACE = 'return_v'

    def r96(self):

        self.while_entrance = self.NXQ


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
                self.v.append(token[idx][0])
                # self.e.append(token[idx][0])
            elif token[idx][1] in ['IDT']:
                key = current_state + '->' + 'id'
                self.id.append(token[idx][0])
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
                print(token[idx][0])
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

                    j = int(value[1:])
                    print('r',j)
                    if self.fg == True: #未发生语法错误时才需要翻译
                        if j == 1:
                            self.r1(sigs)
                        elif j == 2:
                            print(token[idx])
                            self.r2(sigs)
                        elif j == 4:
                            self.r4(sigs)
                        elif j == 5:
                            self.r5(sigs)
                        elif j == 6:
                            self.r6()
                        elif j == 8:
                            self.r8()
                        elif j in [9, 10, 11]:
                            self.r9_11(sigs[-1])
                        elif j in [12, 13]:
                            self.r12_13()
                        elif j == 14:
                            self.r14()
                        elif j == 15:
                            self.r15()
                        elif j == 16:
                            self.r16()
                        elif j == 17:
                            self.r17()
                        elif j == 18:
                            self.r18()
                        elif j == 19:
                            self.r19()
                        elif j == 20:
                            self.r20()
                        elif j == 21:
                            self.r21()
                        elif j == 22:
                            self.r22()
                        elif j == 23:
                            self.r23()
                        elif j == 24:
                            self.r24(sigs)
                        elif j == 25:
                            self.r25(sigs)
                        elif j == 26:
                            self.r26()
                        elif j == 27:
                            self.r27()
                        elif j == 28:
                            self.r28()
                        elif j == 29:
                            self.r29()
                        elif j == 30:
                            self.r30()
                        elif j == 31:
                            self.r31()
                        elif j == 32:
                            self.r32()
                        elif j == 33:
                            self.r33()
                        elif j == 34:
                            self.r34()
                        elif j == 35:
                            self.r35()
                        elif j == 36:
                            self.r36()
                        elif j == 37:
                            self.r37()
                        elif j == 38:
                            self.r38()
                        elif j == 39:
                            self.r39()
                        elif j == 40:
                            self.r40()
                        elif j == 41:
                            self.r41(sigs)
                        elif j == 42:
                            self.r42()

                        elif j == 43:
                            self.r43()
                        elif j == 44:
                            self.r44()
                        elif j == 45:
                            self.r45()
                        elif j == 46:
                            self.r46()
                        elif j == 47:
                            self.r47()
                        elif j == 50:
                            self.r50(sigs)
                        elif j == 51:
                            self.r51()
                        elif j == 52:
                            self.r52()
                        elif j == 53:
                            self.r53()
                        elif j == 54:
                            self.r54()
                        elif j == 55:
                            self.r55()
                        elif j == 56:
                            self.r56()
                        elif j == 57:
                            self.r57()
                        elif j == 58:
                            self.r58()
                        elif j == 59:
                            self.r59()
                        elif j == 61:
                            self.r61()
                        elif j == 67:
                            self.r67()
                        elif j in [68, 69]:
                            self.r68_69(sigs)
                        elif j in [70, 71]:
                            self.r70_71(sigs)
                        elif j == 72:
                            self.r72(sigs)
                        elif j == 79:
                            self.r79(sigs)
                        elif j == 80:
                            self.r80()
                        elif j == 81:
                            self.r81()

                        elif j == 82:
                            self.r82()
                        elif j == 83:
                            self.r83()
                        elif j == 84:
                            self.r84()
                        elif j == 85:
                            self.r85()

                        # elif j == 82:
                        #     self.r82()
                        # elif j == 83:
                        #     self.r83(sigs)
                        elif j == 86:
                            self.r86(sigs)
                        elif j == 89:
                            self.r89()
                        elif j == 90:
                            self.r90()
                        elif j == 91:
                            self.r91()
                        elif j == 92:
                            self.r92()
                        elif j == 94:
                            self.r94()
                        elif j == 95:
                            self.r95()

                        elif j == 96:
                            self.r96()


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
                        print(key, token[idx], '不在字典中')
                        idx = self.error_process(State, sigs, token, idx)
                        fg = False
                        # break
                elif value == 'acc':
                    print('接受成功')
                    info = ''
                    fg = True
                    break
                elif str(value).isdigit():
                    info = token[idx] + '异常！'
                    infos.append(info)
                    print('异常！')
                else:
                    info = token[idx][0] + '附近出现语法错误！' + ':: row: '+str(token[idx][2]) + '  col: '+ str(token[idx][3])
                    infos.append(info)
                    print(key, token[idx], '不在字典中')
                    idx = self.error_process(State, sigs, token, idx)
                    fg = False
                    # break
            else:
                info = token[idx][0] + '附近出现语法错误！' + ':: row: '+str(token[idx][2]) + '  col: '+ str(token[idx][3])
                infos.append(info)
                print(key, token[idx], '不在字典中')
                idx = self.error_process(State, sigs, token, idx)
                fg = False
                # break
        # print(current_state)
        return fg, infos

    def entry(self, s):
        token, errors = parseString(s)
        if errors:
            print('词法分析不通过！')
            return
        else:
            return self.doentry(token)

    def error_process(self, State, sigs, token, idx):
        '''
        采用恐慌模式
        进行错误处理
        :return:
        '''
        self.fg = False
        while State:
            fg, v = isexist_goto(all_sheet, State[-1])
            if fg:
                fw = getFollowSet(follow, v)[0]
                print(fw)
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

    def modify_jump(self, bond):
        '''
        大于 bond的j语句末尾元素减去1
        :param bond:
        :return:
        '''
        for code in self.codes:
            if code[0][0] == 'j' and int(code[-1]) > bond:
                code[-1] = int(code[-1]) - 1


    def optimize_code(self):
        '''
        做一些基础的优化
        :return:
        '''
        del_idx = []
        for i in range(1, len(self.codes)):

            if self.codes[i-1][-1] == self.codes[i][1] and self.codes[i][0] == '=' and self.codes[i][1] != 'return_v':
                self.codes[i-1][-1] = self.codes[i][-1]
                # 删除一条
                self.modify_jump(i)
                del_idx.append(i)
        for i, idx in enumerate(del_idx):
            del self.codes[idx - i]