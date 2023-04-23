from typing import List, Any

import data
import re


tablet_index =[]


def Syntax(senline):
    i = 0
    k = 0
    lex=[]
    Index=-1
    _index = 0
    count = len(senline)

    if count > 2 :
        if senline[0][2] == 'ID' and senline[1][2] == 'TYPE':
            tablet_index.append([senline[0][1], senline[1][1], senline[2][1]])
    else:
        if senline[0][2] == 'ID':
            tablet_index.append([senline[0][2]])

    count  = len(senline)
    if count >1:
        f = senline[1][1]
        if f == ':':
            lex.append(('l:'+ senline[0][0]))
        if senline[1][1] == 'SEGMENT' or senline[1][1] == 'ENDS':
            lex.append('N:'+(senline[0][0]))
            lex.append('M:'+(senline[1][0]))
            lex.append(1)
        if count > 2:
            if senline[1][-1] == 'TYPE':
                lex.append('N:'+(senline[0][0]))
                lex.append('M:'+(senline[1][0]))
                lex.append('1')
            if senline[2][-1] == 'HEX' or  senline[2][-1] == 'DEC' or senline[2][-1] == 'BIN':
                lex.append('O:'+(senline[2][0]))
                lex.append(1)
            if senline[0][-1] == 'COMMAND' or senline[1][-1] == 'COMMAND':
                lex.append('M:'+(senline[0][0]))
                lex.append(1)
                if senline[1][-1] == 'ID' or senline[1][-1] == '16_REG' or senline[1][-1] == '8_REG':
                    lex.append('O:'+senline[1][0])
                    k = int(senline[1][0])
                    while i < count:
                        if senline[i][1] == ',':
                            Index = int(senline[i][0])
                            break
                        i += 1
                    if Index < 0:
                        lex.append(count-k+1)
            Index = -1
            while i < count:
                if senline[i][1] == ',':
                    Index = int(senline[i][0])

                    break
                i +=1
            if Index != -1:
                k = Index - k
                lex.append(k)
                lex.append('O:'+senline[Index][0])
                lex.append(count - 1 - Index + 1)
        if count < 3:
            if senline[0][-1] == 'COMMAND':
                lex.append('M:'+(senline[0][0]))
                lex.append(1)
                if senline[1][-1] == '16_REG' or senline[1][-1] == 'ID':
                    lex.append('O:'+(senline[1][0]))
                    i = 0
                    Index = -1
                    k = int(senline[1][0])
                    while i < count:
                        if senline[i][1] == ',':
                            Index = int(senline[i][0])
                            break
                        i += 1
                    if Index < 0:
                        lex.append(count-k+1)



    if count == 1 :
         if senline[0][-1] == 'COMMAND':
            lex.append('M:'+(senline[0][0]))
            lex.append(1)
         if senline[0][-1]  == 'DIRECTIVE':
            lex.append('M:'+(senline[0][0]))
            lex.append(1)
    j = 0
    LEX = ' '
    while j < len(lex):
        LEX = LEX + str(lex[j])
        LEX = LEX +' '
        j+=1
   # print(LEX)
    return LEX

def operat(oper):
    id  = -2
    if (oper == '+' ) :
        id = 0
    elif(oper == '-'):
        id = 1
    if (oper == '*') :
        id = 2
    elif(oper == '/'):
        id = 3
    if (oper == '(' or oper == ')'):
        id = -1
    return id
def dexstra(math):
    #math = " ( 124 + 23 * ( 98 / 45 ) - 62 )"
    kls = math.split()
    steckdata = []
    steckoperation = []
  #  print(kls)
   # print(tablet_index)
    count = len(kls)
    i = 0
    while (i <count):
        if(kls[i].isdigit()):
            steckdata.append((kls[i]))
            i += 1
            continue
        elif (kls[i] == '(' ):
            steckoperation.append(kls[i])
            i += 1
            continue
        elif(kls[i] == '+' or kls[i] == '-'):
            chack = steckoperation.pop()
            steckoperation.append(chack)
            if (operat(chack) != -1) :
                newdata = 0
                b = float(steckdata.pop())
                a = float(steckdata.pop())
                op = steckoperation.pop()
                opo = operat(op)
                if (opo == 0):
                    newdata = a + b
                elif(opo == 1):
                    newdata = a - b
                elif (opo == 2):
                    newdata = a * b
                elif (opo == 3):
                    newdata = a / b
                steckdata.append(newdata)
                continue
            if ((operat(chack) == -1)) :
               # steckoperation.append(chack)
                steckoperation.append(kls[i])
                i +=1
                continue
        elif(kls[i] == '*' or kls[i] == '/'):
            chack = steckoperation.pop()
            op =operat(chack)
            if ((op == 2)or(op == 3)):
                newdata = 0
                b = float(steckdata.pop())
                a = float(steckdata.pop())
                if (op == 2):
                    newdata = a * b
                elif (op == 3):
                    newdata = a / b
                steckdata.append(newdata)
                continue
            if ((op == -1) or (op == 0)or (op == 1)):
                steckoperation.append(chack)
                steckoperation.append(kls[i])
                i += 1
                continue
        if (kls[i] == ')'):
            thend  = steckoperation.pop()
            steckoperation.append(thend)
            b = float(steckdata.pop())
            a = float(steckdata.pop())
            while (thend != '('):
                chack  = steckoperation.pop()
                if (operat(chack) != -1):
                    newdata  = 0
                    op =  operat(chack)
                    if ( op == 0):
                        newdata = a + b
                    elif (op == 1):
                        newdata = a - b
                    elif (op == 2):
                        newdata = a * b
                    elif (op == 3):
                        newdata = a / b
                    steckdata.append(newdata)
                    thend = steckoperation.pop()
                    continue
        i += 1
        continue
    result = steckdata[0]
    return result



label_offset = 0
Seg = []
OFFSET = []
T_D = []
tuor = []
SEGMENTS=[]


def Segmen_16reg_or_8seg(regist):
    if regist == 'AX' or regist == 'AL':
        return '000'
    if regist == 'CX' or regist == 'CL':
        return '001'
    if regist == 'DX' or regist == 'DL':
        return '010'
    if regist == 'BX' or regist == 'BL':
        return '011'
    if regist == 'SP' or regist == 'AH':
        return '100'
    if regist == 'BP' or regist == 'CH':
        return '101'
    if regist == 'SI' or regist == 'DH':
        return '110'
    if regist == 'DI' or regist == 'BH':
        return '111'
    return 'error'
def M_R(RM):

    if RM == '[SI]':
        return '100'
    elif RM == '[DI]':
        return '101'
    elif RM == '[BP]':
        return '011'
    elif RM == '[BX]':
        return '111'
    return 'error'

def PREfSEG(pref):

    if pref == 'ES':
        return '26'
    if pref == 'CS':
        return '2E'
    if pref == 'SS':
        return '36'
    if pref == 'DS':
        return '3E'
    if pref == 'FS':
        return '64'
    if pref == 'GS':
        return '65'
    return 'error'

SEGment = []

def sen_offset(senline, struc_senline,under,line):

    f = -1
    if (len(senline) < 2):
        if senline[0] == 'END':
            a = -1
            strst =" " #+ senline[0]
            tuor.append(strst)
            return a
    offset = under
    result = DecToHex(offset)
    if data._offset != -1:
        offset = data._offset
        result = DecToHex(offset)
        data._offset = -1
    i = 0
    count = len(senline)
    strst = result +" "
    # while(i<count):
    #     strst+=senline[i]
    #     strst+=" "
    #     i+=1
    tuor.append(strst)

    OFFSET.append(result)
    tabl_ID = []
    find_N = struc_senline.find("N:")
    if find_N != -1:
        f = int(struc_senline[find_N+2])
        if senline[-1] != "SEGMENT" and  senline[-1] != "ENDS" and find_ID(senline[0]) == -1:
            Seg.append(senline[0])
            return offset
        if (senline[f] == "SEGMENT" and senline[0] != "ENDS"):
            SEGment.append(senline[f-1])
            if data.flag_segment  is True:
                Seg.append(line[0])
                data.tmp_offset = offset
                offset = 0
                i = 0
                count = len(senline)
                result = DecToHex(offset)
                strst = result + " "
                # while (i < count):
                #     strst += senline[i]
                #     strst += "    "
                #     i += 1
                del tuor[-1]
                tuor.append(strst)
                data.flag_segment = True
            if (data.flag_segment  == False and data.tmp_offset !=-1) :
                offset = data.tmp_offset
                Seg.append(line[0])
            else:
                offset = 0
                i = 0
                count = len(senline)
                result = DecToHex(offset)
                strst = result + " "
                # while (i < count):
                #     strst += senline[i]
                #     strst += "    "
                #     i += 1
                del tuor[-1]
                tuor.append(strst)
                data.flag_segment = True
                Seg.append(senline[0])
        elif senline[f] == "DB":
            tabl_ID.append(senline[0])
            tabl_ID.append(senline[f])
            tabl_ID.append(result)
            offset += 1
            tabl_ID.append(Seg[-1])
        elif senline[f] == "DD":
            tabl_ID.append(senline[0])
            tabl_ID.append(senline[f])
            offset += 4
            tabl_ID.append(result)
            tabl_ID.append(Seg[-1])
        elif senline[f] == "DW":
            tabl_ID.append(senline[0])
            tabl_ID.append(senline[f])
            offset += 2
            tabl_ID.append(result)
            tabl_ID.append(Seg[-1])

        if (senline[f] == "ENDS"):
            del Seg[-1]
            SEGMENTS.append([ senline[0],"16 bit",result,"PARA","NONE"])
            if data.tmp_offset != -1:
                del Seg[-1]
                result = " "
                under = offset
                result = DecToHex(offset)
                data._offset = data.tmp_offset
                data.tmp_offset = -1
                OFFSET.append(result)
                return result
            else :
                offset = under
                #del Seg[-1]
            data.flag_segment = False
           # offset = 0
    else :
        offset = offset
    find_L = struc_senline.find("l:")
    if find_L != -1:
        tabl_ID.append(senline[0])
        tabl_ID.append("NEAR")
        offset = offset
        tabl_ID.append(result)
        tabl_ID.append(Seg[-1])
        label_offset = offset
    find_M = struc_senline.find("M:")
    f = -1
    if(find_M != -1):
        f = int(struc_senline[find_M + 2])
        f -=1
        if(senline[f] == "JNE"):
           # print(Seg)
            offset+= int(JNE(offset,senline[1]))
        elif(senline[f] == "STOSB"):
            offset += int(STOSB())
        elif(senline[f] == "PUSH"):
            offset += int(PUSH(line))
        elif(senline[f] == "MUL"):
            offset += int(MUL(line))
        elif(senline[f] == "ADD"):
            offset += int(ADD(line))
        elif (senline[f] == "AND"):
            offset += int(AND(line))
        elif (senline[f] == "CMP"):
            offset += int(CMP(line))
        elif (senline[f] == "MOV"):
            offset += MOV(line)
        elif (senline[f] == "SUB"):
            offset += int(SUB(line))
        elif (senline[f] == "TEST"):
            offset += int(TEST(line))
    result  = " "
    under = offset
    result = DecToHex(offset)


    if (len(tabl_ID) > 1 ):
        T_D.append(tabl_ID)
    #T_D.append(tabl_ID)
    return result

def STOSB():
    return 1
def PUSH(senline):
    if senline[1][2] == '16_REG':
        return 1
    return 0
def MUL(senline):
    
    return 4

def ADD(senline):
   # print(senline)
    count  = len(senline)
    if(senline[1][2] == '16_REG' and senline[count - 2][2] == '16_REG'):
        return 4
    if (senline[1][2] == '8_REG' and senline[count - 2][2] == '8_REG'):
        return 4
    return 4

def AND(senline):
    if (senline[1][2] == '16_REG' and senline[3][2] == '16_REG'):
        return 2
    if (senline[1][2] == '8_REG' and senline[3][2] == '8_REG'):
        return 2
    return 2

def CMP(senline):
    i = 0
    count = len(senline)
    while(i < count):
        if senline[i][2] == 'ID':
            break
        i+=1
    if (senline[i+2][2] == '16_REG' and senline[6][2] == '16_REG'):
        return 4
    if (senline[i+2][2] == '8_REG' and senline[6][2] == '8_REG'):
        return 4
    return 4
def MOV(senline):
    k = 0
    if senline[1][2] == '16_REG' and senline[3][2] == 'SEG_REG' and senline[4][1] == ':':
        k += 1
    k +=4
    return k
def SUB(senline):
    if senline[1][2] == '8_REG':
        return 2
    return 2
def TEST(senline):
    if senline[1][2] == 'ID'and senline[3][2] == '16_REG':
        return 5
    return 5
def JNE(offset, lable_name):
  #  print (offset)
   # print(lable_name)
    i = 0
    count = len(T_D)
    while (i < count):
        if (T_D[i][0] == lable_name ):
            a = int(T_D[i][2],16)
            #print(T_D[i][0])
            if ((offset - a) < -128 or (offset - a) >127):
                return 4
            else:
                return 2
        i+=1
    return 4

def PRINT_TABL_IDENT():
    i = 0
    count = len(T_D)
    a = " "
    #print(T_D)
    tmp = 1
    while (i < count):
        if i > 0 :
            k = 0
            z = i
            while(k<i):
                if T_D[i] == T_D[k]:
                    tmp = -1
                    break
                k+=1
        if tmp == 1:
            if T_D[i][1]  == 'NEAR':
                a += T_D[i][0] + "..\t\t" + T_D[i][1] + "\t\t" + T_D[i][2] + "\t\t" + T_D[i][3] + "\n"
            else:
                a += T_D[i][0] + "....\t\t"+T_D[i][1]+"\t\t\t"+T_D[i][2] + "\t\t" +T_D[i][3] + "\n"
        i+=1
   # print(a)
    return a


def chack_error(var):

    if var.find('error') != -1 :
        return 'stop'

    return 0
def PRINT_LST():
    i = 0
    count = len(tuor)
    b = ""
    while(i < count):
        b+= tuor[i]+"   "+code_command[i]+"\n"
        if find_err(code_command[i]) != 0 :
            break
        if chack_error(tuor[i]) != 0 or chack_error(code_command[i]) != 0 :
            b +="\n       ERROR\n"
        i+=1
    return b

def find_err(var):
    if var.find('ENDS') != 1:
        return 0
    elif var.find('END') != -1:
        return 1
    return 0

def PRINT_SEGS():
    i = 0
    count = len(SEGMENTS)
    c= ""
    tmp = 1
    while(i < count):
        if i > 0:
            k = 0
            while (k < i):
                if SEGMENTS[i][0] == SEGMENTS[k][0]:
                    tmp = -1
                    break
                k += 1
        if tmp == 1:
            c += SEGMENTS[i][0]+"...\t\t\t"+SEGMENTS[i][1]+"\t\t"+SEGMENTS[i][2]+"\t\t"+ SEGMENTS[i][3]+ "\t "+SEGMENTS[i][4]+"\n"
            tmp = 1
        i+=1
    return c

varrr = []
code_command = []

def func():
    # i = data.indecount-1
    # count = len(tuor)
    # print(tuor[data.indecount])
    # while (i<count):
    #     tmp =int(tuor[data.indecount],16)
    #     tmp -= 4
    #     tuor[data.indecount]
    #     i+=1
    # del tuor[-1]
    return 0

def Second(senline, struc_senline,under,line):

    offset = sen_offset(senline, struc_senline,under,line)
    data.indecount+=1
    del tuor[-1]
   # print(T_D)
   #test = tuor[-1]
    del tuor[-1]
    #test1 = tuor[-1]

    f = -1
    tabl_ID = []
    if struc_senline == ' ':
        i = 0
        count = len(SEGment)
        while(i  < count):
            if SEGment[i] == senline[0]:
               break
            i+=1
        code_command.append(senline[0] + ' '+senline[1] + '    error')
    find_N = struc_senline.find("N:")
    if find_N != -1:
        f = int(struc_senline[find_N+2])
        if senline[f] == "DB":
            MEM_Chack(senline[-1],senline[f])
            code_command.append(write_VAR(senline[-1],line[-1][-1])+'            '+' ' +write_str(senline))

            return offset
        elif senline[f] == "DD":
           MEM_Chack(senline[-1], senline[f])
           code_command.append(write_VAR(senline[-1],line[-1][-1])+'             '+' ' +write_str(senline))

           return offset
        elif senline[f] == "DW":
            MEM_Chack(senline[-1], senline[f])
            code_command.append(write_VAR(senline[-1],line[-1][-1])+'            '+' ' +write_str(senline))

            return offset
    else :

        find_L = struc_senline.find("l:")
        if find_L != -1:
            strstr = ' '
            i = 0
            count = len(senline)
            while (i < count):
                strstr += senline[i]
                strstr += "   "
                i += 1
            code_command.append('               ' + strstr)


    find_M = struc_senline.find("M:")
    f = -1
    if(find_M != -1):
        f = int(struc_senline[find_M + 2])
        f -=1
        if(senline[f] == "JNE"):
            if  JNE_2(senline, line, struc_senline) == 'error':
                func()
            #  code_command.append(erorchuck(element))

            return offset
        if(senline[f] == "STOSB"):
            element = STOSB_2(senline)
            code_command.append(erorchuck(element))

            return offset
        elif(senline[f] == "PUSH"):
            element = PUSH_2(senline,line)
            code_command.append(erorchuck(element))

            return offset
        elif(senline[f] == "MUL"):
            element = MUL_2(senline,line,struc_senline)

          #  code_command.append(erorchuck(element))
            return offset
        elif(senline[f] == "ADD"):
            element = ADD_2(senline, line, struc_senline)

           # code_command.append(erorchuck(element))
            return offset
        elif (senline[f] == "AND"):
            element = AND_2(senline, line, struc_senline)

        # code_command.append(erorchuck(element))
            return offset
        elif (senline[f] == "CMP"):
            element = CMP_2(senline, line, struc_senline)

        # code_command.append(erorchuck(element))
            return offset
        elif (senline[f] == "MOV"):
            element = MOV_2(senline, line, struc_senline)

        # code_command.append(erorchuck(element))
            return offset
        elif (senline[f] == "SUB"):
            element = SUB_2(senline, line, struc_senline)

            return offset
        elif (senline[f] == "TEST"):
            element = TEST_2(senline, line, struc_senline)

            return offset
        else:
            strstr = ' '
            i = 0
            count = len(senline)
            while (i < count):
                strstr += senline[i]
                strstr += "   "
                i += 1
            code_command.append('               ' +strstr )


def erorchuck(test):
    if test != 'error':
        return test
    else:
        return 'error'

def write_str(senline):
    strstr = ' '
    i = 0
    count = len(senline)
    while (i < count):
        strstr += senline[i]
        strstr += "   "
        i += 1
    return strstr

def find_ID(find):
    find_index = -1
    count = len(T_D)
    i = 0
    while (i < count):
        if T_D[i][0] == find:
            return i
        i+=1
    return 'error'

def Normal_var_write( var):
    count = len(var)

    if count == 2:
        return var
    elif count < 2:
        var = '0' + var
        return var
    if count == 4:
        return var
    if count < 4:
        if var[0] == '0':
            return var[1:]
        else:
            var = '0' + var
            return var
    if count == 8:
        return var
    elif count < 8:
        while (len(var)!=8):
            var = '0'+ var
        return var
    return var

def STOSB_2(senline):
    if len(senline) > 1:
        return 'error'
    return 'AA          ' +write_str(senline)
def PUSH_2(senline,line):
    count = len(senline)
    if(count != 2):
        return 'error'
    else:
        if line[1][-1] == "16_REG":
            return '50          ' +write_str(senline)
        else:
            return 'error'
    return 'error'

def MUL_2(senline,line, struc_senline):
    find_O = struc_senline.find("O:")
    f = -1
    if (find_O != -1):
        f = int(struc_senline[find_O + 2])
        f -= 1
        colum_3 = ''
        colum_4 = ''
        writ_tmp = ''
        writ_tmp1 = ''
        out_OK = ''
        if Pref_seg(senline[f+1]) == 0:
           # if(find_ID(senline[f])!= 'error'):

                if find_ID(senline[f]) != 'error':
                    colum_3 += other(senline[f])
                else:
                    colum_3 = 'error'
                if (other_2(line[f]) != 'error'):
                    colum_4 += other_2(line[f])

                if senline[f+1] =='[' and senline[f+3] == ']':
                    tmp = check_vars(senline[f])
                    tmp1 = find_MOD_R_M(f, senline, line)

                    if tmp1.find('M:') != -1 and tmp1 != 'error' :
                        out1 = des(f, senline, line)
                        if out1 != 'error':
                            out_OK += out1
                        M1 = tmp1.find('M:')
                        i = M1 + 2
                        while i < len(tmp1):
                            writ_tmp1 += tmp1[i]
                            i += 1
                        writ_tmp = '100'
                        out_OK += writ_tmp +  writ_tmp1
                        #colum_2 = Pr_colum_2(out_OK)

                    if tmp1 == 'error' and tmp == 'error':
                        code_command.append('F7  ' + "  " + '0000' + ' ' + write_str(senline) + 'error')
                    if tmp1 == 'error':
                        out_OK ='error'
                    colum_2 = Pr_colum_2(out_OK)
                    if tmp == '16_REG' :
                        code_command.append('F7  '+colum_2 +' '+colum_3+' '+colum_4+write_str(senline))
                    elif tmp == '8_REG' :
                        code_command.append('F6  '+ colum_2 +' '+colum_3+' '+colum_4+' ' +write_str(senline))
                    #else:
                     #   code_command.append('error')

                    # if line[f+2][-1] == '16_REG' :
                    #     code_command.append('F7')
                    # elif line[f+2][-1] == '8_REG' :
                    #     code_command.append('F6')
                    # else:
                    #     code_command.append('error')
        else:
            tmp_cod = PREfSEG(senline[f+1]) + ':'
            if tmp_cod == 'error:':
                return -1
            find_ID(senline[f])
            if senline[f+4] =='[' and senline[f+6] == ']':
                tmp1 = find_MOD_R_M(f+3, senline, line)

                if tmp1.find('M:') != -1 and tmp1 != 'error':
                    out1 = des(f+3, senline, line)
                    if out1 != 'error':
                        out_OK += out1
                    M1 = tmp1.find('M:')
                    i = M1 + 2
                    while i < len(tmp1):
                        writ_tmp1 += tmp1[i]
                        i += 1
                    writ_tmp = '100'
                    out_OK += writ_tmp + writ_tmp1
                colum_2 = hex(int(out_OK, 2))
                colum_2 = Pr_colum_2(colum_2)
                print(colum_2[2:])
                if line[f+5][-1] == '16_REG' :
                    tmp_cod += 'F7  '+colum_2+' ' +write_str(senline)
                    code_command.append(tmp_cod)
                elif line[f+5][-1] == '8_REG' :
                    tmp_cod += 'F6  '+colum_2++' ' +write_str(senline)
                    code_command.append(tmp_cod)
                else:
                    code_command.append('error')
    return 0

def Pr_colum_2(colum_2):
    if colum_2 != 'error':
        colum_2 = hex(int(colum_2, 2))
        colum_2 = colum_2.upper()
        colum_2 = colum_2[2:]
        return colum_2
    return 'error'
def COL_2(f,f1, senline, line):

    tmp1 = find_MOD_R_M(f, senline, line)
    writ_tmp = ''
    writ_tmp1 = ''
    out_OK = ''
    if tmp1 == 'error':
        return 'error'
    else:
        out1 = des(f, senline, line)
        out_OK +='01'
        if tmp1.find('R:') != -1:
            # M1 = tmp1.find('R:')
            # i = M1 + 2
            # while i < len(tmp1):
            #     writ_tmp1 += tmp1[i]
            #     i += 1
            writ_tmp = '101100'
            out_OK += writ_tmp
    colum_2 = Pr_colum_2(out_OK)

    return colum_2

def MOD_R_M(f1, f2,senline, line):
    tmp1 = find_MOD_R_M(f1,senline,line)
    tmp2 = find_MOD_R_M(f2,senline,line)
    writ_tmp = ''
    writ_tmp1 = ''
    out_OK = ''
    if tmp1 == 'error' or tmp2 == 'error':
        return 'error'
    else:
        out1 = des(f1, senline, line)
        out2 = des(f2, senline, line)
        if out1 != 'error' or out2 != 'error':
            if out1 == '00' and out2 == '00':
                out_OK += '11'
            elif out1 < out2:
                out_OK += out2
            else:
                out_OK += out1
        if tmp2 == 'imm' and tmp1.find('M:') != -1:
            M1 = tmp1.find('M:')
            i = M1 + 2
            while i < len(tmp1):
                writ_tmp1 += tmp1[i]
                i += 1
            writ_tmp = '000'
            out_OK += writ_tmp + writ_tmp1

        if tmp1.find('M:') != -1 and tmp2 != 'imm':
            if tmp2.find('R:') != -1:
               # R1 = tmp2.find('R:')
                M1 = tmp1.find('M:')
                i = M1+2
                while i < len(tmp1):
                    writ_tmp += tmp1[i]
                    i+=1
                R1 = tmp2.find('R:')
                i = R1+2
                while i < len(tmp2):
                    writ_tmp1 += tmp2[i]
                    i += 1
                out_OK+=writ_tmp1+writ_tmp
            else:
                return 'error'
        if tmp1.find('R:') != -1:
            if tmp2.find('M:') != -1:
                R1 = tmp1.find('R:')
                M1 = tmp2.find('M:')
                i = M1 + 2
                while i < len(tmp1):
                    writ_tmp += tmp2[i]
                    i += 1
               # R1 = tmp2.find('R:')
                i = R1 + 2
                while i < len(tmp1):
                    writ_tmp1 += tmp1[i]
                    i += 1
                out_OK += writ_tmp1 + writ_tmp
            elif tmp2.find('R:') != -1:
                R1 = tmp2.find('R:')
                M1 = tmp1.find('R:')
                i = M1 + 2
                while i < len(tmp1):
                    writ_tmp += tmp1[i]
                    i += 1
                i = R1 + 2
                while i < len(tmp2):
                    writ_tmp1 += tmp2[i]
                    i += 1
                out_OK += writ_tmp + writ_tmp1

    return out_OK

def find_MOD_R_M(f,senline,line):

    tmp1 = ''
    if PREfSEG(senline[f]) == 'error':
        if(find_ID(senline[f])!='error'):

            tmp =  senline[f+1] +senline[f+2] +senline[f+3]
            tmp1 = M_R(tmp)
            if tmp1 !='error':
                return 'M:'+tmp1
            else:
                return 'error'

        elif Segmen_16reg_or_8seg(senline[f]) != 'error':
            return 'R:' + Segmen_16reg_or_8seg(senline[f])
        elif line[f][-1] == 'BIN' or line[f][-1] == 'DEC' or line[f][-1] == 'HEX':
            return 'imm'
    else:
        if (find_ID(senline[f+2]) != 'error'):

            tmp = senline[f + 3] + senline[f + 4] + senline[f + 5]
            tmp1 = M_R(tmp)
            if tmp1 != 'error':
                return 'M:' + tmp1
            else:
                return 'error'

        elif Segmen_16reg_or_8seg(senline[f+2]) != 'error':
            return 'R:' + Segmen_16reg_or_8seg(senline[f+2])
        elif line[f+2][-1] == 'BIN' or line[f+2][-1] == 'DEC' or line[f+2][-1] == 'HEX':
            return 'imm'
    return 'error'

def des(f, senline, line):

    if (find_ID(senline[f]) != 'error'):
        tmp = senline[f + 1] + senline[f + 2] + senline[f + 3]
        tmp1 = M_R(tmp)
        if tmp1 != 'error':
            return '10'
        else:
            return 'error'
    elif Segmen_16reg_or_8seg(senline[f]) != 'error':
        return '00'
    elif line[f][-1] == 'BIN' or line[f][-1] == 'DEC' or line[f][-1] == 'HEX':
        return '01'
    if PREfSEG(senline[f]) != 'error':
        if (find_ID(senline[f+2]) != 'error'):
            tmp = senline[f + 3] + senline[f + 4] + senline[f + 5]
            tmp1 = M_R(tmp)
            if tmp1 != 'error':
                return '10'
            else:
                return 'error'
        elif Segmen_16reg_or_8seg(senline[f+2]) != 'error':
            return '00'
        elif line[f+2][-1] == 'BIN' or line[f+2][-1] == 'DEC' or line[f+2][-1] == 'HEX':
            return '01'
    return 'error'


def other(var):

    index = find_ID(var)
    colum_3 = T_D[index][2]

    return colum_3


def other_2(var):

    colum_4  = ''
    if var [-1] == 'BIN':
        colum_4 = var[1]
        return colum_4[:-1]
    if var [-1] == 'HEX':
        colum_4 = var[1]
        return colum_4[:-1]
    if var [-1] == 'DEX':
        colum_4 = var[1]
        return colum_4

    return 'error'

def check_vars(var):
    find_index = -1
    count = len(T_D)
    i = 0
    while (i < count):
        if T_D[i][0] == var:
            if T_D[i][1] == 'DB' :
                return '8_REG'
            else:
                return '16_REG'
        i += 1
    return 'error'


def ADD_2(senline,line, struc_senline):
    find_O = struc_senline.find("O:")
    f = -1
    colum_3 =''
    colum_4 = ''
    if (find_O != -1):
        f = int(struc_senline[find_O + 2])
        f -= 1
        o1 = oper_1(f,'ADD',senline,line,struc_senline)
        if find_ID(senline[f]) != 'error':
           colum_3 +=' '+ other(senline[f])+' '
        if (other_2(line[f])!= 'error'):
            colum_4 += ' '+other_2(line[f])+' '
        find_O_2 = struc_senline.rfind('O:')
        f_2  = int(struc_senline[find_O_2 + 2])-1
        if find_ID(senline[f_2]) != 'error':
           colum_3 += ''+other(senline[f_2])+' '
        else :
            colum_3 += '     '+' '
        if (other_2(line[f_2])!= 'error'):
            colum_4 +=''+ other_2(line[f_2])
        else :
            colum_4 += '     '
        o2 = oper_1(f_2, 'ADD', senline, line, struc_senline)
        colum_2 =Pr_colum_2(MOD_R_M(f,f_2,senline,line))
        code_command.append(comp_comand('ADD',o1,o2)+'  '+colum_2 +' '+colum_3+'  '+colum_4 + write_str(senline))
        return 0

def AND_2(senline,line, struc_senline):
    find_O = struc_senline.find("O:")
    f = -1
    colum_3 = ''
    colum_4 = ''
    if (find_O != -1):
        f = int(struc_senline[find_O + 2])
        f -= 1
        o1 = oper_1(f,'AND',senline,line,struc_senline)
        if find_ID(senline[f]) != 'error':
           colum_3 += ''+other(senline[f])
        if (other_2(line[f])!= 'error'):
            colum_4 += ''+other_2(line[f])
        find_O_2 = struc_senline.rfind('O:')
        f_2  = int(struc_senline[find_O_2 + 2])-1
        if find_ID(senline[f_2]) != 'error':
           colum_3 +=''+ other(senline[f_2])
        else :
            colum_3 += '     '
        if (other_2(line[f_2])!= 'error'):
            colum_4 += ''+other_2(line[f_2])
        else :
            colum_4 += '     '
        o2 = oper_1(f_2, 'AND', senline, line, struc_senline)
        colum_2 =Pr_colum_2(MOD_R_M(f,f_2,senline,line))

        code_command.append(comp_comand('AND',o1,o2)+'  '+colum_2 +'  '+colum_3+' '+colum_4 + write_str(senline))
        return 0

def CMP_2(senline,line, struc_senline):
    find_O = struc_senline.find("O:")
    f = -1
    colum_3 = ''
    colum_4 = ''
    if (find_O != -1):
        f = int(struc_senline[find_O + 2])
        f -= 1
        o1 = oper_1(f,'CMP',senline,line,struc_senline)
        if find_ID(senline[f]) != 'error':
           colum_3 += ''+other(senline[f])
        if (other_2(line[f])!= 'error'):
            colum_4 += ''+other_2(line[f])
        find_O_2 = struc_senline.rfind('O:')
        f_2  = int(struc_senline[find_O_2 + 2])-1
        if find_ID(senline[f_2]) != 'error':
           colum_3 += ''+other(senline[f_2])
        else :
            colum_3 += '     '
        if (other_2(line[f_2])!= 'error'):
            colum_4 += ''+other_2(line[f_2])
        else :
            colum_4 += '     '
        o2 = oper_1(f_2, 'CMP', senline, line, struc_senline)
        colum_2 =Pr_colum_2(MOD_R_M(f,f_2,senline,line))
        code_command.append(comp_comand('CMP',o1,o2)+'  '+colum_2 +'  '+colum_3+' '+colum_4+'' +write_str(senline))
        return 0

def MOV_2(senline,line, struc_senline):
    find_O = struc_senline.find("O:")
    f = -1
    colum_3 = ''
    colum_4 = ''
    if (find_O != -1):
        f = int(struc_senline[find_O + 2])
        f -= 1
        o1 = oper_1(f,'MOV',senline,line,struc_senline)
        if find_ID(senline[f]) != 'error':
            colum_3 += ''+other(senline[f])
        if (other_2(line[f])!= 'error'):
            colum_4 += ''+other_2(line[f])
        find_O_2 = struc_senline.rfind('O:')
        f_2  = int(struc_senline[find_O_2 + 2])-1
        if PREfSEG(senline[f_2]) != 'error':
            if senline[f_2+1] ==':':
                if find_ID(senline[f_2+2]) != 'error':
                    colum_3 += '' + other(senline[f_2+2])
                else:
                    colum_3 += '     '
                if (other_2(line[f_2+2]) != 'error'):
                    colum_4 += '' + other_2(line[f_2+2])
        if find_ID(senline[f_2]) != 'error':
            colum_3 += ''+other(senline[f_2])
        else :
            colum_3 += '     '
        if (other_2(line[f_2])!= 'error'):
            colum_4 += ''+other_2(line[f_2])
        else :
            colum_4 += '     '
        o2 = oper_1(f_2, 'MOV', senline, line, struc_senline)
        colum_2 =Pr_colum_2(MOD_R_M(f,f_2,senline,line))
        code_command.append(comp_comand('MOV',o1,o2)+'  '+colum_2 +' '+colum_3+' '+colum_4+'' +write_str(senline))
        return 0
def TEST_2(senline,line, struc_senline):
    find_O = struc_senline.find("O:")
    f = -1
    colum_3 = ''
    colum_4 = ''
    if (find_O != -1):
        f = int(struc_senline[find_O + 2])
        f -= 1
        o1 = oper_1(f,'TEST',senline,line,struc_senline)
        if find_ID(senline[f]) != 'error':
           colum_3 += ''+other(senline[f])
        if (other_2(line[f])!= 'error'):
            colum_4 += ''+other_2(line[f])
        find_O_2 = struc_senline.rfind('O:')
        f_2  = int(struc_senline[find_O_2 + 2])-1
        if find_ID(senline[f_2]) != 'error':
           colum_3 +=other(senline[f_2])
        else :
            colum_3 += '      '
        if (other_2(line[f_2])!= 'error'):
            colum_4 +=other_2(line[f_2])
        else :
            colum_4 += '     '
        o2 = oper_1(f_2, 'TEST', senline, line, struc_senline)
        colum_2 = Pr_colum_2(MOD_R_M(f,f_2,senline,line))
        count  = len(line)
        if line[count-1][-1] == 'BIN' :
            code_command.append('F6'+'  '+colum_2 +  ' '+colum_3+' '+colum_4+'' +write_str(senline))
        else:
            code_command.append(comp_comand('TEST',o1,o2) +'  '+colum_2 +' '+colum_3+''+colum_4+'     ' +write_str(senline))
        return 0

def SUB_2(senline,line, struc_senline):
    find_O = struc_senline.find("O:")
    f = -1
    colum_3 = ''
    colum_4 = ''
    if (find_O != -1):
        f = int(struc_senline[find_O + 2])
        f -= 1
        o1 = oper_1(f,'SUB',senline,line,struc_senline)
        if find_ID(senline[f]) != 'error':
           colum_3 += other(senline[f])
        if (other_2(line[f])!= 'error'):
            colum_4 += other_2(line[f])
        find_O_2 = struc_senline.rfind('O:')
        f_2  = int(struc_senline[find_O_2 + 2])-1
        if find_ID(senline[f_2]) != 'error':
           colum_3 +=''+ other(senline[f_2])
        else :
            colum_3 += '     '
        if (other_2(line[f_2])!= 'error'):
            colum_4 += ''+ other_2(line[f_2])
        else :
            colum_4 += '     '
        o2 = oper_1(f_2, 'SUB', senline, line, struc_senline)
        colum_2 = COL_2(f,f_2,senline,line)
        code_command.append(comp_comand('SUB',o1,o2)+'  '+ colum_2+' '+colum_3+'   '+colum_4+' ' +write_str(senline))
        return 0





def JNE_2(senline,line, struc_senline):
    if find_ID(senline[-1]) != 'error' :
        colum4 = ''
        colum4 = JNE_90(senline[-1])
        code_command.append('75'+colum4+ write_str(senline))
        return 0
    else:
        code_command.append('75' + '            '+ write_str(senline) + 'error')
    return 'error'

def JNE_90(var):
    index = find_ID(var)
    if index != 'error':
        tmp = other(var)
        if(abs(int(tmp,16) - int(tuor[data.indecount],16)) <= int('0100',2)):

            return '  02  90 90        '

    return  ' F2                   '


def comp_comand(cmnd,first_operand,second_operand):
    strcommand = ''

    if first_operand == 'error' or second_operand == 'error':
        return 'error'
    elif cmnd == 'ADD':
        if first_operand == 0 and second_operand == 1 or (first_operand == 1 and second_operand == 0):
            return 'error'
        if first_operand == 0 and second_operand == 0:
            strcommand = '02'
            return strcommand
        elif first_operand == 1 and second_operand == 1:
            strcommand = '03'
            return strcommand
        elif first_operand == 0 and second_operand[-1] == '0':
            strcommand =  second_operand[:-1] +'02'
            return strcommand
        elif first_operand == 1 and second_operand[-1] == '2':
            strcommand =  second_operand[:-1] + '03'
            return strcommand
        elif first_operand[-1] == '0' and second_operand == 0:
            strcommand = first_operand[:-1] + '02'
            return strcommand
        elif first_operand[-1] == '1' and second_operand == 1:
            strcommand = first_operand[:-1] + '03'
            return strcommand
        else:
            return 'error'


    if cmnd == 'AND':
        if first_operand == 0 and second_operand == 1 or (first_operand == 1 and second_operand == 0):
            return 'error'
        if first_operand == 0 and second_operand == 0:
            strcommand = '22'
            return strcommand
        elif first_operand == 1 and second_operand == 1:
            strcommand = '23'
            return strcommand
        elif first_operand == 0 and second_operand[-1] == '0':
            strcommand = second_operand[:-1]  +'22'
            return strcommand
        elif first_operand == 1 and second_operand[-1] == '2':
            strcommand = second_operand[:-1]  +'23'
            return strcommand
        elif first_operand[-1] == '0' and second_operand == 0:
            strcommand = first_operand[:-1] + '22'
            return strcommand
        elif first_operand[-1] == '1' and second_operand == 1:
            strcommand = first_operand[:-1] + '23'
            return strcommand
        else:
            return 'error'
    if cmnd == 'CMP':
        if first_operand == 0 and second_operand == 1 or (first_operand == 1 and second_operand == 0):
            return 'error'
        if first_operand == 0 and second_operand == 0:
            strcommand = '38'
            return strcommand
        elif first_operand == 1 and second_operand == 1:
            strcommand = '39'
            return strcommand
        elif first_operand == 0 and second_operand[-1] == '0':
            strcommand = second_operand[:-1]  + '38'
            return strcommand
        elif first_operand == 1 and second_operand[-1] == '2':
            strcommand = second_operand[:-1]  + '39'
            return strcommand
        elif first_operand[-1] == '0' and second_operand == 0:
            strcommand = first_operand[:-1] + '38'
            return strcommand
        elif first_operand[-1] == '1' and second_operand == 1:
            strcommand =first_operand[:-1]+ '39'
            return strcommand
        else:
            return 'error'
    if cmnd == 'MOV':
        if first_operand == 'error' or second_operand == 'error' :
            return 'error'
        if first_operand == 0 or second_operand == 1 :
            return 'error'

        if first_operand == 0 and second_operand == 0:
            strcommand = '8A'
            return strcommand
        elif first_operand == 1 and second_operand == 1 or second_operand == 0:
            strcommand = '8B'
            return strcommand
        elif first_operand == 0 and second_operand[-1] == '0':
            strcommand = second_operand[:-1]  + ' 8A'
            return strcommand
        elif first_operand == 1 and second_operand[-1] == '1':
            strcommand = second_operand[:-1]  + ' 8B'
            return strcommand
        elif first_operand[-1] == '0' and second_operand == 0:
            strcommand = first_operand[:-1] + '8A'
            return strcommand
        elif first_operand[-1] == '1' and second_operand == 1:
            strcommand = first_operand[:-1] + '8B'
            return strcommand
        else:
            return 'error'
    if cmnd == 'TEST':
        if first_operand == 0 and second_operand == 1 or (first_operand == 1 and second_operand == 0):
            return 'error'
        if first_operand == 0 and second_operand == 0:
            strcommand = 'F6'
            return strcommand
        elif first_operand == 1 and second_operand == 1:
            strcommand = 'F7'
            return strcommand
        elif first_operand == 0 and second_operand == 2:
            strcommand = 'F6'
            return strcommand
        elif first_operand == 1 and second_operand == 2:
            strcommand =  'F7'
            return strcommand
        else:
            return 'error'
    if cmnd == 'SUB':
        if first_operand == 0 and second_operand == 1 or (first_operand == 1 and second_operand == 0):
            return 'error'
        if first_operand == 0 and second_operand == 2:
            strcommand = '2C'
            return strcommand
        elif first_operand == 1 and second_operand == 2:
            strcommand = '2D'
            return strcommand
        elif first_operand == 4 and second_operand == 2:
            strcommand = '80'
            return strcommand
        elif first_operand == 3 and second_operand == 2:
            strcommand = '83'
            return strcommand
        else:
            return 'error'
    return 0


def oper_1(f,command,senline,line,struc_senline):

    operand_variant = ''
    operand_variant2 = ''

    if command == 'ADD' or command == 'AND' or command == 'CMP' or command == 'MOV' or command == 'TEST' or command == 'SUB':
        operand_variant = '8_REG'
        operand_variant2 = '16_REG'



    if Pref_seg(senline[f]) == 0:
        if line[f][-1] is operand_variant:
            if command == 'SUB':
                if line[f][1] == 'AL':
                    return 0
                else:
                    return 4
            return 0
        elif line[f][-1] is operand_variant2:
            if command == 'SUB':
                if line[f][1] == 'AX':
                    return 1
                else:
                    return 3

            return 1
        elif(find_ID(senline[f] )!= 'error'):
           if senline[f+1] == '[' and senline[f + 3] == ']':
               if line[f+2][-1] == operand_variant:
                   return 0
               if line[f+2][-1] == operand_variant2:
                   return 1
        elif line[f][-1] == 'BIN'  or line[f][-1] == 'DEC' or line[f][-1] == 'HEX':
            return 2
        elif line[f][1] == '(' :
            count  = len(senline)
            math = ""
            while(f < count):
                math += senline[f] + " "
                f+=1
            number = int(dexstra(math))
          #  print(number)
            return 2


    else:
        tmp_cod = PREfSEG(senline[f]) + ':'
        if tmp_cod == 'error:':
            return -1
        if (find_ID(senline[f+2])!='error'):
            if senline[f+3] =='[' and senline[f+5] ==']':
                if line[f+4][-1] is operand_variant:
                    if command == 'SUB':
                        if line[f+4][1] == 'AL':
                            tmp_cod + '0'
                        else:
                            tmp_cod + '4'
                    return tmp_cod + '0'
                if line[f+4] [-1]is operand_variant2:
                    if command == 'SUB':
                        if line[f][1] == 'AX':
                            return tmp_cod + '1'
                        else:
                            return tmp_cod + '3'
                    return tmp_cod + '1'
                else :
                    return 'error'
    return 0


def Pref_seg (pref):
    tmp = PREfSEG(pref)
    if tmp != 'error':
        return pref

    return 0


def MEM_Chack(number,type):
    if type == 'DB':
        if(number[-1] == 'H'):
            num = number[:-1]
            if num >= hex(-128) and num <= hex(127):
                return True
        if(number[-1] == 'B'):
            num = number[:-1]
            if num >= bin(-128) and num <= bin(127):
                return True
        if(number[-1] == 'D' or help(number[-1])):
            num = number[:-1]
            if num >= '-128' and num <= '127':
                return True
    if type == 'DW':
        if (number[-1] == 'H'):
            num = number[:-1]
            if num >= hex(-32768) and num <= hex(32767):
                return True
        if (number[-1] == 'B'):
            num = number[:-1]
            if num >= bin(-32768) and num <= bin(32767):
                return True
        if (number[-1] == 'D' or help(number[-1])):
            num = number[:-1]
            if num >= '-32768' and num <= '32767':
                return True
    if type == 'DD':
            if (number[-1] == 'H'):
                num = number[:-1]
                if num >= hex(-2147483648) and num <= hex(-2147483647):
                    return True
            if (number[-1] == 'B'):
                num = number[:-1]
                if num >= bin(-2147483648) and num <= bin(-2147483647):
                    return True
            if (number[-1] == 'D' or help(number[-1])):
                num = number[:-1]
                if num >= '-2147483648' and num <= '2147483647':
                    return True

    return False

def help(helpp):
    i = 0
    while(i < 10):
        if str(i) == helpp:
            return True
        i+=1
    return False

def write_VAR(number,line):
    if line == 'error':
        return 'error'
    if number[-1] == 'H':
        return Normal_var_write(number[:-1])
    if number[-1] == 'B':
        return Normal_var_write(number[:-1])
    if number[-1] == 'D':
        return Normal_var_write(number[:-1])
    return Normal_var_write(number)


def convert_base(num, to_base=10, from_base=16):
    # first convert to decimal number
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    # now convert decimal to 'to_base' base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]



def DecToHex(off):
    dec = hex(off)
    dec = dec.replace("x", "0")
    if len(dec) < 4:
        dec = "0" + dec
    return str(dec.upper())
