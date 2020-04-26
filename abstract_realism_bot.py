import os
from dotenv import load_dotenv
import tweepy
import requests
import json
import random

load_dotenv()

abstract = []
real = []


def twitter_api():
    api_key = os.getenv("API_KEY")
    api_secret_key = os.getenv("API_SECRET_KEY")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api


# twitter_api().update_status(status="hello world!")

def get_abstract():
    i = 0
    while i < 36:
        i += 1
        urls = 'https://www.wikiart.org/en/paintings-by-style/abstract-art?json=2&page=' + str(i)
        r = requests.get(urls)
        parsed = json.loads(r.content)
        abstract_paints = parsed['Paintings']
        abstract.append(abstract_paints)
        continue

    return abstract


def get_real():
    i = 0
    while i < 60:
        i += 1
        urls = 'https://www.wikiart.org/en/paintings-by-style/realism?json=2&page=' + str(i)
        r = requests.get(urls)
        parsed = json.loads(r.content)
        real_paints = parsed['Paintings']
        real.append(real_paints)
        continue

    return real


def save_json(parsed_data_list, parsed_data_list_2):
    painting_list = json.dumps(parsed_data_list)
    painting_list2 = json.dumps(parsed_data_list_2)
    with open('abstract.json', 'w') as f:
        f.write(painting_list)
        f.close()
    with open('real.json', 'w') as f:
        f.write(painting_list2)
        f.close()
    print("json files have been saved.")


def open_abstract_json():
    abstract_paintings = json.load(open('abstract.json'))
    print("Abstract Paintings json file has been opened.")
    return {'abstract_paintings': abstract_paintings}


def open_real_json():
    realism_paintings = json.load(open('real.json'))
    print("Realism Paintings json file has been opened.")
    return {'realism_paintings': realism_paintings}


def randomly_select_piece(art_list):
    randomize = random.choice(art_list)
    random_select = random.choice(randomize)
    random_image = random_select['image']
    year = random_select['year']
    title = random_select['title']
    artist_name = random_select['artistName']
    print(random_image, year, artist_name, title)

    return {'random_select': random_select, 'random_image': random_image,
            'year': year, 'title': title, 'artistName': artist_name}


def save_abstract_image(random_image):
    r = requests.get(random_image)
    with open('abstract.jpg', 'wb') as f:
        f.write(r.content)
        print('abstract.jpg saved.')
    return r.status_code


def save_real_image(random_image):
    r = requests.get(random_image)
    with open('real.jpg', 'wb') as f:
        f.write(r.content)
        print("real.jpg saved.")
    return r.status_code


def assemble_tweet(selected_1, selected_2):
    title_1 = selected_1['title']
    artist_name_1 = selected_1['artistName']
    year_1 = selected_1['year']

    title_2 = selected_2['title']
    artist_name_2 = selected_2['artistName']
    year_2 = selected_2['year']

    tweet = f"{title_1}, {artist_name_1}, {year_1} (abstract)\n" \
            f"{title_2}, {artist_name_2}, {year_2} (realism)" \
            f"\n#abstractart #realism  "
    print(tweet)

    filenames = ['abstract.jpg', 'real.jpg']

    media_ids = []
    for filename in filenames:
        res = twitter_api().media_upload(filename)
        media_ids.append(res.media_id)

    twitter_api().update_status(status=tweet, media_ids=media_ids)
    print('tweet sent.')


# get_abstract()
# get_real()
# save_json(abstract, real)


saved_abstract = open_abstract_json()
abstract_art = saved_abstract['abstract_paintings']


saved_real = open_real_json()
realism_art = saved_real['realism_paintings']

selected_real = randomly_select_piece(realism_art)
selected_abstract = randomly_select_piece(abstract_art)

abstract_image = save_abstract_image(selected_abstract['random_image'])
real_image = save_real_image(selected_real['random_image'])


assemble_tweet(selected_abstract, selected_real)




