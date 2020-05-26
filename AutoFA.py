# -*- coding:utf-8 -*-
# @Time   : 2020-05-13 21:20
# @Author : Rage
# @File   : AutoFA.py

import graphviz  as gv




class Node:
    def __init__(self, state, char):
        self._state_num = state
        self._path_char = char
        self._next_nodes = []


class NFA:
    def __init__(self, head, tail):
        self._head_node = head
        self._tail_node = tail


class Auto_FA:
    def __init__(self, exp=""):
        self._exp = exp
        self._state_num = -1
        self._nfa = []
        self._symbol = []


    def get_state_num(self):
        self._state_num += 1
        return self._state_num

    #创建nfa
    def creat_nfa(self, c):
        headnode = Node(self.get_state_num(), 'E')
        tailnode = Node(self.get_state_num(), c)
        headnode._next_nodes.append(tailnode)

        nfa = NFA(headnode, tailnode)
        return nfa

    #遇到'.'符号时表示链接
    def And(self, fna1, fna2):
        # newheadnode = Node(self.get_state_num(), 'E')
        # newtailnode = Node(self.get_state_num(), 'E')

        fna1._tail_node._next_nodes.append(fna2._head_node)
        # newheadnode._next_nodes.append(fna1._head_node)
        # fna2._tail_node._next_nodes.append(newtailnode)
        newheadnode = fna1._head_node
        newtailnode = fna2._tail_node

        nfa = NFA(newheadnode, newtailnode)
        return nfa

    #遇到‘|’符号时的操作
    def Or(self, nfa1, nfa2):
        old_headnode1 = nfa1._head_node
        old_tailnode1 = nfa1._tail_node
        old_headnode2 = nfa2._head_node
        old_tailnode2 = nfa2._tail_node

        newheadnode = Node(self.get_state_num(), 'E')
        newtailnode = Node(self.get_state_num(), 'E')
        newheadnode._next_nodes.append(old_headnode1)
        newheadnode._next_nodes.append(old_headnode2)
        old_tailnode1._next_nodes.append(newtailnode)
        old_tailnode2._next_nodes.append(newtailnode)

        nfa = NFA(newheadnode, newtailnode)
        return nfa

    #遇到*
    def closure(self, old_nfa):
        old_headnode = old_nfa._head_node
        old_tailnode = old_nfa._tail_node

        newheadnode = Node(self.get_state_num(), 'E')
        newtailnode = Node(self.get_state_num(), 'E')
        newheadnode._next_nodes.append(old_headnode)
        old_tailnode._next_nodes.append(newtailnode)
        newheadnode._next_nodes.append(newtailnode)
        old_tailnode._next_nodes.append(old_headnode)

        nfa = NFA(newheadnode, newtailnode)
        return nfa



    def exp_standard(self):
        exp = self._exp + '$'
        i = 0
        while True:
            if exp[i] not in ['(',')','*','|']:
                if exp[i+1] not in [')','*','|','$']:
                    # print(exp[:i+1])
                    # print(exp[i + 1:])
                    exp = exp[:i+1] + '.' + exp[i+1:]
                    i += 2
                else:
                    i += 1
            else:
                i += 1
            if exp[i] == '$':
                break
        print(exp)
        self._exp = exp

    def exp_to_nfa(self):
        i = 0
        for i in range(len(self._exp)):
            if self._exp[i] == "(":
                self._symbol.append('(')

            elif self._exp[i] == ')':

                while self._symbol and self._symbol[-1] != '(':
                    nfa2 = self._nfa.pop()
                    nfa1 = self._nfa.pop()

                    if self._symbol[-1] == '.':
                        new_nfa = self.And(nfa1, nfa2)
                        self._nfa.append(new_nfa)
                    else:
                        new_nfa = self.Or(nfa1, nfa2)
                        self._nfa.append(new_nfa)
                    self._symbol.pop()
                self._symbol.pop()
                #判断）右边是否为（或非运算符
                if i != len(self._exp) - 1 and self._exp[i + 1] != '|' \
                        and self._exp[i + 1] != ')' and self._exp[i+1] != '*':
                    self._symbol.append('.')

            elif self._exp[i] == "|":
                # if self._symbol:
                while self._symbol and self._symbol[-1] == '.':
                    nfa2 = self._nfa.pop()
                    nfa1 = self._nfa.pop()

                    new_nfa = self.And(nfa1, nfa2)
                    self._nfa.append(new_nfa)
                    self._symbol.pop()
                self._symbol.append('|')

            elif self._exp[i] == '*':
                nfa = self._nfa.pop()
                new_nfa = self.closure(nfa)
                self._nfa.append(new_nfa)

                if i != len(self._exp) -1 and self._exp[i+1] != '|' \
                        and self._exp[i+1] != ')':
                    self._symbol.append('.')

            else:
                new_nfa = self.creat_nfa(self._exp[i])
                if i != len(self._exp) - 1 and self._exp[i + 1] != '|' \
                        and self._exp[i + 1] != ')' and self._exp[i+1] != '*':
                    self._symbol.append('.')
                self._nfa.append(new_nfa)

        # print(self._symbol)
        # print(self._nfa)


        while self._symbol:
            c = self._symbol.pop()

            if c == '|':
                nfa2 = self._nfa.pop()
                nfa1 = self._nfa.pop()

                new_nfa = self.Or(nfa1, nfa2)
                self._nfa.append(new_nfa)
            else:
                nfa2 = self._nfa.pop()
                nfa1 = self._nfa.pop()

                new_nfa = self.And(nfa1, nfa2)
                self._nfa.append(new_nfa)

            if len(self._symbol) == 0:
                break
        # print(self._symbol)
        # print(self._nfa)


    def show(self):
        tt = []
        flag = set()
        head = self._nfa[0]._head_node
        tt.append(head)
        flag.add(head)

        while True:
            aa = tt.pop()

            print(aa._path_char, aa._state_num, end=' -> ')
            if aa._next_nodes:
                for j in aa._next_nodes:
                    if j not in flag:
                        tt.append(j)
                        flag.add(j)
                    print(j._path_char, j._state_num, end=' ')
            print()
            if not tt:
                break

    def get_path(self):
        c = set()
        for i in self._exp:
            if i not in ['(',')','|','*']:
                c.add(i)
        # print(type(c))
        return c



    def trans_dfa(self):
        self._end_state = self.get_state_num() - 1
        nodes_strat = self.states_strat()
        lable = self.get_path()

        self.succeed_path_nodes(nodes_strat, lable)


    def dfa_table(self, lable):
        for i in range(len(self._table['I'])):
            for j in self._table.keys():
                print(str(j) + " :[", end=" ")
                for x in self._table[j][i]:
                    print(x._path_char, x._state_num, end=" ")
                print("]")
            print()

        self._dfa = {}
        self._dfa = {'I':[i for i in range(len(self._table['I']))]}
        for i in lable:
            self._dfa.update({i:[]})

        for i in range(len(self._table['I'])):
            for j in lable:
                if self._table[j][i]:
                    self._dfa[j].append(self._table['I'].index(self._table[j][i]))
                else:
                    self._dfa[j].append('$')

        print("DFA : ", end="")
        print(self._dfa)

    ###求DFA初始I
    def states_strat(self):
        nodes_strat = set()
        head = self._nfa[0]._head_node
        nodes_strat.add(head)
        tt = []
        tt.append(head)
        while True:
            aa = tt.pop()

            if aa._next_nodes:
                for j in aa._next_nodes:
                    if j._path_char == 'E' and j not in nodes_strat:
                        nodes_strat.add(j)
                        tt.append(j)
                        # print(j._state_num, j._path_char)
            if not tt:
                break

        print(nodes_strat)
        return list(nodes_strat)

    def get_E_closure(self, current_nodes=""):

        nodes = set()
        for cn in current_nodes:
            # print(cn._path_char, cn._state_num)
            nodes.add(cn)
            tt = []
            tt.append(cn)
            while True:
                aa = tt.pop()

                if aa._next_nodes:
                    for j in aa._next_nodes:
                        if j._path_char == 'E' and j not in nodes:
                            tt.append(j)
                            nodes.add(j)
                            # print(j._path_char, j._state_num, end=' ')
                if not tt:
                    break

        return list(nodes)

    def succeed_path_nodes(self, nodes_start, lable):
        table = {}
        table.update({'I': []})
        I = []
        I.append(nodes_start)

        for i in lable:
            table.update({i: []})

        print(lable)

        while I:
            nodes = I.pop()
            table['I'].append(nodes)

            for j in lable:
                # print("\n====")
                cc = []
                for i in nodes:
                    for x in i._next_nodes:
                        if x._path_char == j and x not in cc:
                            cc.append(x)


                if cc:
                    cc = self.get_E_closure(cc)
                    table[j].append(cc)
                    if cc not in table['I'] and cc not in I:

                        I.append(cc)
                else:
                    table[j].append(cc)


        self._table = table

        # print(len(table['b']))
        # print(table)
        # for i in range(len(table['I'])):
        #     for j in table.keys():
        #         print(len(table[j][i]), end=" ")
        #     print()
        self.dfa_table(lable)

    def first_table(self):
        lable = self.get_path()

        tt1, tt2 = [], []

        for i in self._table['I']:
            flag = 0
            for j in i:
                if j._state_num == self._end_state:
                    tt2.append(i)
                    flag = 1
            if flag == 0:
                tt1.append(i)

        split = [tt1, tt2]
        for ind, t in enumerate(split):
            x = []
            for i in t:
                index = self._table['I'].index(i)
                x.append(index)
            split[ind] = x
        # print(split)

        table = {}
        for i in lable:
            table.update({i: []})

        for i in lable:
            for ind, j in enumerate(self._table[i]):
                if j:
                    index = self._table['I'].index(j)
                    for type, x in enumerate(split):
                        if index in x:
                            table[i].append(type)
                else:
                    table[i].append('$')

        # print(table, split)

        return table, split

    def update_table(self, table, split):
        lable = self.get_path()

        for i in lable:
            for ind, j in enumerate(self._table[i]):
                if j:
                    index = self._table['I'].index(j)
                    for type, x in enumerate(split):
                        if index in x:
                            table[i][ind] = type
        return table

    def get_dfa_end_state(self):
        dfa_end_state = []
        for index, i in enumerate(self._table['I']):
            for j in i:
                if j._state_num == self._end_state:
                    dfa_end_state.append(index)
        return dfa_end_state

    def simplify_dfa(self):
        table, splist = self.first_table()

        # print(table, splist)


        splist_ready = splist[::-1]
        lable = self.get_path()

        while splist_ready:
            aa = splist_ready.pop()
            if not aa:
                continue

            type = []
            for i in aa:
                t = []
                for l in lable:
                    t.append(table[l][i])
                # print(t)
                if t and t not in type:
                    type.append(t)

            # print(type)

            state = []
            for t in range(len(type)):
                state.append([])
            # print(state)
            for i in aa:
                t = []
                for l in lable:
                    t.append(table[l][i])
                # print(t)
                for index, tp in enumerate(type):
                    if t == tp:
                       state[index].append(i)
            # print(state)
            flag = 0
            if state:
                for ss in state:
                    if ss not in splist:
                        flag = 1
                        splist.append(ss)
                        splist_ready.append(ss)
            if aa in splist and flag == 1:
                splist.remove(aa)


            table = self.update_table(table,splist)
            # print(table)

            # print(splist_ready)
        # print(table)
        # print(splist)

        self._simplify_dfa = {'I': splist}

        for i in lable:
            self._simplify_dfa.update({i: []})

        if [] in splist:
            splist.remove([])
        # print(splist)
        for i in splist:
            for l in lable:
                a = self._dfa[l][i[0]]
                for index, states in enumerate(splist):
                    if a in states:
                        self._simplify_dfa[l].append(index)

                if a == '$':
                    self._simplify_dfa[l].append(a)


        print(self._simplify_dfa)
        self._splist = splist
        print(self._splist)


    def draw_png(self):
        self.draw_nfa()
        self.draw_dfa()
        self.draw_mfa()

    def draw_nfa(self):
        f = gv.Digraph('./image/nfa', format="png")
        f.attr(rankdir='LR')


        tt = []
        flag = set()
        head = self._nfa[0]._head_node
        f.attr('node', shape='circle')
        f.node(str(head._state_num))
        f.attr('node', shape='point')
        f.node('s')
        f.edge('s', str(head._state_num), label=head._path_char)
        nodes = [head._state_num]


        tt.append(head)
        flag.add(head)

        while True:
            aa = tt.pop()

            # print(aa._path_char, aa._state_num, end=' -> ')
            if aa._state_num == self._end_state:
                if aa._state_num not in nodes:
                    f.attr('node', shape='doublecircle')
                    f.node(str(aa._state_num))
                    nodes.append(aa._state_num)
            else:
                if aa._state_num not in nodes:
                    f.attr('node', shape='circle')
                    f.node(str(aa._state_num))
                    nodes.append(aa._state_num)

            if aa._next_nodes:
                for j in aa._next_nodes:
                    if j not in flag:
                        tt.append(j)
                        flag.add(j)

                    if j._state_num == self._end_state:
                        if j._state_num not in nodes:
                            f.attr('node', shape='doublecircle')
                            f.node(str(j._state_num))
                            nodes.append(j._state_num)
                    else:
                        if j._state_num not in nodes:
                            f.attr('node', shape='circle')
                            f.node(str(j._state_num))
                            nodes.append(j._state_num)
                    f.edge(str(aa._state_num), str(j._state_num), label=j._path_char)

            if not tt:
                break

        f.render()

    def draw_dfa(self):
        lable = self.get_path()
        end_states = self.get_dfa_end_state()
        # print(end_states)

        f = gv.Digraph('./image/dfa', format="png")
        f.attr(rankdir='LR', size='8,5')

        # f.attr('node', shape='doublecircle')

        for j in self._dfa['I']:

            if j in end_states:
                f.attr('node', shape='doublecircle')
                f.node(str(j))
            else:
                f.attr('node', shape='circle')
                f.node(str(j))

        f.attr('node', shape='point')
        f.node('s')
        f.edge('s', str(0), label='E')


        for j in self._dfa['I']:
            for l in lable:
                if self._dfa[l][j] != '$':
                    f.edge(str(j), str(self._dfa[l][j]), label=l)

        f.render()

    def draw_mfa(self):
        lable = self.get_path()
        end_states = self.get_dfa_end_state()
        # print(end_states)

        f = gv.Digraph('./image/mfa', format="png")
        f.attr(rankdir='LR', size='8,5')

        for i in self._simplify_dfa['I']:
            flag = 0
            count = 0
            for l in lable:
                ind = self._simplify_dfa['I'].index(i)
                if self._simplify_dfa[l][ind] == '$':
                    count += 1
                if count == len(lable):
                    flag = 1


            if flag == 0:
                if i[0] in end_states:
                    f.attr('node', shape='doublecircle')
                    f.node(str(i[0]))
                else:
                    f.attr('node', shape='circle')
                    f.node(str(i[0]))


        f.attr('node', shape='point')
        f.node('s')
        f.edge('s', str(0), label='E')

        # print(self._simplify_dfa)
        for index, i in enumerate(self._simplify_dfa['I']):
            j = i[0]
            for l in lable:
                if self._simplify_dfa[l][index] != '$':
                    ii = self._simplify_dfa[l][index]
                    f.edge(str(j), str(self._simplify_dfa['I'][ii][0]), label=l)

        f.render()


