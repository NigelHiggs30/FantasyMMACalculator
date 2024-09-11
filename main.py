from modules.scraper import get_fight_data
from modules.utils import convert_time_to_seconds
from modules.fight_link import url_links
from modules.fight_points_evaluator import evaluate_fight_points
from modules.parser import WebPageParser
from modules.calculator import FantasyPointsCalculator

from bs4 import BeautifulSoup
import requests
import argparse

if __name__ == "__main__":
       
    parser = argparse.ArgumentParser(description="Scrape UFC fighter details.")
    
    parser.add_argument(
        "url",
        type=str,
        help="URL of the UFC fighter details page."
    )
    
    parser.add_argument(
    "--all",
    action="store_true",
    help="Process all fight links from the page."
    )

    args = parser.parse_args()
    url = args.url

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Check fight_link
    fighters_links = url_links(soup)

    if args.all:
        # Loop through all fighter links if --all is passed
        for fighter_link in fighters_links:
            evaluate_fight_points(fighter_link)
    else:
        # Process only the first fighter link
        evaluate_fight_points(fighters_links[0])