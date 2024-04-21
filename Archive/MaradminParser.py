import feedparser

rss_url = 'https://www.marines.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=6&Site=481&max=100&category=14336'
maradminTitles = ["APPROVED SELECTIONS TO STAFF SERGEANT", "OFFICER PROMOTIONS FOR", "1STLT PROMOTIONS FOR", 
                  "APPROVED SELECTIONS TO GUNNERY SERGEANT", "DUTY ASSIGNMENT MERITORIOUS PROMOTIONS"]


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

        

# # Set of friends' names
# friends_names_set = set((first.lower(), last.lower()) for first, last in friends_names)
# # Reverse the names for MARADMINs that list "last name, First name"
# friends_names_set_reversed = set((first.lower(), last.lower()) for last, first in friends_names) 

# # Find common names between the two sets
# common_names = rss_names_set.intersection(friends_names_set)
# common_names_reversed = rss_names_set.intersection(friends_names_set_reversed)