import requests
from bs4 import BeautifulSoup
import pprint


def get_response_data():
    page = 1
    text_data = ''

    while True:
        res = requests.get(f'https://news.ycombinator.com/news?p={page}')
        s = BeautifulSoup(res.text, 'html.parser')

        # check if all data lists are empty
        if s.select('.rank') and s.select('.titlelink') and s.select('.score'):
            text_data += res.text
            page += 1
        else:
            print('No more data available')
            break

    soup = BeautifulSoup(text_data, 'html.parser')
    ranks_data = soup.find_all('span', class_='rank')
    titles_data = soup.find_all('a', class_='titlelink')
    votes_data = soup.find_all('span', class_='score')

    return [ranks_data, titles_data, votes_data]


def get_hacker_news(ranks, titles, votes):

    data = []
    for pos, rank in enumerate(ranks):
        obj = {}
        obj['rank'] = int(rank.text.replace('.', ''))
        obj['title'] = titles[pos - 1].text
        obj['link'] = titles[pos - 1].get('href')
        obj['vote'] = int(votes[pos - 1].text.split(' ')[0] if votes[pos - 1] else 0)
        data.append(obj)

    # filter votes >= 20 and sort by votes: desc = True
    return sorted(list(filter(lambda x: x['vote'] >= 20, data)), key=lambda el: el['vote'], reverse=True)


custom_data = get_hacker_news(*get_response_data())

pprint.pprint(custom_data)  # [{key1:value1,key2:value2,key3:value3},{...},{...},...]


################################
# *.find_all() or css selectors:
#! title = soup.select('.titlelink')

# *methods in gettin text
#! text == get_text() == getText()
################################
