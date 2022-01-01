import unittest
import cloudscraper
from bs4 import BeautifulSoup

from app import helpers

class TestHelpers(unittest.TestCase):
    scraper = cloudscraper.create_scraper()

    def test_fetch_model_avatar(self):
        link_works = [
            'https://jable.tv/models/yua-mikami/',
            'https://jable.tv/models/shinoda-yuu/',
            'https://jable.tv/models/aizawa-minami/',
            'https://jable.tv/models/momonogi-kana/'
        ]

        for link in link_works:
            avatar = helpers.fetch_model_avatar(self.scraper, link)
            self.assertNotEqual(
                avatar,
                'https://raw.githubusercontent.com/konsav/email-templates/master/images/list-item.png'
            )

        link_not_works = [
            'https://jable.tv/models/kaede-karen/',
            'https://jable.tv/models/miru/',
            'https://jable.tv/models/f0e279c00b2a7e1aca2ef4d31d611020/'
        ]

        for link in link_not_works:
            avatar = helpers.fetch_model_avatar(self.scraper, link)
            self.assertEqual(
                avatar,
                'https://raw.githubusercontent.com/konsav/email-templates/master/images/list-item.png'
            )
    # <-- End of test_fetch_model_avatar()

    def test_get_tags(self):
        response = BeautifulSoup(
            self.scraper.get('https://jable.tv/videos/ssis-233/').content,
            'lxml'
        )
        tags = helpers.get_tags(response)
        self.assertEqual(
            tags,
            ['主奴調教','制服誘惑','角色劇情','少女','巨乳','短髮','絲襪','黑絲','調教','潮吹','凌辱','NTR','美腿','OL','錄像','廁所','偷拍']
        )
        
        response = BeautifulSoup(
            self.scraper.get('https://jable.tv/videos/ssis-204/').content,
            'lxml'
        )
        tags = helpers.get_tags(response)
        self.assertEqual(
            tags,
            ['主奴調教','角色劇情','少女','巨乳','顏射','短髮','出軌','痴女','調教']
        )
    # <-- End of test_get_tags()

    def test_get_videos(self):
        response = BeautifulSoup(
            self.scraper.get('https://jable.tv/models/arina-hashimoto/').content,
            'lxml'
        )
        video = helpers.get_videos(
            scraper=self.scraper,
            response=response,
            model='橋本有菜',
            limit=1
        )[0]
        
        self.assertEqual(video['model'], '橋本有菜')
        self.assertEqual(video['id'], 'FSDSS-335')
        self.assertEqual(video['name'], '【要照我說的那樣尿哦】橋本有菜 超快感JOI！ ASMR小惡魔的射精輔助 橋本有菜')
        self.assertEqual(video['link'], 'https://jable.tv/videos/fsdss-335/')
    # <-- End of test_get_video()


if __name__ == '__main__':
    unittest.main()
