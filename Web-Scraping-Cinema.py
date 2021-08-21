import bs4, requests

print('Are you searching for a film(0) or an actor(1) ?')
choise = input()

#Input validation
while(choise != '1' and choise != '0'):
    print('Invalid input')
    choise = input()


if(choise != '1'):
    print('Good choise, what film are you looking for?')
    film_title = input()

    #ROTTEN TOMATOES

    #Searching user's film on Rotten Tomatoes
    LINK = 'https://www.rottentomatoes.com/search?search='
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36'}
    response = requests.get(LINK +''.join(film_title), headers = headers)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    #Finding list's films
    film_list = soup.find('search-page-media-row')
    #If film_list == None that's mean that there are no films found
    if(film_list == None):
        film_name_rotten = 'Not Found'
        rating_rotten = 'Not Found'
    else:
        #Finding first film's link
        a_film = film_list.find_all('a')
        link_film = str(a_film[0].get('href'))

        #Finding ratings
        response = requests.get(link_film, headers = headers)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        rating_rotten = str(soup.find('score-board').get('tomatometerscore'))

        #Finding film name
        film_name_rotten = soup.find(class_ = 'scoreboard__title').text


    #METACRITIC

    #Searching user's film on metacritic
    LINK = 'https://www.metacritic.com/search/movie/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36'}
    response = requests.get(LINK + ''.join(film_title) + ''.join('/results'), headers = headers)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    #Finding list's films
    film_list = soup.find('div', class_='result_wrap')
    #If film_list == None that's mean that there are no films found
    if(film_list == None):
        film_name_metacritic = 'Not Found'
        rating_div_metacritic = 'Not Found'
    else:
        #Finding first film's link
        a_film = film_list.find_all('a')
        link_film = str(a_film[0].get('href'))
        link_film_full = ''.join('https://www.metacritic.com') + link_film

        #Finding ratings
        response = requests.get(link_film_full, headers = headers)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        #There are a lot of possibilities in metacritic(different classes for different ratings), 
        #so there is an handle for all of them
        if  (soup.find('span', class_='metascore_w larger movie positive') != None):
            rating_div_metacritic = soup.find('span', class_='metascore_w larger movie positive').text
        elif(soup.find('span', class_='metascore_w larger movie mixed') != None):
            rating_div_metacritic = soup.find('span', class_='metascore_w larger movie mixed').text
        elif(soup.find('span', class_='metascore_w larger movie negative') != None):
            rating_div_metacritic = soup.find('span', class_='metascore_w larger movie negative').text
        elif(soup.find('span', class_='metascore_w larger movie tbd') != None):
            rating_div_metacritic = 'To Be Decided'
        elif(soup.find('span', class_ = 'metascore_w larger movie positive perfect') != None):
            rating_div_metacritic = soup.find('span', class_='metascore_w larger movie positive perfect').text

        #Finding film name
        film_name_metacritic = soup.find(class_ = 'product_page_title oswald').find('h1').text

        


    #IMDB

    #Searching user's film on metacritic
    LINK = 'https://www.imdb.com/find?s=tt&q='
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36'}
    response = requests.get(LINK + ''.join(film_title), headers = headers)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    #Finding list's films
    film_list = soup.find('div', class_='findSection')
    #If film_list == None that's mean that there are no films found
    if(film_list == None):
        film_name_IMDb = 'Not Found'
        rating_div_IMDb = 'Not Found'
    else:
        #Finding first film's link
        a_film = film_list.find_all('a')
        link_film = str(a_film[2].get('href'))
        link_film_full = ''.join('https://www.imdb.com') + link_film

        #Finding ratings
        response = requests.get(link_film_full)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        #In case of film found but the rating's not found
        try:
            rating_div_IMDb = soup.find('span', class_='AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV').text
        except AttributeError:
            rating_div_IMDb = 'Not Found'
            
        #Finding film name
        film_name_IMDb = soup.find(class_ = 'TitleBlock__Container-sc-1nlhx7j-0 hglRHk').find('h1').text
    
            

        
    #Printing movies found because can be different for site to site
    print('\n******MOVIES FOUND******')
    print('IMDb: '+ film_name_IMDb)
    print('Metacritic: '+ film_name_metacritic)
    print('Rotten Tomatoes: '+ film_name_rotten)

    #Printing film's ratings
    print('\n******RATINGS******')

    #IMDb
    if(rating_div_IMDb == 'Not Found'):
        print('IMDb: Not Found')
    else:
        print('IMDb: ' + rating_div_IMDb + '/10')

    #Metacritic
    if(rating_div_metacritic == 'Not Found'):
        print('Metacritic: Not Found')
    elif(rating_div_metacritic == 'To Be Decided'):
        print('Metacritic: To Be Decided')
    else:
        print('Metacritic: ' + rating_div_metacritic + '/100')

    #Rotten Tomatoes
    if(rating_rotten == 'Not Found' or rating_rotten == ''):
        print('Rotten Tomatoes: Not Found')
    else:
        print('Rotten Tomatoes: ' + rating_rotten + '%')


    #Priting movie info (from IMDb)
    print('\n******MOVIE INFO******')
    try:
        movie_info = soup.find('span', class_ = 'GenresAndPlot__TextContainerBreakpointL-cum89p-1 gwuUFD')
    except NameError:
        movie_info = None
    if(movie_info == None or movie_info.text == ''):
        print('Not Found')
    else:
        print(movie_info.text)

    #Printing movie genre(s) (from IMDb)
    print('\n******GENRE(S)******')
    #In case of film or genre(s) not found
    try:
        movie_genres = soup.find('div', class_ = 'ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL').find_all('span', class_ = 'ipc-chip__text')
        for i in range(len(movie_genres)):
            print(movie_genres[i].text)
    except(NameError, TypeError, AttributeError, IndexError):
        print('Not Found')
    
    #Printing movie director(s) (from IMDb)
    print('\n******DIRECTOR(S)******')
    #In case of film or director(s) not found
    try:
        movie_directors = soup.find('div', class_ = 'ipc-metadata-list-item__content-container').find_all('li', class_ = 'ipc-inline-list__item')
        for i in range(len(movie_directors)):
            print(movie_directors[i].text)
    except(NameError, TypeError, AttributeError, IndexError):
        print('Not Found')
    

    #Printing movie actor (from IMDb)
    print('\n******MAIN ACTOR******')
    try:
        movie_actor = soup.find_all('a', class_ = 'StyledComponents__ActorName-y9ygcu-1 eyqFnv')
        print(movie_actor[0].text)
    except(NameError, TypeError, AttributeError, IndexError):
        print('Not Found')


else:
    print('Nice, what actor are you looking for?')
    actor_name = input()

    #Searching user's actor on IMDb
    LINK = 'https://www.imdb.com/find?s=nm&q='
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36'}
    response = requests.get(LINK + ''.join(actor_name) + ''.join('&ref_=nv_sr_sm'), headers = headers)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    #In case of actor not found
    try:
        #Finding actor list and actor's pagelink
        actor_list = soup.find_all('div', class_='findSection')
        a_actor = actor_list[0].find_all('a')
        link_actor = str(a_actor[2].get('href'))
        link_actor_full = ''.join('https://www.imdb.com') + link_actor

        #Finding actor name
        actor_name = actor_list[0].find(class_ = 'result_text').find('a').text
        print('\nActor Found: '+ actor_name)

        #Finding and printing filmography
        print('\n******FILMOGRAPHY******')
        response_filmography = requests.get(link_actor_full, headers = headers)
        response_filmography.raise_for_status()
        soup = bs4.BeautifulSoup(response_filmography.text, 'html.parser')

        #In case of actor found but filmography not found
        try:
            filmography = soup.find('div', id = 'filmo-head-actor').find_next('div').find_all('b')
            for i in range(len(filmography)):
                print(filmography[i].text)
        except (TypeError, AttributeError):
            print('Not Found')
    except IndexError:
        print('\nNo Actor Found\n')

    