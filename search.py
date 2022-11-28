from collections import deque

import time

import logging
from typing import Union

logging.basicConfig(
    level=logging.DEBUG,
    filename='myProgramLog.txt',
    format=' %(asctime)s - %(levelname)s - %(message)s')


def timeit(method):
    """Логирует время работы функции"""

    def timed(*args):
        ts = time.perf_counter()
        result = method(*args)
        te = time.perf_counter()
        running_time = f"{te - ts:0.4f}"

        logging.debug('%r %r %r sec' % (method.__name__, args, running_time))
        return result

    return timed


class AhoCorasickTree(object):

    def __init__(self, keywords: list) -> None:
        """
        Алгоритм Ахо-Корасика
        :param keywords: дерево бора.
        """

        # Инициализируем корневой узел
        self.AhoCorasickList = list()
        self.AhoCorasickList.append({'value': '', 'next_states': [], 'suff_link': 0, 'output': []})

        self.add_keywords(keywords)  # Добавляем все подстроки
        self.set_suf_link()  # переходы

    def add_keywords(self, keywords: list) -> None:
        """ Добавляем все подстроки в список подстрок """
        for keyword in keywords:
            self.add_keyword(keyword)

    def find_next_state(self, current_state, value) -> Union["node", None]:
        """Находим следующее состояние"""
        for node in self.AhoCorasickList[current_state]["next_states"]:
            if self.AhoCorasickList[node]["value"] == value:
                return node
        return None

    def add_keyword(self, keyword: str) -> None:
        """Добавляем подстроки в дерево и помечаем терминальные точки"""
        current_state = 0
        index = 0
        child = self.find_next_state(current_state, keyword[index])
        while child is not None:
            current_state = child
            index = index + 1
            if index < len(keyword):
                child = self.find_next_state(current_state, keyword[index])
            else:
                break

        for i in range(index, len(keyword)):
            node = {'value': keyword[i], 'next_states': [], 'suff_link': 0, 'output': []}
            self.AhoCorasickList.append(node)
            self.AhoCorasickList[current_state]["next_states"].append(len(self.AhoCorasickList) - 1)
            current_state = len(self.AhoCorasickList) - 1

        self.AhoCorasickList[current_state]["output"].append(keyword)

    def set_suf_link(self) -> None:
        """Устанавливаем суффиксные ссылки"""
        new_deque = deque()

        for node in self.AhoCorasickList[0]["next_states"]:
            new_deque.append(node)
            self.AhoCorasickList[node]["suff_link"] = 0

        while new_deque:
            tmp = new_deque.popleft()

            for child in self.AhoCorasickList[tmp]["next_states"]:
                new_deque.append(child)
                state = self.AhoCorasickList[tmp]["suff_link"]

                while self.find_next_state(state, self.AhoCorasickList[child]["value"]) is None and state != 0:
                    state = self.AhoCorasickList[state]["suff_link"]

                self.AhoCorasickList[child]["suff_link"] = self.find_next_state(state,
                                                                                self.AhoCorasickList[child]["value"])

                if self.AhoCorasickList[child]["suff_link"] is None:
                    self.AhoCorasickList[child]["suff_link"] = 0

                self.AhoCorasickList[child]["output"] = self.AhoCorasickList[child]["output"] + \
                                                        self.AhoCorasickList[self.AhoCorasickList[child]["suff_link"]][
                                                            "output"]

    def get_keywords_found(self, line):
        """Возвращает индекс, где нашлась подстрока, в формате (индекс начала, значение подстроки)"""

        current_state = 0
        keywords_found = []

        for i in range(len(line)):

            while self.find_next_state(current_state, line[i]) is None and current_state != 0:
                current_state = self.AhoCorasickList[current_state]["suff_link"]
            current_state = self.find_next_state(current_state, line[i])

            if current_state is None:
                current_state = 0
            else:
                for k in self.AhoCorasickList[current_state]["output"]:
                    keywords_found.append((i - len(k) + 1, k))

        return keywords_found


@timeit
def search(string: str, sub_string: str or tuple, case_sensitivity: bool, method: str, count: int):
    """Шаблон функции поиска"""

    if not case_sensitivity:
        string = string.lower()

        if isinstance(sub_string, tuple):
            sub_string = tuple([word.lower() for word in sub_string])
        else:
            sub_string = sub_string.lower()

    if isinstance(sub_string, str):
        sub_string_new = [sub_string]
        trie = AhoCorasickTree(sub_string_new)
    else:
        trie = AhoCorasickTree(list(sub_string))

    result = trie.get_keywords_found(string)

    if isinstance(sub_string, tuple):
        counter = 0

        if method == "last":
            result = result[::-1]

        information = dict()
        for word in sub_string:
            information[word] = []

        for pair in result:
            counter += 1
            if counter <= count:
                information[pair[1]].append(pair[0])

        for key, item in information.items():
            if item:
                information[key] = tuple(item)
            else:
                information[key] = None
    else:
        information = []

        for item in result:
            information.append(item[0])

        if method == "last":
            information = list(information[::-1])[:count]
        elif method == "first":
            information = list(information[:count])

        if information:
            information = tuple(information)

    if len(information) == 0:
        information = None
    elif isinstance(information, dict):
        is_value = False
        for _, value in information.items():
            if value is not None:
                is_value = True
        if not is_value:
            information = None

    return information
