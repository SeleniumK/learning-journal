import os
import requests
import json
from learning_journal.models import DBSession, Base, Entry
import transaction
from sqlalchemy import create_engine


def get_journal_entries():
    url = "https://sea401d2.crisewing.com/api/export?apikey="
    key = os.environ.get("JOURNAL_KEY", "")
    params = {"username": "SeleniumK"}
    response = requests.get(url + key, params=params)
    response.raise_for_status()
    return response.text


def get_compatible_dicts(json_listings):
    listing_collection = []
    for listing in json_listings:
        entry = {
            "title": listing["title"],
            "text": listing["text"],
            "created": listing["created"],
        }
        listing_collection.append(entry)
    return listing_collection


def populate_db(listing):
    entry = Entry(**listing)
    DBSession.add(entry)


def import_entries():
    results = get_journal_entries()
    json_listings = json.loads(results)
    return get_compatible_dicts(json_listings)


def main():
    database_url = os.environ.get('DATABASE_URL', None)
    engine = create_engine(database_url)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        for entry in import_entries():
            populate_db(entry)


if __name__ == "__main__":
    main()
