import requests
from bs4 import BeautifulSoup


def write_html_to_file(html: str, file_name: str):
    """
    Функция для записи HTMl данных в файл (чтобы не дергать лишний раз сервис)
    :param html: HTML верстка
    :param file_name: название выходного файла
    """
    with open(file_name, "w") as file:
        file.write(html)


def read_html_from_file(file_name: str) -> str:
    """
    Функция для чтения HTML данных из файла
    :param file_name: название файла откуда необходимо прочитать данные
    :return: прочитанные данные из файла
    """
    with open(file_name, "r") as file:
        result = file.read()
    return result


def make_request(url: str) -> str:
    """
    Функция для получения HTML верстки с сайта
    :param url: страница к которой необходимо сделать запрос
    :return: HTML разметку (пустая строка в случае ошибки запроса)
    """
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    return ""


def parse_html(html: str) -> list:
    """
    Функция для парсинга HTML с целью нахождения номеров законопроектов
    :param html: HTML верстка страницы которую парсим
    :return: массив со всеми номерами законопроектов
    """
    soup = BeautifulSoup(html, "lxml")
    projects = soup.find_all("div", {"class": "click_open"})
    result: list = []
    for project in projects:
        project_num = project.find("span", {"class": "o_num"}).text.split("\n")[0]
        result.append(f"{project_num}\n")
    return result


def main():
    # Основные URL
    result_url_pattern = "http://asozd.duma.gov.ru/main.nsf/(Spravka)?OpenAgent&RN="
    url = "https://sozd.duma.gov.ru/oz?b%5BNumberSpec%5D=&b%5BAnnotation%5D=&b%5BYear%5D=&b%5BIsArchive%5D%5B0%5D=cnv-2&b%5BFzNumber%5D=&b%5BNameComment%5D=&b%5BResolutionnumber%5D=&b%5BfirstCommitteeCond%5D=and&b%5BsecondCommitteeCond%5D=and&b%5BExistsEventsDate%5D=&b%5BMaxDate%5D=&b%5BDecisionsDateOfCreate%5D=&b%5BconclusionRG%5D=&b%5BdateEndConclusionRG%5D=&b%5BResponseDate%5D=&b%5BAmendmentsDate%5D=&b%5BSectorOfLaw%5D=&b%5BClassOfTheObjectLawmakingId%5D=34f6ae40-bdf0-408a-a56e-e48511c6b618&date_period_from_Year=&date_period_to_Year=&cond%5BClassOfTheObjectLawmaking%5D=any&cond%5BThematicBlockOfBills%5D=any&cond%5BPersonDeputy%5D=any&cond%5BFraction%5D=any&cond%5BRelevantCommittee%5D=any&cond%5BResponsibleCommittee%5D=any&cond%5BHelperCommittee%5D=any&cond%5BExistsEvents%5D=any&cond%5BLastEvent%5D=any&cond%5BExistsDecisions%5D=any&cond%5BLastDecisions%5D=any&cond%5BQuestionOfReference%5D=any&cond%5BSubjectOfReference%5D=any&cond%5BFormOfTheObjectLawmaking%5D=any&cond%5BinSz%5D=any&date_period_from_ExistsEventsDate=&date_period_to_ExistsEventsDate=&date_period_from_MaxDate=&date_period_to_MaxDate=&date_period_from_DecisionsDateOfCreate=&date_period_to_DecisionsDateOfCreate=&date_period_from_dateEndConclusionRG=&date_period_to_dateEndConclusionRG=&date_period_from_ResponseDate=&date_period_to_ResponseDate=&date_period_from_AmendmentsDate=&date_period_to_AmendmentsDate=&count_items=250#data_source_tab_b"

    # Получаем HTMl и записываем в файл (после сохранения файла закомментить!)
    html_data = make_request(url)
    write_html_to_file(html_data, "data.html")

    # Считываем HTML из файла и парсим его
    html_data = read_html_from_file("data.html")
    projects_nums = parse_html(html_data)

    # Записываем полученный результат в файл
    with open("result.txt", "w") as file:
        file.writelines(f"{result_url_pattern}{num}" for num in projects_nums)


if __name__ == '__main__':
    main()
