# results-scraper
Web scraping scripts for FINA swimming results.

script.py fetches competition summary data including name and id and saves to csv. Competition name and id will be utilised by future scripts to fetch individual competition results.

## Instructions
To run the script, utilise the following steps.

Clone the repo:

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
