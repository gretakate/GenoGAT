#!/bin/bash

set -e

# Create and activate a virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Download dataset from Kaggle
echo "Downloading dataset from Kaggle..."
kaggle datasets download -d gretakintzley/ncbi-sars-cov-2-rna-sequences
echo "Unzipping dataset..."
unzip ncbi-sars-cov-2-rna-sequences.zip
mkdir -p data
mv raw_covid_rna_test/* data/
mv raw_covid_rna_train/* data/
rm ncbi-sars-cov-2-rna-sequences.zip
rm -r raw_covid_rna_test
rm -r raw_covid_rna_train

# Install Badread from GitHub
echo "Installing Badread from GitHub..."
pip install git+https://github.com/rrwick/Badread.git

echo "Setup complete."
