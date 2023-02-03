# results-scraper
Web scraping scripts for FINA swimming results.

script.py scrapes competition metadata including name and id and saves to csv. Competition name and id will be utilised by future scripts to scrape individual competition results.

## Instructions
To run the script, utilse the following steps.

Clone to repo:

`git@github.com:michaelwknott/results-scraper.git`

Change into the results-scraper directory:

`cd results-scraper`

Create a virtual environment:

`python -m venv .venv --prompt .`

Activate the virtual environment:

`source .venv/bin/activate`

Install dependencies:

`python -m pip install -r requirements.txt`

Run the script:

`python script.py`
