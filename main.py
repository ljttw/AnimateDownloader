from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests as rq

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('query')
    url = f"https://anime1.me/?s={search_query}"
    #get page and parse it
    page = rq.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #get all article
    articles = soup.find_all('article')
    #get article > header > h2 > a > href
    anime_list = {}
    for article in articles:
        header = article.find('header')
        h2 = header.find('h2')
        a = h2.find('a')
        anime_list[a.text] = a['href']
    
    #while is a href text is "較舊的文章" then get href link and parse it again
    while True:
        try:
            next_page = soup.find('div', class_='nav-previous')
            if(next_page == None):
                break
            a = next_page.find('a')
            url = a['href']
            page = rq.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            articles = soup.find_all('article')
            for article in articles:
                header = article.find('header')
                h2 = header.find('h2')
                a = h2.find('a')
                anime_list[a.text] = a['href']
        except:
            break
        
    
    # sort by key
    anime_list = dict(sorted(anime_list.items()))
    
    #remove if key not contain search query
    for key in list(anime_list):
        if search_query not in key:
            del anime_list[key]
            
    #foreach value get page and parse it
    for key in anime_list:
        url = anime_list[key]
        page = rq.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        #click button (class = "vjs-big-play-button")
        button = soup.find('button', class_='vjs-big-play-button')
        #get video link
        
    
    return render_template('result.html', result=anime_list)

    
    

if __name__ == '__main__':
    app.run(debug=True)