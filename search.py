from collections import deque

import time

import logging

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

    def __init__(self, keywords, lowercase=False):
        """ creates a trie of keywords, then sets fail transitions
        :param keywords: trie of keywords
        :param lowercase: convert all strings to lower case
        """
        """
        Алгоритм Ахо-Корасика
        :param keywords: дерево бора.
        :param lowercase
        """

        self.lowercase = lowercase

        # initalize the root of the trie
        self.AdjList = list()
        self.AdjList.append({'value': '', 'next_states': [], 'fail_state': 0, 'output': []})

        self.add_keywords(keywords)
        self.set_fail_transitions()

    def add_keywords(self, keywords):
        """ Добавляем все подстроки в список подстрок """
        for keyword in keywords:
            self.add_keyword(keyword)

    def add_keywords_and_values(self, kvs):
        """ add all keywords and values in list of (k,v) """
        for k, v in kvs:
            self.add_keyword(k)

    def find_next_state(self, current_state, value):
        for node in self.AdjList[current_state]["next_states"]:
            if self.AdjList[node]["value"] == value:
                return node
        return None

    def add_keyword(self, keyword):
        """ add a keyword to the trie and mark output at the last node """
        current_state = 0
        j = 0
        if self.lowercase: keyword = keyword.lower()
        child = self.find_next_state(current_state, keyword[j])
        while child != None:
            current_state = child
            j = j + 1
            if j < len(keyword):
                child = self.find_next_state(current_state, keyword[j])
            else:
                break
        for i in range(j, len(keyword)):
            node = {'value': keyword[i], 'next_states': [], 'fail_state': 0, 'output': []}
            self.AdjList.append(node)
            self.AdjList[current_state]["next_states"].append(len(self.AdjList) - 1)
            current_state = len(self.AdjList) - 1
        self.AdjList[current_state]["output"].append(keyword)

    def set_fail_transitions(self):
        q = deque()
        child = 0
        for node in self.AdjList[0]["next_states"]:
            q.append(node)
            self.AdjList[node]["fail_state"] = 0
        while q:
            r = q.popleft()
            for child in self.AdjList[r]["next_states"]:
                q.append(child)
                state = self.AdjList[r]["fail_state"]
                while self.find_next_state(state, self.AdjList[child]["value"]) is None and state != 0:
                    state = self.AdjList[state]["fail_state"]
                self.AdjList[child]["fail_state"] = self.find_next_state(state, self.AdjList[child]["value"])
                if self.AdjList[child]["fail_state"] is None:
                    self.AdjList[child]["fail_state"] = 0
                self.AdjList[child]["output"] = self.AdjList[child]["output"] + \
                                                self.AdjList[self.AdjList[child]["fail_state"]]["output"]

    def get_keywords_found(self, line):
        """ returns true if line contains any keywords in trie, format: (start_idx,kw,value) """
        if self.lowercase:
            line = line.lower()
        current_state = 0
        keywords_found = []

        for i in range(len(line)):
            while self.find_next_state(current_state, line[i]) is None and current_state != 0:
                current_state = self.AdjList[current_state]["fail_state"]
            current_state = self.find_next_state(current_state, line[i])
            if current_state is None:
                current_state = 0
            else:
                for k in self.AdjList[current_state]["output"]:
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
        sub_string_new = tuple([sub_string])
        trie = AhoCorasickTree(sub_string_new)
    else:
        trie = AhoCorasickTree(sub_string)

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
