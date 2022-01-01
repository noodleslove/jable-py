import datetime
from bs4 import BeautifulSoup
from cloudscraper import CloudScraper

def fetch_model_avatar(scraper: CloudScraper, model_url: str) -> str:
    # Fetch url page content
    response = BeautifulSoup(scraper.get(model_url).content, 'lxml')

    try: # Try to fetch avatar img source
        html = response.find('img', {'class': 'avatar'})
        avatar = html['src']
    except TypeError: # Use a placeholder if theres no avatar
        avatar = 'https://raw.githubusercontent.com/konsav/email-templates/master/images/list-item.png'

    return avatar


def get_tags(response: BeautifulSoup) -> list[str]:
    tags = list()
    html = response.find('h5', {'class': 'tags h6-md'})

    # Loop through every tag
    for tag in html.find_all('a'):
        tags.append(tag.contents[0])

    return tags

def get_date(response: BeautifulSoup) -> datetime:
    now = datetime.datetime.now()
    raw_time = response \
        .find('span', {'class': 'mr-3'}) \
        .contents[0].split(' ')

    x = raw_time[0]
    _type = raw_time[1]

    if _type == '小時前':
        upload_time = now - datetime.timedelta(hours=x)
    elif _type == '天前':
        upload_time = now - datetime.timedelta(days=x)
    elif _type == '個星期前':
        upload_time = now - datetime.timedelta(weeks=x)
    elif _type == '個月前':
        upload_time = now - datetime.timedelta(days=x*30)
    elif _type == '年前':
        upload_time = now - datetime.timedelta(days=x*365)
    else:
        upload_time = now

    return upload_time

def get_videos(
    scraper: CloudScraper,
    response: BeautifulSoup,
    model: str
) -> list[dict[str, str]]:
    content = list()
    
    # Loop through model page
    for html in response.find_all('div', {'class': 'col-6 col-sm-4 col-lg-3'}):
        video = dict()
        
        # Add model name to video
        video['model'] = model
        
        # Parse video id and video name
        raw_name = html.h6.contents[0].contents[0].split(' ')
        video_id = raw_name[0]
        name = ' '.join(raw_name[1:])
        
        video['id'] = video_id
        video['name'] = name
        
        # Parse video image source
        video['image'] = html.img['data-src']
        
        # Parse video link
        video['link'] = html.a['href']
        
        # Parse video view count
        subtitle = html.find('p', {'class': 'sub-title'})
        views = subtitle.contents[2].replace(' ', '').strip('\n')
        views = int(views)
        video['views'] = views

        # Parse video like count
        likes = subtitle.contents[4].replace(' ', '').strip('\n')
        likes = int(likes)
        video['likes'] = likes

        # Fetch video page
        video_page = BeautifulSoup(scraper.get(video['link']).content, 'lxml')

        # Get video tags
        video['tags'] = get_tags(video_page)
        # Get video upload time
        video['upload time'] = get_date(video_page)

        # Check if there's subtitle
        if '中文字幕' in video['tags']:
            video['subtitile'] = True
        else:
            video['subtitle'] = False
        
        # Add video to model content
        content.append(video)

    return content

