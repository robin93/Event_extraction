## Read csv file with specific columns and return them in a list with time, description and hashtags

import sys, argparse, csv
import datetime
import re
import twokenize as tk

# open csv file
def file_list(filepath,include_columns):
    ifile  = open(filepath, "rb")
    reader = csv.reader(ifile)
    rownum = 0

    hashwords = re.compile("#\S*",re.I)
    linkwords = re.compile("http\S*",re.I)
    reference = re.compile("@\S*",re.I)

    listo = []
    for row in reader:
        if rownum == 0:
            header = row
        else:
            listi = []
            for col in include_columns:
                if col == 1:
                    time = datetime.datetime.strptime(row[col], "%a %b %d %H:%M:%S +0000 %Y")
                    listi.append(time)
                elif col == 6:
                    query = str(row[col])
                    for res in re.finditer(linkwords,query):
                        query = query.replace(res.group(),"")
                    for res in re.finditer(hashwords,query):
                        query = query.replace(res.group(),"")
                    for res in re.finditer(reference,query):
                        query = query.replace(res.group(),"")
                    query = tk.squeezeWhitespace(query)
                    query = tk.normalizeTextForTagger(query.decode('latin-1').encode("utf-8").decode('utf8'))
                    listi.append(query)
                else:
                    listi.append(row[col])
            listo.append(listi)
        rownum += 1
    return listo
