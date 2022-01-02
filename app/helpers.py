import random
import smtplib
import datetime
from types import NoneType
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
from cloudscraper import CloudScraper
from email.message import EmailMessage

# Local packages
from .secrets import email, app_pw
from .constants import default_subjects, default_models, default_avatar

# -------------------------------------
# Web scraping helper functions
# -------------------------------------

def fetch_model_avatar(response: BeautifulSoup) -> str:
    """Scrape model avatar image data

    Args:
        response (BeautifulSoup): Webpage of the model

    Returns:
        str: Model avatar image source
    """
    html = response.find('img', {'class': 'avatar'})
    avatar = default_avatar

    if type(html) == NoneType: # When theres no avatar
        return avatar
    elif html.has_attr('src'): # When it has src attribute
        avatar = html['src']
    elif html.has_attr('data-cfsrc'): # When it has data-cfsrc attribute
        avatar = html['data-cfsrc']

    return avatar
# <-- End of fetch_model_avatar()

def get_tags(response: BeautifulSoup) -> list[str]:
    """Scrape tags for a video

    Args:
        response (BeautifulSoup): Webpage of the video

    Returns:
        list[str]: Tags for this video
    """
    tags = list()
    html = response.find('h5', {'class': 'tags h6-md'})

    # Loop through every tag
    for tag in html.find_all('a'):
        tags.append(tag.contents[0])

    return tags
# <-- End of get_tags()

def get_date(response: BeautifulSoup) -> datetime:
    """Scrape upload date of a video

    Args:
        response (BeautifulSoup): Webpage of the video

    Returns:
        datetime: Upload time of this video
    """
    now = datetime.datetime.now()
    raw_time = response \
        .find('span', {'class': 'mr-3'}) \
        .contents[0].split(' ')

    x = int(raw_time[0])
    _type = raw_time[1]

    if _type == '小時前':
        upload_time = now - datetime.timedelta(hours=x)
    elif _type == '天前':
        upload_time = now - datetime.timedelta(days=x)
    elif _type == '星期前':
        upload_time = now - datetime.timedelta(weeks=x)
    elif _type == '個月前':
        upload_time = now - datetime.timedelta(days=x*30)
    elif _type == '年前':
        upload_time = now - datetime.timedelta(days=x*365)
    else:
        upload_time = now

    return upload_time.strftime('%m/%d/%Y')
# <-- End of get_date()

def get_videos(
    scraper: CloudScraper,
    response: BeautifulSoup,
    model: str,
    limit: int=0
) -> list[dict[str, str]]:
    """Scrape videos data on jable.tv

    Args:
        scraper (CloudScraper): Scraper engine
        response (BeautifulSoup): Webpage content of the model
        model (str): Name of the model
        limit (int, optional): Number of videos to scrape. Defaults to 0.

    Returns:
        list[dict[str, str]]: [description]
    """
    content = list()
    
    # Loop through model page
    for html in response.find_all('div', {'class': 'col-6 col-sm-4 col-lg-3'}, limit=limit):
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
# <-- End of get_videos()

# -------------------------------------
# Email helper functions
# -------------------------------------

def send_email(recipients: list[str], body: str) -> None:
    """Send email with given body to given recipients

    Args:
        recipients (list[str]): List of recipients' email address
        body (str): Body of the email
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, app_pw)

    message = EmailMessage()
    message['From'] = email
    message['To'] = ', '.join(recipients)
    message['Subject'] = random.choice(default_subjects)
    message.set_content(body, subtype='html')

    server.send_message(message)

    server.quit()
# <-- End of send_mail()

# -------------------------------------
# Database helper functions
# -------------------------------------

def read_models(db_path: str, table: str) -> dict[str, str]:
    """Read all models from database model table, and load to buffer

    Args:
        db_path (str): Path to database
        table (str): Name of models table

    Returns:
        dict[str, str]: A dictionary of models info, [key]: model name, 
        [value]: link to model webpage
    """
    models = dict()
    db = TinyDB(db_path).table(table)

    if len(db) == 0:
        for model, url in default_models.items():
            db_insert_model(db, model, url)
        return default_models

    # Loop through all models in database
    for model in db.all():
        name = model['model']
        link = model['link']

        # Add model to buffer
        models[name] = link

    return models
# <-- End of read_models()

def db_insert_model(
    db: TinyDB,
    model: str,
    link: str,
    avatar: str=default_avatar
) -> bool:
    flag = False
    query = Query()

    if not db.contains(query['model'] == model):
        flag = True

        # Structure document object
        doc = dict()
        doc['model'] = model
        doc['link'] = link
        doc['avatar'] = avatar

        db.insert(doc)

    return flag
# <-- End of db_insert_model()

def db_update_model(
    db: TinyDB,
    model: str,
    avatar: str=default_avatar
) -> bool:
    flag = False
    query = Query()['model'] == model

    doc = db.search(query)[0]
    if (not doc['avatar'] == avatar) and (not avatar == default_avatar):
        flag = True
        # When avatar is not default avatar and they are different
        db.update({'avatar': avatar}, query)

    return flag
# <-- End of db_update_model()

def db_insert_videos(
    db: TinyDB,
    content: list[dict]
) -> bool:
    """Insert only new data to database

    Args:
        db (TinyDB): The database object for saving data

    Returns:
        bool: True if there's new data save to database, False
        otherwise
    """
    # Set flag
    flag = False

    # Set query
    query = Query()

    # Loop through all videos of a model
    for video in content:
        # Query database to get video with same id and link
        video_query = query.fragment({
            'id': video['id'],
            'link': video['link']
        })
        
        # Check if query result is not zero
        is_video_exist = len(db.search(video_query)) > 0
        
        # Check if video already exist in database
        if not is_video_exist:
            flag = True
            # If not exist insert to database
            db.insert(video)
        else:
            db.update({'views': video['views']}, video_query)

    return flag
# <-- End of insert_new_only_db()