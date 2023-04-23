import os
import data
import lex as LexAn
import syntax


def main():
   # syntax.MEM_Chack('107H','DW')
    #print(data.tablet_segment)
    #teste = syntax.MEM_Chack(123,'DB','HEX')
    asm_file = open(data.WAYTOASM)
    tmp_file = open(data.WAYTOLST,'w')
    count_line = 0
    j = 0
    ListOfSen = []
    SenLine_string = []
    SenLine_offset = []
    under  = 0
    Tabl_ID =[]

    offset = []


    #tmp_file.write("0000")
    for line in asm_file:
        line = line.replace('\n',''). replace('\t','')
        lst = LexAn.ParseFileToList(line)

        if len(lst) == 0:
            continue
       # tmp_file.write(line)
      #  tmp_file.write('\n')
        SenLine = []
        SenLine.append([line])
        i = 0
        count = len(lst)
        newsenline = []
        k = 1
        while i < count:
            _type = LexAn.SetLexemeType(lst[i])
            SenLine.append([lst[i], _type])
            i += 1

           # tmp_file.write(str(i))
            #tmp_file.write('\t')
            #tmp_file.write(lst[i-1])
            #tmp_file.write('\t')
            #if _type != "error" :
            #    tmp_file.write(str(len(lst[i-1])))
            #tmp_file.write('\t')
            #tmp_file.write(_type)
            newsenline.append([str(i),lst[i-1],_type])
            #tmp_file.write('  \n')


           # print(SenLine[1:])
           # ListOfSen.append(syntax.SenLine(SenLine[1:]))
            #print(syntax.isStartSegment(ListOfSen[j]))
            #ListOfSen[j].SyntaxSize()
            #you = syntax.DecToHex(ListOfSen[j].getOffset())
            #SenLine_offset.append(you)
            #SenLine_string.append(SenLine[0][0])
            #print(you)
            #print(SenLine[0][0])
            j += 1

          #  if (data.stopflag == True):
           #     print('(! Error on line {0})'.format(j + 1), file=tmp_file)
            #    break
       # tmp_file.write('\n')
     #   offset.append('0000')
      #  offset.extend(SenLine_offset)
        # offset.pop()
       # print(newsenline)
        Asew = syntax.Syntax(newsenline)
       # tmp_file.write(Asew)


        #tmp_file.write('\n\n')
        if i == 0:
            print("0000"+"\t"+line+"\n")
        else:
           # print(off + "\t" + line + "\n")
            off = syntax.sen_offset(lst,Asew, under,newsenline)
           # syntax.Second(lst,Asew, under,newsenline)
           # print(syntax.varrr)
           # print(syntax.code_command)
            if off  == -1:
                break
            under = syntax.convert_base(off)
           # print(off + "\t" + line + "\n")
            under = int(under)
 #   while()
    asm_file.close()
    tmp_file.close()
    asm_file = open(data.WAYTOASM)
    tmp_file = open(data.WAYTOLST, 'w')
    under = 0
    for line in asm_file:
        line = line.replace('\n',''). replace('\t','')
        lst = LexAn.ParseFileToList(line)

        if len(lst) == 0:
            continue
        SenLine = []
        SenLine.append([line])
        i = 0
        count = len(lst)
        newsenline = []
        k = 1
        while i < count:
            _type = LexAn.SetLexemeType(lst[i])
            SenLine.append([lst[i], _type])
            i += 1

            newsenline.append([str(i),lst[i-1],_type])
            j += 1
        Asew = syntax.Syntax(newsenline)

        if i == 0:
            print("0000"+"\t"+line+"\n")
        else:
           # print(off + "\t" + line + "\n")
            off = syntax.sen_offset(lst,Asew, under,newsenline)
            syntax.Second(lst,Asew, under,newsenline)

            if off  == -1:
                break
            under = syntax.convert_base(off)
           # print(off + "\t" + line + "\n")
            under = int(under)

  #  print(syntax.tuor)
  #  print(syntax.OFFSET)
  #  print(syntax.T_D)


    #print(syntax.varrr)
    #print(syntax.code_command)
    tmp_file.write(syntax.PRINT_LST())
    tmp_file.write("\nNAME\t\t\tTYPE\t\tVALUE\t\tATTR\t\t\n")
    tmp_file.write(syntax.PRINT_TABL_IDENT())
    tmp_file.write("\nNAME\t\t\tSIZE\t\tLENGTH\t\tCOMBINE CLASS\t\t\n")
    tmp_file.write(syntax.PRINT_SEGS())
    #print(syntax.OFFSET)
   # print(syntax.SEGment)
    #print(data.tablet_segment)

main()