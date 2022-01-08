import os
import time
import random
import cloudscraper
import numpy as np
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query

# Local packages
from . import helpers
from .secrets import email
from .constants import default_subjects


class Scraper:
    def __init__(self) -> None:
        """Constructor for Scraper"""
        # Set random seed
        random.seed(time.time())

        # Initialize webscraping engine
        self.scraper = cloudscraper.create_scraper()

        # Data paths
        self._data_path: str = os.path.normpath(  # Set path to data directory
            os.path.join(os.path.dirname(__file__), "../data/")
        )
        self._db_path: str = os.path.join(self._data_path, "db.json")

        # Load model buffer
        self.models = helpers.read_models(self._db_path, "models")

    # <-- End of __init__()

    def add_model(self, model: str, url: str) -> None:
        """Add a model to database models table

        Args:
            model (str): Model name
            url (str): Link to model page
        """
        self.models[model] = url

    # <-- End of add_model()

    def remove_model(self, model_name: str) -> bool:
        """Remove a model from database and buffer

        Args:
            model_name (str): Name of the model to be removed

        Returns:
            bool: True if removes successfully, False otherwise
        """
        flag = False
        db = TinyDB(self._db_path).table("models")
        query = Query()["model"] == model_name

        # Check if database contains model
        if db.contains(query):
            flag = True
            db.remove(query)  # If so remove it

        # Check if buffer contains model
        if model_name in self.models:
            flag = True
            self.models.pop(model_name)

        return flag

    # <-- End of remove_model()

    def fetch(self) -> None:
        """Fetch, parse and save data"""
        # Set content to an empty list
        content = np.array([])

        models_db = TinyDB(self._db_path).table("models")
        videos_db = TinyDB(self._db_path).table("videos")

        # Loop through all models and scrape
        for model, url in self.models.items():
            # Fetch webpage data
            response = BeautifulSoup(self.scraper.get(url).content, "lxml")
            # Update model avatar
            avatar = helpers.fetch_model_avatar(response)
            if not helpers.db_insert_model(models_db, model, url, avatar):
                # When model already exists in database check if it needs
                # to update avatar
                helpers.db_update_model(models_db, model, avatar)
            # Append data to content list
            content = np.append(
                content, helpers.get_videos(self.scraper, response, model)
            )

        helpers.db_insert_videos(videos_db, content.tolist())

    # <-- End of fetch()

    def format_daily_email(self) -> str:
        # Load email templates
        with open(
            os.path.join(self._data_path, "daily_email_content.html"), "r"
        ) as file:
            template = file.read()
        with open(os.path.join(self._data_path, "daily_email.html"), "r") as file:
            body = file.read()

        # Get a random video
        db = TinyDB(self._db_path).table("videos")
        video = random.choice(db.all())

        # Get two random models
        db = TinyDB(self._db_path).table("models")
        models = random.sample(db.all(), 2)

        template = template.format(
            # Recommend video
            model=video["model"],
            image=video["image"],
            name=video["name"],
            views=f'{video["views"]:,}',
            likes=f'{video["likes"]:,}',
            tags=", ".join(video["tags"]),
            link=video["link"],
            # Suggest model 1
            suggested_model_1=models[0]["model"],
            avatar_1=models[0]["avatar"],
            punchline_1=random.choice(default_subjects),
            suggested_model_link_1=models[0]["link"],
            # Suggest model 2
            suggested_model_2=models[1]["model"],
            avatar_2=models[1]["avatar"],
            punchline_2=random.choice(default_subjects),
            suggested_model_link_2=models[1]["link"],
        )

        body = body.replace("{% content %}", template)

        with open(os.path.join(self._data_path, "output.html"), "w") as file:
            file.write(body)

        return body

    # <-- End of format_daily_email()

    def format_weekly_email(self) -> str:
        """Use email format in data directory to format email body

        Returns:
            str: The email body in string
        """
        # Fetch email headline template
        with open(
            os.path.join(self._data_path, "weekly_email_headline.html"), "r"
        ) as file:
            headline = file.read()

        # Fetch email video template
        with open(
            os.path.join(self._data_path, "weekly_email_content.html"), "r"
        ) as file:
            template = file.read()

        htmls = np.array([])
        videos_db = TinyDB(self._db_path).table("videos")
        videos = helpers.db_select_videos(videos_db, self.models.keys())

        # Loop through data in a step of 2
        for idx in np.arange(1, len(videos), 2):
            # Append headline
            htmls = np.append(
                htmls, headline.replace("{% headline %}", videos[idx]["model"])
            )

            htmls = np.append(
                htmls,
                template.format(
                    # Left video box
                    image_1=videos[idx - 1]["image"],
                    name_1=videos[idx - 1]["name"],
                    link_1=videos[idx - 1]["link"],
                    # String format for , between numbers
                    views_1=f'{videos[idx - 1]["views"]:,}',
                    # Right video box
                    image_2=videos[idx]["image"],
                    name_2=videos[idx]["name"],
                    link_2=videos[idx]["link"],
                    # String format for , between numbers
                    views_2=f'{videos[idx]["views"]:,}',
                ),
            )

        # Format email body, connect everything together
        with open(os.path.join(self._data_path, "weekly_email.html"), "r") as file:
            body = file.read()
            body = body.replace("{% content %}", "\n".join(htmls))

        return body

    # <-- End of format_weekly_email()

    def send_daily_email(self) -> None:
        """Send daily email to recipients with random recommend video"""
        body = self.format_daily_email()
        helpers.send_email([email], body)  # DEBUG

    # <-- End of send_email()

    def send_weekly_email(self) -> None:
        body = self.format_weekly_email()
        helpers.send_email([email], body)  # DEBUG


# <-- End of class Scraper
