import os
import time
import random
import smtplib
import cloudscraper
from . import helpers
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
from .secrets import email, app_pw
from .constants import default_subjects, default_models
from email.message import EmailMessage


class Scraper:

    def __init__(self) -> None:
        """Constructor for Scraper
        """
        # Initialize variables
        self.scraper = cloudscraper.create_scraper()
        self._data_path: str = os.path.normpath( # Set path to data directory
            os.path.join(os.path.dirname(__file__), '../data/')
        )
        self._db_path: str = os.path.join(self._data_path, 'db.json')
        self.subjects: list[str] = default_subjects

        # Check if database has any data
        db = TinyDB(self._db_path).table('models')

        if len(db) == 0:
            self.models: dict[str, str] = default_models
            self.fetch_models()
        else:
            self.read_models()
    # <-- End of __init__()

    def read_models(self) -> None:
        """Read all models from database model table, and load to buffer
        """
        self.models = dict()
        db = TinyDB(self._db_path).table('models')

        # Loop through all models in database
        for model in db.all():
            name = model['model']
            link = model['link']

            # Add model to class buffer
            self.models[name] = link
    # <-- End of read_models()

    def add_model(self, model: tuple[str, str]) -> bool:
        """Add a model to database models table

        Args:
            model (tuple[str, str]): Model information, [0]: model name 
            [1]: link to model page

        Returns:
            bool: True if add model successfully, False otherwise
        """
        flag = False
        db = TinyDB(self._db_path).table('models')
        query = Query()

        if not db.contains(query['model'] == model[0]):
            flag = True
            
            # Construct database document object
            model_info = dict()
            model_info['model'] = model[0]
            model_info['link'] = model[1]
            model_info['avatar'] = self.fetch_avatar(model[1])

            # Save to database and buffer
            db.insert(model_info)
            self.models[model[0]] = model[1]

        return flag
    # <-- End of add_model()

    def remove_model(self, model_name: str) -> bool:
        """Remove a model from database and buffer

        Args:
            model_name (str): Name of the model to be removed

        Returns:
            bool: True if removes successfully, False otherwise
        """
        flag = False
        db = TinyDB(self._db_path).table('models')
        query = Query()['model'] == model_name

        # Check if database contains model
        if db.contains(query):
            flag = True
            db.remove(query) # If so remove it
            self.models.pop(model_name)

        return flag

    def fetch_avatar(self, url: str) -> str:
        """Fetch avatar image source

        Args:
            url (str): Link to the model page

        Returns:
            str: Model avatar image source
        """
        # Fetch website data
        response = BeautifulSoup(self.scraper.get(url).content, 'lxml')

        try: # Try to fetch avatar img source
            html = response.find('img', {'class': 'avatar'})
            avatar = html['src']
        except TypeError: # Use a placeholder if theres no avatar
            avatar = 'https://raw.githubusercontent.com/konsav/email-templates/master/images/list-item.png'

        return avatar
    # <-- End of fetch_avatar()

    def fetch_models(self) -> bool:
        models = list()
        # Loop through all models and scrape
        for model, url in self.models.items():
            model_info = dict()

            model_info['model'] = model
            model_info['avatar'] = self.fetch_avatar(url)

            models.append(model_info)

        return self.insert_models_db(
            TinyDB(os.path.join(self._data_path, 'db.json')).table('models'),
            models
        )
    # <-- End of fetch_models()


    def fetch_videos(self) -> bool:
        """Fetch and parse data

        Returns:
            bool: True if new data was found, False otherwise
        """
        # Set content to an empty list
        content = list()
        
        # Loop through all models and scrape
        for model, url in self.models.items():
            # Fetch website data
            response = BeautifulSoup(self.scraper.get(url).content, 'lxml')
            # Append data to content list
            content.extend(
                helpers.get_videos(self.scraper, response, model)
            )

        # Save new data to database when finish
        return self.insert_videos_db(
            # save to `videos` table
            TinyDB(os.path.join(self._data_path, 'db.json')).table('videos'),
            content
        )
    # <-- End of fetch_videos()


    def insert_models_db(self, db: TinyDB, content: list[dict[str, str]]) -> bool:
        """Insert all newly fetch data to database

        Args:
            db (TinyDB): Database object for saving fetch data
            content (list[dict[str, str]]): Content to be inserted

        Returns:
            bool: True if theres new model inserted, False otherwise
        """
        # Set flag
        flag = False

        # Set query
        query = Query()

        # Loop through all models
        for model in content:
            # Insert model to database
            if not db.contains(query['model'] == model):
                flag = True
                db.insert(model)
        
        return flag
    # <-- End of insert_models_db()


    def insert_videos_db(self, db: TinyDB, content: list[dict]) -> bool:
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


    def format_daily_email(self) -> str:
        # Set random seed
        random.seed(time.time())

        # Load email templates
        with open(os.path.join(self._data_path, 'email_main.html'), 'r') as file:
            template = file.read()
        with open(os.path.join(self._data_path, 'email.html'), 'r') as file:
            body = file.read()

        # Get a random video
        db = TinyDB(self._db_path).table('videos')
        video = random.choice(db.all())
        
        # Get two random models
        db = TinyDB(self._db_path).table('models')
        models = random.sample(db.all(), 2)

        template = template.format(
            # Recommend video
            model=video['model'],
            image=video['image'],
            name=video['name'],
            views=f'{video["views"]:,}',
            likes=f'{video["likes"]:,}',
            tags=', '.join(video['tags']),
            link=video['link'],
            # Suggest model 1
            suggested_model_1=models[0]['model'],
            avatar_1=models[0]['avatar'],
            # Suggest model 2
            suggested_model_2=models[1]['model'],
            avatar_2=models[1]['avatar']
        )

        body = body.replace('{% content %}', template)

        with open(os.path.join(self._data_path, 'output.html'), 'w') as file:
            file.write(body)

        return body
    # <-- End of format_daily_email()


    def format_weekly_email(self) -> str:
        """Use email format in data directory to format email body

        Returns:
            str: The email body in string
        """
        # Fetch email headline template
        with open(os.path.join(self._data_path, 'headline.html'), 'r') as file:
            headline = file.read()

        # Fetch email video template
        with open(os.path.join(self._data_path, 'component.html'), 'r') as file:
            template = file.read()
        
        htmls = list()
        for model, videos in self.contents.items():
            # Append headline
            htmls.append(headline.replace('{% headline %}', model))
            
            # Loop through data in a step of 2
            for idx in range(1, len(videos), 2):
                htmls.append(template.format(
                    # Left video box
                    videos[idx - 1]['image'],
                    videos[idx - 1]['name'],
                    videos[idx - 1]['link'],
                    # String format for , between numbers
                    f'{videos[idx - 1]["views"]:,}',
                    # Right video box
                    videos[idx]['image'],
                    videos[idx]['name'],
                    videos[idx]['link'],
                    # String format for , between numbers
                    f'{videos[idx]["views"]:,}'
                ))
        
        # Format email body, connect everything together
        with open(os.path.join(self._data_path, 'base.html'), 'r') as file:
            body = file.read()
            body = body.replace('{% content %}', '\n'.join(htmls))

        return body
    # <-- End of format_weekly_email()


    def send_email(self, body: str, recipients: list[str]) -> None:
        """Send email with latest video data

        Args:
            body (str): The body of email
            recipients (list[str]): The list of recipients for this email
        """
        server = smtplib.SMTP('smtp.gmail.com', 587)
        
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, app_pw)
        
        message = EmailMessage()
        message['From'] = email
        message['To'] = ', '.join(recipients)
        message['Subject'] = random.choice(self.subjects)
        body = self.format_email()
        message.set_content(body, subtype='html')
        
        server.send_message(message)
        
        server.quit()
    # <-- End of send_email()
# <-- End of class Scraper