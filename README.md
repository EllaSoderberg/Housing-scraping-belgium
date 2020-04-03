# Housing-scraping-belgium
Scripts to scrape housing websites in Belgium

Recently my boyfriend and I have been searching for a new place to live, so I decided to make the process easier by scraping Belgian housing websites and gather relevant data to make comparing our options easier. 

# Installation
In order to run this project you will need [selenium](https://selenium-python.readthedocs.io/) for python, follow the instructions in the docs to install. 

Packages required are: 
  - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  - requests
  - re
  - json
  - time 
  - geopy

They can all be installed using pip: 
```sh
$ py -m pip install beautifulsoup4
```

Clone this project to your repo, change the variables in main.py and you should be ready to go!

# Rank the results
We also made a google sheet to give each apartment a score. You can find the template to this sheet with example data [here](https://docs.google.com/spreadsheets/d/1M--u27KMpi3oJuI7_zLkbxMeG8rvfr79zhKL5j1zNgM/edit?usp=sharing)

# Todos
 * Add more housing websites!
