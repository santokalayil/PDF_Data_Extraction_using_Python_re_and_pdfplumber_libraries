# !sudo apt-get install ocrmypdf -q  # directly it iwll install python module also
# !pip3 install pdfplumber -q

import os
import ocrmypdf # it is needed only if we need to ocr image only pdf is there.
import pdfplumber

pdf_url = "Carmelaram - Result II Semester 2020-'21.pdf"

with pdfplumber.open(pdf_url) as pdf:
    pages = pdf.pages
    print(pages, pages[0]); print(100*"=")
    page = pages[0] # we can use for loop but here only one page 
    text = page.extract_text()
    print(text)

'''
# alternate way to ocr if it is image.. it is not at all an image
os.system(f"ocrmypdf {pdf_url} output.pdf") # output nonzero - 502 
# so trying in direct terminal using !
!ocrmypdf "Carmelaram - Result II Semester 2020-'21.pdf" output.pdf"
# not working...
# '''

import re
result_list = []  # initializing  results list to add record dictionary to the this list
pattern = re.compile(r"([A-Za-z]+)\s*([A-Z][A-Za-z ]*)\s*(\d{1,2})\s*(\d{1,2})")
start_pattern = re.compile(r"Parish\s*Name\s*Class\s*Marks")
# .*\s*.*\s*\d{1,2}\s*\d{1,2}
started = False
for line in text.split('\n'):
    if started:  # checking if line with data found and started data grab loop started
        for match in pattern.finditer(line): # matching
            #print(match.group(0))
            if match:
                print(f'match found - {match}')
                record = {} # initializing dictionary of each record
                parish_name, name, std, marks = match.groups()
                parish_name, name, std, marks = parish_name.strip(), name.strip(), std.strip(), marks.strip()
                # print("{}-{}-{}-{}".format(parish_name, name, std, marks))
                record['Parish'], record['Name'], record['Class'], record['Marks'] = parish_name, name, std, marks
                result_list.append(record)  # adding to the list each record dictionary
            else: # this section is actually optional
                break  # once data-grab-loop started and after-a-while nothing is found in pattern matching
                # it means that table section is over therefore, breaking the loop
    elif start_pattern.search(line): # if start pattern found, starting data grab loop, then
        started = True  #  setting started as True and continuing loop without anything else
        continue
    else:
        continue # since nothing of interest, normal loop is continue without doing anything

print(result_list)

# using pandas to tabularize the data
import pandas as pd
df = pd.DataFrame(result_list)
print(df)

n = 1
df.to_csv(f"result_{n}.csv", index=False) # saving as csv file for later usage