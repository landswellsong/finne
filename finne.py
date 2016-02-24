#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO error handling

import http.client, re, sys, urllib.parse, json
from pprint import pprint

p = re.compile("google.visualization.Query.setResponse[(](.*)[)];$")

def GDocsQuery(url, query):
    conn = http.client.HTTPSConnection("docs.google.com")
    conn.request("GET", "/spreadsheets/d/" + url + "/gviz/tq?tq=" + urllib.parse.quote(query))
    res = conn.getresponse()
    dt = res.read()
    conn.close()
    return json.loads(p.search(dt.decode("utf-8")).group(1))

# Settings
hourlimit = 10
hourrate = 10
boards = [ "Лабораторія", "Організаційне", "Актуальні проекти"]

# Fetching user column
users = {}
query = GDocsQuery(sys.argv[1], "select F, sum(D) where "+" or ".join(map(lambda x: "B='"+x+"'", boards))+" group by F")
print("select F, sum(D) where "+" and ".join(map(lambda x: "B='"+x+"'", boards))+" group by F")

pprint(query)
