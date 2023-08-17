from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """Абстрактный класс для API и получения вакансий"""

    @abstractmethod
    def get_requests(self):
        """Функция для отправки запроса"""
        pass

    @abstractmethod
    def get_vacancies(self):
        """Функция для получения вакансий"""
        pass


class AbstractJson(ABC):
    """Абстрактный класс для работы с json файлом"""

    @abstractmethod
    def create_file(self):
        """Сохранение в файл списка вакансий"""
        pass

    @abstractmethod
    def load_file(self):
        """Загрузка из файла списка вакансий"""
        pass
