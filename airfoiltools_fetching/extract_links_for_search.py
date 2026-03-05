import requests
from bs4 import BeautifulSoup

url = "http://airfoiltools.com/search/index?m%5BtextSearch%5D=&m%5BmaxCamber%5D=0&m%5BminCamber%5D=&m%5BmaxThickness%5D=&m%5BminThickness%5D=&m%5Bgrp%5D=&m%5Bsort%5D=5&m%5Bpage%5D=12&m%5Bcount%5D=136"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
links = [a['href'] for a in soup.find_all("a", string="Source dat file")]
for link in links:
    print(link)