#!/usr/bin/env python3

"""
Комментарий к решению:

Помимо упомянутых в концепции команд и запросов:
1) добавлена вспомогательная команда clear() в целях эффективности реализации
(т.к. удаление по одному элементу занимало бы O(n) времени или хуже с учетом
реаллокаций в реализации)

2) добавлен вспомогательный запрос length() для получения длины массива
и более удобной итерации по элементам массива

3) добавлена команда set_item() для изменения значения i-го элемента
так же в целях эффективности; имеет сложность O(1).
Реализация через remove/insert имела бы сложность O(N)
"""

from abc import ABC, abstractmethod
import ctypes


class AbstractDynArray(ABC):
    # коды статусов
    APPEND_OK = 0
    APPEND_FAIL = 1
    INSERT_OK = 0
    INSERT_FAIL = 1
    REMOVE_OK = 0
    REMOVE_FAIL = 1
    GET_ITEM_OK = 0
    GET_ITEM_FAIL = 1
    SET_ITEM_OK = 0
    SET_ITEM_FAIL = 1

    # КОНСТРУКТОР
    # постусловие: создан пустой динамический массив
    @abstractmethod
    def __init__(self):
        pass

    # КОМАНДЫ
    # добавление элемента в конец массива
    # постусловие: элемент добавлен в конец массива
    @abstractmethod
    def append(self, item):
        pass

    # вставка элемента по индексу
    # предусловие: индекс корректный, в пределах границ [0; length]
    # постусловие: в i-ю позицию вставлен объект item, все последующие элементы сдвинуты на 1 шаг вправо;
    #              если i равен размеру массива, объект item добавлен в конец массива
    @abstractmethod
    def insert(self, item, i):
        pass

    # удаление элемента по индексу
    # предусловие: индекс корректный, в пределах границ [0; length-1]
    # постусловие: удален элемент по индексу i, все последующие элементы сдвинуты на 1 шаг влево
    @abstractmethod
    def remove(self, i):
        pass

    # очистка всех элементов
    # постусловие: массив пустой
    @abstractmethod
    def clear(self):
        pass

    # изменить значение i-го элемента
    # предусловие: индекс корректный, в пределах границ [0; length-1]
    # постусловие: значение i-го элемента равно заданному (value)
    @abstractmethod
    def set_item(self, i, value):
        pass

    # ЗАПРОСЫ
    # получение элемента по индексу
    # предусловие: индекс корректный, в пределах границ [0; length-1]
    @abstractmethod
    def get_item(self, index):
        pass

    # получить длину массива
    @abstractmethod
    def length(self):
        pass

    # ЗАПРОСЫ СТАТУСОВ
    # возвращает APPEND_*
    @abstractmethod
    def get_append_status(self):
        pass

    # возвращает INSERT_*
    @abstractmethod
    def get_insert_status(self):
        pass

    # возвращает REMOVE_*
    @abstractmethod
    def get_remove_status(self):
        pass

    # возвращает GET_ITEM_*
    @abstractmethod
    def get_get_item_status(self):
        pass

    # возвращает SET_ITEM_*
    @abstractmethod
    def get_set_item_status(self):
        pass


class DynArray(AbstractDynArray):
    # КОНСТРУКТОР
    def __init__(self):
        self.clear()

    # КОМАНДЫ
    def append(self, item):
        self.__append_status__ = self.APPEND_FAIL
        if self.__count__ == self.__capacity__:
            self.__resize__(2 * self.__capacity__)
        self.__array__[self.__count__] = item
        self.__count__ += 1
        self.__append_status__ = self.APPEND_OK

    def insert(self, item, i):
        if i < 0 or i > self.__count__:
            self.__insert_status__ = self.INSERT_FAIL
        else:
            if self.__count__ == self.__capacity__:
                new_capacity = 2*self.__capacity__
                new_array = self.__make_array__(new_capacity)
                for j in range(self.__count__, 0, -1):
                    if j <= i:
                        new_array[j-1] = self.__array__[j-1]
                    else:
                        new_array[j] = self.__array__[j-1]
                new_array[i] = item
                self.__array__ = new_array
                self.__capacity__ = new_capacity
            else:
                for j in range(self.__count__, i, -1):
                    self.__array__[j] = self.__array__[j-1]
                self.__array__[i] = item
            self.__count__ += 1
            self.__insert_status__ = self.INSERT_OK

    def remove(self, i):
        if i < 0 or i >= self.__count__:
            self.__remove_status__ = self.REMOVE_FAIL
        else:
            if (self.__capacity__ > 16) and (self.__count__-1 < self.__capacity__/2):
                new_capacity = int(self.__capacity__/1.5)
                if new_capacity < 16:
                    new_capacity = 16
                new_array = self.__make_array__(new_capacity)
                for j in range(self.__count__-1):
                    if j < i:
                        new_array[j] = self.__array__[j]
                    else:
                        new_array[j] = self.__array__[j+1]
                self.__array__ = new_array
                self.__capacity__ = new_capacity
            else:
                for j in range(i, self.__count__-1):
                    self.__array__[j] = self.__array__[j+1]
            self.__count__ -= 1
            self.__remove_status__ = self.REMOVE_OK

    def clear(self):
        self.__count__ = 0
        self.__capacity__ = 16
        self.__array__ = self.__make_array__(self.__capacity__)
        self.__append_status__ = self.APPEND_FAIL
        self.__insert_status__ = self.INSERT_FAIL
        self.__remove_status__ = self.REMOVE_FAIL
        self.__get_item_status__ = self.GET_ITEM_FAIL
        self.__set_item_status__ = self.SET_ITEM_FAIL

    def set_item(self, i, value):
        if i < self.__count__:
            self.__array__[i] = value
            self.__set_item_status__ = self.SET_ITEM_OK
        else:
            self.__set_item_status__ = self.SET_ITEM_FAIL

    # ЗАПРОСЫ
    def get_item(self, index):
        value = None
        if index < self.__count__:
            value = self.__array__[index]
            self.__get_item_status__ = self.GET_ITEM_OK
        else:
            self.__get_item_status__ = self.GET_ITEM_FAIL
        return value

    def length(self):
        return self.__count__

    # ЗАПРОСЫ СТАТУСОВ
    def get_append_status(self):
        return self.__append_status__

    def get_insert_status(self):
        return self.__insert_status__

    def get_remove_status(self):
        return self.__remove_status__

    def get_get_item_status(self):
        return self.__get_item_status__

    def get_set_item_status(self):
        return self.__set_item_status__

    # вспомогательные private функции
    def __make_array__(self, new_capacity):
        return (new_capacity * ctypes.py_object)()

    def __resize__(self, new_capacity):
        new_array = self.__make_array__(new_capacity)
        for i in range(self.__count__):
            new_array[i] = self.__array__[i]
        self.__array__ = new_array
        self.__capacity__ = new_capacity
