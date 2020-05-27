# -*- coding:utf-8 -*-
# @Time   : 2020-05-23 11:43
# @Author : Rage
# @File   : operator_first.py



class Oper_First:
    def __init__(self, input_str="", grammer=""):
        self.scanf_process(input_str, grammer)

    def scanf_process(self, input_str="", grammer=""):
        # 测试样例文法
        if grammer:
            grammer = grammer.split('\n')
            # print(grammer)
            for index, g in enumerate(grammer):
                grammer[index] = g.split("->")
            if grammer[0][1][0] != '#':
                t = ['S']
                t.append('#'+str(grammer[0][0][0])+'#')

                grammer.insert(0, t)
            # print(grammer)
            self.grammar = grammer
        else:
            self.grammar = [["A", "#E#"],
                            ["E", "E+T"],
                            ["E", "T"],
                            ["T", "T*F"],
                            ["T", "F"],
                            ["F", "P|F"],
                            ["F", "P"],
                            ["P", "(E)"],
                            ["P", "i"]]
        if input_str:
            self.input_str = input_str+"#"
        else:
            self.input_str = "i+i#"

    #返回所有的左边的非终结符
    def get_state(self):
        result = []
        for i in self.grammar:
            if i[0] not in result:
                result.append(i[0])
        return result

    def get_firstvt(self):
        state = self.get_state()
        # print(state)
        # 初始化FIRST表
        firstvt_table = {i:[] for i in state}
        # print(firstvt_table)
        for i in state:
            result = self.get_first_recursion(i)
            firstvt_table[i].extend(result)
        # print(firstvt_table)
        return firstvt_table

    # First集合
    # P->a...或者P->Qa...
    def get_first_recursion(self, target):
        result = []
        for g in self.grammar:
            # 当前要推导的符号和式子相同
            if g[0] == target:
                # 判断是否为终结符号
                # P->a...
                if g[1][0].islower() or not g[1][0].isalpha():
                    for i in g[1][0]:
                        if i not in result:
                            result.extend(i)
                else:
                    # P->Qa...
                    # 若为非终结符号,进行递归查询
                    # 若非终结符号为自身，则不进行递归查询
                    if target != g[1][0]:
                        temp = self.get_first_recursion(g[1][0])
                        for i in temp:
                            if i not in result:
                                result.extend(i)
                    # 若后续有终结符号，则也加入
                    if len(g[1]) >= 2:
                        if g[1][1].islower() or g[1][1].isalpha() == False:
                            for i in g[1][1]:
                                if i not in result:
                                    result.extend(i)
        return result

    def get_lastvt(self):
        # 获取FIRST中的状态集合
        state = self.get_state()
        # 初始化FIRST表
        lastvt_table = {i: [] for i in state}
        # print(lastvt_table)
        for i in state:
            result = self.get_last_recursion(i)
            lastvt_table[i].extend(result)
        # print(lastvt_table)
        return lastvt_table

    # P->...a或者P->...aQ
    def get_last_recursion(self, target):
        result = []
        for g in self.grammar:
            # 当前要推导的符号和式子相同
            if g[0] == target:
                # 判断是否为终结符号
                # P->...a
                if g[1][-1].islower() or g[1][-1].isalpha() == False:
                    # print(g[1][-1])
                    for i in g[1][-1]:
                        if i not in result:
                            result.extend(i)
                else:
                    # P->...aQ
                    # 若为非终结符号
                    # 若非终结符号为自身，则不进行递归查询
                    if target != g[1][-1]:
                        temp = self.get_last_recursion(g[1][-1])
                        for i in temp:
                            if i not in result:
                                result.extend(i)
                    # 若后续有终结符号，则也加入
                    if len(g[1]) >= 2:
                        # print(g[1][-2])
                        if g[1][-2].islower() or g[1][-2].isalpha() == False:
                            for i in g[1][-2]:
                                if i not in result:
                                    result.extend(i)
        return result

    # 得到firstvt、lastvt所有的终极符
    def get_priority_state(self, firstvt, lastvt):
        state = []
        for i in firstvt.values():
            state += i
        for i in lastvt.values():
            state += i
        state = list(set(state))
        # print(state)
        return state

    # 确定符号的位置
    def get_x_y(self, c_x, c_y, state):
        # 得到行坐标
        x, y = -1, -1
        for i in range(len(state)):
            if c_x == state[i]:
                x = i
        for i in range(len(state)):
            if c_y == state[i]:
                y = i
        return x, y

    # 得到优先关系表
    def get_priority_table(self, firstvt, lastvt):
        # 标记该文法是否符合算法优先文法任一终结符号之间至多只有一种关系
        isflag = True
        state = self.get_priority_state(firstvt, lastvt)
        # 初始化预测分析表
        table = [["0" for col in range(len(state))] for row in range(len(state))]

        # 寻找=关系
        # P->...ab...或者P->...aQb...
        for g in self.grammar:
            # 得到该文法语句长度
            length = len(g[1])
            for i in range(len(g[1])):
                if i + 2 > length - 1:
                    break
                if (g[1][i] == g[1][i + 2] and g[1][i] == "#") or (g[1][i] == "(" and g[1][i + 2] == ")"):
                    x, y = self.get_x_y(g[1][i], g[1][i + 2], state)
                    if table[x][y] != "0":
                        isflag = False
                    table[x][y] = "="
        # 寻找<关系
        # P->...aR...而R->b...或R->Qb...
        for g in self.grammar:
            # 得到该文法的长度
            length = len(g[1])
            for i in range(len(g[1])):
                # 若出现数字越界，跳出
                if i + 1 > length - 1:
                    break
                # 如果该符号是终结符号且下一位是非终结符号(右左)
                if g[1][i] in state and g[1][i + 1] not in state:
                    # 取出FIRSTVT的元素，对关系表进行修改
                    temp = firstvt[g[1][i + 1]]
                    for t in temp:
                        x, y = self.get_x_y(t, g[1][i], state)
                        if table[y][x] != "0":
                            isflag = False
                        table[y][x] = "<"
        # 寻找>关系
        # P->...Rb...而R->...a或R->...aQ
        for g in self.grammar:
            # 得到该文法的长度
            length = len(g[1])
            for i in range(len(g[1])):
                # 若出现数字越界，跳出
                if i + 1 > length - 1:
                    break
                # 如果该符号是终结符号且下一位是非终结符号
                if g[1][i] not in state and g[1][i + 1] in state:

                    # 取出LASTVT的元素，对关系表进行修改
                    temp = lastvt[g[1][i]]
                    for t in temp:
                        x, y = self.get_x_y(t, g[1][i + 1], state)
                        if table[x][y] != "0":
                            isflag = False
                        table[x][y] = ">"

        return table, state, isflag

    def statute(self, input, symbol):
        # 用来记录标志位规约情况

        for g in self.grammar:
            #判断是否在文法中
            if len(g[1]) == len(input) and symbol in g[1]:
                # 用来进行符号规约
                count = 0
                for x in range(len(g[1])):
                    if g[1][x] == symbol:
                        count += 1
                    elif str(g[1][x]).isupper() and str(input[x]).isupper():
                        count += 1
                # 查看是否能进行规约
                if count == len(g[1]):
                    return True
            elif symbol.isalpha():
                return True

        return False

    # 使用算符优先表分析输入串
    def analysis_operator(self, table, state):
        steps = []
        # 初始化分析栈
        ana_stack = []
        # 输入串栈
        input_stack = []
        # 对栈初始化，入栈
        ana_stack.append("#")
        input_stack.extend(list(reversed((self.input_str))))
        # print(input_stack)
        # 用来打印输出顺序
        show_count = 1
        steps.append(["步骤", "栈", "优先关系", "剩余输入串", "移进或规约"])
        # print("%s %8s %8s %8s %8s" % ("步骤", "栈", "优先关系", "剩余输入串", "移进或规约"))
        while True:
            step = []
            step.append(show_count)
            # print(show_count, end="")
            show_count += 1
            step.append("".join(ana_stack))
            # print("%12s" % ("".join(ana_stack)), end="")
            # 充当指针，指向当前栈内参与比较的元素，默认是栈顶
            indicator = len(ana_stack) - 1
            # 如果为非终结符号，向栈底读取字符，至到读取到非终结字符
            if ana_stack[indicator].isupper():
                for i in reversed(range(len(ana_stack) - 1)):
                    if ana_stack[i].isupper() == False:
                        indicator = i
                        break

            # print(ana_stack[indicator], input_stack[-1])
            # 对栈顶符号进行比较,
            if input_stack[-1].isalpha() and len(input_stack[-1]) == 1:
                # print(input_stack[-1])
                x, y = self.get_x_y(ana_stack[indicator], 'i', state)
            else:
                x, y = self.get_x_y(ana_stack[indicator], input_stack[-1], state)
            relationship = table[x][y]
            step.append(relationship)
            # print("%8s" % (relationship), end="")
            step.append("".join(list((reversed("".join(input_stack))))))
            # print("%14s" % "".join(list((reversed("".join(input_stack))))), end="")
            if (relationship == "<" or relationship == "=") and len(input_stack) != 1:
                step.append("移进")
                # print("%8s" % ("移进"))
            elif relationship == ">":
                step.append("归约")
                # print("%8s" % ("归约"))
            else:
                step.append("接受")
                # print("%8s" % ("接受"))
            # break
            steps.append(step)

            # 如果运算栈内只剩下非终结符号一个，并且输入栈无符号，则规约成功
            if len(ana_stack) == 2 and len(input_stack) == 1:
                break
        #
            # 执行移入操作
            if relationship == "<" or relationship == "=":
                ana_stack.append(input_stack.pop())
                # print(input_stack, ana_stack)
                # break
            # 执行规约操作
            elif relationship == ">":
                if indicator == len(ana_stack) - 1:
                    # 如果规约符号位于栈顶，则只将栈顶的非终结符号进行规约
                    if self.statute(ana_stack[indicator], ana_stack[indicator]):
                        ana_stack.pop()
                        ana_stack.append("N")
                else:
                    # 如果不位于栈顶，则将运算符左右两边的符号一起进行规约
                    if self.statute(ana_stack[indicator - 1:indicator + 2], ana_stack[indicator]):
                        ana_stack.pop()
                        ana_stack.pop()
                        ana_stack.pop()
                        ana_stack.append("N")


        return steps


    def judge_grammar(self):

        # 得到FIRSTVT集合
        firstvt = self.get_firstvt()
        # 得到LASTVT集合
        lastvt = self.get_lastvt()
        # 得到算符优先关系表
        table, state, isflag = self.get_priority_table(firstvt, lastvt)

        return isflag, firstvt, lastvt, table, state

    def run(self):


        print("进行构造的文法G[S]")
        for i in self.grammar:
            print("%s -> %s" % (i[0], i[1]))
        print("===============================================", end="\n")

        # 得到FIRSTVT集合
        firstvt = self.get_firstvt()
        print("该文法的FIRSTVT:")
        for key, value in firstvt.items():
            print("FIRSTVT(%s) = {%s}" % (key, str(value)[1:-1]))
        print("===============================================", end="\n")

        # 得到LASTVT集合
        lastvt = self.get_lastvt()
        print("该文法的LASTVT集合:")
        for key, value in lastvt.items():
            print("LASTVT(%s) = {%s}" % (key, str(value)[1:-1]))
        print("===============================================", end="\n\n")

        # 得到算符优先关系表
        table, state, isflag = self.get_priority_table(firstvt, lastvt)
        if not isflag:
            print("该文法是否属于算符优先文法:%s" % (str(isFlag)), end="\n\n")
        else:
            print("%27s" % ("算符优先关系表"))
            print("---------------------------------------------------------")
            for i in state:
                print("%8s" % i, end="")
            print()
            for i in range(len(table)):
                print("%s" % state[i], end="")
                print("%7s" % table[i][0], end="")
                for x in table[i][1:]:
                    print("%8s" % x, end="")
                print("")

            # 对文法进行算符分析
            print("接下来对输入串 %16s 进行规约" % (self.input_str))
            print("---------------------------------------------------")
            steps = self.analysis_operator(table, state)
            # print(steps)

        return steps
