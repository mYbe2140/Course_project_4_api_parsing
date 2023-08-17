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


class SuperJobAPI(AbstractAPI):
    """Класс для получения информации по API с сайта SuperJob.ru"""

    def __init__(self, vacancy: str):
        self.vacancy = vacancy
        self.vacancies = []
        self.__url = 'https://api.superjob.ru/2.0/vacancies/'
        self.__key = 'objects'
        self.__params = {'keyword': self.vacancy,
                         'page': 0,
                         'count': 100
                         }
        self.__headers = {
            'X-Api-App-Id': "v3.r.137731249.b7fe13521a4bbb6ac31e5abf2855f5ca9db946d0.3b6587be779e179b65760cac0d523dcc8a3b38a2"
        }

    @property
    def url(self):
        return self.__url

    @property
    def params(self):
        return self.__params

    @property
    def key(self):
        return self.__key

    @property
    def headers(self):
        return self.__headers

    def get_requests(self):
        data = requests.get(self.__url, headers=self.__headers, params=self.__params)
        return data.json()[self.__key]

    def get_vacancies(self, pages_count=1):
        while self.__params['page'] < pages_count:
            print(f"SuperJob, Парсинг страницы {self.__params['page'] + 1}", end=": ")
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
            if vac['payment_from'] is None and vac['payment_to'] is None:
                salary = {'salary': False}
            else:
                salary = {'salary': True}

                vacancy_params = {'id': vac['id'],
                                  'title': vac['profession'],
                                  'employer': vac['firm_name'],
                                  'url': vac['link'],
                                  'experience': vac['experience']['title'],
                                  'salary_from': vac['payment_from'],
                                  'salary_to': vac['payment_to'],
                                  'currency': vac['currency'],
                                  'api': 'SuperJob'
                                  }
                vacancy_params.update(salary)
                converted_vacancies.append(vacancy_params)

        return converted_vacancies


class Vacancy:
    """Класс для обработки и сравнения вакансий"""

    def __init__(self, title, employer, url, experience, salary,
                 salary_from, salary_to, currency, api):
        self.title = title
        self.employer = employer
        self.url = url
        self.experience = experience
        self.salary = salary
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.api = api

    def __gt__(self, other):
        if not other.salary_from:
            return True
        elif not self.salary_from:
            return False
        return self.salary_from >= other.salary_from

    def __str__(self):
        if self.salary is False:
            salary_from = 'не указана'
            salary_to = ''
            currency = ''

        else:
            currency = self.currency
            if self.salary_from and self.salary_from != 0:
                salary_from = f'От {self.salary_from}'
            else:
                salary_from = f''
            if self.salary_to and self.salary_to != 0:
                salary_to = f'До {self.salary_to}'
            else:
                salary_to = f''

        return f'Вакансия: {self.title}\nРаботодатель: {self.employer}\nURL: {self.url}\n' \
               f'Зарплата: {salary_from} {salary_to} {currency}'
