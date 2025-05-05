# Prompt Tuning for Structured Data Extraction

This repository contains scripts for extracting structured JSON data from unstructured text descriptions using Oracle Cloud Infrastructure (OCI) Generative AI Service.

## Overview

These scripts demonstrate how to:
1. Define a JSON schema for structured data extraction
2. Create a prompt with specific instructions for the LLM
3. Process and validate the LLM's response
4. Extract and save the resulting JSON data

## Scripts

- `prompt_tuning.py` - Uses OCI Generative AI with Meta Llama 3.3 70B model
- `prompt_tuning_cohere.py` - Uses OCI Generative AI with Cohere model

## Sample Data

The repository includes sample tree evaluation data in Italian and the extracted JSON outputs:
- `samples/tree_evaluation.txt` - Sample input text
- `samples/extracted_tree_data.json` - Output from Llama model
- `samples/extracted_tree_data_cohere.json` - Output from Cohere model

## Requirements

- Python 3.6+
- OCI Python SDK
- OCI CLI configured with appropriate credentials

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt