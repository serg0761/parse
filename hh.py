from bs4 import BeautifulSoup as bs
import requests


def get_link(lang, page):
    vacancy = 'программист'
    link = 'https://ekaterinburg.hh.ru/search/vacancy?text=' + vacancy + '+' + lang + \
    '&page=' + str(page)
    return link
    


def hh_parse(link, head):
    result =  {}
    session = requests.Session()
    request = session.get(link,headers = head)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa':'vacancy-serp__vacancy'})
        for div in divs:
            title = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'})['href']
            salary = div.find('div', attrs={'data-qa':'vacancy-serp__vacancy-compensation'})
            if salary is None:
                res_salary = '--'
            else:
                res_salary = salary.text
            result[str(title)] = href, res_salary
    else:
        print('NO OK')
    
    return result
 

        
lang = str(input('Введите язык программирования?'))

head = {'accept':'*/*', 
           'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


vacancies = {}
for page in range(0, 4):
    link = get_link(lang, page)
    vacancies.update(hh_parse(link, head))


print(vacancies)