"""Шаблон модуля search"""


def char_num(char) -> int:
    # Возвращает номер символа в латинском алфавите

    if char.lower() != char:
        return ord(char) - 39
    return ord(char) - ord('a')


class Vertex:
    def __init__(self, id_vertex, alph_size, parent, char_to_parent) -> None:
        self.id = id_vertex  # id_vertex узла
        self.son = [None] * alph_size  # Список переходов в рамках бора (список сыновей)
        self.is_terminal = False  # Флаг того, заканчивается ли строка в этой вершине
        self.parent = parent  # Родитель узла
        self.char_to_parent = char_to_parent  # По какому символу мы пришли (символ до родителя)
        self.suff_link = None  # Храним суффиксную ссылку
        self.go = [None] * alph_size  # Вычисляемые переходы


class AhoCorasickTree:
    def __init__(self, alph_size) -> None:
        self.alph_size = alph_size  # Размер алфавита данного бора, от алфавита зависит то, сколько переходов
        self.vertices = [Vertex(0, alph_size, None, None)]  # Список вершин, добавляем в него корень дерева
        self.root = self.vertices[0]

    def size(self) -> int:
        # Размер нашего бора, сколько в нём вершин
        return len(self.vertices)

    def last(self) -> Vertex:
        # Последняя добавленная вершина
        return self.vertices[-1]

    def add(self, string) -> None:
        # Функция добавления строки в бор
        vertex = self.root
        for index in range(len(string)):
            char_index = char_num(string[index])
            if vertex.son[char_index] is None:  # Если перехода нет
                # Вставляем новую вершину
                self.vertices.append(Vertex(self.size(), self.alph_size, vertex, string[index]))
                vertex.son[char_index] = self.last()
            # Идём по ней
            vertex = vertex.son[char_index]
        # Помечаем, что эта вершина конечная
        vertex.is_terminal = True

    def get_suff_link(self, vertex) -> Vertex:
        # Получение ссылки
        # Вычисляет суффиксную ссылку из нашей вершины
        if vertex.suff_link is None:
            if vertex == self.root or vertex.parent == self.root:
                vertex.suff_link = self.root
            else:
                vertex.suff_link = self.get_link(self.get_suff_link(vertex.parent), vertex.char_to_parent)
        return vertex.suff_link

    def get_link(self, vertex, char) -> Vertex:
        # Получение перехода
        char_index = char_num(char)
        if vertex.go[char_index] is None:
            # Если есть переход по ребру бора
            if vertex.son[char_index]:
                # Это и есть наш переход
                vertex.go[char_index] = vertex.son[char_index]
            # Если перехода по бору нет, и мы находимся в корне
            elif vertex == self.root:
                vertex.go[char_index] = self.root
            # Мы стоим не в корне и хотим перейти из нас
            # Перейдем по суффиксной ссылке и оттуда попробуем
            # перейти по нашему символу char
            else:
                vertex.go[char_index] = self.get_link(self.get_suff_link(vertex), char)

        return vertex.go[char_index]

    """
    def find(self, string):
        # Функция нахождения в боре
        vertex = self.root
        for index in range(len(string)):
            if vertex.son[char_num(string[index])] is None:
                # Если символа нет, значит такой строки в боре нет
                return False
            vertex = vertex.son[char_num(string[index])]
        return vertex.is_terminal
    """


def search(string: str, sub_string: str or tuple, case_sensitivity: bool, method: str, count: int):
    """Шаблон функции поиска"""

    if not case_sensitivity:
        string = string.lower()

        if isinstance(sub_string, tuple):
            sub_string = tuple([word.lower() for word in sub_string])
        else:
            sub_string = sub_string.lower()

    alphabet_size = 52
    trie = AhoCorasickTree(alphabet_size)

    if isinstance(sub_string, tuple):
        for word in sub_string:
            trie.add(word)
    else:
        trie.add(sub_string)

    vertex = trie.root
    result = []
    for index in range(len(string)):
        vertex = trie.get_link(vertex, string[index])
        if vertex.is_terminal:
            result.append(index + 1 - len(sub_string))
            if method == 'first' and len(result) == count:
                break

    if method == 'last':
        result = list(result[::-1])[:count]

    if len(result) == 0:
        return None
    return tuple(result)
