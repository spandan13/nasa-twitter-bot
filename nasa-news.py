import requests #The python requests module
from bot import requests as req #The requests module within the repo
import bs4
from bot import status
from settings import config
from logs import logger
import twitterbot as twtbot

def make_soup(url):
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, "lxml")
    return soup

def get_news_articles():
    soup = make_soup('https://www.jpl.nasa.gov/news?sortBy=latestDate')
    output = soup.find_all('div', class_='SearchResultCard')
    new_news = []
    with open(config.log_file, 'r') as log:
        already_posted = log.read()
    for index, article in enumerate(output):
        link = output[index]('a')[0].get('href')
        if not link in already_posted:
            new_news.append(article)
    return new_news

def tweet_poster(news):
    if len(news) == 0:
        print("No new updates found!")
    else:
        for article in news:
            title = article('h2')[0].text
            link = article('a')[0].get('href')
            full_link = 'https://www.jpl.nasa.gov' + link
            soup = make_soup(full_link)
            output = soup.find('div', class_='BaseImagePlaceholder')
            try: # Normal image
                img_link = output('img')[0].get('data-src')
                img_id = str(img_link).split('images/')[1].split('.')[0]
            except IndexError: # Probably a youtube video
                try:
                    video_link = output('iframe')[0].get('src')
                    img_id = str(video_link).split('/')[-1].split('?')[0]
                    img_link = (f"https://img.youtube.com/vi/{img_id}/maxresdefault.jpg")
                except IndexError:
                    img_id = "default_img"
                    img_link = "https://cdn.mos.cms.futurecdn.net/baYs9AuHxx9QXeYBiMvSLU.jpg"
            media = req.get_img_file(img_link, img_id, config.temp_downloads, news=True)
            tweet_text = (f"\U0001F4F0 #NASA News Update: {title}.\n\U000027A1 More Details: {full_link}")
            t = status.Tweet(media, tweet_text, reply_id=None)
            tweet_id = t.post_to_twitter(config.api, config.auth_v1)
            post_number = twtbot.get_post_number(config.log_file)
            log_line = logger.log_line(post_number, tweet_id, media.split('/')[5], link, request_user='NEWS')
            logger.add_line(log_line, config.log_file)
            print(f"News posted: {''.join(title.split()[:4])} - {tweet_id}")


def main():
    new_news = get_news_articles()
    tweet_poster(new_news)

if __name__ == "__main__":
    main()