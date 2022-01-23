import numpy as np
from tinydb import TinyDB, Query

# Local packages
from .helpers import convert_timestamp, format_video_names
from .constants import default_models, default_avatar

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
        name = model["model"]
        link = model["link"]

        # Add model to buffer
        models[name] = link

    return models
# <-- End of read_models()


def db_insert_model(
    db: TinyDB, model: str, link: str, avatar: str = default_avatar
) -> bool:
    """Insert model to database

    Args:
        db (TinyDB): Model database
        model (str): Model name
        link (str): Url of model webpage
        avatar (str, optional): Avatar image source. Defaults to default_avatar.

    Returns:
        bool: True if it inserted model, False otherwise
    """
    flag = False
    query = Query()

    if not db.contains(query["model"] == model):
        flag = True

        # Structure document object
        doc = dict()
        doc["model"] = model
        doc["link"] = link
        doc["avatar"] = avatar

        db.insert(doc)

    return flag
# <-- End of db_insert_model()


def db_update_model(db: TinyDB, model: str, avatar: str = default_avatar) -> bool:
    """Update model avatar

    Args:
        db (TinyDB): Models database
        model (str): Model name
        avatar (str, optional): Avatar image source. Defaults to default_avatar.

    Returns:
        bool: True if it updated avatar, False otherwise
    """
    flag = False
    query = Query()["model"] == model

    doc = db.search(query)[0]
    if (not doc["avatar"] == avatar) and (not avatar == default_avatar):
        flag = True
        # When avatar is not default avatar and they are different
        db.update({"avatar": avatar}, query)

    return flag
# <-- End of db_update_model()


def db_insert_videos(db: TinyDB, content: list[dict]) -> bool:
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
        video_query = query.fragment({"id": video["id"], "link": video["link"]})

        # Check if query result is not zero
        is_video_exist = len(db.search(video_query)) > 0

        # Check if video already exist in database
        if not is_video_exist:
            flag = True
            # If not exist insert to database
            db.insert(video)
        else:
            db.update({"views": video["views"]}, video_query)

    return flag
# <-- End of insert_new_only_db()


def db_cleanup(db: TinyDB, models: dict[str, str]) -> None:
    """Remove videos of models not in database.

    Args:
        db (TinyDB): Videos database
        models (dict[str, str]): Models buffer
    """
    query = Query()

    # Remove all videos of model not in models buffer
    db.remove(query["model"].test(lambda x: x not in models))
# <-- End of db_cleanup()


def db_select_videos(db: TinyDB, models: list[str]) -> list[dict]:
    """Randomly select videos from database for email content.

    Args:
        db (TinyDB): Videos database
        models (list[str]): List of wanted models to watch

    Returns:
        list[dict]: List of randomly selected videos
    """
    query = Query()
    videos = np.array([])

    for model in models:
        model_videos = np.array(db.search(query.model == model))

        # format videos
        convert_timestamp(model_videos)
        format_video_names(model_videos)

        model_videos = np.array(
            sorted(model_videos, key=lambda v: v["upload time"], reverse=True)
        )
        videos = np.append(videos, model_videos[:2])

    return videos
# <-- End of db_select_videos()


def insert_email(emails):
    def transform(doc):
        doc.append()


def db_insert_schedule(
    db: TinyDB,
    email: str,
    minute: int,
    hour: int,
    dow: list[str]
):
    query = Query().fragment({'minute': minute, 'hour': hour, 'dow': dow})

    if not db.contains(query):
        db.insert({'emails': [email], 'minute': minute,
                  'hour': hour, 'dow': dow})
    else:
        db.update(lambda x: x['emails'].append(email), query)
