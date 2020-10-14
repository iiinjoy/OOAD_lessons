#!/usr/bin/env python3

"""
Задание 1.
----------
Напишите небольшой пример кода с комментариями, где применяются наследование, композиция и полиморфизм.

Решение.
--------
Предположим, требуется создать хранилище вида Ключ-Значение, но абстрагироваться
от реализации через интерфейс (реализацию АТД) IKeyValueStorage, и сделать две реализации,
наследующие этот интерфейс: хранилище в ОЗУ (MemStorage) и файловое персистентное хранилище (FileStorage).

1) пример наследования
интерфейс/базовый класс: IKeyValueStorage
классы-наследники: MemStorage, FileStorage

2) пример композиции
реализация FileStorage содержит внутри объект класса MemStorage; использует его,
например, в качестве кэша

3) пример полиморфизма
Функции write_to_storage/read_from_storage принимают в качестве аргумента объекты,
реализующие интерфейс IKeyValueStorage (не так явно, как в статически типизированных языках).
Таким образом, подменяя реализации (подстановка Liskov) интерфейса IKeyValueStorage,
мы получаем полиморфное поведение. В частности, выбирая между MemStorage/FileStorage:
 - меняется свойство хранилища: временное/постоянное
 - выводится разная информация о хранилище (метод info() )

Комментарий к решению.
----------------------
Реализация FileStorage для простоты не содержит работу с файлами.
Проектирование для упрощения АТД не производилось (разбиение на команды/запросы/запросы статусов,
проверка пред-/постусловий)

Далее пример кода.
"""

from abc import ABC, abstractmethod


class IKeyValueStorage(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def get(self, key):
        pass


class MemStorage(IKeyValueStorage):  # 1) пример наследования
    def __init__(self):
        self.storage = {}

    def info(self):
        return "MemStorage"

    def set(self, key, value):
        self.storage[key] = value

    def get(self, key):
        return self.storage[key]


class FileStorage(IKeyValueStorage):  # 1) пример наследования
    def __init__(self, filename):
        self.filename = filename
        self.memstorage = MemStorage()  # 2) пример композиции

    def info(self):
        return "FileStorage, file: " + self.filename

    def set(self, key, value):
        self.memstorage.set(key, value)
        # тут конкретная реализация, работа с файлом
        pass

    def get(self, key):
        result = self.memstorage.get(key)
        # тут конкретная реализация, работа с файлом
        return result


def write_to_storage(s):
    s.set("answer", "42")
    s.set("login", "iiinjoy")


def read_from_storage(s):
    print("Storage info: {}".format(s.info()))
    print("answer = {}".format(s.get("answer")))
    print("login = {}".format(s.get("login")))


def ex1():
    print("Ex 1.")

    # 3) пример полиморфизма
    ms = MemStorage()
    write_to_storage(ms)
    read_from_storage(ms)

    fs = FileStorage("file.db")
    write_to_storage(fs)
    read_from_storage(fs)


"""
Задание 2.
----------
Напишите небольшой пример кода с комментариями, где в наследовании применяется
как расширение класса-родителя, так и специализация класса-родителя.

Решение.
--------
интерфейс/базовый класс: VirtualPrinter
классы-наследники: LaserPrinter, PDFPrinter

1) пример расширения:
в классах наследниках есть методы расширяющие функционал основного:
- в LaserPrinter: метод получения уровня тонера в принтере
- в PDFPrinter: назначение папки для сохранения результирующих документов PDF

2) пример специализации:
в классах наследниках методы print_document определяются конкретной реализацией
- в LaserPrinter это будет растеризация и отправка документа на печать через API драйвера принтера/службы печати системы
- в PDFPrinter возможной реализацией будет обращение к библиотеке по работе с документами, конвертирующей в PDF

"""


class VirtualPrinter(ABC):
    PRINTER_STATUS_OK = 0
    PRINTER_STATUS_FAIL = 1

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def print_document(self, document):
        pass

    @abstractmethod
    def get_status(self):
        pass


class LaserPrinter(VirtualPrinter):
    PRINTER_STATUS_BUSY = 2

    def __init__(self):
        pass

    def print_document(self, document):  # 2) пример специализации
        print("printing on LaserPrinter, document = \"{}\"".format(document))

    def get_status(self):
        return self.PRINTER_STATUS_BUSY

    def get_toner_level_percent(self):  # 1) пример расширения
        return 42


class PDF_Printer(VirtualPrinter):
    def __init__(self):
        self._dir = "/tmp"
        pass

    def print_document(self, document):  # 2) пример специализации
        print("printing to pdf-file, document = \"{}\", saving to: {}".format(document, self._dir))

    def get_status(self):
        return self.PRINTER_STATUS_OK

    def set_pdf_output_dir(self, d):  # 1) пример расширения
        self._dir = d


def ex2():
    print("Ex 2.")

    test_page = "PrinterTestPage"

    laser_printer = LaserPrinter()
    laser_printer.print_document(test_page)

    pdf_printer = PDF_Printer()
    pdf_printer.set_pdf_output_dir("/PDF/")
    pdf_printer.print_document(test_page)


if __name__ == '__main__':
    ex1()
    ex2()


"""
Задание 3.
----------
Расскажите, как в выбранном вами языке программирования поддерживается концепция "класс как модуль".

Решение.
--------
Согласно документации языка Python,
    Модулем является файл, содержащий определения и утверждения на языке Python.
Имя файла == это название модуля + суффикc ".py"
При подключении модуля(файла) создается объект(единственный) принадлежащий встроенному (специальному)
классу `module`, в полях которого, с помощью интроспекции можно получить все определения и утверждения из файла.
Таким образом, модуль тоже является объектом некого класса (class 'module).

Модуль в Python (файл) может содержать несколько определений пользовательских (прикладных) классов.
Все в языке Python является объектом и имеет общий базовый класс (class 'type).
Т.е. отдельные определения и утверждения из файла - это базовые синтаксические единицы и могут быть размещены в отдельных файлах.
Следовательно, можно размещать определение пользовательского класса в отдельном файле, а значит,
язык программирования Python поддерживает концепцию "класс как модуль".

"""
