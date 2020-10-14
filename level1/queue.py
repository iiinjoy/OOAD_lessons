#!/usr/bin/env python3

from abc import ABC, abstractmethod
import ctypes


class AbstractQueue(ABC):
    PUSH_OK = 0
    PUSH_ERR = 1
    POP_OK = 0
    POP_ERR = 1
    PEEK_OK = 0
    PEEK_ERR = 1

    # КОНСТРУКТОР
    # постусловие: создана пустая очередь
    @abstractmethod
    def __init__(self):
        pass

    # КОМАНДЫ
    # постусловие: элемент добавлен к конец очереди
    @abstractmethod
    def push(self, item):
        """добавить элемент в конец очереди"""
        pass

    # предусловие: очередь не пустая
    # постусловие: элемент удален из начала очереди
    @abstractmethod
    def pop(self):
        """удалить элемент из начала очереди"""
        pass

    # постусловие: очередь пуста
    @abstractmethod
    def clear(self):
        """очистить очередь"""
        pass

    # ЗАПРОСЫ
    @abstractmethod
    def size(self):
        """вернуть текущий размер очереди"""
        pass

    # предусловие: очередь не пустая
    @abstractmethod
    def peek(self):
        """вернуть значение элемента в начале очереди, не удаляя его"""
        pass

    # запросы статусов
    @abstractmethod
    def get_push_status(self):
        """возвращает PUSH_*"""
        pass

    @abstractmethod
    def get_pop_status(self):
        """возвращает POP_*"""
        pass

    @abstractmethod
    def get_peek_status(self):
        """возвращает PEEK_*"""
        pass


class Queue(AbstractQueue):

    def __init__(self):
        self.clear()

    def push(self, item):
        self.__queue__.append(item)
        self.__push_status__ = self.PUSH_OK

    def pop(self):
        if self.size() > 0:
            self.__queue__.pop(0)
            self.__pop_status__ = self.POP_OK
        else:
            self.__pop_status__ = self.POP_ERR

    def clear(self):
        self.__queue__ = []
        self.__push_status__ = self.PUSH_ERR
        self.__pop_status__ = self.POP_ERR
        self.__peek_status__ = self.PEEK_ERR

    def size(self):
        return len(self.__queue__)

    def peek(self):
        result = None
        if self.size() > 0:
            result = self.__queue__[0]
            self.__peek_status__ = self.PEEK_OK
        else:
            self.__peek_status__ = self.PEEK_ERR
        return result

    def get_push_status(self):
        return self.__push_status__

    def get_pop_status(self):
        return self.__pop_status__

    def get_peek_status(self):
        return self.__peek_status__
