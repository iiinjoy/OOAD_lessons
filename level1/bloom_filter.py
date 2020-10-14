#!/usr/bin/env python3

from abc import ABC, abstractmethod


class AbstractBloomFilter(ABC):

    # KOHCTPYKTOP
    @abstractmethod
    # постусловие: создан фильтр Блюма с битовым массивом длины f_len
    def __init__(self, f_len):
        pass

    # КОМАНДЫ
    # постусловие: строка добавлена в фильтр
    @abstractmethod
    def add(self, str1):
        """добавить строку str1 в фильтр"""
        pass

    @abstractmethod
    # постусловие: фильтр очищен
    def clear(self):
        """очистить фильтр"""
        pass

    # ЗАПРОСЫ
    @abstractmethod
    def is_value(self, str1):
        """вернет True, если строка str1 имеется в фильтре, иначе False"""
        pass


class BloomFilter(AbstractBloomFilter):

    # KOHCTPYKTOP
    def __init__(self, f_len):
        self.__filter_len__ = f_len
        self.__bitmask__ = 0

    def __hash1__(self, str1):
        acc = 0
        for c in str1:
            code = ord(c)
            acc = ((acc * 17) + code) % self.__filter_len__
        return (1 << acc)

    def __hash2__(self, str1):
        acc = 0
        for c in str1:
            code = ord(c)
            acc = ((acc * 223) + code) % self.__filter_len__
        return (1 << acc)

    # КОМАНДЫ
    def add(self, str1):
        mask = self.__hash1__(str1) | self.__hash2__(str1)
        self.__bitmask__ |= mask

    def clear(self):
        self.__bitmask__ = 0

    # ЗАПРОСЫ
    def is_value(self, str1):
        mask = self.__hash1__(str1) | self.__hash2__(str1)
        return (self.__bitmask__ & mask) == mask
