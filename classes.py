import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import random

class Movies:
  HEADER = {'Accept': '*/*', 'Connection': 'keep-alive', 
  'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36 OPR/54.0.2952.64'}
  URL = "https://www.imdb.com/chart/top"
  URL2 = 'https://www.rottentomatoes.com/top/bestofrt/#:~:text=Best%20of%20Rotten%20Tomatoes%20%20%20%20Rank,%20%20525%20%2051%20more%20rows%20'

  def __init__(self):
    self.soup = self.get_page(self.URL)
    self.soup_rotten = self.get_page(self.URL2)
    self.get_all_movies_imdb()
    self.get_all_movies_rotten_tomatoes()
  
  def get_page(self,url):
    r = requests.get(url, headers=self.HEADER)
    if r.status_code == 200:
      soup = BeautifulSoup(r.text, 'html.parser')
      return soup
    return r.status_code
  
  def get_all_movies_imdb(self):
    self.movies250 = []
    td = self.soup.select_one('tbody').select('td')
    for i, val in enumerate(td):
      if i%5 == 0:
        rank, title, year = td[i+1].getText().strip().split('\n')
        rating = td[i+2].getText().strip()
        self.movies250.append({'rank':int(rank.replace('.','')),'title':title.strip(), 'year':int(year[1:-1]), 'rating':float(rating)})
    return self.movies250
  
  def get_all_movies_rotten_tomatoes(self):
    self.movies100 = []
    td2 = self.soup_rotten.find('table',class_='table').select('td')
    for k, val2 in enumerate(td2):
      if k%4 == 0:
        rank = int(td2[k].getText()[:-1])
        score = td2[k+1].getText().strip()
        *title, year = td2[k+2].getText().strip().split('(')
        title = '('.join(title)
        year = int(year[:-1])
        reviewers = td2[k+3].getText().strip()
        self.movies100.append({'rank':rank, 'title':title, 'year':year, 'reviewer_count':reviewers})
    return self.movies100


class AppManager(Movies):
  menu = """
    1. Top 10 Movies from IMDB 
    2. Top 10 Movies from Rotten Tomatoes
    3. Random Movie
    4. Random Movie from IMDB 
    5. Random Movie from Rotten Tomatoes
    5. Quit 
    """
  def show_top10_imdb(self):
    t = PrettyTable(['rank','title (year)', 'rating'], align='l')
    for data in self.movies250[:10]:
      t.add_row([data['rank'], f"{data['title']} ({data['year']})",data['rating'] ])
    print('IMDB TOP 10')
    print(t)
  
  def show_top10_rotten_tomatoes(self):
    t = PrettyTable(['rank','title (year)', 'reviewer_count'], align='l')
    for data in self.movies100[:10]:
      t.add_row([data['rank'], f"{data['title']} ({data['year']})",data['reviewer_count'] ])
    print('ROTTEN TOMATOES TOP 10')
    print(t)
  
  def show_random_movie(self,source=None):
    ''' Takes input "imdb" or "rt" to return a random movie
    from given source, if no source is entered, returns random
    movie from a combination of the two sources'''
    try:
      if source == None:
        selected = random.choice(self.movies100 + self.movies250)
        print('\n-------------------------------------\n')
        print(f"{selected['title']} ({selected['year']})")
        print('\n-------------------------------------')

      elif source.lower() == 'imdb':
        selected = random.choice(self.movies250)
        print('\n-------------------------------------\n')
        print(f"{selected['title']} ({selected['year']})")
        print('\n-------------------------------------')
         
      elif source.lower() == 'rt':
        selected = random.choice(self.movies100)
        print('\n-------------------------------------\n')
        print(f"{selected['title']} ({selected['year']})")
        print('\n-------------------------------------')
      
      if source not in [None,'imdb', 'rt', 'IMDB', 'RT']:
        print('\n-------------------------------------\n')
        print('Invalid input')
        print('\n-------------------------------------')

    except AttributeError as e:
      print(e)
