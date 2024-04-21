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
        if word.isalpha():
                newline.append(word)



surrnames = ['III', 'II', 'IV', 'V', 'JR', 'SR']
for i,line in enumerate(maradminNamePairs):
        if len(line) != 4 and len(line) != 2:
                if len(line) == 6:
                        cleanedMaradminNamePairs.append([line[0],line[2],line[3],line[5]])
                if len(line) == 5:
                        if line[1] in surrnames and line[3] not in surrnames:
                                cleanedMaradminNamePairs.append([line[0],line[2],line[3],line[4]])
                        elif line[3] in surrnames and line[1] not in surrnames:
                               cleanedMaradminNamePairs.append([line[0],line[1],line[2],line[4]])
        else:
               cleanedMaradminNamePairs.append(line)



for line in cleanedMaradminNamePairs:
       if len(line) == 4:
                name1 = line[0:2]
                name2 = line[2:5]
                maradminNames.append([name1[0],name1[1][0]])
                maradminNames.append([name2[0],name2[1][0]])
       else:
              maradminNames.append([line[0],line[1][0]])
              


