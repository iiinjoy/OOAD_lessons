#!/usr/bin/env python3
from abc import ABC, abstractmethod


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


class HashTable(AbstractHashTable):

    __REMOVED_FLAG__ = 0

    def __init__(self, max_size):
        self.__size__ = max_size
        self.__step__ = 3
        self.__slots__ = [None] * self.__size__
        self.__add_status__ = self.ADD_STATUS_FAIL

    def __hash_fun__(self, value):
        # djb2
        acc = 5381
        for c in value:
            code = ord(c)
            acc = ((acc << 5) + acc) + code
        return acc % self.__size__

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

    def has(self, value):
        (found, _) = self.__find__(value)
        return found

    def get_add_status(self):
        return self.__add_status__
