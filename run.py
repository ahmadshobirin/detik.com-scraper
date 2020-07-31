import glob
import json

import requests
import bs4
import os
import pandas
session = requests.Session()

def berita_bola():
    url = 'https://sport.detik.com/sepakbola/'
    res = session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    content = res.findAll('li', attrs={'class': 'gtm_newsfeed_artikel'})
    # print(content)
    data = []
    no = 1
    for item in content:
        print(f'Get berita bola ...{no}')
        url = item.find('a')['href'].strip()
        title = item.find('h2').text.strip()
        date = item.find('span', attrs={'class':'f11'}).text.replace('Sepakbola | ', '').strip()
        temp_data_detail = open_berita_detail(url)
        image_url = temp_data_detail['image_url']
        description = temp_data_detail['description']
        data.append({
            "url": url,
            "title": title,
            "date": date,
            'image_url': image_url,
            'description': description
        })
        no += 1

    json_file(data, './results/detik-bola.json')
    print("get berita bola is done...")

def berita_sports():
    url = 'https://sport.detik.com/sport-lain'
    res = session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    content = res.findAll('div', attrs={'class': 'desc_nhl'})
    data = []
    no = 1
    for item in content:
        print(f'Get berita sports lain ...{no}')
        url = item.find('a')['href'].strip()
        title = item.find('h2').text.strip()
        date = item.find('span', attrs={'class': 'f11'}).text.replace('detikSport | ', '').strip()
        temp_data_detail = open_berita_detail(url)
        image_url = temp_data_detail['image_url']
        description = temp_data_detail['description']
        data.append({
            "url": url,
            "title": title,
            "date": date,
            'image_url': image_url,
            'description': description
        })
        no += 1

    json_file(data, './results/detik-sport-lain.json')
    print("get berita sports is done...")

def berita_bisnis():
    url = 'https://finance.detik.com/indeks'
    res = session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    content = res.findAll('article', attrs={'class': 'list-content__item'})

    data = []
    no = 1
    for item in content:
        print(f'Get berita bisnis ...{no}')
        url = item.find('a', attrs={"class":"media__link"})['href'].strip()
        res = session.get(url)
        res = bs4.BeautifulSoup(res.content, 'html.parser')
        title = res.find('h1', attrs={"class":'detail__title'}).text.strip()
        image_url = res.find('img', attrs={"class":"img-zoomin"})
        if(image_url is not None):
            image_url = image_url['src']
        description = res.find('div', attrs={'class': 'detail__body-text'}).text.strip()
        data.append({
            "url": url,
            "title": title,
            'image_url': image_url,
            'description': description
        })
        no += 1
    json_file(data, './results/detik-bisnis.json')
    print("get berita bisnis is done...")

def open_berita_detail(url):
    res = session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    image_url = res.find('img')['src'].strip()
    description = res.find('div', attrs={'id':'detikdetailtext'})
    if description is not None :
        description = description.text.strip()
    return {"image_url": image_url, "description": description}

def json_file(response, name_file):
    if os.path.exists(name_file) == True:
        os.remove(name_file)
    data = []
    for item in response:
        data.append(item)
    with open(name_file, 'w') as outfile:
        json.dump(response, outfile)

def excel_file():
    print('Export all data to csv file...')
    files = sorted(glob.glob('./results/*.json'))
    data_berita = []
    exists_file = "./csv/all-berita-data.xlsx"
    writer = pandas.ExcelWriter(exists_file, engine='xlsxwriter')
    for file in files:
        print(file)
        with open(file) as outfile:
            data = json.load(outfile)
            data_berita = data

        csv = pandas.DataFrame(data_berita)
        sheet_name = file.replace('./results/', '')
        sheet_name = sheet_name.replace('.json', '')
        csv.to_excel(writer, sheet_name=sheet_name)
    #
    writer.save()
    writer.close()

    print('Export all data to csv file is done...')

def menu():
    while True:
        menu = ''
        menu += 'https://www.detik.com/ SCRAPER \n'
        menu += '===================================\n'
        menu += 'Choose Menu :\n'
        menu += '1. Scrap berita bola terbaru \n'
        menu += '2. Scrap berita sports lain terbaru \n'
        menu += '3. Scrap berita bisnis terbaru \n'
        menu += '4. Export berita ke csv \n'
        menu += 'Pilih nomor : '
        option = int(input(menu))
        if(option == 1):
            berita_bola()
        elif(option == 2):
            berita_bisnis()
        elif(option == 3):
            berita_sports()
        elif(option == 4):
            excel_file()

def run():
    menu()

if __name__ == "__main__":
    run()