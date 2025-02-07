''' IMPORT STANDARD LIBRARIES '''
import requests
import csv
import logging
import re


''' IMPORT 3RD PARTY LIBRARIES '''
# NONE

''' DEFINE PSEUDO CONSTANTS '''
#2025 URL for ALNAVS
alnav25 = "https://www.mynavyhr.navy.mil/Portals/55/Messages/ALNAV/ALN2025/ALN25"

#Friends list
csv_file = "F:\OneDrive\Brain\Hobbies\GitHub\maradmin-alert\contacts.csv"

''' LOCAL FUNCTIONS '''

def contactsGrabber(_csv):
    """Read CSV and extract names in 'LASTNAME FIRST_INITIAL' format"""
    friends_names = []
    with open(_csv, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            first_name = row['first_name'].strip().upper()
            last_name = row['last_name'].strip().upper()
            first_initial = first_name[0]  # Get only the first letter of first name
            friends_names.append((last_name, first_initial))
    return friends_names  # Returns ["LASTNAME F", "ANOTHERNAME A", ...]

def alnavPuller(alnavNumber):
    """Fetch ALNAV text content"""
    alnav_url = f"{alnav25}{alnavNumber}.txt"
    response = requests.get(alnav_url)

    if response.status_code == 200:
        return response.text.upper()  # Convert text to uppercase for case-insensitive search
    else:
        print(f"Error fetching {alnav_url}: {response.status_code}")
        return ""

def search_names_in_text(names, text):
    """Search for partial name matches in the text with tab support"""
    matches = []
    for last, first_initial in names:
        # Regex to find LASTNAME followed by a tab and first initial (handling middle names)
        pattern = rf"{last}\s+\t?{first_initial}[A-Z]?"  # \s+ for spaces, \t? for optional tab
        if re.search(pattern, text):
            matches.append(f"{last} {first_initial}.")  # Format output as "LAST F."
    return matches


''' LOCAL CLASSES '''
# NONE

''' MAIN ENTRY POINT '''

if __name__ == "__main__":
    """Main Script Execution"""
    try:
    
        friends_names = contactsGrabber(csv_file)
        
        for i in range(1000):
            alnav_text = alnavPuller(str(i).zfill(3))

        #alnav_text = alnavPuller("013")

            if alnav_text:
                matched_names = search_names_in_text(friends_names, alnav_text)

                if matched_names:
                    print("Found Matches:")
                    for name in matched_names:
                        print(name)
                else:
                    print("No matches found.")
    except Exception as err:
        logging.critical("\n\nScript Aborted     ", "Exception =     ", err)
