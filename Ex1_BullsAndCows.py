from random import randint

# Получение случайного(ну типа) числа
game_num = randint(0, 9999)
# Строковый вариант числа вида 0000 - 9999 будет использоваться в операции сравнения
game_str = f'{game_num//1000}{game_num%1000//100}{game_num%100//10}{game_num%10}'

# Количество шагов
steps = 1
# Игровой цикл
while True:
    # Переменные для быков и коров
    bulls, cows = 0, 0
    # Цикл корректного ввода числа
    while True:
        user_num = int(input(f'Шаг: {steps}\n Введите число в диапазоне [0, 9999]: '))
        user_str = f'{user_num//1000}{user_num%1000//100}{user_num%100//10}{user_num%10}'
        # Если введенное число не корректно, ввод повторяется
        if user_num not in range(10000):
            print('Введеное число не входит в запрашиваемый промежуток, введите снова\n')
        else:
            break
    # Если число отгадано вывод количества шагов и прерывание основного цикла
    if user_num == game_num:
        print(f'Вы отгадали! Всего за {steps} шагов!')
        break
    # Вычисление "коров" и "быков"
    else:
        for char in user_str:
            if game_str[user_str.index(char)] == char:
                bulls += 1
            elif char in game_str:
                cows += 1
    # Вывод количества совпадений
    print(f'{bulls} быков и {cows} коров!')
    steps += 1
