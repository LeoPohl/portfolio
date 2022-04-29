import email
import csv
import requests
from bs4 import BeautifulSoup
import pprint
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def my_sites(page_name):
    return render_template(page_name)

def write_to_csv(data):
    with open('database.csv', mode='a') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thanks.html')
        except:
            return 'did not save to database'
    else:
        return 'something failed'

def write_to_json(data):
    with open('./templates/hacker_news.json', 'w', encoding='utf-8') as output:
        json.dump(data, output, ensure_ascii=False)

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
    hn = sort_stories_by_votes(hn)
    index = 0
    for item in hn:
        hn[index]['id'] = index+1
        index+=1
    
    return write_to_json(hn)

@app.route('/hacker_news.html')
def get_hacker_news():
    res_page1 = requests.get('https://news.ycombinator.com/news')
    res_page2 = requests.get('https://news.ycombinator.com/news?p=2')
    soup = BeautifulSoup(res_page1.text, 'html.parser')
    soup.append(BeautifulSoup(res_page2.text, 'html.parser'))

    links = soup.select('.titlelink')
    subtext = soup.select('.subtext')
    create_custom_hn(links, subtext)
    return render_template('hacker_news.html')

@app.route('/data')
def get_hn_data():
    with open('./templates/hacker_news.json', 'r', encoding='utf-8') as output:
        hacker_news = json.load(output)
        return json.dumps(hacker_news)