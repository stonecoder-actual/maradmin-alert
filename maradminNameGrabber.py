from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


url = "https://www.marines.mil/News/Messages/Messages-Display/Article/3707403/fy24-approved-selections-to-gunnery-sergeant/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
bodyText = (soup.find('div', class_='body-text'))

if bodyText:
        # Extract text content from the <div> element
        text_content = bodyText.get_text(separator='\r\n')

        # Split the text content into lines
        lines = text_content.split('\\r\\n')
        print(lines[40:41])
        pattern = r'([A-Z]+\s+[A-Z]{2})'

        namesInMaradmins = []

        for line in lines:
                matches = re.findall(pattern,line)
                if len(matches) > 0:
                        namesInMaradmins.append(matches)
        
        for place,line in enumerate(namesInMaradmins):
                line = str(line)
                namesInMaradmins[place] = line.strip('\\xa0')

print(namesInMaradmins[1]) 
