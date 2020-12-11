#!/usr/bin/env python3

'''
Задание 9.
----------
Постройте в вашем языке программирования базовую иерархию из двух классов General и Any. Унаследуйте General от универсального базового класса, если таковой имеется в языке или стандартной библиотеке/фреймворке, и реализуйте семь фундаментальных операций для него, используя для этого по возможности возможности стандартных библиотек.

Решение.
--------
'''
from __future__ import annotations
from abc import ABC, abstractmethod
import copy as C
from typing import List, Optional, cast
# только с Python 3.8:
from typing import final


class General(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def copy(self) -> General:
        """сконструировать и вернуть поверхностную копию (shallow copy)"""
        pass

    @abstractmethod
    def deep_copy(self) -> General:
        """сконструировать и вернуть глубокую копию (deep copy)"""
        pass

    @abstractmethod
    def is_(self, other: General) -> bool:
        """строгая проверка на равенство (сравнение ссылок)"""
        pass

    @abstractmethod
    def equal(self, other: General) -> bool:
        """проверка на равенство (глубокий вариант)"""
        pass

    @abstractmethod
    def serialize(self) -> str:
        """сериализация в строковое представление"""
        pass

    @abstractmethod
    def deserialize(self, in_str: str) -> Optional[General]:
        """десериализация из строкового представления"""
        pass

    @abstractmethod
    def print_(self) -> None:
        """печать объекта"""
        pass

    @abstractmethod
    def is_of_type(self, type_: type) -> bool:
        """проверка, является ли тип текущего объекта указанным типом"""
        pass

    @abstractmethod
    def get_type(self) -> type:
        """получить типа объекта (класса, экземпляром которого он был создан)"""
        pass


class Any(General):
    def __init__(self) -> None:
        pass

    def copy(self) -> Any:
        obj = C.copy(self)
        return obj

    def deep_copy(self) -> Any:
        obj = C.deepcopy(self)
        return obj

    def is_(self, other: General) -> bool:
        return self is other

    def equal(self, other: General) -> bool:
        return other.is_of_type(Any)

    def __str__(self) -> str:
        return self.serialize()

    def __repr__(self) -> str:
        return self.__str__()

    def serialize(self) -> str:
        return "Any()"

    def deserialize(self, in_str: str) -> Optional[General]:
        if in_str == "Any()":
            return Any()
        return None

    def print_(self) -> None:
        print(self.serialize())

    def is_of_type(self, type_: type) -> bool:
        return self.__class__ is type_

    def get_type(self) -> type:
        return self.__class__


class AList(Any):
    def __init__(self, *elements: Any) -> None:
        self.list: List[Any] = [*elements]

    def copy(self) -> AList:
        c = AList()
        c.list = C.copy(self.list)
        return c

    def deep_copy(self) -> Any:
        c = AList()
        c.list = C.deepcopy(self.list)
        return c

    def equal(self, other: General) -> bool:
        if not other.is_of_type(AList):
            return False
        L2: AList = cast(AList, other)
        if len(self.list) != len(L2.list):
            return False
        for i in range(len(self.list)):
            if not self.list[i].equal(L2.list[i]):
                return False
        return True

    def serialize(self) -> str:
        return "AList(" + ", ".join(list(map(str, self.list))) + ")"

    def deserialize(self, in_str: str) -> Optional[General]:
        # TODO
        return None


"""
Комментарий к решению.
----------------------
1) Метод клонирования объекта поглощен реализацией глубокого копирования:
в Python'е запись во входной параметр функции не имеет эффекта (можно эмулировать, передавая аргумент внутри массива, но данный подход не идиоматичен). Поэтому реализация глубокого копирования в существующий объект затруднен: сделал просто возврат нового объекта - то же, что и клонирование. Оставлен один метод deep_copy (глубокое копирование/клонирование).

2) в демонстративных целях создан прикладной класс списка AList, наследующий класс Any, реализующий 7 фундаментальных операций (кроме функции десериализации, и прикладных методов класса АТД AList - append/get/size и т.п.)

3) для копирования/глубокого копирования использована стандартная библиотека "copy"

"""

"""
Задание 10.
-----------

Выясните, имеется ли в вашем языке программирования возможность запрета переопределения методов в потомках, и приведите пример кода.

Решение.
--------
"""


class Base(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @final
    def print_name(self) -> None:
        print("name : {}".format(self.name()))


class Foo(Base):
    def name(self) -> str:
        return "Foo"

    # Эта строка приведет к ошибке в type-checker'е
    def print_name(self) -> None:
        print("I am Foo")


"""
Комментарий к решению.
----------------------

В Python начиная с версии 3.8 появился квалификатор @final, в частности запрещающий переопределение метода в классах-потомках (а кроме того, запрещающий наследование и переприсваивание переменной или атрибута). Работает только в type-checker'е, в рантайме игнорируется.

$ mypy --strict --show-column-numbers lesson4.py
lesson4.py:179:5: error: Cannot override final attribute "print_name" (previously declared in base class "Base")

"""
