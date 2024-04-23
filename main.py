import requests
from bs4 import BeautifulSoup
import os 
from concurrent.futures import ThreadPoolExecutor

def download(url, filename):
 response = requests.get(url)
 path_to_file = f'{filename}.png'

 with open(path_to_file, 'wb') as handle:
    handle.write(response.content)

 print(f'Файл {path_to_file} успешно скачан!')

def stickers(name):
 sticker = BeautifulSoup(requests.get(f'https://api.allorigins.win/raw?url=https://vkklub.ru/ru/search/?q={name}').text, 'html.parser').find('div', 'textsblock').find('div', 'title').find('a', href=True)['href'].split('/')[3]
 urls = []
 names = []
 ran = 0
 ran = len(BeautifulSoup(requests.get(f'https://api.allorigins.win/raw?url=https://vkklub.ru/ru/stickers/{sticker}/').text, 'html.parser').find_all('div', 'stickers_list_item'))

 os.makedirs(f'{sticker}_stickers')

 for i in range(ran):
  id = ''
  if len(str(i)) == 1:
    id = '00' + str(i)
  elif len(str(i)) == 2:
    id = '0' + str(i)
  urls.append(f'https://vkklub.ru/_data/stickers/{sticker}/sticker_vk_{sticker}_{id}.png')
  names.append(f'{sticker}_stickers/{id}')

  with ThreadPoolExecutor(max_workers=16) as executor:
    executor.map(download, urls, names)
    urls.remove(f'https://vkklub.ru/_data/stickers/{sticker}/sticker_vk_{sticker}_{id}.png')
    names.remove(f'{sticker}_stickers/{id}')
#input('\033[33m {}' .format('[+]Enter name: '))

with open('stickers.txt') as file:
  lines = [line.rstrip() for line in file]

for name in lines:
  stickers(name)
