'''
作者： yan
创建时间： 2020/5/13
侵权必究
'''

def conform(elem, e, left, right):
    if 'left' not in e:
        return False
    if left != e['left']:
        return False
    if 'right' not in e:
        return  False
    if right != e['right']:
        return False
    if elem == e['sign'] or elem in e['affi_sign']:
        return True
    else:
        return False


def isleaf(e):
    '''
    判断节点是不是叶子节点
    :param e:
    :return:
    '''
    if 'son' in e or 'left' in e or 'right' in e:
        return False
    else:
        return True



def is_in_DAG(DAG, elem, son = None, left = None, right = None):
    '''
    判断DAG是否已经存在结点elem
    :param DAG:  list
    :param elem:  str
    :return:  bool
    '''

    if not son and not left and not right:
        for e in DAG:
            if elem == e['sign'] or elem in e['affi_sign']:
                return True
    elif son:
        for e in DAG:
            if 'son' in e:
                if (elem == e['sign'] or elem in e['affi_sign']) and son in e['son']:
                    return True
    else:
        for e in DAG:
            lf = index_of_DAG(DAG, left)
            rg = index_of_DAG(DAG, right)
            if conform(elem, e, lf, rg):
                return True
    return False

def append_affi_sign(DAG, sign, affi_sign,left = None, right = None):
    # 在DAG中寻找到 标记为sign的节点
    print('APPEND',sign, affi_sign)
    if left and right:
        lr = index_of_DAG(DAG, left)
        rg = index_of_DAG(DAG, right)
        for elem in DAG:
            if elem['sign'] == sign or sign in elem['affi_sign']:
                if 'left' in elem and lr == elem['left'] and \
                    'right' in elem and rg == elem['right']:
                    elem['affi_sign'].append(affi_sign)
                    return
    else:
        for elem in DAG:
            if elem['sign'] == sign or sign in elem['affi_sign']:
                elem['affi_sign'].append(affi_sign)
                return
    print('未找到标记为 {} 的DAG节点'.format(sign))

def index_of_DAG(DAG, x, left = None, right = None):
    '''
    返回附属标记含x的元素下标
    :param DAG:
    :param x:
    :return:
    '''
    if x not in ['+', '-', '/', '*']:
        for i, e in enumerate(DAG):
            if x in e['affi_sign'] or x == e['sign']:
                return i
    return None
    print('未找到包含附属标记为{} 的节点'.format(x))

def delete(DAG, sign):
    '''
    删除已有的标记 sign
    :param DAG:
    :param sign:
    :return:
    '''

    for e in DAG:
        if sign in e['affi_sign']:
            e['affi_sign'].remove(sign)

def link(DAG, father, son = None, left = None, right = None):
    '''
    连接附属标记含x 与附属标记含y的相连
    :param DAG:
    :param x:
    :param y:
    :return:
    '''
    if son:
        e2 = index_of_DAG(DAG, son)

        if 'son' not in  father:
            father['son'] = []
        father['son'].append(e2)
        if 'father' not in DAG[e2]:
            DAG[e2]['father'] = []
        # DAG[e2]['father'].append(e1)
    else:
        lf = index_of_DAG(DAG, left)
        rg = index_of_DAG(DAG, right)


        father['left'] = lf
        father['right'] = rg
        # if 'father' not in DAG[lf]:
        #     DAG[lf]['father'] = []
        # # DAG[lf]['father'].append()
        # if 'father' not in DAG[rg]:
        #     DAG[rg]['father'] = []
        # DAG[rg]['father'].append(fa)

def create_DAG(codes: list):
    '''

    :param codes:  中间代码（4元式）
    :return:  DAG
    '''

    DAG = []    #初始为空

    for code in codes:
        #此处的code是tuple(str,str,str,str)
        if code[0] == '=':
            # 若是 x = y, 其中间代码形式为: ('=', 'y', '', 'x')
            if is_in_DAG(DAG, code[3]):
                # 删除之前的code[3]
                delete(DAG, code[3])
                pass
            if not is_in_DAG(DAG, code[1]):

                DAG.append({'sign': code[1], 'affi_sign': [code[3]]})
            else:
                # 将x加入y节点的附属标记
                append_affi_sign(DAG, code[1], code[3])

        elif code[0] == '@':
            # 若是 x = op y, 四元式是：('op', 'y', '', 't') ('=', 't', '' ,'x')
            # 查找是否存在结点 y，若不存在，则新建结点 y
            if is_in_DAG(DAG, code[3]):
                # 删除之前的code[3]
                delete(DAG, code[3])
                pass
            if not is_in_DAG(DAG, code[1]):

                DAG.append({'sign': code[1], 'affi_sign': []})
            # 再查找是否 存在一个结点 op，其子结点为 y
            if not is_in_DAG(DAG, code[0], son = code[1]):
                # 连接两节点
                father = {'sign': code[0], 'affi_sign': [code[3]]}
                link(DAG, father, son = code[1])
                DAG.append(father)
        elif code[1] != '' and code[2] != '':
            # 若是 x = y op z, 四元式是：('op', 'y', 'z', 't') ('=', 't', '' ,'x')
            if is_in_DAG(DAG, code[3]):
                # 删除之前的code[3]
                delete(DAG, code[3])
                pass
            if not is_in_DAG(DAG, code[1]):
                DAG.append({'sign': code[1], 'affi_sign': []})
            if not is_in_DAG(DAG, code[2]):
                DAG.append({'sign': code[2], 'affi_sign': []})
            if not is_in_DAG(DAG, code[0], left = code[1], right = code[2]):
                print(code, 'YYYY')
                father = {'sign': code[0], 'affi_sign': [code[3]]}

                link(DAG, father, left = code[1], right = code[2])
                DAG.append(father)
            else:
                append_affi_sign(DAG, code[0], code[3], code[1], code[2])

    return DAG


def optimize(DAG):
    '''
    优化DAG
    :param DAG:
    :return:
    '''
    # 合并已知量
    for e in DAG:
        if e['affi_sign']:
            e['affi_sign'] = e['affi_sign'][0]

    code = []
    # 生成新代码
    for e in DAG:
        if 'son' in e:
            son = DAG[e['son']]
            if not son['affi_sgin'] or isleaf(son) :
                code.append((e['sign'], son['conform'], '', e['affi_sign'] ))
            else:
                code.append((e['sign'], son['affi_sign'], '', e['affi_sign'] ))
        elif 'left' in e and 'right' in e:
            left = DAG[e['left']]
            right = DAG[e['right']]
            if not left['affi_sign'] or isleaf(left):
                arg1 = left['sign']
            else:
                arg1 = left['affi_sign']

            if not right['affi_sign'] or isleaf(right):
                arg2 = right['sign']
            else:
                arg2 = right['affi_sign']
            code.append((e['sign'], arg1, arg2, e['affi_sign']))

    return code
