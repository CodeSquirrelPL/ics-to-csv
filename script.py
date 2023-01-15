import re
import html
from datetime import datetime

OPENING_KEYWORD = 'BEGIN:VEVENT'
CLOSING_KEYWORD = 'END:VEVENT'
DESIRED_ATTRIBUTES = ['DTSTART', 'SUMMARY', 'DESCRIPTION', 'URL']
OUTPUT_FILE_PATH = 'calendarAs.csv'
INPUT_FILE_PATH = 'frankfurt2023.ics'
REDUNDANT_EVENTS = ['Full Moon', 'Moon at Last Quarter', 'Moon at First Quarter']

def remove_url(description):
    regex = '\.\shttps:\/\/.+'
    return re.sub(regex, '', description)

def line_into_attribute(input_line):
    [attribute_name, attribute_value] = re.split(':', input_line, 1)
    if attribute_name in DESIRED_ATTRIBUTES:
        if (attribute_name=='DESCRIPTION'):
            attribute_value = remove_url(attribute_value)
            attribute_value = html.unescape(attribute_value)
        if (attribute_name=='DTSTART'):
            attribute_value = time_from_ical(attribute_value)
        return [attribute_name, attribute_value]
    else:
        return [False, False]

def lines_into_event(lines):
    event = {}
    for line in lines:
        [attribute_name, attribute_value] = line_into_attribute(line)
        if (attribute_name and attribute_value):
            event[attribute_name] = attribute_value
    return event

def items_list_into_csv_text(items):
    output = ""
    for item in items:
        for attribute in item.values():
            output = output + '"' + attribute + '",'
        output += '\n'
    return output

def save_as_csv(text):
    output_file = open(OUTPUT_FILE_PATH, 'w', encoding='utf8')
    output_file.write(text)

def time_from_ical(iCalTime):
    output = datetime.strptime(iCalTime, "%Y%m%dT%H%M%SZ")
    return output.isoformat()

all_events = []

input_file = open(INPUT_FILE_PATH, 'r', encoding='utf8')

for line in input_file:
    line = re.sub('\n', '', line)
    if (line == OPENING_KEYWORD):
        all_event_attributes = []
        for event_description_line in input_file:
            event_description_line = re.sub('\n', '', event_description_line)
            if (event_description_line!= CLOSING_KEYWORD):
                all_event_attributes.append(event_description_line)
            else:
                event = lines_into_event(all_event_attributes)
                all_events.append(event)
                break
        

input_file.close()

output_text = items_list_into_csv_text(all_events)

save_as_csv(output_text)


