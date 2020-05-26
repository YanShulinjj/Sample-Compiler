from graphviz import Digraph

def draw(codes):
    '''

    :param codes:
    :return:
    '''
    dot = Digraph(comment='The Round Table', filename='visible', format='png', strict=False)
    idx = 1
    for code in codes:
        s = code['sign'] + '|' + ''.join(code['affi_sign'])
        dot.node(str(idx), s)
        idx += 1
    for i, code in enumerate(codes):
        if 'son' in code:
            dot.edge(str(i+1), str(code['son'][0] + 1))
        if 'left' in code:
            dot.edge(str(i+1), str(code['left'] + 1))
        if 'right' in code:
            dot.edge(str(i+1), str(code['right'] + 1))
    print('yyyyyyy')
    dot.render()
