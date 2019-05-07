![Build Status](https://travis-ci.com/aml-spring-19/homework-3-sudo.svg?token=AJqy8UpM4w9TVN6sptzA&branch=master)

# Homework 3
Base Repository for Homework 3

Team Members:

Alexandra Sudomoeva; UNI: as5402

Basil Vetas; UNI: bsv2111

## Data

Link to data dictionary:
https://www.cms.gov/OpenPayments/Downloads/OpenPaymentsDataDictionary.pdf

## Setup

1. If you don't have Pipenv installed:
```bash
brew install pipenv
```
or
```bash
pip install pipenv
```

2. Install dependencies:

For xgboost to install properly there are a few extra steps:
```bash
brew install gcc@8
```

After installing `gcc@8`, set it as your compiler:
```bash
export CC=gcc-8
export CXX=g++-8
```

Then install the dependencies like usual:
```bash
pipenv install --dev
```

3. Use Jupyter Notebook kernel in a virtualenv:
```bash
pipenv shell
python -m ipykernel install --user --name=`basename $VIRTUAL_ENV` --display-name "AML Homework3"
```

## Jupyter Notebook

Open notebook in virtualenv shell (make sure the AML Homework3 kernel is selected):
```bash
jupyter notebook
```

## Testing

Run unit tests in virtualenv shell:
```bash
pipenv shell
pytest
```
