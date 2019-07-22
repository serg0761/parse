driver.common.by import By
from selenium.webdriver.common.keys import Keys

from pymongo import MongoClient


url = 'https://mail.ru'
driver = webdriver.Chrome()
driver.get(url)


assert 'Mail.ru' in driver.title
driver.find_element_by_id('mailbox:login').send_keys('bsn_test_box')
driver.find_element_by_id('mailbox:password').send_keys('justparol99')
driver.find_element_by_id('mailbox:submit').click()
wait = WebDriverWait(driver, 15);
wait.until(EC.title_contains('Входящие'));
assert 'Входящие' in driver.title

all_letters = driver.find_elements_by_xpath("//a[contains(@class,'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal')]")


date_for_base = []
for let in all_letters:
    link = let.get_attribute('href')
    author = let.find_element_by_class_name('ll-crpt').get_attribute('title')
    date = let.find_element_by_class_name('llc__item_date').get_attribute('title')
    subject = let.find_element_by_class_name('ll-sj__normal').text
    date_for_base.append({'author':author, 'date':date, 'subject':subject, 'link':link})


for date in date_for_base:
    link = date['link']
    driver.get(link)
    wait.until(EC.presence_of_element_located((By.XPATH,"//*[contains(@id,'_BODY')]")))
    let_text =  driver.find_element_by_xpath("//*[contains(@id,'_BODY')]").text
    date['text'] = let_text
    driver.back()
    wait.until(EC.title_contains('Входящие'))


client = MongoClient('mongodb://127.0.0.1:27017')

db = client['mail']
maildb = db.mail
maildb.insert_many(date_for_base)

driver.close()

