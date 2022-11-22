import os
import argparse
import search
import random
import re

from colorama import init
from typing import Union


def reading_file(file_name: str = "") -> Union[str, bool]:
    """Чтение строки из файла"""
    file_strings = ""
    string = ""
    if not file_name:
        file_name = input("Введите имя файла (с расширением), откуда нужно считать строку: ")

    if not os.path.exists(file_name):
        print("Такого файла не существует.")
        return False

    with open(file_name, "r", encoding='utf-8') as file:
        for line in file:
            file_strings += line

    if file_strings and file_strings != " " * len(file_strings):
        string = ''.join(file_strings.split("\n"))

    print("Считано из файла: ")
    print(string)

    return string


def check_fields(string: str, lst_sub_strings: Union[str, list[str]],
                 case_sensitivity: bool, method: str, count: int) -> bool:
    """Проверка наличия значений у полей"""
    empty_fields = []
    if not string:
        empty_fields.append("Строка для поиска")

    if not lst_sub_strings:
        empty_fields.append("Подстроки для поиска")

    if case_sensitivity not in (True, False):
        empty_fields.append("Чувствительность к регистру")

    if not method:
        empty_fields.append("Метод поиска")

    if not count:
        empty_fields.append("Количество вхождений")

    if empty_fields:
        print("У вас отсутствуют следующие поля:")
        for field in empty_fields:
            print(f"\t{field}")
        return False

    return True


def colored_print_tuple(string: str, all_sub_strings: Union[str, list[str]], result: Union[None, tuple, dict]) -> None:
    """Вывод для того случая, когда передана одна подстрока"""

    output_string = ""
    color = random.randint(31, 36)  # Берём все цвета, кроме чёрного и белого
    coloring_indexes = []  # Индексы символов, которые мы будем раскрашивать

    # Получаем индексы символов, которые мы будем раскрашивать
    for i in result:
        for j in range(i, i + len(all_sub_strings)):
            coloring_indexes.append(j)

    # Получаем пару (индекс, символ)
    for letter in enumerate(string):
        # Если символ по этому индексу необходимо раскрасить
        if letter[0] in coloring_indexes:
            letter = list(letter)

            output_string += f"\033[{color}m {letter[1]}\033[0m".replace(' ', '')
            continue

        output_string += letter[1]

    print("Найденные подстроки:")
    print(output_string)
    print("Набор индексов начала каждой подстроки:")
    print(f"\033[{color}m{result}\033[0m")


def colored_print_dict(string: str, result: Union[None, tuple, dict]) -> None:
    """Печать нескольких подстрок"""
    count_row = 0  # Количество строк, которое выводится

    for key in result:  # Получаем ключи словаря

        count_row += 1

        if count_row > 10:  # Ограничение на количество выводимого текста
            break

        output_string = ""
        color = random.randint(31, 36)  # Берём все цвета, кроме чёрного и белого
        coloring_indexes = []  # Индексы символов, которые мы будем раскрашивать

        if result[key]:  # Если подстрока найдена

            # Получаем индексы символов, которые мы будем раскрашивать
            for i in result[key]:
                for j in range(i, i + len(key)):
                    coloring_indexes.append(j)

            # Получаем пару (индекс, символ)
            for letter in enumerate(string):
                if letter[0] in coloring_indexes:
                    letter = list(letter)

                    output_string += f"\033[{color}m {letter[1]}\033[0m".replace(' ', '')
                    continue

                output_string += letter[1]

            print("Найденные подстроки:")
            print(output_string)
            print("Набор индексов начала каждой подстроки:")
            print(f"\033[{color}m{key}: {result[key]}\033[0m")

        else:
            print("Найденные подстроки:")
            print(string)
            print("Найденные подстроки:")
            print(f"\033[{color}m{key}: {result[key]}\033[0m")


def colored_output(string: str, all_sub_strings: Union[str, list[str]], result: Union[None, tuple, dict]) -> None:
    """Красивый вывод строк"""
    if isinstance(result, tuple):
        colored_print_tuple(string, all_sub_strings, result)
    else:
        colored_print_dict(string, result)


def search_substring_in_string(string: str, sub_strings: Union[str, list[str]],
                               case_sensitivity: bool, method: str, count: int) -> None:
    """Вызов функции поиска из модуля"""

    if len(sub_strings) == 1:
        all_sub_strings = sub_strings[0]
    else:
        all_sub_strings = tuple(sub_strings)

    result = search.search(string, all_sub_strings, case_sensitivity, method, count)

    if not result:
        print("Подстроки не найдены.")

    colored_output(string, all_sub_strings, result)


def parse_args() -> Union[bool, str]:
    """Обработка параметров командной строки"""

    # Осуществляем разбор аргументов командной строки
    parser = argparse.ArgumentParser(description="Получение параметров для поиска подстроки в введённой строке")

    parser.add_argument("-f", "--file", type=str, dest="file", help="Путь до файла")
    parser.add_argument("-s", "--string", type=str, dest="string", help="Исходная строка")
    parser.add_argument("-ss", "--sub_string", type=str, dest="sub_string",
                        help="Одна или несколько подстрок, которые необходимо найти")
    parser.add_argument("-cs", "--case_sensitivity", type=bool, dest="case_sensitivity",
                        help="Чувствительность к регистру", default=True)
    parser.add_argument("-m", "--method", type=str, dest="method", help="Метод поиска")
    parser.add_argument("-c", "--count", type=int, dest="count", help="Количество совпадений, которое нужно найти")
    args = parser.parse_args()  # В эту переменную попадает результат разбора аргументов командной строки.

    if_args = bool(args.file) + bool(args.string) + bool(args.sub_string) + bool(args.method) + bool(args.count)

    if not if_args:
        # Если параметры командной строки не переданы
        return "no_args"

    if not (args.string or args.file):
        # Если не была передана строка или путь к файлу
        print("Укажите строку или путь к файлу.")
        return False

    if not args.sub_string:
        print("Укажите подстроки, которые необходимо искать.")
        return False

    if not args.method:
        print("Укажите метод поиска.")
        return False

    if not args.count:
        print("Укажите количество совпадений, которое нужно найти.")
        return False

    string = ""

    if args.string:
        string = args.string

    elif args.file:
        string = reading_file(args.file)
        if not string:
            return False

    sub_strings = args.sub_string.replace(" ", "").split(",")

    case_sensitivity = None

    if args.case_sensitivity is bool:
        case_sensitivity = args.case_sensitivity

    method = None

    if args.method in ("first", "last"):
        method = args.method

    count = 0

    if args.count > 0:
        count = args.count

    search_substring_in_string(string, sub_strings, case_sensitivity, method, count)
    return True


def parameters_output(string: str, sub_strings: Union[str, list[str]],
                      case_sensitivity: bool, method: str, count: int) -> None:
    """Печать настроек поиска"""
    print(f"Строка: {string};")
    print("Подстроки:")
    for sub_string in enumerate(sub_strings):
        print(f"{sub_string[1]};")
    print(f"Чувствительность к регистру: {case_sensitivity};")
    print(f"Количество вхождений подстроки в строку, которое нужно найти: {count};")
    print(f"Метод поиска: {method};")


def get_string_menu() -> None:
    """Вывод меню для выбора ввода строки"""
    print("1 - Ввести строку вручную;")
    print("2 - Считать строку из файла.")


def get_string() -> str:
    """Получение строки"""
    string = ""
    pattern = re.compile("^[a-zA-Z]+$")
    get_string_menu()

    choice = input("Введите желаемый номер команды: ")

    while not string:
        if choice == "1":
            string = input("Введите строку, в которой будет производиться поиск подстрок: ")
            is_valid = False
            while not is_valid:
                if not string.strip(" ") or not pattern.match(string):
                    print("Введите нормальную строку.")
                    string = input("Введите строку, в которой будет производиться поиск подстрок: ")
                else:
                    is_valid = True

        elif choice == "2":
            result = reading_file(string)
            while not pattern.match(result):
                print("Недопустимый ввод. Попробуйте снова.")
                result = reading_file(string)
            if result:
                string = result

        else:
            print("Такого пункта нет")
            choice = input("Введите желаемый номер команды: ")

    return string


def get_sub_string() -> Union[str, list[str]]:
    """Получение подстроки"""
    pattern = re.compile("^[a-zA-Z]+$")
    sub_strings = []
    sub_string_entered = input("Введите строки, которые нужно искать в строке (нажмите Enter для остановки): ")
    while sub_string_entered != "" or not sub_strings:
        if sub_string_entered != "":
            if sub_string_entered and sub_string_entered != " " * len(sub_string_entered) and pattern.match(
                    sub_string_entered):
                sub_strings.append(sub_string_entered.strip(" "))
            else:
                print("Недопустимый ввод. Попробуйте снова.")

        sub_string_entered = input(
            "Введите строки, которые нужно искать в строке (нажмите Enter для остановки): ")

    return sub_strings


def get_case_sensitivity() -> bool:
    """Получение параметра чувствительности к регистру"""

    choice = input("Поиск должен быть чувствителен к регистру (True) или нет (False): ")
    while choice not in ["True", "False"]:
        print("Введено неверное значение. Попробуйте снова.")
        choice = input("Поиск должен быть чувствителен к регистру (True) или нет (False): ")

    if choice == "True":
        case_sensitivity = True
    else:
        case_sensitivity = False

    return case_sensitivity


def get_count() -> int:
    """Получение параметра количества совпадений, которые нужно найти"""
    choice = input("Введите количество совпадений, которые нужно найти: ")
    while not choice.isnumeric() or int(choice) <= 0:
        print("Введено неверное значение. Попробуйте снова.")
        choice = input("Введите количество совпадений, которые нужно найти: ")

    count = int(choice)
    return count


def get_method() -> str:
    """Получение параметра метода поиска"""
    choice = input("Поиск должен быть с начала (first) или с конца (last): ")

    while choice not in ["first", "last"]:
        print("Введено неверное значение. Попробуйте снова.")
        choice = input("Поиск должен быть с начала (first) или с конца (last): ")

    method = choice
    return method


def start_search(string: str, sub_strings: Union[str, list[str]],
                 case_sensitivity: bool, method: str, count: int) -> None:
    """Вызов поиска"""
    item = sub_strings[0] if len(sub_strings) == 1 else tuple(sub_strings)
    return_data = search.search(string, item, case_sensitivity, method, count)
    if not return_data:
        print("Данной подстроки нет в строке")
    colored_output(string, item, return_data)


def menu() -> None:
    """Меню программы"""
    print("    Меню программы")
    print("1 - Ввод параметров;")
    print("2 - Просмотр введённых параметров;")
    print("3 - Поиск;")
    print("4 - Выход из программы.")


def main() -> None:
    """Точка входа"""

    message = "Введите желаемый номер команды: "
    command_numb = 0

    init()  # Инициализируем Colorama

    string, method = "", ""
    sub_strings = []
    case_sensitivity = ""
    count = 0

    if_parse = parse_args()

    while command_numb != "4" and if_parse == "no_args":
        menu()  # Вызов меню
        command_numb = input(message)

        if command_numb == "1":  # Ввод параметров
            string = get_string()
            sub_strings = get_sub_string()
            case_sensitivity = get_case_sensitivity()
            count = get_count()
            method = get_method()

        elif command_numb == "2":
            if not string:
                print("Параметры ещё не введены.")
            else:
                parameters_output(string, sub_strings, case_sensitivity, method, count)

        elif command_numb == "3":
            if not string:
                print("Параметры ещё не введены.")
            else:
                search_substring_in_string(string, sub_strings, case_sensitivity, method, count)

        elif command_numb == "4":
            print("Завершение программы...")

        else:
            print("Введено неверное значение, попробуйте снова.")


if __name__ == '__main__':
    main()
