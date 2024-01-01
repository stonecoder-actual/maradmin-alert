import feedparser
import requests
from bs4 import BeautifulSoup
#from prettytable import PrettyTable
import csv

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
            #table = PrettyTable()
            #table.field_names = ["First Name", "Middle Initial", "Last Name", "Rank", "MCC Code"]

            names_from_page = []
            for line in lines:
                # Extract information from each line
                parts = line.split()
                if len(parts) >= 3:
                    full_name = ' '.join(parts[:-2])
                    rank = parts[-2]
                    mcc_code = parts[-1]

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
                    #table.add_row([first_name, middle_initial, last_name, rank, mcc_code])

                    # Add the extracted names to the list
                    names_from_page.append((first_name.lower(), last_name.lower()))
                                
            # Print the table
            #print(table)

            # Return the extracted names
            return names_from_page
        else:
            print(f"Error: <div class='body-text'> not found on the webpage: {url}")
            return []
    else:
        print(f"Error: Unable to fetch the webpage. Status code: {response.status_code}")
        return []

def extract_information_1stlt(url, title):
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
            table.field_names = ["Last Name", "Middle Initial", "First Name", "DOR", "MCC"]

            names_from_page = []
            for line in lines:
                # Extract information from each line
                parts = line.split()
                if len(parts) >= 5:
                    last_name = parts[0]
                    middle_initial = parts[1]
                    first_name = parts[2]
                    dor = parts[3]
                    mcc = parts[4]

                    # Add a row to the table
                    table.add_row([last_name, middle_initial, first_name, dor, mcc])

                    # Add the extracted names to the list
                    names_from_page.append((first_name.lower(), last_name.lower(), "1STLT"))

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


def read_names_from_csv(csv_file):
    names = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            first_name = row['first_name']
            last_name = row['last_name']
            names.append((first_name.lower(), last_name.lower()))
    return names

def monitor_rss_feed(rss_url, desired_titles, friends_names):
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Set to store names from the RSS feed
    rss_names_set = set()

    # Iterate through entries in the feed
    for entry in feed.entries:
        # Check if the entry title contains any of the desired titles
        if any(title in entry.title.upper() for title in desired_titles):
            # Extract information from the linked webpage
            linked_webpage_url = entry.link
            print(f"\nScraping webpage: {linked_webpage_url}")

            # Use the appropriate extraction function based on the title
            if "1STLT" in entry.title.upper():
                names_from_page = extract_information_1stlt(linked_webpage_url, entry.title)
            else:
                names_from_page = extract_information(linked_webpage_url, entry.title)

            # Add the extracted names to the set
            rss_names_set.update(names_from_page)

    # Set of friends' names
    friends_names_set = set((first.lower(), last.lower()) for first, last in friends_names)

    # Find common names between the two sets
    common_names = rss_names_set.intersection(friends_names_set)
    
    # Display the common names
    for first, last in common_names:
        print(f"Match found: {first.capitalize()} {last.capitalize()}")

# Function to extract names from the RSS feed webpage
def extract_names_from_rss(url):
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

            # Create a list to store extracted names
            names_list = []

            for line in lines:
                # Extract information from each line
                parts = line.split()
                if len(parts) >= 2:
                    names_list.append(tuple(parts[:2]))

            return names_list
        else:
            print(f"Error: <div class='body-text'> not found on the webpage: {url}")
    else:
        print(f"Error: Unable to fetch the webpage. Status code: {response.status_code}")

# Replace 'your_rss_feed_url_here' with the actual URL of the RSS feed you want to monitor
rss_url = 'https://www.marines.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=6&Site=481&max=10&category=14336'
desired_titles = ["OFFICER PROMOTIONS FOR", "1STLT PROMOTIONS FOR"]

# Replace 'path/to/your/contacts.csv' with the actual path to your CSV file
csv_file_path = 'contacts.csv'
friends_names = read_names_from_csv(csv_file_path)

monitor_rss_feed(rss_url, desired_titles, friends_names)