from src.api_classes import HeadHunterAPI, SuperJobAPI
from src.json_class import WorkFile


def job_selection():
    keyword = input(f'Введите ключевое слово для поиска: ').lower()
    return keyword


def data_search(vacancy):
    """Загрузка информации с сайтов для поиска работы """

    user_input = input(f'Выберите плтформу для поиска:\n'
                       f'1 - поиск на платформе hh.ru\n'
                       f'2 - поиск на платформе superjob.ru\n'
                       f'3 - поиск на обеих платформах\n'
                       f'Ваш выбор: '
                       )

    if user_input == '1':
        hh = HeadHunterAPI(vacancy)
        converted_vacancies = hh.validate_vacancies()
    elif user_input == '2':
        sj = SuperJobAPI(vacancy)
        converted_vacancies = sj.validate_vacancies()
    else:
        hh = HeadHunterAPI(vacancy)
        sj = SuperJobAPI(vacancy)
        converted_vacancies = hh.validate_vacancies()
        converted_vacancies.extend(sj.validate_vacancies())

    return converted_vacancies


def main():
    vacancy = job_selection()
    converted_vacancies = data_search(vacancy)
    print(f'Найдено: {len(converted_vacancies)} вакансий \n\n')

    wf = WorkFile(vacancy, converted_vacancies)
    vacancies = wf.sorted_by_salary()

    sorted_by = input(f'Отсортировать вакансии?:\n'
                      f'1 - по минимальной зарплате по убыванию\n'
                      f'2 - по максимальной зарплате по убыванию\n'
                      f'3 - не сортировать ')

    if sorted_by == '1':
        vacancies = sorted(vacancies, reverse=True)
    elif sorted_by == '2':
        vacancies = sorted(vacancies, key=lambda x: x.salary_to if x.salary_to else 0, reverse=True)

    for vacs in vacancies:
        print(vacs, end='\n\n')

    print(f'Подобрано вакансий: {len(vacancies)}')


if __name__ == '__main__':
    main()
