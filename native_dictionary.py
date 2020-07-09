#!/usr/bin/env python3

from abc import ABC, abstractmethod


class AbstractNativeDictionary(ABC):
    # Константы
    ADD_STATUS_OK = 0
    ADD_STATUS_FAIL = 1
    REMOVE_STATUS_OK = 0
    REMOVE_STATUS_FAIL = 1
    GET_STATUS_OK = 0
    GET_STATUS_FAIL = 1

    # КОНСТРУКТОР
    # постусловие: создан пустой словарь
    @abstractmethod
    def __init__(self):
        pass

    # КОМАНДЫ
    # постусловие: пара ключ-значение добавлена в словарь
    @abstractmethod
    def add(self, key, value):
        """добавить пару ключ-значение в словарь"""
        pass

    # предусловие: в словаре имеется значение по данному ключу
    # постусловие: значение по ключу удалено из словаря
    @abstractmethod
    def remove(self, key):
        """удалить значение по данному ключу из словаря"""
        pass

    # постусловие: словарь очищен
    @abstractmethod
    def clear(self):
        """очистить словарь"""
        pass

    # ЗАПРОСЫ
    # предусловие: ключ есть в словаре
    @abstractmethod
    def get(self, key):
        """получить значение по ключу"""
        pass

    @abstractmethod
    def size(self):
        """возвращает количество элементов в словаре"""
        pass

    @abstractmethod
    def has_key(self, key):
        """проверить наличие ключа в словаре"""
        pass

    # запросы статусов
    @abstractmethod
    def get_add_status(self):
        """возвращает ADD_STATUS*"""
        pass

    @abstractmethod
    def get_remove_status(self):
        """возвращает REMOVE_STATUS*"""
        pass

    @abstractmethod
    def get_get_status(self):
        """возвращает GET_STATUS*"""
        pass


class NativeDictionary(AbstractNativeDictionary):

    __REMOVED_FLAG__ = 0

    def __init__(self, max_size):
        self.__size__ = max_size
        self.__step__ = 3
        self.__slots__ = [None] * self.__size__
        self.__values__ = [None] * self.__size__
        self.__add_status__ = self.ADD_STATUS_FAIL
        self.__remove_status__ = self.REMOVE_STATUS_FAIL
        self.__get_status__ = self.GET_STATUS_FAIL

    def __hash_fun__(self, value):
        # djb2
        acc = 5381
        for c in value:
            code = ord(c)
            acc = ((acc << 5) + acc) + code
        return acc % self.__size__

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

    # КОМАНДЫ
    def add(self, key, value):
        self.__add_status__ = self.ADD_STATUS_FAIL
        (found, slot) = self.__find__(key)
        if found:
            self.__values__[slot] = value
            self.__add_status__ = self.ADD_STATUS_OK
        elif slot is not None:
            self.__slots__[slot] = key
            self.__values__[slot] = value
            self.__add_status__ = self.ADD_STATUS_OK

    def remove(self, key):
        self.__remove_status__ = self.REMOVE_STATUS_FAIL
        (found, slot) = self.__find__(key)
        if found:
            self.__slots__[slot] = self.__REMOVED_FLAG__
            self.__values__[slot] = None
            self.__remove_status__ = self.REMOVE_STATUS_OK

    def clear(self):
        self.__slots__ = [None] * self.__size__
        self.__values__ = [None] * self.__size__

    # ЗАПРОСЫ
    def get(self, key):
        self.__get_status__ = self.GET_STATUS_FAIL
        (found, slot) = self.__find__(key)
        result = None
        if found:
            self.__get_status__ = self.GET_STATUS_OK
            result = self.__values__[slot]
        return result

    def size(self):
        def is_filled(slot):
            return slot is not None and slot != self.__REMOVED_FLAG__
        return sum(is_filled(s) for s in self.__slots__)

    def has_key(self, key):
        (found, _) = self.__find__(key)
        return found

    # запросы статусов
    def get_add_status(self):
        return self.__add_status__

    def get_remove_status(self):
        return self.__remove_status__

    def get_get_status(self):
        return self.__get_status__
