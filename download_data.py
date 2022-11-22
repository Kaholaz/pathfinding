#!/usr/bin/env python3
import os

files = {
    "https://www.idi.ntnu.no/emner/idatt2101/Astjerne/opg/norden/noder.txt": "noder.txt",
    "https://www.idi.ntnu.no/emner/idatt2101/Astjerne/opg/norden/kanter.txt": "kanter.txt",
    "https://www.idi.ntnu.no/emner/idatt2101/Astjerne/opg/norden/interessepkt.txt": "interessepkt.txt",
    "https://www.idi.ntnu.no/emner/idatt2101/Astjerne/opg/island/noder.txt": "island_noder.txt",
    "https://www.idi.ntnu.no/emner/idatt2101/Astjerne/opg/island/kanter.txt": "island_kanter.txt",
    "https://www.idi.ntnu.no/emner/idatt2101/Astjerne/opg/island/interessepkt.txt": "island_interessepkt.txt",
}

if __name__=="__main__":
    for path, file_name in files.items():
        os.system(f"wget {path} -O {file_name}")