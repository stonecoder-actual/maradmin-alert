''' IMPORT STANDARD LIBRARIES '''
import feedparser
import requests
import csv
import logging
import re

''' IMPORT 3RD PARTY LIBRARIES '''
from prettytable import PrettyTable     # pip install prettytable
from bs4 import BeautifulSoup

''' DEFINE PSEUDO CONSTANTS '''
# Pulls last 50 MARADMINS published
rss_url = 'https://www.marines.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=6&Site=481&max=50&category=14336'

# MARADMIN titles we want to scrape
maradminTitles = ["OFFICER PROMOTIONS FOR", "1STLT PROMOTIONS FOR", "BOARD RESULTS"]

csv_file_path = 'contacts.csv'

''' LOCAL FUNCTIONS '''
def read_names_from_csv(csv_file):
    names = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            first_name = row['first_name']
            last_name = row['last_name']
            names.append((first_name.lower(), last_name.lower()))
    return names

def extract_information(url, title):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <div> element with class "body-text"
        body_text_div = soup.find('div', class_='body-text')

        if body_text_div:
            # Extract text content from the <div> element
            text_content = body_text_div.get_text(separator='\n')

            # Split the text content into lines
            lines = text_content.split('\n')

            # Create a PrettyTable instance
            table = PrettyTable()
            table.field_names = ["First Name", "Middle Initial", "Last Name", "Rank", "MCC Code"]

            names_from_page = []
            for line in lines:
                # Extract information from each line
                parts = line.split()
                if len(parts) >= 3:
                    full_name = ' '.join(parts[:-2])
                    rank = parts[-2]
                    mcc_code = parts[-1]
                    
                    full_name = full_name.replace(',', '').strip()

                    # Split the full name into first name, middle initial, and last name
                    names = full_name.split()
                    first_name = names[0]
                    middle_initial = ''  # Initialize to an empty string
                    last_name = ''  # Initialize to an empty string

                    # Check if there is a middle initial
                    if len(names) > 1:
                        # Check if the middle initial is formatted correctly (one letter followed by a period)
                        if len(names[1]) == 2 and names[1][1] == '.':
                            middle_initial = names[1][0]
                            last_name = names[-1]                          
                        else:
                            last_name = names[1]
                    else:
                        # If there is no middle name, consider the next part as the last name
                        last_name = names[-1]

                    # Add a row to the table
                    table.add_row([first_name, middle_initial, last_name, rank, mcc_code])

                    # Add the extracted names to the list
                    names_from_page.append((first_name.lower(), last_name.lower()))
                                
            # Print the table
            print(table)

            # Return the extracted names
            return names_from_page
        else:
            print(f"Error: <div class='body-text'> not found on the webpage: {url}")
            return []
    else:
        print(f"Error: Unable to fetch the webpage. Status code: {response.status_code}")
        return []


def monitor_rss_feed(rss_url, maradminTitles, friends_names):
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Set to store names from the RSS feed
    rss_names_set = set()
    names_and_urls = {}

    # Iterate through entries in the feed
    for entry in feed.entries:
        # Check if the entry title contains any of the desired titles
        if any(title in entry.title.upper() for title in maradminTitles):
            # Extract information from the linked webpage
            linked_webpage_url = entry.link
            print(f"\nScraping webpage: {linked_webpage_url}")

            names_from_page = extract_information(linked_webpage_url, entry.title)
            
            rss_names_set.update((name, linked_webpage_url) for name in names_from_page)

            # Add the extracted names to the set
            rss_names_set.update(names_from_page)
            

    # Set of friends' names
    friends_names_set = set((first.lower(), last.lower()) for first, last in friends_names)
    # Reverse the names for MARADMINs that list "last name, First name"
    friends_names_set_reversed = set((first.lower(), last.lower()) for last, first in friends_names) 

    # Find common names between the two sets
    common_names = rss_names_set.intersection(friends_names_set)
    common_names_reversed = rss_names_set.intersection(friends_names_set_reversed)
    
    # Display the common names
    for first, last, linked_webpage_url in common_names:
        print(f"Match found: {first.capitalize()} {last.capitalize()} - URL: {url}")
        
    common_names = rss_names_set.intersection(friends_names_set_reversed)
        
    for first, last, linked_webpage_url in common_names:
        print(f"Match found: {first.capitalize()} {last.capitalize()} - URL: {url}")


''' LOCAL CLASSES '''
# NONE

''' MAIN ENTRY POINT '''

if __name__ == "__main__":
    ''' Main Script Entry Point '''
    
    try:
        
        friends_names = read_names_from_csv(csv_file_path)    
        monitor_rss_feed(rss_url, maradminTitles, friends_names)
    
        
    except Exception as err:
        logging.critical("\n\nScript Aborted     ", "Exception =     ", err)         