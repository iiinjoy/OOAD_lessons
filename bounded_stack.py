#!/usr/bin/env python3

from abc import ABC, abstractmethod


# АТД для BoundedStack:
class AbstractBoundedStack(ABC):
    PUSH_NIL = 0  # push() еще не вызывалась
    PUSH_OK = 1  # последняя push() отработала нормально
    PUSH_ERR = 2  # последняя push() отработала с ошибкой - стек полон

    POP_NIL = 0  # pop() ещё не вызывалась
    POP_OK = 1  # последняя pop() отработала нормально
    POP_ERR = 2  # стек пуст

    PEEK_NIL = 0  # peek() ещё не вызывалась
    PEEK_OK = 1  # последняя peek() вернула корректное значение
    PEEK_ERR = 2  # стек пуст

    # конструктор:
    # предусловие: опция capacity > 0 (максимально допустимое количество элементов в стеке)
    # предусловие: если опция capacity не задана, то capacity по умолчанию 32
    # постусловие: создан новый пустой стек, ограниченный опцией capacity
    @abstractmethod
    def __init__(self, capacity=32):
        pass

    # команды:
    # предусловие: текущий размер стека меньше capacity (стек не полон)
    # постусловие: в стек добавлено новое значение
    @abstractmethod
    def push(self, value):
        pass

    # предусловие: стек не пустой;
    # постусловие: из стека удалён верхний элемент
    @abstractmethod
    def pop(self):
        pass

    # постусловие: из стека удалятся все значения
    @abstractmethod
    def clear(self):
        pass

    # запросы:
    # предусловие: стек не пустой
    @abstractmethod
    def peek(self):
        pass

    @abstractmethod
    def size(self):
        pass

    # дополнительные запросы:
    @abstractmethod
    def get_push_status(self):  # возвращает значение PUSH_*
        pass

    @abstractmethod
    def get_pop_status(self):  # возвращает значение POP_*
        pass

    @abstractmethod
    def get_peek_status(self):  # возвращает значение PEEK_*
        pass


# реализация АТД BoundedStack
class BoundedStack(AbstractBoundedStack):

    def __init__(self, capacity=32):
        self.__capacity__ = capacity
        self.clear()

    def push(self, value):
        if self.size() < self.__capacity__:
            self.__stack__.append(value)
            self.__push_status__ = self.PUSH_OK
        else:
            self.__push_status__ = self.PUSH_ERR

    def pop(self):
        if self.size() > 0:
            self.__stack__.pop()
            self.__pop_status__ = self.POP_OK
        else:
            self.__pop_status__ = self.POP_ERR

    def clear(self):
        self.__stack__ = []
        self.__push_status__ = self.PUSH_NIL
        self.__pop_status__ = self.POP_NIL
        self.__peek_status__ = self.PEEK_NIL

    # запросы:
    def peek(self):
        result = None
        if self.size() > 0:
            result = self.__stack__[-1]
            self.__peek_status__ = self.PEEK_OK
        else:
            self.__peek_status__ = self.PEEK_ERR
        return result

    def size(self):
        return len(self.__stack__)

    # дополнительные запросы:
    def get_push_status(self):
        return self.__push_status__

    def get_pop_status(self):
        return self.__pop_status__

    def get_peek_status(self):
        return self.__peek_status__
