import re
import string
import data

def ParseFileToList(line):
    lst = line.split(' ')
    i = 0
    count = len(lst)
    while i < count:
        lst[i] = lst[i].upper()
        if re.match('\'.*',lst[i]) or re.match('".*',lst[i]):
            lst[i] += ' ' + lst[i+1]
            lst.pop()
            count -= 1
            lst[i] = lst[i].lower()

        if re.search('.([:\\+\\*\\[\\]\\(\\),])',lst[i]):
            pat = '([{}])'.format(re.escape(string.punctuation))
            buf = lst[i+1:count]
            s = lst[i]
            DelFromList(lst,i,count-1)
            tmp = re.split(pat, s)

            for node in tmp:
                if node == '':
                    tmp.remove(node)
            lst.extend(tmp)
            lst.extend(buf)
            count = len(lst)

        i+=1
    i=0
    while i < len(lst):
        if lst[i] == '':
            lst.remove(lst[i])
        else:
            i+=1
    return lst

def SetLexemeType(lexeme):
  if lexeme == '':
    return 'empty_line'
  _type = ''
  for t in data.Lexemes:
    lexLst = re.findall(data.Lexemes[t], lexeme)
    if len(lexLst) > 0 and lexLst[0] == lexeme:
      _type = t
      return _type
    else:
      lexLst = re.findall('[A-Z][0-9A-Z]{0,5}', lexeme)
      if len(lexLst) > 0 and lexLst[0] == lexeme:
        _type = 'ID'
  if _type == 'ID' and len(lexeme) > 6:
    data.stopflag = True
    return 'error'
  if _type == '':
    data.stopflag = True
    _type = 'error'
  return _type



def DelFromList(lst, start, count):
  while start <= count:
    lst.pop()
    start += 1