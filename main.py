import os
import pytube
import lyrics
import requests
from bs4 import BeautifulSoup

#search and download song from YouTube

def yt_download(song_name, artist_name):
	url_yt = 'https://www.youtube.com/results?search_query=' + song_name.replace(' ', '+')
	res_yt = requests.get(url_yt, stream = True)
	soup_yt = BeautifulSoup(res_yt.text, 'html.parser')
	
	for link in soup_yt.find_all('a'):
		href = link.get('href')
			
		if href.find('/watch') != -1:
			yt = pytube.YouTube('https://youtube.com' + href)
			stream = yt.streams.first()
			print('downloading..... ' + song_name + artist_name)
			stream.download('billboard_top_100_songs/' + song_name)
			lyrics.Azlyrics.lyrics_fetch(song_name)
			break
	
#fetching names of songs and artists from Billboard

def songs_and_artists_list():
	url_bill = 'https://www.billboard.com/charts/hot-100'
	res_bill = requests.get(url_bill)

	if res_bill.status_code == 200:
		print('fetching songs names.... ')
		soup_bill = BeautifulSoup(res_bill.text, 'html.parser')
		songs_list = soup_bill.find_all('h2', class_ = 'chart-row__song')
		artists_list = soup_bill.find_all(class_ = 'chart-row__artist')		
	
		for index in range(0,100):
			os.mkdir('billboard_top_100_songs/' + songs_list[index].get_text())
			yt_download(songs_list[index].get_text(), artists_list[index].get_text())
	else:
		print('connection not established')

if __name__ == '__main__':
	os.makedirs('billboard_top_100_songs', exist_ok = True)
	songs_and_artists_list()
