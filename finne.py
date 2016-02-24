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

def DoQuery():
    return GDocsQuery(sys.argv[1], "select F, sum(D), sum(E) "+
        "where G = '"+curweek+"' and ("+
        " or ".join(map(lambda x: "B='"+x+"'", boards))+
        ") group by F")

def ToMoney(n):
    return "$"+str(round(hourrate * min(n, hourlimit),2))

# Settings
hourlimit = 10
hourrate = 10
boards = [ "Лабораторія", "Організаційне", "Актуальні проекти"]

# Fetching data
print(curweek + ":")
query = DoQuery()["table"]["rows"]
for row in query:
    print("-> "+row["c"][0]["v"]+": "+ToMoney(row["c"][1]["v"]) + " / "+ToMoney(row["c"][2]["v"]))
