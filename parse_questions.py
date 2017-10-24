from bs4 import BeautifulSoup as bs
import re
import json
import os
import sys

text_file = open('Posts.xml', 'r')

print('text_file opened')

for i,line in enumerate(text_file):
    print(i/1985871)