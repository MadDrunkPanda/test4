import requests
import re
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import lxml
import json

id_regex = re.compile(r"\d+")

headers_gen = Headers(os="win", browser="chrome")

main_s = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers_gen.generate())
main_hh_html = main_s.text
main_soup = BeautifulSoup(main_hh_html, "lxml")
main_tag = main_soup.find("main", class_="vacancy-serp-content")


def get_data():
    data = []
    for vacancy_tag in main_tag.find_all("div", class_="vacancy-serp-item__layout"):
        header_tag = vacancy_tag.find("h3")
        header = header_tag.text
        # нашел название вакансии

        a_tag = header_tag.find("a")
        link = a_tag["href"]
        # отдельная ссылка

        company_tag = vacancy_tag.find("div", class_="vacancy-serp-item__meta-info-company")
        company_tag2 = company_tag.find("a", class_="bloko-link bloko-link_kind-tertiary")
        x = r"\xa0"
        company1 = company_tag2.text
        company = re.sub(x, ' ', company1)
        # достал название компании

        city = vacancy_tag.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
        # город

        vac_link = requests.get(link, headers=headers_gen.generate())
        vac_html = vac_link.text
        vac_soup = BeautifulSoup(vac_html, "lxml")
        vac_text = vac_soup.find('div', {'data-qa': 'vacancy-description'}).text
        # прошел по ссылке.получил описание вакании

        salary_tag = vacancy_tag.find('span', class_='bloko-header-section-2')
        if salary_tag == None:
            salary1 = 'Зарплата не указана'
        else:
            salary1 = salary_tag.text
        z = r"\u202f000 "
        salary = re.sub(z, ' 000', salary1)

        if "Django" or "django" or "Flask" or "flask" in vac_text:
            data.append(
                {
                "header": header,
                "link": link,
                "company": company,
                "city": city,
                "salary": salary
            }
            )
    return data

def write_json(dictdata, filename):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(dictdata, outfile, ensure_ascii=False)


write_json(get_data(),'writescrap.json')