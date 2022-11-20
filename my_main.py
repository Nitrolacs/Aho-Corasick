import os
import argparse
import search

from colorama import init
from typing import Union


def reading_file(file_name: str = "") -> Union[str, bool]:
    """Чтение строки из файла"""
    file_strings = ""
    string = ""

    if not os.path.exists(file_name):
        print("Такого файла не существует.")
        return False

    with open(file_name, "r", encoding='utf-8') as file:
        for line in file:
            file_strings += line

    if file_strings and file_strings != " " * len(file_strings):
        string = ''.join(file_strings.split("\n"))

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


def colored_output(string: str, all_sub_strings: Union[str, list[str]], result: Union[None, tuple, dict]) -> None:
    """Красивый вывод строк"""
    if isinstance(result, tuple):
        print_tuple(string, all_sub_strings, result)
    else:
        print_dict(string, result)


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

    sub_strings = args.sub_string.split(",")

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


def menu() -> None:
    """Меню программы"""
    print("    Меню программы")
    print("1 - Ввод параметров;")
    print("2 - Поиск;")
    print("3 - Выход из программы.")


def main() -> None:
    """Точка входа"""

    message = "Введите желаемый номер команды: "
    command_numb = 0

    init()  # Инициализируем Colorama

    string, method = "", ""
    sub_strings = []
    case_sensitivity = True
    count = 0

    if_parse = parse_args()

    while command_numb != "3" and if_parse == "no_args":
        menu()  # Вызов меню
        command_numb = input(message)
        if command_numb == "1":  # Ввод параметров
            change = ""
            all_field = check_fields(string, sub_strings, case_sensitivity, method, count)
            if all_field:
                print("Имеющиеся настройки: ")
                print_settings(string, sub_strings, case_sensitivity, method, count)
                while change not in ("y", "n"):
                    print("Введите корректное значение. ")
                    change = input("Желаете изменить параметры?(y/n) ").lower()

            if all_field is False or change == "y":
                string = get_string(string)
                lst_sub_strings = get_sub_string(sub_strings)
                case_sensitivity = get_case_sensitivity(case_sensitivity)
                count = get_count(count)
                method = get_method(method)

        elif command_numb == "2":
            search_def(string, sub_strings, case_sensitivity, method, count)

        elif command_numb == "3":
            print("Завершение программы...")

        else:
            print("Введено неверное значение, попробуйте снова.")


if __name__ == '__main__':
    main()
