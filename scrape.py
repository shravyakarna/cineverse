import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver

# Launch web driver and fetch the page
driver = webdriver.Safari()
driver.get('https://letterboxd.com/dave/list/imdb-top-250/by/release-earliest/page/3/')
driver.implicitly_wait(10)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract film slugs
films = [div['data-film-slug'] for div in soup.find_all('div', class_='film-poster')]
filmurls = ["https://letterboxd.com/film/" + x for x in films]

# Initialize lists to store data
titles = []
release_years = []
summaries = []
runtimes = []
ratings = []
genres_ = []
languages = []
directors = []
main_casts = []
image_urls = []
reviews1=[]
reviews2=[]
reviews3=[]



# Iterate through each movie URL
for url in filmurls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract movie title and release year
    title_release_tag = soup.find('meta', property='og:title')
    if title_release_tag:
        title_release = title_release_tag['content']
        title, release_year = re.match(r'(.+) \((\d{4})\)', title_release).groups()
    else:
        title = None
        release_year = None
    titles.append(title)
    release_years.append(release_year)

    # Extract movie duration
    runtime_match = re.search(r'runTime: (\d+)', str(soup))
    runtime = int(runtime_match.group(1)) if runtime_match else None
    runtimes.append(runtime)

    # Extract movie rating
    rating_tag = soup.find('meta', attrs={'name': 'twitter:data2'})
    rating = rating_tag['content'] if rating_tag else None
    ratings.append(rating)

    # Extracting movie genres
    genre_div = soup.find('div', class_='text-sluglist capitalize')
    genre_links = genre_div.find_all('a') if genre_div else []
    genres = [link.text.strip() for link in genre_links]
    genres_.append(genres)

    # Extracting movie language
    language_h3 = soup.find('h3', string=re.compile('Language', re.IGNORECASE))
    language_div = language_h3.find_next_sibling('div', class_='text-sluglist') if language_h3 else None
    language_link = language_div.find('a') if language_div else None
    language = language_link.text.strip() if language_link else None
    languages.append(language)

    # Extract directors and main cast
    cast_list = soup.find('div', class_='cast-list')
    director_tag = soup.find('meta', attrs={'name': 'twitter:label1', 'content': 'Directed by'})
    director = director_tag.find_next_sibling('meta', attrs={'name': 'twitter:data1'})['content'] if director_tag else None

    main_casts_ = []
    if cast_list:
        actors = cast_list.find_all('a', class_='tooltip')
        main_casts_ = [actor.text.strip() for actor in actors[:5]]  
    directors.append(director)
    main_casts.append(main_casts_)  # Append the main_casts_ list, not the main_casts list

    # Extract plot summary
    plot_summary_tag = soup.find('div', class_='truncate')
    plot_summary = plot_summary_tag.text.strip() if plot_summary_tag else None
    summaries.append(plot_summary)

    # Extract image URL
    image_url_tag = soup.find('meta', property='og:image')
    image_url = image_url_tag['content'] if image_url_tag else None
    image_urls.append(image_url)

    reviews=[]


    for film_detail in soup.find_all('li', class_='film-detail')[:3]:  # Slice to get only the first 3 reviews
        review = film_detail.find('div', class_='body-text').text.strip()
        reviews.append(review)
        
    reviews1.append(reviews[0])
    reviews2.append(reviews[1])
    reviews3.append(reviews[2])


# Check if all lists have the same length
data_lengths = [len(titles), len(release_years), len(runtimes), len(ratings), len(genres_), len(languages), len(directors), len(main_casts), len(summaries), len(image_urls),len(reviews1),len(reviews2),len(reviews3)]
if len(set(data_lengths)) != 1:
    raise ValueError("All lists must have the same length")

# Create dictionary with movie data
movie_data = {
    'title': titles,
    'release year': release_years,
    'duration': runtimes,
    'rating': ratings,
    'genres': genres_,
    'language': languages,
    'directors': directors,
    'main cast': main_casts,
    'plot summary': summaries,
    'image url': image_urls,
    'reviewsone': reviews1,
    'reviewstwo': reviews2,
    'reviewsthree': reviews3

}

# Convert dictionary to DataFrame
movies_df = pd.DataFrame(movie_data)

# Save DataFrame to CSV file
movies_df.to_csv('moviedata.csv', index=False, sep='|')



