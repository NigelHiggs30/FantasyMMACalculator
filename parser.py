import re
from bs4 import BeautifulSoup
from utils import convert_time_to_seconds

class WebPageParser:
    def __init__(self, html_content: str):
        """
        Initialize the parser with the HTML content.

        :param html_content: The HTML content of the webpage to parse.
        """
        self.html_content = html_content

    def winner_looser(self) -> tuple:

        # Determine who won/lost
        winner_loser = self.html_content.find("div", class_="b-fight-details__persons clearfix")

        # Find all the fighter elements within the winner_loser div
        fighters = winner_loser.find_all('div', class_='b-fight-details__person')

        # Initialize a dictionary to store the results
        fight_results_dic = {}
        fight_results = []

        # Extract the relevant details for each fighter
        for fighter in fighters:
            # Extract the result (W or L)
            result = fighter.find('i', class_='b-fight-details__person-status').text.strip()

            # Extract the fighter's name
            name = fighter.find('a', class_='b-link b-fight-details__person-link').text.strip()

            # Store the result in the dictionary
            fight_results_dic[name] = result
            fight_results.append([name,result])

        fighter_1_name = fight_results[0][0]
        fighter_2_name = fight_results[1][0]

        # ##test output
        # print(f"Fighter 1: {fighter_1_name}")
        # print(f"Fighter 2: {fighter_2_name}")
     
        return fight_results_dic, fighter_1_name, fighter_2_name

    def extract_fight_details(self) -> tuple:
        """
        Extracts fight details such as method, round, time, and format.

        :return: A tuple containing the extracted fight details.
        """
        # Find the div containing fight details
        row = self.html_content.find("div", class_="b-fight-details__content")

        # Extract the fight method
        fight_method = row.find_all("i", style="font-style: normal")[0].text.strip()

        # Extract the fight round
        fight_round = row.find_all("i", class_="b-fight-details__text-item")[0].text.strip()
        match = re.search(r'\b[0-5]\b', fight_round)
        fight_round = int(match.group(0))

        # Extract the fight time
        fight_time = row.find_all("i", class_="b-fight-details__text-item")[1].text.strip()
        match = re.search(r'\b[0-5]:[0-5][0-9]\b', fight_time)
        fight_time = match.group(0)

        # Extract the fight time format
        fight_format = row.find_all("i", class_="b-fight-details__text-item")[2].text.strip()
        match = re.search(r'\b([0-5])\sRnd\b', fight_format)
        fight_format = match.group(1)

        # print(fight_method, fight_round, fight_time, fight_format)
        return fight_method, fight_round, fight_time, fight_format

    def extract_scoring_moves(self) -> tuple:
        """
        Extracts and returns the scoring moves data for two fighters.
        
        :return: A tuple containing scoring details for both fighters.
        """
        moves = self.html_content.find("tbody", class_="b-fight-details__table-body")
        rows = moves.find_all("td")

        # Extract and separate data for each fighter
        strikes_fighter1 = rows[4].find_all('p')[0].text.strip()
        strikes_fighter2 = rows[4].find_all('p')[1].text.strip()

        match1 = re.search(r'(\b\d{1,3})\s+of', strikes_fighter1)
        match2 = re.search(r'(\b\d{1,3})\s+of', strikes_fighter2)
        strikes_fighter1 = match1.group(1)
        strikes_fighter2 = match2.group(1)

        significant_strikes_fighter1 = rows[2].find_all('p')[0].text.strip()
        significant_strikes_fighter2 = rows[2].find_all('p')[1].text.strip()

        match1 = re.search(r'(\b\d{1,3})\s+of', significant_strikes_fighter1)
        match2 = re.search(r'(\b\d{1,3})\s+of', significant_strikes_fighter2)
        significant_strikes_fighter1 = match1.group(1)
        significant_strikes_fighter2 = match2.group(1)

        control_time_fighter1 = rows[9].find_all('p')[0].text.strip()
        control_time_fighter2 = rows[9].find_all('p')[1].text.strip()

        control_time_fighter1 = convert_time_to_seconds(control_time_fighter1)
        control_time_fighter2 = convert_time_to_seconds(control_time_fighter2)

        takedown_fighter1 = rows[5].find_all('p')[0].text.strip()
        takedown_fighter2 = rows[5].find_all('p')[1].text.strip()

        match1 = re.search(r'(\b\d{1,3})\s+of', takedown_fighter1)
        match2 = re.search(r'(\b\d{1,3})\s+of', takedown_fighter2)
        takedown_fighter1 = match1.group(1)
        takedown_fighter2 = match2.group(1)

        reversal_sweep_fighter1 = rows[8].find_all('p')[0].text.strip()
        reversal_sweep_fighter2 = rows[8].find_all('p')[1].text.strip()

        knockdown_fighter1 = rows[1].find_all('p')[0].text.strip()
        knockdown_fighter2 = rows[1].find_all('p')[1].text.strip()

        return (
        strikes_fighter1, strikes_fighter2,
        significant_strikes_fighter1, significant_strikes_fighter2,
        control_time_fighter1, control_time_fighter2,
        takedown_fighter1, takedown_fighter2,
        reversal_sweep_fighter1, reversal_sweep_fighter2,
        knockdown_fighter1, knockdown_fighter2
        )

