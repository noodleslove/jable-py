import random
import smtplib
import datetime
import numpy as np
from bs4 import BeautifulSoup
from cloudscraper import CloudScraper
from email.message import EmailMessage

# Local packages
from .secrets import email, app_pw
from .constants import default_subjects, default_avatar

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
    html = response.find("img", {"class": "avatar"})
    avatar = default_avatar

    if html is None:  # When theres no avatar
        return avatar
    elif html.has_attr("src"):  # When it has src attribute
        avatar = html["src"]
    elif html.has_attr("data-cfsrc"):  # When it has data-cfsrc attribute
        avatar = html["data-cfsrc"]

    return avatar
# <-- End of fetch_model_avatar()


def get_tags(response: BeautifulSoup) -> list[str]:
    """Scrape tags for a video

    Args:
        response (BeautifulSoup): Webpage of the video

    Returns:
        list[str]: Tags for this video
    """
    tags = np.array([])
    html = response.find("h5", {"class": "tags h6-md"})

    # Loop through every tag
    for tag in html.find_all("a"):
        tags = np.append(tags, tag.contents[0])

    return tags.tolist()
# <-- End of get_tags()


def get_date(response: BeautifulSoup) -> datetime:
    """Scrape upload date of a video

    Args:
        response (BeautifulSoup): Webpage of the video

    Returns:
        datetime: Upload time of this video
    """
    now = datetime.datetime.now()
    raw_time = response.find("span", {"class": "mr-3"}).contents[0].split(" ")

    x = int(raw_time[0])
    _type = raw_time[1]

    if _type == "小時前":
        upload_time = now - datetime.timedelta(hours=x)
    elif _type == "天前":
        upload_time = now - datetime.timedelta(days=x)
    elif _type == "星期前":
        upload_time = now - datetime.timedelta(weeks=x)
    elif _type == "個月前":
        upload_time = now - datetime.timedelta(days=x * 30)
    elif _type == "年前":
        upload_time = now - datetime.timedelta(days=x * 365)
    else:
        upload_time = now

    return upload_time.strftime("%m/%d/%Y")
# <-- End of get_date()


def get_videos(
    scraper: CloudScraper, response: BeautifulSoup, model: str, limit: int = 0
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
    for html in response.find_all(
        "div", {"class": "col-6 col-sm-4 col-lg-3"}, limit=limit
    ):
        video = dict()

        # Add model name to video
        video["model"] = model

        # Parse video id and video name
        raw_name = html.h6.contents[0].contents[0].split(" ")
        video_id = raw_name[0]
        name = " ".join(raw_name[1:])

        video["id"] = video_id
        video["name"] = name

        # Parse video image source
        video["image"] = html.img["data-src"]

        # Parse video link
        video["link"] = html.a["href"]

        # Parse video view count
        subtitle = html.find("p", {"class": "sub-title"})
        views = subtitle.contents[2].replace(" ", "").strip("\n")
        views = int(views)
        video["views"] = views

        # Parse video like count
        likes = subtitle.contents[4].replace(" ", "").strip("\n")
        likes = int(likes)
        video["likes"] = likes

        # Fetch video page
        video_page = BeautifulSoup(scraper.get(video["link"]).content, "lxml")

        # Get video tags
        video["tags"] = get_tags(video_page)
        # Get video upload time
        video["upload time"] = get_date(video_page)

        # Check if there's subtitle
        if "中文字幕" in video["tags"]:
            video["subtitile"] = True
        else:
            video["subtitle"] = False

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
    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, app_pw)

    message = EmailMessage()
    message["From"] = email
    message["To"] = ", ".join(recipients)
    message["Subject"] = random.choice(default_subjects)
    message.set_content(body, subtype="html")

    server.send_message(message)

    server.quit()
# <-- End of send_mail()


def convert_timestamp(videos: list[dict]) -> None:
    for video in videos:
        video["upload time"] = datetime.datetime.strptime(
            video["upload time"], "%m/%d/%Y"
        )
# <-- End of convert_timestamp()


def format_video_names(videos: list[dict]) -> None:
    CHAR_LIMIT = 30
    CHAR_LIMIT_WITH_DOT = CHAR_LIMIT - 3
    for video in videos:
        video["name"] = (
            video["name"] if len(video["name"]) < CHAR_LIMIT else
            video["name"][:CHAR_LIMIT_WITH_DOT] + "..."
        )
# <-- End of format_video_names()
