import requests
from configparser import ParsingError
from src.abstract_class import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для получения информации по API с сайта hh.ru"""

    def __init__(self, vacancy: str):
        self.vacancy = vacancy
        self.vacancies = []
        self.__url = 'https://api.hh.ru/vacancies'
        self.__key = 'items'
        self.__params = {
            'text': self.vacancy,
            'page': 0,
            'per_page': 100
        }

    @property
    def url(self):
        return self.__url

    @property
    def key(self):
        return self.__key

    @property
    def param(self):
        return self.__params

    def get_requests(self):
        """Функция, отправляющая запрос на сайт"""
        data = requests.get(self.__url, params=self.__params)
        return data.json()[self.__key]

    def get_vacancies(self, pages_count=1):
        while self.__params['page'] < pages_count:
            print(f"HeadHunter, Парсинг страницы {self.__params['page'] + 1}", end=": \n")
            try:
                response = self.get_requests()
            except ParsingError:
                print('Ошибка получения данных')
                break
            self.vacancies.extend(response)
            self.__params['page'] += 1
        return self.vacancies

    def validate_vacancies(self):
        """Валидация списка вакансий с фильтрацией вакансий не входящих в запрос"""

        self.get_vacancies()
        converted_vacancies = []
        for vac in self.vacancies:
            if self.vacancy in vac['name'].lower():
                if vac.get('salary') is not None:
                    salary = {'salary': True,
                              'salary_from': vac['salary']['from'],
                              'salary_to': vac['salary']['to'],
                              'currency': vac['salary']['currency']
                              }
                else:
                    salary = {'salary': False,
                              'salary_from': None,
                              'salary_to': None,
                              'currency': None
                              }
                vacancy_params = {'id': vac['id'],
                                  'title': vac['name'],
                                  'employer': vac['employer']['name'],
                                  'url': vac['alternate_url'],
                                  'experience': vac['experience']['name'],
                                  'api': 'HeadHunter'
                                  }
                vacancy_params.update(salary)
                converted_vacancies.append(vacancy_params)

        return converted_vacancies
