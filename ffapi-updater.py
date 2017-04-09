#!/usr/bin/env python3

# ------------------------------------------------------------------------------
#
#    ffapi-updater - Update Freifunk API file
#    Copyright (C) 2016 Benjamin Schmitt
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Source code available at: https://github.com/Little-Ben/ffapi-updater
#
# ------------------------------------------------------------------------------
# This python script counts all active nodes (online = true) in NODEFILE
# and updates the node count and lastchange date (UTC) in APIFILE.
# ------------------------------------------------------------------------------
# Configuration start
APIFILE = '/srv/api/FreifunkWestpfalz-api.json'
NODESFILE = '/var/freifunk/yanic/data/nodes.json'
# Configuration end 
# ------------------------------------------------------------------------------

VERSION = 'V1.1.1'

import json
from pprint import pprint
from datetime import datetime

print("\nffapi-updater",VERSION,"Copyright (C) 2016 Benjamin Schmitt")
print("----------------------------------------------------------------------")
print("This program comes with ABSOLUTELY NO WARRANTY.")
print("This is free software, and you are welcome to redistribute it,")
print("see LICENSE for details.")
print("Source code available at: https://github.com/Little-Ben/ffapi-updater")
print("----------------------------------------------------------------------")

with open(APIFILE) as data_file:
    data = json.load(data_file)

with open(NODESFILE) as node_file:
    dataNodes = json.load(node_file)

#count active nodes
iNodeCount=0
for node in dataNodes["nodes"]:
    if node["flags"]["online"] == True:
        iNodeCount = iNodeCount + 1

#data update
print("UTC time:\t\t ", datetime.utcnow().strftime("%Y-%m-%dT%T.%f"))
iNodeCountOld=data["state"]["nodes"]
print("node count old:\t\t ", str(iNodeCountOld))
data["state"]["nodes"] = iNodeCount
data["state"]["lastchange"] = datetime.utcnow().strftime("%Y-%m-%dT%T.%f")
print("node count new:\t\t ", str(data["state"]["nodes"]))

if iNodeCountOld != iNodeCount:
    #write new api file, sorted and prettyprinted - only if node count changed
    with open(APIFILE, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
    bApiChanged=True
else:
    bApiChanged=False

#write end message depending if changes happend
print("----------------------------------------------------------------------")
if bApiChanged == True:
    strEndMessage="API file updated successfully."
else:
    strEndMessage="API file unchanged."
print(strEndMessage, "DONE.\n")

exit(0)
