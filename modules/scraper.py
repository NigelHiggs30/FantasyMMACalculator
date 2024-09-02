import requests
from bs4 import BeautifulSoup

def get_fight_data(url: str)-> BeautifulSoup:
    # Given a link, we should be able to return the fantasy MMA score of the fight.
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    return soup