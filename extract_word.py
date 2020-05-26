'''
词法分析脚本文件
'''

from pySwitch import switch

with open('configs/KeyWords.txt', 'r') as f:
    keywords = f.read().split('\n')




def isSpace(ch):
    '''
    :param ch: char, character
    :return: Bool, is or is not the SPACE character
    '''
    if ch in [',', ';', ' ', '\t', '\n']:
        return True
    else:
        return False


def isDelimiter(ch):
    '''
    :param ch: char, character:
    :return: Bool, is and is not the Delimiter character(分界符)
    '''

    if ch in ['(', ')', '[', ']', '{', '}', ',', ';', '<', '>', '#', '.']:
        return True
    else:
        return False


def isNotSpecial(ch):
    '''

    :param ch:
    :return:
    '''
    if str(ch).isidentifier() or isNum(ch) or isSpace(ch) or isOp(ch) or isDelimiter(ch):
        return True
    else:
        return False


def isNum(ch):
    '''

    :param ch:
    :return:
    '''
    if '0' <= ch <= '9':
        return True
    else:
        return False


def isOp(ch):
    '''
    '''
    if ch in ['+', '=', '<', '&', '^', '%', '~', '!', '>', '*', '/', '-', '|']:
        return True
    else:
        return False


def classfy(state, word):
    end_states_identfier = [14]
    end_states_const = [51, 3, 5, 7, 9, 12, 18, 20]
    end_states_op = [37, 38, 28, 29, 31, 32, 34, 36, 40, 41, 43, 44, 46, 47, 53, 54, 56, 57]
    end_states_bounder = [48]
    end_states_explain = [23, 26]

    if state in end_states_identfier:
        if word in keywords:
            return 'KEYWORD'
        else:
            return 'IDT'
    elif state in end_states_const:
        return 'CONST'
    elif state in end_states_op:
        return 'OP'
    elif state in end_states_bounder:
        return 'BOUND'
    elif state in end_states_explain:
        return 'EXPLAIN'


def parseString(st):
    '''
    :param st:  String, the origin code
    :return:  Tuple,( WordList, ErrorList)
    '''

    st = st+' '
    state = 0  # origin state
    words = []
    errors = []

    temp_word = ''

    idx = 0
    col = 0
    row = 0

    end_states_truncation = [3, 5, 7, 9, 12, 14, 23, 38,  29, 32, 36, 41, 44, 47, 51, 54, 57]  # end_state with * in plot
    end_states_joint = [18, 20, 26, 37, 28, 31, 34, 40, 28, 43, 46, 48, 49, 53, 56]  # end_state without  * in plot
    end_states_error = [50]

    while idx < len(st):
        while state not in end_states_truncation + end_states_joint + end_states_error:
            for case in switch(state):


                ch = str(st[idx])

                if case(0):
                    if ch == '0':
                        state = 1
                        temp_word += ch
                    elif isNum(ch):
                        state = 8
                        temp_word += ch
                    elif ch.isalpha() or ch == '_':
                        state = 13
                        temp_word += ch
                    elif ch == '\'':
                        state = 15
                        temp_word += ch
                    elif ch == '\"':
                        state = 19
                        temp_word += ch
                    elif ch == '/':
                        state = 21
                        temp_word += ch
                    elif ch == '+':
                        state = 27
                        temp_word += ch
                    elif ch == '-':
                        state = 30
                        temp_word += ch

                    elif ch == '*':
                        state = 33
                        temp_word += ch

                    elif ch in ['%',  '^', '~', '=', '!']:
                        state = 39
                        temp_word += ch

                    elif ch == '>':
                        state = 42
                        temp_word += ch

                    elif ch == '<':
                        state = 45
                        temp_word += ch

                    elif ch == '&':
                        state = 52
                        temp_word += ch

                    elif ch == '|':
                        state = 55
                        temp_word += ch
                    elif isDelimiter(ch):
                        state = 48
                        temp_word += ch

                    elif ch.isspace():
                        state = 49

                    else:
                        state = 50
                        temp_word += ch


                elif case(1):
                    if ch in ['x', 'X']:
                        state = 2
                        temp_word += ch

                    elif '1' <= ch <= '7':
                        state = 4
                        temp_word += ch

                    elif ch in ['b', 'B']:
                        state = 6
                        temp_word += ch


                    elif isNotSpecial(ch) and not isNum(ch):
                        state = 51

                    else:  # Unidentifiy
                        state = 50
                        temp_word += ch


                elif case(2):
                    if ch.isalpha() or isNum(ch):
                        state = 2
                        temp_word += ch

                    elif isNotSpecial(ch) and not ch.isalpha():  # 0x *** hexadecimal(十六进制数）
                        state = 3

                    else:
                        state = 50
                        temp_word += ch


                elif case(4):
                    if '0' <= ch <= '7':
                        state = 4
                        temp_word += ch

                    elif isNotSpecial(ch) and not ch.isalpha():  # 0**  octonary(八进制)
                        state = 5


                    else:
                        state = 50
                        temp_word += ch


                elif case(6):
                    if ch in ['0', '1']:
                        state = 6
                        temp_word += ch

                    elif isNotSpecial(ch) and not ch.isalpha() and ch not in ['3', '4', '5', '6', '7', '8', '9']:
                        state = 7

                    else:
                        state = 50
                        temp_word += ch


                elif case(8):
                    if isNum(ch):
                        state = 8
                        temp_word += ch

                    elif ch == '.':
                        state = 10
                        temp_word += ch

                    elif ch in ['e', 'E']:
                        state = 11
                        temp_word += ch

                    elif isNotSpecial(ch) and not ch.isalpha():  # decimalism(十进制)
                        state = 9

                    else:
                        state = 50
                        temp_word += ch


                elif case(10):
                    if isNum(ch):
                        state = 10
                        temp_word += ch

                    elif ch in ['e', 'E']:
                        state = 11
                        temp_word += ch

                    elif isNotSpecial(ch) and not ch.isalpha():
                        state = 12

                    else:
                        state = 50
                        temp_word += ch


                elif case(11):
                    if isNum(ch):
                        state = 11
                        temp_word += ch

                    elif isNotSpecial(ch) and not ch.isalpha():
                        state = 12

                    else:
                        state = 50
                        temp_word += ch


                elif case(13):
                    if ch.isalpha() or ch.isdigit() or ch == '_':
                        state = 13
                        temp_word += ch

                    elif isNotSpecial(ch):
                        state = 14

                    else:
                        state = 50
                        temp_word += ch


                elif case(15):
                    if ch == '\\':
                        state = 16
                        temp_word += ch

                    else:  # 任意字符
                        state = 17
                        temp_word += ch


                elif case(16):
                    if ch in ['a', 'b', 'f', 'n', 'r', 't', 'w', '\\', '\'', '\"', '?',
                              '0']:  # need transfer the character
                        state = 17
                        temp_word += ch

                    else:
                        state = 50
                        temp_word += ch


                elif case(17):
                    if ch == '\'':
                        state = 18
                        temp_word += ch

                    else:
                        state = 50
                        temp_word += ch


                elif case(19):
                    if ch == '\"':
                        state = 20
                        temp_word += ch

                    else:
                        state = 19
                        temp_word += ch


                elif case(21):
                    if ch == '/':
                        state = 22
                        temp_word += ch

                    elif ch == '*':
                        state = 24
                        temp_word += ch

                    elif ch == '=':
                        state = 37
                        temp_word += ch

                    elif isNotSpecial(ch):
                        state = 38

                    else:
                        state = 50
                        temp_word += ch


                elif case(22):
                    if ch == '\n':
                        state = 23

                    else:
                        state = 22
                        temp_word += ch


                elif case(24):
                    if ch == '*':
                        state = 25
                        temp_word += ch

                    else:
                        state = 24
                        temp_word += ch


                elif case(25):
                    if ch == '/':
                        state = 26
                        temp_word += ch

                    else:
                        state = 24
                        temp_word += ch


                elif case(27):
                    if ch in ['+', '=']:
                        state = 28
                        temp_word += ch

                    elif isNotSpecial(ch) and not isOp(ch):
                        state = 29

                    else:
                        state = 50
                        temp_word += ch


                elif case(30):
                    if ch in ['-', '=']:
                        state = 31
                        temp_word += ch

                    # elif ch == '0':
                    #     state = 1
                    #     temp_word += ch

                    # elif '1' <= ch <= '9':
                    #     state = 8
                    #     temp_word += ch

                    elif isNotSpecial(ch) and not  isOp(ch):
                        state = 32

                    else:
                        state = 50
                        temp_word += ch

                elif case(33):
                    if ch == '=':
                        state = 34
                        temp_word += ch

                    elif ch == '*':
                        state = 35
                        temp_word += ch

                    elif isNotSpecial(ch) and not isOp(ch):
                        state = 36

                    else:
                        state = 50
                        temp_word += ch


                elif case(35):
                    if ch == '*':
                        state = 35
                        temp_word += ch

                    elif isNotSpecial(ch):
                        state = 36

                    else:
                        state = 50
                        temp_word += ch

                elif case(39):
                    if ch == '=':
                        state = 40
                        temp_word += ch

                    elif isNotSpecial(ch):
                        state = 41

                    else:
                        state = 50
                        temp_word += ch


                elif case(42):
                    if ch in ['>', '=']:
                        state = 43
                        temp_word += ch

                    elif isNotSpecial(ch) and not isOp(ch):
                        state = 44

                    else:
                        state = 50
                        temp_word += ch
 

                elif case(45):
                    if ch in ['<', '=']:
                        state = 46
                        temp_word += ch

                    elif isNotSpecial(ch) and not isOp(ch):
                        state = 47

                    else:
                        state = 50
                        temp_word += ch
                elif case(52):
                    if ch in ['&', '=']:
                        state = 53
                        temp_word += ch

                    elif isNotSpecial(ch) and not isOp(ch):
                        state = 54
                    else:
                        state = 50
                        temp_word += ch

                elif case(55):
                    print('yyy')
                    if ch in ['|', '=']:
                        state = 56
                        temp_word += ch

                    elif isNotSpecial(ch) and not isOp(ch):
                        state = 57
                    else:
                        state = 50
                        temp_word += ch

            if ch == '\n':
                row += 1
                col = 0
            else:
                col += 1
            idx += 1
            if idx >= len(st):
                break
        if state in end_states_truncation:
            idx -= 1
            if col == 0:
                row -= 1
            else:
                col -= 1
            if temp_word and state not in [23, 26]:
                class_ = classfy(state, temp_word)
                words.append((temp_word, class_, row+1, col+1))
            temp_word = ''
        elif state in end_states_joint:
            if temp_word and state not in [23, 26]:
                class_ = classfy(state, temp_word)
                words.append((temp_word, class_, row+1, col+1))
            temp_word = ''
        else:
            errors.append((temp_word, row+1, col+1))
            temp_word = ''
        state = 0

    return words, errors
