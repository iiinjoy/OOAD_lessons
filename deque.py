#!/usr/bin/env python3


class ParentQueue():
    REMOVE_FRONT_STATUS_OK = 0
    REMOVE_FRONT_STATUS_FAIL = 1
    GET_FRONT_STATUS_OK = 0
    GET_FRONT_STATUS_FAIL = 1

    # КОНСТРУКТОР
    # постусловие: создана пустая очередь
    def __init__(self):
        self.clear()

    # КОМАНДЫ
    # постусловие: очередь пуста
    def clear(self):
        """очистить очередь"""
        self.__deque__ = []
        self.__remove_front_status__ = self.REMOVE_FRONT_STATUS_FAIL
        self.__get_front_status__ = self.GET_FRONT_STATUS_FAIL

    # постусловие: элемент добавлен в конец очереди
    def add_tail(self, item):
        """добавить элемент в конец очереди"""
        self.__deque__.append(item)

    # предусловие: очередь не пуста
    # постусловие: элемент удален из начала очереди
    def remove_front(self):
        """удалить элемент из начала очереди"""
        if self.size() > 0:
            self.__deque__.pop(0)
            self.__remove_front_status__ = self.REMOVE_FRONT_STATUS_OK
        else:
            self.__remove_front_status__ = self.REMOVE_FRONT_STATUS_FAIL

    # ЗАПРОСЫ
    def size(self):
        """возвращает размер очереди"""
        return len(self.__deque__)

    # предусловие: очередь не пуста
    def get_front(self):
        """получить элемент из головы очереди"""
        result = None
        if self.size() > 0:
            result = self.__deque__[0]
            self.__get_front_status__ = self.GET_FRONT_STATUS_OK
        else:
            self.__get_front_status__ = self.GET_FRONT_STATUS_FAIL
        return result

    # ЗАПРОСЫ СТАТУСОВ
    def get_remove_front_status(self):
        """возвращает REMOVE_FRONT_STATUS_*"""
        return self.__remove_front_status__

    def get_get_front_status(self):
        """возвращает GET_FRONT_STATUS_*"""
        return self.__get_front_status__


class Queue(ParentQueue):
    DEQUEUE_STATUS_OK = 0
    DEQUEUE_STATUS_FAIL = 1
    GET_STATUS_OK = 0
    GET_STATUS_FAIL = 1

    # КОМАНДЫ:
    # постусловие: элемент добавлен в конец очереди
    def enqueue(self, item):
        """добавить элемент в конец очереди"""
        self.add_tail(item)

    # предусловие: очередь не пуста
    # постусловие: элемент удален из начала очереди
    def dequeue(self):
        """удалить элемент из начала очереди"""
        self.remove_front()

    # ЗАПРОСЫ
    # предусловие: очередь не пуста
    def get(self):
        """получить элемент из головы очереди"""
        return self.get_front()

    # ЗАПРОСЫ СТАТУСОВ
    def get_dequeue_status(self):
        """возвращает DEQUEUE_STATUS_*"""
        status = self.DEQUEUE_STATUS_FAIL
        if self.get_remove_front_status() == self.REMOVE_FRONT_STATUS_OK:
            status = self.DEQUEUE_STATUS_OK
        return status

    def get_get_status(self):
        """возвращает GET_STATUS_*"""
        status = self.GET_STATUS_FAIL
        if self.get_get_front_status() == self.GET_FRONT_STATUS_OK:
            status = self.GET_STATUS_OK
        return status


class Deque(ParentQueue):
    REMOVE_TAIL_STATUS_OK = 0
    REMOVE_TAIL_STATUS_FAIL = 1
    GET_TAIL_STATUS_OK = 0
    GET_TAIL_STATUS_FAIL = 1

    # КОМАНДЫ
    # постусловие: очередь пуста
    def clear(self):
        """очистить очередь"""
        ParentQueue.clear(self)
        self.__remove_tail_status__ = self.REMOVE_TAIL_STATUS_FAIL
        self.__get_tail_status__ = self.GET_TAIL_STATUS_FAIL

    # постусловие: элемент добавлен в начало очереди
    def add_front(self, item):
        """добавить элемент в начало очереди"""
        self.__deque__.insert(0, item)

    # предусловие: очередь не пуста
    # постусловие: элемент удален из конца очереди
    def remove_tail(self):
        """удалить элемент из конца очереди"""
        if self.size() > 0:
            self.__deque__.pop()
            self.__remove_tail_status__ = self.REMOVE_TAIL_STATUS_OK
        else:
            self.__remove_tail_status__ = self.REMOVE_TAIL_STATUS_FAIL

    # ЗАПРОСЫ
    # предусловие: очередь не пуста
    def get_tail(self):
        """получить элемент из конца очереди"""
        result = None
        if self.size() > 0:
            result = self.__deque__[-1]
            self.__get_tail_status__ = self.GET_TAIL_STATUS_OK
        else:
            self.__get_tail_status__ = self.GET_TAIL_STATUS_FAIL
        return result

    # ЗАПРОСЫ СТАТУСОВ
    def get_remove_tail_status(self):
        """возвращает REMOVE_TAIL_STATUS_*"""
        return self.__remove_tail_status__

    def get_get_tail_status(self):
        """возвращает GET_TAIL_STATUS_*"""
        return self.__get_tail_status__
