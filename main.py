from bs4 import BeautifulSoup
import requests
import json

# AggieSeek the GOAT
def get_seats(soup: BeautifulSoup) -> dict:
    all_fields = soup.find_all('td', class_='dddefault')
    return int(all_fields[3].text)

def main():
    # term number is from https://howdy.tamu.edu/api/all-terms (W kkakdugee)
    # this term number is for Spring 2025
    term_in = 202511
    with open('config.json', 'r') as file:
        data = json.load(file)
    for webhook, classes in data.items():
        for section in classes:
            crn = section["crn"]
            response = requests.get(f'https://compass-ssb.tamu.edu/pls/PROD/bwykschd.p_disp_detail_sched?term_in={term_in}&crn_in={crn}')
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                seats = get_seats(soup)
                if seats != 0:
                    prof = section["prof"]
                    course = section["course"]
                    notify(webhook, "SEATS AVAILABLE", f'{course} with {prof} is available.\nAggie Schedule Builder: https://tamu.collegescheduler.com/terms/Spring%202025%20-%20College%20Station/options')
            else:
                notify(webhook, "Response Error", "Status Code: " + response.status_code)

def notify(webhook, title, description):
    discord_json = {
            "embeds" : [{"description" : description, "title" : title}]
    }
    result = requests.post(webhook, json = discord_json)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

if __name__ == "__main__":
    main()
