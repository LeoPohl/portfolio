import requests
from bs4 import BeautifulSoup
import pprint

res_page1 = requests.get('https://news.ycombinator.com/news')
res_page2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(res_page1.text, 'html.parser')
soup.append(BeautifulSoup(res_page2.text, 'html.parser'))

links = soup.select('.titlelink')
subtext = soup.select('.subtext')

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['points'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        votes = subtext[idx].select('.score')
        if len(votes):
            title = item.getText()
            href = item.get('href', None) 
            points = int(votes[0].getText().replace(' points', '')) 
            if points > 99:
                hn.append({'title': title, 'link': href, 'points': points})
    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(links, subtext))