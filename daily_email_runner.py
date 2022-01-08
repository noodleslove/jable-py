from app.scraper import Scraper

if __name__ == "__main__":
    s = Scraper()
    s.send_daily_email()
