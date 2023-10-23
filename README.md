# Sci-Hub PDF Downloader

A script to automate the downloading of academic papers from Sci-Hub using a list of DOIs (Digital Object Identifiers).

## Description

This script reads a list of DOIs from a JSON file, processes each DOI to obtain the direct PDF URL from Sci-Hub, and downloads the PDFs to a specified directory on your local machine. 
If a download fails, the DOI is saved to a list of failed DOIs, which is then saved to a JSON file for further reference.

## Dependencies

- Python 3
- `requests`
- `beautifulsoup4`
- `wget`
- `tqdm`

Install the required dependencies using pip:

```bash
pip install requests beautifulsoup4 wget tqdm
```

## Usage

1. Ensure you have a file named `DOI_LIST_1.json` in a directory named `data`. Each entry in the JSON file should be a dictionary with at least the keys `'DOI'` and `'title'`.

Example `DOI_LIST_1.json` content:
```json
[
    {"DOI": "10.1038/nature12373", "title": "A title of a paper"},
    {"DOI": "10.1038/nature12374", "title": "Another title of a paper"}
]
```

2. Run the script:
```bash
python scraper.py
```

3. The script will create a directory named `downloads` (if it doesn't already exist) and save the downloaded PDFs there. If any downloads fail, a file named `failed_DOIs.json` will be created in the `data` directory, listing the DOIs that failed.

## Notes

- This script is intended for personal use to automate the process of downloading academic papers for bibliographic research, especially for researchers who lack the necessary resources or subscriptions to access certain papers.
- Please be aware of and respect the terms of service of Sci-Hub and the copyright laws applicable in your jurisdiction when using this script.
