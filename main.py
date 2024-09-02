from scraper import get_fight_data
from utils import convert_time_to_seconds
from fight_link import url_links
from parser import WebPageParser
from calculator import FantasyPointsCalculator
from bs4 import BeautifulSoup
import requests
import argparse

def main(url):
     ##url of specific fight.
    # url = "http://ufcstats.com/fight-details/4047e98132306cd5"
    website_data = get_fight_data(url)
    # print(website_data)

    #parsing logic for the variables of interest.
    parser_html = WebPageParser(website_data)

     # Extract fight details
    fight_results_dic, fighter_1_name, fighter_2_name = parser_html.winner_looser()
    fight_method, fight_round, fight_time, fight_format = parser_html.extract_fight_details()
    
    # Extract scoring moves
    fight_data = parser_html.extract_scoring_moves()

    # Initialize the FantasyPointsCalculator with the parsed fight details
    calculator = FantasyPointsCalculator(
        fight_results_dic, 
        fighter_1_name, 
        fighter_2_name, 
        fight_method, 
        fight_round, 
        fight_time, 
        fight_format
    )

    fighter_1_score, fighter_2_score = calculator.calculate_points(*fight_data)

    # Determine the winner
    winner = None
    if fight_results_dic[fighter_1_name] == "W":
        winner = fighter_1_name
    elif fight_results_dic[fighter_2_name] == "W":
        winner = fighter_2_name

    if fight_round == 1:
        #assign points
        if winner == fighter_1_name:
                fighter_1_score += 90
        elif winner == fighter_2_name:
                fighter_2_score += 90  # type: ignore
        # check if fight ended 60 seconds in
        temp = convert_time_to_seconds(fight_time)
        if int(temp) <=60:
            #bonus points.
            if winner == fighter_1_name:
                fighter_1_score += 25
            elif winner == fighter_2_name:
                fighter_2_score += 25  # type: ignore

    if fight_round == 2:
            #assign points
        if winner == fighter_1_name:
                fighter_1_score += 70
        elif winner == fighter_2_name:
                fighter_2_score += 70  # type: ignore

    if fight_round == 3:
        #assign points
        if fight_method == "Decision - Unanimous" or fight_method == "Decision - Split":
            if winner == fighter_1_name:
                    fighter_1_score += 30
            elif winner == fighter_2_name:
                    fighter_2_score += 30  # type: ignore
        else:
            if winner == fighter_1_name:
                    fighter_1_score += 45
            elif winner == fighter_2_name:
                    fighter_2_score += 45  # type: ignore

    if fight_round == 4:
            #assign points
        if winner == fighter_1_name:
                fighter_1_score += 40
        elif winner == fighter_2_name:
                fighter_2_score += 40  # type: ignore

    if fight_round == 5:
        #assign points
        if fight_method == "Decision - Unanimous" or fight_method == "Decision - Split":
            if winner == fighter_1_name:
                    fighter_1_score += 30
            elif winner == fighter_2_name:
                    fighter_2_score += 30  # type: ignore
                    
        if winner == fighter_1_name:
                fighter_1_score += 40
        elif winner == fighter_2_name:
                fighter_2_score += 40  # type: ignore

    print(f"{fighter_1_name}: {fighter_1_score}")
    print(f"{fighter_2_name}: {fighter_2_score}\n")
    
if __name__ == "__main__":
    
#     url = "http://ufcstats.com/fighter-details/23024fdfc966410a"
#     response = requests.get(url)

#     soup = BeautifulSoup(response.text,"html.parser")

#     #lets check fight_link 
#     fighters_links = url_links(soup)

#     for x in range(len(fighters_links)):
#         main(fighters_links[x])
   
    parser = argparse.ArgumentParser(description="Scrape UFC fighter details.")
    parser.add_argument(
        "url",
        type=str,
        help="URL of the UFC fighter details page."
    )

    args = parser.parse_args()
    url = args.url

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Check fight_link
    fighters_links = url_links(soup)

    for x in range(len(fighters_links)):
        main(fighters_links[x])