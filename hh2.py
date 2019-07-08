from bs4 import BeautifulSoup as bs
import requests
#from pymongo import MongoClient


def get_link(lang, page):
    vacancy = 'программист'
    link = 'https://ekaterinburg.hh.ru/search/vacancy?text=' + vacancy + '+' + lang + \
    '&page=' + str(page)
    return link
    


def hh_parse(link, head):
    result =  []
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
                min_salary = '--'
                max_salary = '--'
            else:
                currency = salary.text[-4:].strip().lower()
                if currency == 'eur':
                    k = 71.66
                elif currency == 'usd':
                    k = 63.58
                else:
                    k = 1
                first_word = salary.text[:2].lower()
                spam = salary.text.split('-')
                spam_salary = []
                for sal in spam:
                    spam_s = sal.split()
                    for spams in spam_s:
                        try:
                            spam_salary.append(int(spams))
                        except ValueError:
                            pass
                res_salary = []
                for i in range(0, len(spam_salary), 2):
                    if spam_salary[i + 1] == 0:
                        res_salary.append(int(str(spam_salary[i]) + '000') * k)
                    else:
                        res_salary.append(int(str(spam_salary[i]) + str(spam_salary[i + 1])) * k)
                if first_word == 'от':
                    min_salary = min(res_salary)
                    max_salary = '--'
                elif first_word == 'до':
                    max_salary = max(res_salary)
                    min_salary = '--'
                else:
                    min_salary = min(res_salary)
                    max_salary = max(res_salary)
                    
                
            result.append([str(title), href, min_salary, max_salary])
    else:
        print('NO OK')
    
    return result
 

#def to_db(data):
#    hhdbs.insert(data)
#    client = MongoClient('mongodb://127.0.0.1:27017')
#    db = client['goods']
#    goodsdb = db.goods
#     good_data={
#        'name': good_links[i*2]['title'],
#        'href': 'https://www.avito.ru'+good_links[i*2]['href'],
#        'price': price[i]['content']
#    }
#    goodsdb.insert(good_data)





        
lang = str(input('Введите язык программирования?'))

head = {'accept':'*/*', 
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


vacancies = []
for page in range(0, 3):
    link = get_link(lang, page)
    print(page)
    print(hh_parse(link, head))
    #vacancies.append(hh_parse(link, head))


print(vacancies)