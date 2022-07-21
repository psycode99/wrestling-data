from bs4 import BeautifulSoup
import requests

count = 0
search = True
while search:
    if count > 0:
        print(f'\n')

    userinput = input('Which Wrestler do You want to Search Today. Type "exit" to stop: ')
    wrestler = userinput
    userinput = userinput.replace(' ', '-')

    if userinput == 'exit':
        search = False
    else:
        headers = {
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/99.0.4844.51 Safari/537.36'
        }

        url = f'https://www.thesmackdownhotel.com/wrestlers/{userinput}'

        request = requests.get(url=url, headers=headers)
        data = request.text

        soup = BeautifulSoup(data, 'lxml')
        body = soup.body
        div = body.find('div', id='ja-container')
        main = div.find('main', id='ja-mainbody')

        ja_content = main.find('div', id='ja-content')
        article = ja_content.find('article', id='ja-current-content')
        item_page = article.find('div', class_='item-page')
        try:
            wrestling_name = item_page.find('h1', class_='contentheading').text
        except AttributeError:
            print('The wrestler you searched for deos not exit. Check your spelling and try again')
        else:
            gender = item_page.find_all('span', class_='field-value')[0].text
            real_name = item_page.find_all('span', class_='field-value')[1].text
            height_dd = item_page.find('dd', class_='field-entry height')
            height = height_dd.find('span', class_='field-value').text

            weight_dd = item_page.find('dd', class_='field-entry unstyled subfields-inline-text weight')
            weight = weight_dd.find('li').text
            DOB_dd = item_page.find_all('dd', class_='field-entry')[5]
            DOB = DOB_dd.find('span', class_='field-value').text

            birth_place_dd = item_page.find('dd', class_='field-entry from')
            birth_place = birth_place_dd.find('span', class_='field-value').text
            nickname_dd = item_page.find_all('dd', class_='field-entry')[8]
            nickname = nickname_dd.find('span', class_='field-value').text

            titles = item_page.find('dd', class_='field-entry full-width')

            print(f'*************** BASIC DATA ABOUT {wrestler.title()} ********************')
            print(f'Real Name: {real_name}')
            print(f'Gender: {gender}')
            print(f'Date Of Birth: {DOB}')
            print(f'Height: {height}')
            print(f'Weight: {weight}')
            print(f'Birth Place: {birth_place}')
            print(f'Nickname(s): {nickname}')
            print(f'Titles and Accomplishments: ')
            try:
                list_of_titles = titles.find_all('li')
                for title in list_of_titles:
                    print(title.text)
            except AttributeError:
                print('Currently has No Titles')

    count += 1
