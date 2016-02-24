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

# Fetching user column
users = {}
query = GDocsQuery(sys.argv[1], "select F offset 1")

# Filtering users, is there a Google "SQL" api to select unique ones?
for row in query["table"]["rows"]:
    if not row["c"][0]["v"] in users:
        users[row["c"][0]["v"]] = 0

print(users)
