'''
四元式代码 对应汇编代码
'''

es_idx = -2

def transfer(arg1, arg2, arg3):
    '''
    将 A B result 转换成 ds:[_A]  ds:[_B]， es:{_result]
    :param arg1:
    :param arg2:
    :param arg3:
    :return:
    '''

    if str(arg1).isidentifier():
        arg1 = 'DS:[_{}]'.format(arg1)
    if str(arg2).isidentifier():
        arg2 = 'DS:[_{}]'.format(arg2)
    if str(arg3).isidentifier():
        arg3 = 'DS:[_{}]'.format(arg3)
    return arg1, arg2, arg3

def gen_assem_code(code, idx):
    '''
    生成一条汇编代码
    :param code: 一个四元式
    :return:
    '''
    if code[0] == '+':
        # 加法
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tADD AX,{}\n\tMOV {},AX;\n'.format(arg1, arg2, res)

    elif code[0] == '-':
        # 减法
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tSUB AX,{}\n\tMOV {},AX;\n'.format(arg1, arg2, res)

    elif code[0] == '*':
        # 乘法
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tMOV BX,{}\n\tMUL BX\n\tMOV {},AX\n'.format(arg1, arg2, res)

    elif code[0] == '/':
        # 除法
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tMOV DX,0\n\tMOV BX,{}\n\tDIV BX\n\tMOV {},AX\n'.format(arg1, arg2, res)

    elif code[0] == '%':
        # 求余数
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tMOV DX,0\n\tMOV BX,{}\n\tDIV BX\n\tMOV {},DX\n'.format(arg1, arg2, res)

    elif code[0] == '<':
        # 小于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJB _LT\n\tMOV DX,0\n\t_LT:MOV {},DX\n'.format(arg1, arg2, res)

    elif code[0] == '>=':
        # 不小于把 res 置为 0， 否则为 1
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJNB _GE\n\tMOV DX,0\n\t_GE:MOV {},DX\n'.format(arg1, arg2, res)

    elif code[0] == '>':
        # 大于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJA _GT\n\tMOV DX,0\n\t_GT:MOV {},DX\n'.format(arg1, arg2, res)

    elif code[0] == '<=':
        # 不大于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJNA _LE\n\tMOV DX,0\n\t_LE:MOV {},DX\n'.format(arg1, arg2, res)

    elif code[0] == '==':
        # 等于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJE _EQ\n\tMOV DX,0\n\t_EQ:MOV {},DX\n'.format(arg1, arg2, res)

    elif code[0] == '!=':
        # 不等于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,{}\n\tJNE _NE\n\tMOV DX,0\n\t_NE:MOV {},DX\n'.format(arg1, arg2, res)

    elif code[0] == '&&':
        # 等于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV DX,0\n\tMOV AX,{}\n\tCMP AX,0\n\tJE _AND\n\tMOV AX,{}\n\tCMP AX,0\n\tJE _' \
                     'AND\n\tMOV DX,1\n\t_AND:MOV {},DX\n'.format(arg1, arg2, res)

    elif code[0] == 'jnz':
        # 等于把 res 置为 1， 否则为 0
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        res = '_'+res
        assem_code = '\tMOV AX,{}\n\tCMP AX,0\n\tJE _EZ\n\tJMP far ptr {}\n\t_EZ:NOP\n'.format(arg1, res)

    elif code[0] == 'para':

        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV AX,{}\n\tPUSH AX\n'.format(arg1)

    elif code[0] == 'call':
        global es_idx
        arg1, arg2, res = code[1], code[2], code[3]
        arg1 = '_' + arg1
        es_idx += 2
        assem_code = '\tCALL {}\n\tMOV ES:[{}],AX\n'.format(arg1, es_idx)


    elif code[0] == 'ret':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        if arg1 != '':
            assem_code = '\tMOV AX,{}\n\tMOV SP,BP\n\tPOP BP\n\tRET\n'.format(arg1)
        else:
            assem_code = '\tMOV SP,BP\n\tPOP BP\n\tRET\n'.format(arg1)

    elif code[0] == '||':
        arg1, arg2, T = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,0\n\tJNE _OR\n\tMOV AX,{}\n\tCMP AX,0\n\t' \
                     'JNE _OR\n\tMOV DX,0\n\t_OR:MOV {},DX\n'.format(arg1, arg2, T)
    elif code[0] == '!':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        assem_code = '\tMOV DX,1\n\tMOV AX,{}\n\tCMP AX,0\n\tJE _NOT\n\tMOV DX,0\n\t_NOT:MOV {},DX\n'.format(arg1, res)

    elif code[0] == 'j':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        res = '_' + str(res)
        assem_code = '\tJMP far ptr {}\n'.format(res)

    elif code[0] == 'jz':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        res = '_' + str(res)
        assem_code = '\tMOV AX,{}\n\tCMP AX,0\n\tJNE _NE\n\tJMP far ptr P\n\t_NE:NOP\n'.format(arg1, res)

    elif code[0] == 'j>':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        res = '_' + str(res)
        assem_code = '\tMOV AX,{}\n\tCMP AX,{}\n\tJG {}\n'.format(arg1, arg2, res)

    elif code[0] == 'j>=':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        res = '_' + str(res)
        assem_code = '\tMOV AX,{}\n\tCMP AX,{}\n\tJGE {}\n'.format(arg1, arg2, res)

    elif code[0] == 'j==':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        res = '_' + str(res)
        assem_code = '\tMOV AX,{}\n\tCMP AX,{}\n\tJE {}\n'.format(arg1, arg2, res)

    elif code[0] == 'j<':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        res = '_' + str(res)
        assem_code = '\tMOV AX,{}\n\tCMP AX,{}\n\tJL {}\n'.format(arg1, arg2, res)

    elif code[0] == 'j<=':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        res = '_' + str(res)
        assem_code = '\tMOV AX,{}\n\tCMP AX,{}\n\tJLE {}\n'.format(arg1, arg2, res)

    elif code[0] == '=':
        arg1, arg2, res = transfer(code[1], code[2], code[3])
        if code[1] == 'return_v':
            arg1 = 'ES:[{}]'.format(es_idx)

        # res = '_' + str(res)
        assem_code = '\tMOV AX,{}\n\tMOV {}, AX\n'.format(arg1, res)

    elif code[0] == 'sys':

        assem_code = '\tQUIT: MOV AH, 4CH\n\tint 21h\n'

    elif str(code[0]).isidentifier() and code[0] != 'main':
        idx = code[0]
        assem_code = '\tPUSH BP\n\tMOV BP,SP\n\tSUB SP\n'

    else:
        assem_code = ''
    if assem_code != '':
        assem_code = '_'+str(idx)+':\n'+assem_code
    return assem_code

def gen_assemcodes(codes):
    '''

    :param codes:  list
    :return: list
    '''
    global es_idx
    es_idx = -2
    assem_codes = []
    for i, code in enumerate(codes):
        assem_code = gen_assem_code(code, i+1)
        if code[0] == 'para' and codes[i-1][0] == 'call':
            assem_code = assem_code.replace('DS:[_{}]'.format(code[1]), 'ES:[{}]'.format(es_idx))
        assem_codes.append(assem_code)

    return assem_codes
