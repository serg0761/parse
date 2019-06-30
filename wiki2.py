from requests import get
import re


def get_link(topic):
    link = "https://ru.wikipedia.org/wiki/" + topic.capitalize()
    return link


def get_topic_page(link):
    html = get(link).text
    return html


def get_topic_text(link):
    html_content = get_topic_page(link)
    words = re.findall("[а-яА-Я]{3,}",html_content)
    return words


def get_common_words(link):
    words_list = get_topic_text(link)
    rate={}
    for word in words_list:
        if word in rate:
            rate[word] += 1
        else:
            rate[word] = 1
    rate_list = list(rate.items())
    rate_list.sort(key = lambda x :-x[1])

    return rate_list


def visualize_common_words(link):
    words = get_common_words(link)
    for w in words[0:10]:
        print(f'{w[0]} встречается {w[1]} раз')


def get_first_link(link):
    list1 = get_topic_page(link)
    links = re.findall(r'a rel="nofollow" class="external text" href="http(.*?)"',list1)
    first_link = 'http' + links[0]
    
    return first_link
    
topic = str(input())

link = get_link(topic)
first_link = get_first_link(link)
print(first_link)

visualize_common_words(first_link)