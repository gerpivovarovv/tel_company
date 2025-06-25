paswd = '   Asdfg4    '.strip()
simb = ['*', '&', '{', '}', '|', '+']
numbs = [str(i) for i in range(10)]
if len(paswd) < 4 or len(paswd) > 16:
    print('Ошибка кол')
else:
    if paswd == paswd.lower():
        print('Ошибка загл')
    else:
        for i in simb:
            if i in paswd:
                print('Ошибка сим')
                break
            else:
                flag = False
                for j in numbs:
                    if j in paswd:
                        flag = True
                if flag is False:
                    print('Ошибка цифр')
                    break
    print('Ура')
