# Job Skills Analysis for Business Process Management (BPM) [![Under Development](https://img.shields.io/badge/status-Under%20Development-yellow.svg?color=yellow)](https://img.shields.io)


## Introduction
This project aims to analyze job descriptions for positions related to Business Process Management (BPM) and identify the skills required for these positions. The goal is to understand how skill requirements have changed over time.

## Methodology
The project uses job listings data provided by a specific job platform. It includes a natural language processing component to extract relevant information from the job descriptions.

## Implementation
The project is implemented in Python and makes use of various libraries such as pandas, nltk, and matplotlib.

## Getting Started

### Prerequisites
- Python 3.6 or later
- pip/conda

### Directories
- import (data import, translation, html-tag removing, stopword removing, punctuation removing, duplicates removing)
- skills (creating skill list [API + Other Skills])
- preprocessing (other stopwords removing, skill filter, job filter)
- analysis (currently: lda, lsa, token_freuncies)
- visualization (WorkCloud pictures for word frequencies)
- user interface (under development)
- not_in_use (code which is currently out of usage)
