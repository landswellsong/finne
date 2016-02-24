#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO error handling
# TODO specify week no

import http.client, re, sys, urllib.parse, json, datetime
from pprint import pprint

p = re.compile("google.visualization.Query.setResponse[(](.*)[)];$")
curweek = datetime.date.today().strftime("%Y-W%U")

def GDocsQuery(url, query):
    conn = http.client.HTTPSConnection("docs.google.com")
    conn.request("GET", "/spreadsheets/d/" + url + "/gviz/tq?tq=" + urllib.parse.quote(query))
    res = conn.getresponse()
    dt = res.read()
    conn.close()
    return json.loads(p.search(dt.decode("utf-8")).group(1))

def DoQuery(column):
    return GDocsQuery(sys.argv[1], "select F, sum("+column+ ") "+
        "where G = '"+curweek+"' and ("+
        " or ".join(map(lambda x: "B='"+x+"'", boards))+
        ") group by F")

# Settings
hourlimit = 10
hourrate = 10
boards = [ "Лабораторія", "Організаційне", "Актуальні проекти"]

# Fetching data
print(curweek + ":")
query = DoQuery("D")["table"]["rows"]
for row in query:
    print("-> "+row["c"][0]["v"]+": $"+str(round(hourrate * min(row["c"][1]["v"], hourlimit),2)))
