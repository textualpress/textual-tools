#
# main.py
#
# Copyright (c) 2015,
# Mooniak <hello@mooniak.com>
# Ayantha Randika <paarandika@gmail.com>
# Improvements: https://github.com/mooniak/textual-tools
# Released under the GNU General Public License version 3 or later.
# See accompanying LICENSE file for details.

import sys
import json

from fileOps import *
from counter import *
from scraper import scrape
from jsonFormulate import json_formulate


def local_count(name, out=os.getcwd() + "/report.JSON"):
    file_list = folder_reader(name)
    count = Counter()
    count.name = name
    count.source = name
    if file_list == None:
        count.name = name
        print(json.dumps(count))
    else:
        for file in file_list:
            count.count(name + "/" + file)
    writer(out, json_formulate(count))


def web_count(name, levels, out=None):
    folder = scrape(name, levels, out)
    file_list = folder_reader(folder)
    count = Counter()
    count.name = folder
    count.source = name
    if file_list == None:
        return
    else:
        for file in file_list:
            count.count(folder + "/" + file)
    if out == None:
        out = os.getcwd()
    writer(out + "/report.JSON", json_formulate(count))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-l":
        if len(sys.argv) <= 2:
            print("Invalid Location")
        else:
            print("Starting analysis...")
            if len(sys.argv) > 3:
                local_count(sys.argv[2], sys.argv[3])
                print("Done..!")
            else:
                local_count(sys.argv[2])
                print("Done..!")
    elif len(sys.argv) > 1 and sys.argv[1] == "-w":
        if len(sys.argv) <= 2:
            print("Invalid Location")
        else:
            print("Starting analysis...")
            if len(sys.argv) == 3:
                web_count(sys.argv[2], 1)
                print("Done..!")
            elif len(sys.argv) == 4:
                try:
                    level = int(sys.argv[3])
                    web_count(sys.argv[2], level)
                    print("Done..!")
                except ValueError:
                    print("Number of levels must be a integer")
                    return
            elif len(sys.argv) > 4:
                if os.path.isdir(sys.argv[4]):
                    try:
                        level = int(sys.argv[3])
                        web_count(sys.argv[2], level, sys.argv[5])
                        print("Done..!")
                    except ValueError:
                        print("Number of levels must be a integer")
                        return
                else:
                    print("Output location for web count must be a folder")
                    return
    else:
        print("Invalid argument")


if __name__ == "__main__":
    main()