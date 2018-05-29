import requests, urllib3
from bs4 import BeautifulSoup

class Azlyrics:
    def lyrics_fetch(song_name):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 
        url_search = 'https://search.azlyrics.com/search.php?q='  + (song_name.replace(' ', '+')).strip()
        res_search = requests.get(url_search)
        soup = BeautifulSoup(res_search.text, 'html.parser')

        for href in soup.find_all('a', target='_blank'):
            link = href.get('href')

            if link.find((song_name.lower()).replace(' ','')) != -1:
                http = urllib3.PoolManager()
                res_lyrics = http.request('GET', link)
                soup_lyrics = BeautifulSoup(res_lyrics.data, 'lxml')
                lyrics = soup_lyrics.find('div', attrs = {'class': None, 'id': None})

                if lyrics != None:
                    with open('billboard_top_100_songs/' + song_name + '/' +song_name + '.txt', 'w') as lyrics_file:
                        print('downloading lyrics....\n')
                        lyrics_file.write(lyrics.get_text())
                        break
                else:
                    print('lyrics not found')
#if __name__  == '__main__':
#       Azlyrics.lyrics_fetch('meant to be')
			
