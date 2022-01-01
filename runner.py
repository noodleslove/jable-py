from app.scraper import Scraper
from app.secrets import email, recipients

if __name__ == '__main__':
    s = Scraper()

    s.format_daily_email()