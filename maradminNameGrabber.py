from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


url = "https://www.marines.mil/News/Messages/Messages-Display/Article/3707403/fy24-approved-selections-to-gunnery-sergeant/"
response = requests.get(url)
print(response)

soup = BeautifulSoup(response.content, "html.parser")
bodyText = (soup.find('div', class_='body-text'))

if bodyText:
            # Extract text content from the <div> element
            text_content = bodyText.get_text(separator='\r\n')

            # Split the text content into lines
            lines = text_content.split('\r\n')
            print(len(lines[41]))

            namesInMaradmins = []

            for line in lines:
                    namesInMaradmins.append(re.sub('[A-Z]+\s+[A-Z]{2}', '', line))

            print(namesInMaradmins)
            
            

            # for line in lines:
            #         print(line)

            # names_from_page = []
            # for line in lines:
            #     # Extract information from each line
            #     parts = line.split()
            #     if len(parts) >= 5:
            #         last_name = parts[0]
            #         print(last_name)
            #         # middle_initial = parts[1]
            #         first_name = parts[2]
            #         dor = parts[3]
            #         mcc = parts[4]

            #         names_from_page.append((first_name.lower(), last_name.lower(), "1STLT"))
            
            # print(names_from_page)
