# Get material from Braun's lectures.
# author: Michael Eggers, eggers@hm.edu
# 
# usage:
# python get.py <lecturename>
#  where lecturename is one of the following:
#	- fun
#	- algdatii
#	- vss
#	- (and more, but not tested)
#
# for more info see: https://ob.cs.hm.edu/api.html (some parts of the docu seem to be out of date, though.
# eg. the object /api/lectures/algdati.json is not available. Instead the correct location
# is https://ob.cs.hm.edu/api/lectures/algdati/base.json) .
#
# TODOs:
# - check if json object is available
# - make CLI for what to query

import urllib.request
import ssl
import json
import os
import argparse

parser = argparse.ArgumentParser(description="download lecture data from ob.cs.hm.edu")
parser.add_argument("lecturename", metavar="lecture", type=str, help="lecturename to download lecture-data from")
args = parser.parse_args()

lecturename = args.lecturename # change this to get stuff from another lecture
baseURL = "https://ob.cs.hm.edu/api/base.json"
artifactURL = "https://ob.cs.hm.edu/api/lectures/" + lecturename + "/base.json"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

baseURLresponse = urllib.request.urlopen(baseURL, context=ctx).read()
artifactURLresponse = urllib.request.urlopen(artifactURL, context=ctx).read()


baseJSON = json.loads(baseURLresponse)
artifactJSON = json.loads(artifactURLresponse)

filesPrefix = baseJSON["filesPrefix"]
artifactDirs = baseJSON["dirs"]

# add artifacts here:
artifacts = ["slides", "exercises"]

for artifact in artifacts:
	artifactToGet = artifactDirs[artifact]
	suffix = baseJSON["suffixes"][artifactToGet]
	files = artifactJSON["maincontent"][artifactToGet]
	for file in files:
		f = file["file"]
		print(f)
		fullpath = filesPrefix + "/" + lecturename + "/" + artifactToGet + "/" + f + "." + suffix
		print(fullpath)
		content = urllib.request.urlopen(fullpath, context=ctx)
		if not os.path.exists(os.path.join(lecturename, artifactToGet)):
			os.makedirs(os.path.join(lecturename,artifactToGet))
		fileOnDisk = open(lecturename + "/" + artifactToGet + "/" + f + "." + suffix, mode="wb")
		fileOnDisk.write(content.read())
#print(filesPrefix)
#print(suffix)