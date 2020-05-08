#!/usr/bin/env python3


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class ParentList:
    HEAD_STATUS_OK = 0
    HEAD_STATUS_FAIL = 1
    TAIL_STATUS_OK = 0
    TAIL_STATUS_FAIL = 1
    RIGHT_STATUS_OK = 0
    RIGHT_STATUS_FAIL = 1
    PUT_RIGHT_STATUS_OK = 0
    PUT_RIGHT_STATUS_FAIL = 1
    PUT_LEFT_STATUS_OK = 0
    PUT_LEFT_STATUS_FAIL = 1
    REMOVE_STATUS_OK = 0
    REMOVE_STATUS_FAIL = 1
    REPLACE_STATUS_OK = 0
    REPLACE_STATUS_FAIL = 1
    FIND_STATUS_OK = 0
    FIND_STATUS_FAIL = 1
    GET_STATUS_OK = 0
    GET_STATUS_FAIL = 1

    # конструктор
    # постусловие: создан новый пустой список
    def __init__(self):
        self.clear()

    # команды
    # предусловие: список не пуст;
    # постусловие: курсор установлен на первый узел в списке
    def head(self):
        if self.__head__ is not None:
            self.__cursor__ = self.__head__
            self.__head_status__ = self.HEAD_STATUS_OK
        else:
            self.__head_status__ = self.HEAD_STATUS_FAIL

    # предусловие: список не пуст;
    # постусловие: курсор установлен на последний узел в списке
    def tail(self):
        if self.__tail__ is not None:
            self.__cursor__ = self.__tail__
            self.__tail_status__ = self.TAIL_STATUS_OK
        else:
            self.__tail_status__ = self.TAIL_STATUS_FAIL

    # предусловие: правее курсора есть элемент;
    # постусловие: курсор сдвинут на один узел вправо
    def right(self):
        if self.is_value() and self.__cursor__.next is not None:
            self.__cursor__ = self.__cursor__.next
            self.__right_status__ = self.RIGHT_STATUS_OK
        else:
            self.__right_status__ = self.RIGHT_STATUS_FAIL

    # предусловие: список не пуст;
    # постусловие: следом за текущим узлом добавлен новый узел с заданным значением
    def put_right(self, value):
        if self.is_value():
            node = Node(value)
            node.next = self.__cursor__.next
            node.prev = self.__cursor__
            self.__cursor__.next = node
            if node.next is None:
                self.__tail__ = node
            else:
                node.next.prev = node
            self.__put_right_status__ = self.PUT_RIGHT_STATUS_OK
        else:
            self.__put_right_status__ = self.PUT_RIGHT_STATUS_FAIL

    # предусловие: список не пуст;
    # постусловие: перед текущим узлом добавлен новый узел с заданным значением
    def put_left(self, value):
        if self.is_value():
            node = Node(value)
            node.next = self.__cursor__
            node.prev = self.__cursor__.prev
            self.__cursor__.prev = node
            if node.prev is None:
                self.__head__ = node
            else:
                node.prev.next = node
            self.__put_left_status__ = self.PUT_LEFT_STATUS_OK
        else:
            self.__put_left_status__ = self.PUT_LEFT_STATUS_FAIL

    # предусловие: список не пуст;
    # постусловие: текущий узел удалён, курсор смещён к правому соседу, если он есть,
    # в противном случае курсор смещён к левому соседу, если он есть
    def remove(self):
        if self.is_value():
            node = self.__cursor__
            self.__cursor__ = None
            if node.prev is not None:
                node.prev.next = node.next
                self.__cursor__ = node.prev
            else:
                self.__head__ = node.next
            if node.next is not None:
                node.next.prev = node.prev
                self.__cursor__ = node.next
            else:
                self.__tail__ = node.prev
            self.__remove_status__ = self.REMOVE_STATUS_OK
        else:
            self.__remove_status__ = self.REMOVE_STATUS_FAIL

    # постусловие: список очищен от всех элементов
    def clear(self):
        self.__cursor__ = None
        self.__head__ = None
        self.__tail__ = None
        self.__head_status__ = self.HEAD_STATUS_FAIL
        self.__tail_status__ = self.TAIL_STATUS_FAIL
        self.__right_status__ = self.RIGHT_STATUS_FAIL
        self.__put_right_status__ = self.PUT_RIGHT_STATUS_FAIL
        self.__put_left_status__ = self.PUT_LEFT_STATUS_FAIL
        self.__remove_status__ = self.REMOVE_STATUS_FAIL
        self.__replace_status__ = self.REPLACE_STATUS_FAIL
        self.__find_status__ = self.FIND_STATUS_FAIL
        self.__get_status__ = self.GET_STATUS_FAIL

    # постусловие: новый узел добавлен в хвост списка
    def add_tail(self, value):
        node = Node(value)
        if self.__tail__ is not None:
            node.prev = self.__tail__
            self.__tail__.next = node
            self.__tail__ = node
        else:
            self.__head__ = node
            self.__tail__ = node

    # постусловие: в списке удалены все узлы с заданным значением
    def remove_all(self, value):
        node = self.__head__
        while node is not None:
            if node.value == value:
                if node.prev is not None:
                    node.prev.next = node.next
                else:
                    self.__head__ = node.next
                if node.next is not None:
                    node.next.prev = node.prev
                else:
                    self.__tail__ = node.prev
            node = node.next

    # предусловие: список не пуст;
    # постусловие: значение текущего узла заменено на новое
    def replace(self, value):
        if self.is_value():
            self.__cursor__.value = value
            self.__replace_status__ = self.REPLACE_STATUS_OK
        else:
            self.__replace_status__ = self.REPLACE_STATUS_FAIL

    # постусловие: курсор установлен на следующий узел
    # с искомым значением, если такой узел найден
    def find(self, value):
        self.__find_status__ = self.FIND_STATUS_FAIL
        node = self.__cursor__
        while node is not None:
            if node.value == value and node != self.__cursor__:
                self.__cursor__ = node
                self.__find_status__ = self.FIND_STATUS_OK
                break
            node = node.next

    # запросы
    # предусловие: список не пуст
    def get(self):
        value = None
        if self.is_value():
            value = self.__cursor__.value
            self.__get_status__ = self.GET_STATUS_OK
        else:
            self.__get_status__ = self.GET_STATUS_FAIL
        return value

    def is_head(self):
        return self.is_value() and self.__cursor__ == self.__head__

    def is_tail(self):
        return self.is_value() and self.__cursor__ == self.__tail__

    def is_value(self):
        return self.__cursor__ is not None

    def size(self):
        node = self.__head__
        count = 0
        while node is not None:
            count += 1
            node = node.next
        return count

    # запросы статусов (возможные значения статусов)

    def get_head_status(self): # успешно; список пуст
        return self.__head_status__

    def get_tail_status(self): # успешно; список пуст
        return self.__tail_status__

    def get_right_status(self): # успешно; правее нету элемента
        return self.__right_status__

    def get_put_right_status(self): # успешно; список пуст
        return self.__put_right_status__

    def get_put_left_status(self): # успешно; список пуст
        return self.__put_left_status__

    def get_remove_status(self): # успешно; список пуст
        return self.__remove_status__

    def get_replace_status(self): # успешно; список пуст
        return self.__replace_status__

    def get_find_status(self): # следующий найден; следующий не найден/список пуст
        return self.__find_status__

    def get_get_status(self): # успешно; список пуст
        return self.__get_status__


class LinkedList(ParentList):
    pass


class TwoWayList(ParentList):
    LEFT_STATUS_OK = 0
    LEFT_STATUS_FAIL = 1

    # команды

    # постусловие: список очищен от всех элементов
    def clear(self):
        ParentList.clear(self)
        self.__left_status__ = self.LEFT_STATUS_FAIL

    # предусловие: левее курсора есть элемент;
    # постусловие: курсор сдвинут на один узел влево
    def left(self):
        if self.is_value() and self.__cursor__.prev is not None:
            self.__cursor__ = self.__cursor__.prev
            self.__left_status__ = self.LEFT_STATUS_OK
        else:
            self.__left_status__ = self.LEFT_STATUS_FAIL

    # запросы статусов
    def get_left_status(self): # успешно; левее нету элемента
        return self.__left_status__
