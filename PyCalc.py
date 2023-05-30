from math import pi, e
from re import compile, sub


def throwException(warning: str) -> None:
    """
    Функция для отображения ошибок на консоли, вместо прерывания цикла с помощью raise
    """
    print("stderr: {}".format(warning))


def constantCoding(expression: str) -> 'str, None':
    """
    Функция проверяет выражение на наличие лишних символов и заменяет константы(pi && e)
        (временно для проверки регулярными выражениями) на pi >> $$, e >> @ 
    """
    if '@' in expression or '$' in expression:
        return None
    return sub(r'pi', '$$', sub(r'e', '@', expression))


_syntaxCheckers_ = {
    'undefined symbols': compile(r'[^0-9.()*/\-+%@$]'),   # 0-9, '.', '(', ')', '*', '/', '-', '+', '%', '\s', '@', '$'
    'repeating operations': compile(r'[+\-]{2,}|\.{2,}')  # '+', '-', '.'
}


def checkingExpression(expression: str) -> bool:
    """
    Функция для проверки выражения на наличие других символов,
        кроме: 0-9, '.', '(', ')', '*', '/', '-', '+', '%', '\s', '@', '$'.
        Так же проверяется, не повторяются ли подряд '+', '-', '.' 
    """
    buffer = constantCoding(expression)
    if buffer is None:
        return False
    buffer = sub(r'\s', '', buffer)
    undefinedSymbols = syntaxCheckers['undefined symbols'].search(buffer)
    repeatingOperators = syntaxCheckers['repeating operations'].search(buffer)
    return undefinedSymbols is None and repeatingOperators is None


_testList_ = [
    '2+2', '2 * 3', '1 / (-23)', '(-2) // 4', 'pi * (2)', '2+2*2', '2*2()', '1/0', 'sdsds+ sdg', '2 ++ 2', '2 ** 2',
    '2 -- 2', '2 //// 2', '2%3'
]


if __name__ == '__main__':
    print(' /* NOTE: for negative number use brackets like that "(-n)" */')
    while True:
        cin = input(' >>> Input expression: ')
    # for cin in testList:
        if cin == 'quit':
            break
        # print(' >>> Input expression:', cin)
        if checkingExpression(cin):
            try:
                print('result = ' + str(eval(cin, {'pi': pi, 'e': e})))
            except Exception as ex:
                throwException('[{}] Don`t undestand, try again'.format(str(type(ex))[8:-2]))
        else:
            throwException("[SyntaxError] Don`t undestand, try again")
        print()

