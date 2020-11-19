#!/usr/bin/env python3

'''
Задание 7.
----------

Приведите пример кода с комментариями, где применяется динамическое связывание.

Решение.
--------
'''

from abc import ABC, abstractmethod
from typing import List, Sequence, Callable


class IHasher(ABC):
    # абстрактый класс (интерфейс) для классов реализующих хэш функции по определенному алгоритму
    @abstractmethod
    def hash_fun(self, key: str) -> int:
        pass


class SumHasher(IHasher):
    # простой класс подсчета хэша суммирующий значения отдельных символов
    def hash_fun(self, key: str) -> int:
        acc = 0
        for c in key:
            code = ord(c)
            acc = acc + code
        return acc


class DJB2Hasher(IHasher):
    # класс подсчета хэша по алгоритму djb2
    def hash_fun(self, key: str) -> int:
        # djb2
        acc = 5381
        for c in key:
            code = ord(c)
            acc = (acc << 5) + acc + code
        return acc % 4294967296


# использование
hasher: IHasher = SumHasher()
h = hasher.hash_fun("skillsmart")
print(h)
hasher = DJB2Hasher()
h = hasher.hash_fun("skillsmart")
print(h)

'''
Комментарий к решению
--------

В языке Python все переменные являются ссылочными и связываются динамически, тип определяется только во время выполнения.
Так что, в любом случае, пока этот участок не выполнится, тип не известен.

Использовал type annotations в Python в демонстративных целях.
В компилируемых языках, например C++, это более явный пример динамического связывания:

IHasher *hasher = GetHasherSomehowFromLibrary();

На момент компиляции можно предполагать только что объект (точнее указатель на объект) реализует вышеуказанный
интерфейс IHasher, и реализация полностью скрыта. Это пример повторного использования, когда за счет динамического
связывания реализация класса может находится даже вне основного приложения, а именно: в динамически связываемой библиотеке
(dll/so/dylib). Очевидно, можно подменять реализацию, так как в примере на python выше, оставляя прежнюю переменную (ссылку).

'''

'''
Задание 8.
----------

Приведите примеры кода с ковариантностью и контравариантностью, если ваш язык программирования это позволяет.

Решение.
--------

1) Ковариантность
'''


def several_hashes(s: str, hashers: List[IHasher]) -> List[int]:
    hs: List[int] = []
    for h in hashers:
        hs.append(h.hash_fun(s))
    return hs


hashers: List[SumHasher] = [SumHasher(), SumHasher(), SumHasher()]

'''
# mypy --strict --show-column-numbers "lesson3.py"
благодаря аннотации типов и при тайпчекинге (внешнем, через mypy) в python на этой строке мы получаем такие ошибки:
error: Argument 2 to "several_hashes" has incompatible type "List[SumHasher]"; expected "List[IHasher]"
note: "List" is invariant -- see http://mypy.readthedocs.io/en/latest/common_issues.html#variance
note: Consider using "Sequence" instead, which is covariant
-- то что нам нужно: ковариантная последовательность
'''
hs = several_hashes("skillsmart", hashers)


'''
а этот пример пройдет тайпчекинг:
'''


def several_hashes2(s: str, hashers: Sequence[IHasher]) -> List[int]:
    hs: List[int] = []
    for h in hashers:
        hs.append(h.hash_fun(s))
    return hs


hashers2: Sequence[SumHasher] = [SumHasher(), SumHasher(), SumHasher()]
hs2 = several_hashes2("skillsmart", hashers2)
print(hs2)

'''
т.е. в системе тайпчекинга тип список (List) не ковариантный, но у самого Python тип список - обобщенный
(может хранить объекты произвольного типа), к тому же, за счет duck-typing - гетерогенный
(может хранить объекты разных типов).
Так что, можно сказать, что Python поддерживает ковариантность.

2) Контравариантность
'''

'''
Предположим есть такая иерархия Person - Student
класс Student переопределяет метод name(), а также расширяет класс предка
методом record_book_number (номер зачетной книжки)
'''


class Person():
    def name(self) -> str:
        return "Person"


class Student(Person):
    def name(self) -> str:
        return "Student"

    def record_book_number(self) -> int:
        return 12345


'''
Все функции, принимающие объекты класса Person, будут работать и с объектами класса Student,
за счет ковариантности. Обратное вообще говоря неверно.

При контравариантности у делегатов перевернется схема наследования:
'''


class StudentDescriber():
    def get_descr(self, student: Student) -> str:
        return student.name() + ' with record book #' + str(student.record_book_number())


class PersonDescriber(StudentDescriber):
    def get_descr(self, person: Person) -> str:
        return person.name()


student = Student()
person = Person()

pd = PersonDescriber()
print(pd.get_descr(student))
print(pd.get_descr(person))

sd = StudentDescriber()
print(sd.get_descr(student))
# приведет к ошибке
# print(sd.get_descr(person))

'''
Логично, что в классе StudentDescriber метод принимающий Student (get_descr) должен работать и у всех потомков,
которые его переопределяют.

В таких случаях говорят, что функция get_descr(Person)->str является подтипом (subtype) функции get_descr(Student)->str
или контравариантна по первому аргументу.

Таким образом, Python поддерживает контравариантность
'''
