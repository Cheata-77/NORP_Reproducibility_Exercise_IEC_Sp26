# SoQL Query Generation with RAG

## Overview


## Installation

1. (Recommended) Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```
pip install -r requirements.txt
```

## Environment Variables

Edit the `.env` file in the project root directory with the following contents:

```
OPENROUTER_API_KEY=your_openrouter_api_key
SOCRATA_APP_TOKEN=your_socrata_app_token
```

LLM API

* This project utilizes the [Openrouter API](https://openrouter.ai/) for making queries to LLMs.
* You can make an account on the website to obtain an **API KEY** to store in your .env file and utilize several free models.

Chicago Crimes API

* The project accesses the [Chicago Crimes Dataset](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/about_data) via the [Socrata API](https://dev.socrata.com/foundry/data.cityofchicago.org/ijzp-q8t2) (v2.0)
* To get started, first make an account on the [City of Chicago](https://data.cityofchicago.org/) website.
* Once you make a profile, head to [developer settings](https://data.cityofchicago.org/profile/edit/developer_settings) and create a new **APP TOKEN** and store it in your .env file. Note that you need the APP TOKEN not the SECRET TOKEN

## Dataset

The file `data/combined_dataset.csv` is used **only as retrieval context**.

Each row typically contains:
- A natural language query
- Corresponding SoQL parameters
- Schema information
- Optional IUCR context

## Running the Project

From the project root directory:

python main.py


You will be prompted to enter a natural language question.

The program will:
- Retrieve relevant context rows
- Print the retrieved examples
- Generate SoQL parameters using the language model
- Execute the query and display results
