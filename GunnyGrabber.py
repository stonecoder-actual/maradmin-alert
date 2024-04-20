from bs4 import BeautifulSoup
import requests

url = "https://www.marines.mil/News/Messages/Messages-Display/Article/3707403/fy24-approved-selections-to-gunnery-sergeant/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
bodyText = (soup.find('div', class_='body-text'))


text_content = bodyText.get_text(separator='\r\n')

lines = text_content.split('\n')

splitMaradmin = []
maradminLines = []
maradminNamePairs = []
cleanedMaradminNamePairs =[]
maradminNames = []

for line in lines:
        splitMaradmin.append(line.split())

for line in splitMaradmin:
        if len(line) >= 4 and len(line) <= 10 and line[0].isalpha() and line[0].isupper() and len(line[0]) > 1 and line[0] != 'NAME':
                maradminLines.append(line)

newline = []
for line in maradminLines:
      maradminNamePairs.append(newline)
      newline = []
      for word in line:
        if word.isalpha(): #and word != 'III' and word != 'II' and word != 'IV' and word != 'JR':
                newline.append(word)


newline = []
for line in maradminNamePairs:
       cleanedMaradminNamePairs.append(newline)
       newline = []
       if len(line) != 4:
              for word in line:
                     if word != 'III' and word != 'II' and word != 'IV' and word != 'JR' and word != 'SR':
                            newline.append(word)
        elif len(line) == 4:
              newline.append(word)
