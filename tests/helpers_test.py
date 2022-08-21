import datetime
from cloudscraper import create_scraper
from bs4 import BeautifulSoup

from app.helpers import (
    get_date,
    get_tags,
    get_videos,
    fetch_model_avatar
)


class TestHelpers():
    scraper = create_scraper()
    default_avatar = "https://raw.githubusercontent.com/konsav/email-templates/master/images/list-item.png"

    def test_fetch_model_avatar(self):
        link_works = [
            "https://jable.tv/models/yua-mikami//",
            "https://jable.tv/models/shinoda-yuu/",
            "https://jable.tv/models/aizawa-minami/",
            "https://jable.tv/models/momonogi-kana/",
        ]

        for link in link_works:
            response = self.scraper.get(link)
            assert response.status_code == 200

            soup = BeautifulSoup(response.content, "lxml")
            assert isinstance(soup, BeautifulSoup)

            avatar = fetch_model_avatar(soup)
            assert avatar != self.default_avatar

        link_not_works = [
            "https://jable.tv/models/kaede-karen/",
            "https://jable.tv/models/miru/",
            "https://jable.tv/models/f0e279c00b2a7e1aca2ef4d31d611020/",
        ]

        for link in link_not_works:
            response = self.scraper.get(link)
            assert response.status_code == 200

            soup = BeautifulSoup(response.content, "lxml")
            assert isinstance(soup, BeautifulSoup)

            avatar = fetch_model_avatar(soup)
            assert avatar == self.default_avatar
    # <-- End of test_fetch_model_avatar()

    def test_get_tags(self):
        response = self.scraper.get("https://jable.tv/videos/ssis-233/")
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, 'lxml')
        assert isinstance(soup, BeautifulSoup)

        date = get_date(soup)
        assert isinstance(date, str)
        datetime.datetime.strptime(date, '%m/%d/%Y')

        tags = get_tags(soup)
        assert isinstance(tags, list) and \
            all(isinstance(tag, str) for tag in tags)

        response = self.scraper.get("https://jable.tv/videos/ssis-204/")
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, 'lxml')
        assert isinstance(soup, BeautifulSoup)

        date = get_date(soup)
        assert isinstance(date, str)
        datetime.datetime.strptime(date, '%m/%d/%Y')

        tags = get_tags(soup)
        assert isinstance(tags, list) and \
            all(isinstance(tag, str) for tag in tags)
    # <-- End of test_get_tags()

    def test_get_videos(self):
        response = self.scraper.get("https://jable.tv/videos/ssis-233/")
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, 'lxml')
        assert isinstance(soup, BeautifulSoup)

        videos = get_videos(self.scraper, soup, model="橋本有菜", limit=5)
        assert isinstance(videos, list) and \
            all(isinstance(video, dict) for video in videos) and \
            all(video.get('model') is not None for video in videos) and \
            all(video.get('id') is not None for video in videos) and \
            all(video.get('name') is not None for video in videos) and \
            all(video.get('image') is not None for video in videos) and \
            all(video.get('link') is not None for video in videos) and \
            all(video.get('views') is not None for video in videos) and \
            all(video.get('likes') is not None for video in videos) and \
            all(video.get('tags') is not None for video in videos)
    # <-- End of test_get_video()

# <-- End of TestHelpers
