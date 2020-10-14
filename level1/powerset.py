#!/usr/bin/env python3

from abc import ABC, abstractmethod

# AbstractHashTable без изменений из hashtable.py
class AbstractHashTable(ABC):
    ADD_STATUS_OK = 0
    ADD_STATUS_FAIL = 1

    # КОНСТРУКТОР
    # постусловие: создана хэш-таблица под фиксированное количество значений
    @abstractmethod
    def __init__(self, max_size):
        pass

    # КОМАНДЫ
    # предусловие: в таблице есть свободный слот
    # постусловие: в таблицу добавлено значение
    @abstractmethod
    def add(self, value):
        """добавить значение в таблицу"""
        pass

    # постусловие: в таблице отсутствует значение
    @abstractmethod
    def remove(self, value):
        """удалить значение из таблицы"""
        pass

    # ЗАПРОСЫ
    @abstractmethod
    def has(self, value):
        """проверить наличие значения в таблице, возвращает True/False"""
        pass

    # запросы статусов
    @abstractmethod
    def get_add_status(self):
        """возвращает ADD_STATUS*"""
        pass


class AbstractPowerSet(AbstractHashTable):
    # константы
    INTERSECTION_STATUS_OK = 0
    INTERSECTION_STATUS_FAIL = 1
    UNION_STATUS_OK = 0
    UNION_STATUS_FAIL = 1
    DIFFERENCE_STATUS_OK = 0
    DIFFERENCE_STATUS_FAIL = 1

    # KOHCTPYKTOP
    # постусловие: создано множество под фиксированное количество значений
    def __init__(self, max_size):
        pass

    # КОМАНДЫ

    # ЗАПРОСЫ
    @abstractmethod
    def values(self):
        """возвращает элементы в множестве в виде списка"""
        pass

    @abstractmethod
    def size(self):
        """возвращает количество элементов в множестве"""
        pass

    # постусловие: создано множество из одинаковых элементов в текущем множестве и в other_set
    @abstractmethod
    def intersection(self, other_set):
        """пересечение текущего множества и other_set"""
        pass

    # постусловие: создано множество из элементов текущего множества и other_set
    @abstractmethod
    def union(self, other_set):
        """объединение текущего множества и other_set"""
        pass

    @abstractmethod
    # постусловие: создано множество из элементов текущего множества, которых нет в other_set
    def difference(self, other_set):
        """разница текущего множества и other_set"""
        pass

    @abstractmethod
    def issubset(self, other_set):
        """True, если other_set является подмножеством текущего множества, иначе False"""
        pass

    # запросы статусов
    @abstractmethod
    def get_intersection_status(self):
        """возвращает INTERSECTION_STATUS_*"""
        pass

    @abstractmethod
    def get_union_status(self):
        """возвращает UNION_STATUS_*"""
        pass

    @abstractmethod
    def get_difference_status(self):
        """возвращает DIFFERENCE_STATUS_*"""
        pass


class PowerSet(AbstractPowerSet):
    __REMOVED_FLAG__ = 0

    # KOHCTPYKTOP
    def __init__(self, max_size):
        self.__size__ = max_size
        self.__step__ = 3
        self.__slots__ = [None] * self.__size__
        self.__add_status__ = self.ADD_STATUS_FAIL
        self.__intersection_status__ = self.INTERSECTION_STATUS_FAIL
        self.__union_status__ = self.UNION_STATUS_FAIL
        self.__difference_status__ = self.DIFFERENCE_STATUS_FAIL

    def __hash_fun__(self, value):
        # djb2
        acc = 5381
        for c in value:
            code = ord(c)
            acc = ((acc << 5) + acc) + code
        return acc % self.__size__

    # КОМАНДЫ
    def add(self, value):
        self.__add_status__ = self.ADD_STATUS_FAIL
        (found, slot) = self.__find__(value)
        if found:
            self.__add_status__ = self.ADD_STATUS_OK
        elif slot is not None:
            self.__slots__[slot] = value
            self.__add_status__ = self.ADD_STATUS_OK

    def __find__(self, value):
        slot = self.__hash_fun__(value)
        result = (False, None)
        for i in range(self.__size__):
            k = (slot + i * self.__step__) % self.__size__
            v = self.__slots__[k]
            if v is None or v == self.__REMOVED_FLAG__:
                result = (False, k)
                break
            elif v == value:
                result = (True, k)
                break
        return result

    def remove(self, value):
        (found, slot) = self.__find__(value)
        if found:
            self.__slots__[slot] = self.__REMOVED_FLAG__

    # ЗАПРОСЫ
    def has(self, value):
        (found, _) = self.__find__(value)
        return found

    def get_add_status(self):
        return self.__add_status__

    def values(self):
        elems = []
        for i in range(self.__size__):
            v = self.__slots__[i]
            if v is not None and v != self.__REMOVED_FLAG__:
                elems.append(v)
        return elems

    def size(self):
        return len(self.values())

    def intersection(self, other_set):
        self.__intersection_status__ = self.INTERSECTION_STATUS_OK
        s = PowerSet(self.__size__)
        elems = self.values()
        for e in elems:
            if other_set.has(e):
                s.add(e)
                if self.get_add_status() != self.ADD_STATUS_OK:
                    self.__intersection_status__ = self.INTERSECTION_STATUS_FAIL
                    break
        return s

    def union(self, other_set):
        self.__union_status__ = self.UNION_STATUS_OK
        s = PowerSet(self.__size__)
        elems = self.values()
        for e in elems:
            s.add(e)
            if self.get_add_status() != self.ADD_STATUS_OK:
                self.__union_status__ = self.UNION_STATUS_FAIL
                break
        elems = other_set.values()
        for e in elems:
            s.add(e)
            if self.get_add_status() != self.ADD_STATUS_OK:
                self.__union_status__ = self.UNION_STATUS_FAIL
                break
        return s

    def difference(self, other_set):
        self.__difference_status__ = self.DIFFERENCE_STATUS_OK
        s = PowerSet(self.__size__)
        elems = self.values()
        for e in elems:
            s.add(e)
            if self.get_add_status() != self.ADD_STATUS_OK:
                self.__difference_status__ = self.DIFFERENCE_STATUS_FAIL
                break
        elems = other_set.values()
        for e in elems:
            s.remove(e)
        return s

    def issubset(self, other_set):
        elems = other_set.values()
        result = True
        for e in elems:
            if not self.has(e):
                result = False
                break
        return result

    # запросы статусов
    def get_intersection_status(self):
        return self.__intersection_status__

    def get_union_status(self):
        return self.__union_status__

    def get_difference_status(self):
        return self.__difference_status__
