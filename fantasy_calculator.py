import requests
from bs4 import BeautifulSoup
import re

def convert_time_to_seconds(time_str):
    # Split the string into minutes and seconds
    minutes, seconds = map(int, time_str.split(':'))
    
    # Convert to total seconds
    total_seconds = minutes * 60 + seconds
    
    # Return the result as a string
    return str(total_seconds)


# Given a link, we should be able to return the fantasy MMA score of the fight.
url = "http://ufcstats.com/fight-details/ee278a5a25744cac"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

###########################################################################
# Determine who won/lost
winner_loser = soup.find("div", class_="b-fight-details__persons clearfix")

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

print(f"Fighter 1: {fighter_1_name}")
print(f"Fighter 2: {fighter_2_name}")

###############################################################################
##lets find the round it ended, and use time format to verify its range.
##we also need method to determine if it was a decision or a finish. 
##lastly, we need to know the time in case there is a knockout in the first 60 seconds

# Find the div containing fight details, 
row = soup.find("div", class_="b-fight-details__content")


# Extract the fight method
fight_method = row.find_all("i", style="font-style: normal")[0].text.strip()

###################################################################
##regular expressions to isolate the interested variables of interest.

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

# Print the extracted details
print("Fight Method:", fight_method)
print("Fight Round:", fight_round)
print("Fight Time:", fight_time)
print("Fight Format:", fight_format)
################################################################

##############################################################################
#now we need to grab all the scoring moves.
moves = soup.find("tbody",class_="b-fight-details__table-body")
#this makes the objects indexable.
rows = moves.find_all("td")

# Extract and separate data for each fighter
# total strikes
strikes_fighter1 = rows[4].find_all('p')[0].text.strip()
strikes_fighter2 = rows[4].find_all('p')[1].text.strip()

match1 = re.search(r'(\b\d{1,3})\s+of',strikes_fighter1) #regular expression
match2 = re.search(r'(\b\d{1,3})\s+of',strikes_fighter2)
strikes_fighter1 = match1.group(1)
strikes_fighter2 = match2.group(1)

#sig strikes
significant_strikes_fighter1 = rows[2].find_all('p')[0].text.strip()
significant_strikes_fighter2 = rows[2].find_all('p')[1].text.strip()

match1 = re.search(r'(\b\d{1,3})\s+of',significant_strikes_fighter1) #regular expression
match2 = re.search(r'(\b\d{1,3})\s+of',significant_strikes_fighter2)
significant_strikes_fighter1 = match1.group(1)
significant_strikes_fighter2 = match2.group(1)

# control time
control_time_fighter1 = rows[9].find_all('p')[0].text.strip()
control_time_fighter2 = rows[9].find_all('p')[1].text.strip()

control_time_fighter1 = convert_time_to_seconds(control_time_fighter1)
control_time_fighter2 = convert_time_to_seconds(control_time_fighter2)

# takedowns
takedown_fighter1 = rows[5].find_all('p')[0].text.strip()
takedown_fighter2 = rows[5].find_all('p')[1].text.strip()

match1 = re.search(r'(\b\d{1,3})\s+of',takedown_fighter1) #regular expression
match2 = re.search(r'(\b\d{1,3})\s+of',takedown_fighter2)
takedown_fighter1 = match1.group(1)
takedown_fighter2 = match2.group(1)


# reversal sweeps
reversal_sweep_fighter1 = rows[8].find_all('p')[0].text.strip()
reversal_sweep_fighter2 = rows[8].find_all('p')[1].text.strip()

# knockdowns
knockdown_fighter1 = rows[1].find_all('p')[0].text.strip()
knockdown_fighter2 = rows[1].find_all('p')[1].text.strip()

# Print the extracted data
print("Strikes - Fighter 1:", strikes_fighter1)
print("Strikes - Fighter 2:", strikes_fighter2)

print("Significant Strikes - Fighter 1:", significant_strikes_fighter1)
print("Significant Strikes - Fighter 2:", significant_strikes_fighter2)

print("Control Time - Fighter 1:", control_time_fighter1)
print("Control Time - Fighter 2:", control_time_fighter2)

print("Takedown - Fighter 1:", takedown_fighter1)
print("Takedown - Fighter 2:", takedown_fighter2)

print("Reversal/Sweep - Fighter 1:", reversal_sweep_fighter1)
print("Reversal/Sweep - Fighter 2:", reversal_sweep_fighter2)

print("Knockdown - Fighter 1:", knockdown_fighter1)
print("Knockdown - Fighter 2:", knockdown_fighter2)

# print(moves)


##last calculate the fantasy points
fighter_1_score = (int(strikes_fighter1)*.2)+(int(significant_strikes_fighter1)*.2)+(int(control_time_fighter1)*.03)+(int(takedown_fighter1)*5)+(int(reversal_sweep_fighter1)*5)+(int(knockdown_fighter1)*10)
fighter_2_score = (int(strikes_fighter2)*.2)+(int(significant_strikes_fighter2)*.2)+(int(control_time_fighter2)*.03)+(int(takedown_fighter2)*5)+(int(reversal_sweep_fighter2)*5)+(int(knockdown_fighter2)*10)

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
    if fight_method == "Decision - Unanimous":
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
    if fight_method == "Decision - Unanimous":
        if winner == fighter_1_name:
                fighter_1_score += 30
        elif winner == fighter_2_name:
                fighter_2_score += 30  # type: ignore
                
    if winner == fighter_1_name:
            fighter_1_score += 40
    elif winner == fighter_2_name:
            fighter_2_score += 40  # type: ignore

print(f"{fighter_1_name}: {fighter_1_score}")
print(f"{fighter_2_name}: {fighter_2_score}")



