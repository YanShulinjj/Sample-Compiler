#
# @作者 ysl
# 使用文法构建项目集，耗时久
#
from LR1 import createItems, createLR_sheeet

all_g =[
    ('S_', ['Entry']),
    ##########变量声明部分###########
    ('VDCL', ['VDCL', ',', 'id']),                      #1
    ('VDCL', ['VDCL', ',', 'id', '=', 'AE']),           #2
    ('VDCL', ['none']),                                 #3
    ('VDCL', ['Type', 'id']),                           #4
    ('VDCL', ['Type', 'id', '=', 'AE']),                #5

    ##########常量声明部分###########
    ('DCL', ['Head', 'TD']),                            #6
    ('DCL', ['none']),                                  #7
    ('Head', ['const', 'Type']),                        #8
    ('Type', ['int']),                                  #9
    ('Type', ['float']),                                #10
    ('Type', ['char']),                                 #11
    ('TD', ['id', '=', 'c', ',', 'TD']),                #12
    ('TD', ['id', '=', 'c']),                           #13

    ##########算术表达式声明部分###########
    ('AE', ['AE', '+', 'IT']), #{AE.v =IT.v + AE.v}     #14
    ('AE', ['AE', '-', 'IT']), #{AE.v = IT.v - AE.v}    #15
    ('AE', ['IT']), # {AE.v = IT.v}                     #16
    ('IT', ['IT', '*', 'F']), #{ IT.v = F.v * IT.v}     #17
    ('IT', ['IT', '/', 'F']), #{ IT.v = F.v / IT.v}     #18
    ('IT', ['IT', '%', 'F']), #{ IT.v = F.v % IT.v}     #19
    ('IT', ['F']), #{IT.v = F.v}                        #20
    ('F', ['P']),  #{F.v = P.v}                         #21
    ('F', ['-', 'P']),  #{ F.v = - P.v}                 #22
    ('P', ['(', 'AE', ')']), #{P.v = AE.v}              #23
    ('P', ['id']),    #{P.v = entry(id).v}              #24
    ('P', ['c']),                                       #25

    #########布尔表达式声明部分###########
    ('BE', ['BE_or', 'BT']),                            #26
    ('BE_or', ['BE', '||']),                            #27
    ('BE', ['BT']), #3                                  #28
    ('BT', ['BT_and', 'BF']), #4                        #29
    ('BT_and', ['BT', '&&']), #5                        #30
    ('BT', ['BF']), #6                                  #31
    ('BF', ['!', 'BF']), #7                             #32
    ('BF', ['(', 'BE', ')']), #8                        #33
    ('BF', ['AH', 'AE']), #9                            #34
    ('BF', ['id', 'rop', 'id']),                        #35
    ('BF', ['id']), #10                                 #36

    # if语句
    ('S_if', ['C', 'S']), #1  S.CHAIN = merge(C.CHAIN, Ss.CHAIN)                                                                    #37
    ('C', ['if', 'BE']), #2  backpath(BE.TC, NXQ); C.CHAIN = BE.FC                                                              #38
    ('S_if', ['T', 'S']), #3 S.CHAIN = merge(T.CHAIN, S.CHAIN)                                                                     #39
    ('T', ['C', 'S', 'else']), #4 q = NXQ; gencode(j, , , 0); backpath(C.CHAIN, NXQ); T.CHAIN = merge(S.CHAIN, q);              #40
    
	('S', ['id', '=', 'AE', ';']),                                                                                              #41
    ('S', ['VDCL', ';']),  # 语句包含变量定义                                                                                   #42
    ('S', ['DCL', ';']),  # 语句包含常量定义                                                                                    #43
    ('S', ['none']),                                                                                                            #44
    # do - while语句
    ('D', ['do']),                                       #45
    ('U', ['D', 'S', 'while']),                          #46
    ('S_dw', ['U', '(', 'BE', ')', ';']),                #47


    #赋值表达式
    ('E', ['AE']),                                       #48
    ('E', ['BE']),                                       #49
    ('E', ['id', '=', 'AE']),                            #50

    # for 语句
    ('FF', ['for', '(', 'E', ';']),                      #51
    ('A', ['FF', 'E', ';']),                             #52
    ('B', ['A', 'E', ')']),                              #53
    ('S_for', ['B', 'S']), # 表示for语句                     #54

    # 复合语句
    ('S', ['{', 'Ss', '}']),                             #55
    ('Ss', ['S']),                                       #56
    ('Ss', ['Ss', 'S']),                                 #57

    # while 语句
    ('SSw', ['D_w', 'BE', ')']),                   #58
    ('S', ['S_w']),  										#59
	
    # return 语句
    ('S_r', ['return', ';']),                               #60
    ('S_r', ['return', 'AE', ';']),                         #61
    ('S', ['S_r']),                                         #62
    ('S', ['S_b']),                                         #63
    ('S', ['S_c']),                                         #64

    # break 语句
    ('S_b', ['break', ';']),                                #65
    # continue 语句
    ('S_c', ['continue', ';']),                             #66


    # 函数定义
	('FD', ['FDB', 'FB']),				                    #67
	('FDB', ['Type',  'id', '(', 'FDP', ')']),             #68
	('FDB', ['void',  'id', '(', 'FDP', ')']),				 #69
	# 函数定义语句
    ('FDS', ['Type',  'id', '(', 'FDP', ')', ';']),        #70
	('FDS', ['void',  'id', '(', 'FDP', ')', ';']),        #71
 
    ('FDP', ['Type', 'id']),                                #72
    ('FDP', ['FDP', ',', 'FDP']),                           #73
    ('FDP', ['none']),                                      #74
    ('FB', ['{', 'Ss', '}']),                               #75
	#函数定义列表	
    ('FDD', ['none']),                                      #76
    ('FDD', ['FD', 'FDD']),                                 #77
   
	('S', ['FDS']),                                         #78


    ('AH', ['AE', 'rop']),                                  #79
    #主函数
    ('M', ['Ss', 'main']),  								#80
    ('Entry', ['Main', 'FDD']), 		#81
	
	#添加	
	('S', ['S_if']),										#82
	('S', ['S_for']),										#83
	('S', ['S_dw']),										#84
    ('S_w', ['SSw', 'S']),                                 #85
	

    # 函数调用
    ('FC', ['id', '(', 'FCP', ')']),						#86
    ('FCP', ['none']),										#87
    ('FCP', ['FCFS']),										#88
    ('FCFS', ['FCF']),										#89
    ('FCFS', ['FCFS', ',', 'FCF']),							#90
    ('FCF', ['AE']),										#91
    ('FCF', ['FC']),										#92
    ('S', ['FC', ';']),										#93

    ('Main', ['M', '(', ')', '{', 'Ss', '}']),				#94
	('P', ['FC']),											#95
	('D_w',['while', '('])									#96

    ]


items = createItems(all_g)
print('创建items成功')
sheet = createLR_sheeet(items, all_g)

import  pickle
##
pickle.dump(items, open('data/all_LR1_items4.pkl', 'wb'))
pickle.dump((all_g, sheet), open('data/all_sheetLR14.pkl', 'wb'))

print('yes')