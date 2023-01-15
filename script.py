import re
import html
from datetime import datetime

openingKeyword = 'BEGIN:VEVENT'
closingKeyword = 'END:VEVENT'
desiredAttributes = ['DTSTART', 'SUMMARY', 'DESCRIPTION', 'URL']
outputFileName = 'calendarAs.csv'
inputFilePath = 'frankfurt2023.ics'

def RemoveUrl(description):
    regex = '\.\shttps:\/\/.+'
    return re.sub(regex, '', description)

def LineIntoAttribute(inputLine):
    [attributeName, attributeValue] = re.split(':', inputLine, 1)
    if attributeName in desiredAttributes:
        if (attributeName=='DESCRIPTION'):
            attributeValue = RemoveUrl(attributeValue)
            attributeValue = html.unescape(attributeValue)
        if (attributeName=='DTSTART'):
            attributeValue = convertTime(attributeValue)
        return [attributeName, attributeValue]
    else:
        return [False, False]

def LinesIntoEvent(lines):
    event = {}
    for line in lines:
        [attributeName, attributeValue] = LineIntoAttribute(line)
        if (attributeName and attributeValue):
            event[attributeName] = attributeValue
    return event

def itemsListIntoCsvText(items):
    output = ""
    for item in items:
        for attribute in item.values():
            output = output + '"' + attribute + '",'
        output += '\n'
    return output

def saveAsCsv(text):
    outputFile = open(outputFileName, 'w', encoding='utf8')
    outputFile.write(text)

def convertTime(iCalTime):
    output = datetime.strptime(iCalTime, "%Y%m%dT%H%M%SZ")
    return output.isoformat()


allEvents = []

inputFile = open(inputFilePath, 'r', encoding='utf8')

count = 0

line = inputFile.readline()
newLine = re.sub('\n', '', line)
#print('"'+newLine+'"')
if (newLine == 'BEGIN:VCALENDAR'):
    print('file start')

for line in inputFile:
    line = re.sub('\n', '', line)
    if (line == openingKeyword):
        allEventAttributes = []
        for eventDescriptionLine in inputFile:
            eventDescriptionLine = re.sub('\n', '', eventDescriptionLine)
            if (eventDescriptionLine!= closingKeyword):
                allEventAttributes.append(eventDescriptionLine)
            else:
                event = LinesIntoEvent(allEventAttributes)
                allEvents.append(event)
                break
        

inputFile.close()

outputText = itemsListIntoCsvText(allEvents)

saveAsCsv(outputText)


