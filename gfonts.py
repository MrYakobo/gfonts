#!/usr/bin/python3

# script that downloads google fonts from a link and places it in ~/.local/share/fonts
# also runs fc-cache for you

import sys
import os
import re
import subprocess
import shutil
import glob

import zipfile

from pathlib import Path
import tempfile

import requests
from bs4 import BeautifulSoup


def cli():
    if len(sys.argv) > 1:
        html_link = sys.argv[1]
    else:
        if sys.stdin.isatty():
            print('Paste <link href="..."> from google fonts here and press enter (or pass it by argument or stdin):')
        for line in sys.stdin:
            html_link = line
            break

    download(html_link, install=True)


def download(html_link, install=True):
    '''download the fonts in html_link. 
    If install, move the files to the appropiate directory on the operating system.
    Else, return the path to a zip file.
    '''
    soup = BeautifulSoup(html_link, 'lxml')
    link = soup.find_all('link')[0].get('href')

    css = requests.get(link).text

    with tempfile.TemporaryDirectory() as directory:

        dic = {}
        # download files
        for i, url in enumerate(re.findall(r'url\((.+?)\)', css)):
            r = requests.get(url).content

            font_name = re.sub(r"https://fonts.gstatic.com/s/|/v.+", "", url)

            try:
                dic[font_name] += 1
            except KeyError:
                dic[font_name] = 1

            fname = '{}/{}_{}.ttf'.format(directory, font_name, dic[font_name])
            with open(fname, 'wb') as f:
                if sys.stdin.isatty():
                    print("Downloading {}".format(font_name))
                f.write(r)

        if install:
            if sys.platform == 'linux':
                p = "~/.local/share/fonts"
            elif sys.platform == 'darwin':
                p = "~/Library/fonts"
            else:
                # win32, bsd
                home = str(Path.home())
                p = '{}/gfonts/'.format(home)
                os.makedirs("{}/".format(p))
                for f in glob.glob('{}/*.ttf'.format(directory)):
                    shutil.move(f, p)

                print("Fonts are placed in {}".format(p))
                exit(0)

            os.makedirs("{}/".format(p))
            subprocess.call(["sh", "-c", "mv {}/* {}".format(directory, p)])
            subprocess.call(["fc-cache"])
            print("Installed fonts to {}".format(p))
            return

        else:
            _, path = tempfile.mkstemp()
            return shutil.make_archive(path, 'zip', directory), dic.keys()


if __name__ == 'main':
    cli()
