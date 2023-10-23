import requests
from bs4 import BeautifulSoup
import json
import os
from termcolor import colored
from tqdm import tqdm
import wget
import csv
from analyzer import analyze_pdf

def get_clean_pdf_url(url):
    return url.split(".pdf")[0] + ".pdf"

def get_pdf_url(doi):
    response = requests.get(f"https://sci-hub.se/{doi}")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    embed_tag = soup.find('embed', id='pdf')
    if embed_tag:
        src = embed_tag['src']
        
        if not isinstance(src, str):
            src = str(src)
        
        if src.startswith("//"):
            src = "https:" + src
        elif src.startswith("/downloads/"):
            src = "https://sci-hub.se" + src

        cleaned_src = get_clean_pdf_url(src)
        return cleaned_src
    return None

def write_to_csv(title, year, doi, analysis_results):
    with open('data/downloaded_papers.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        row = [title, year, doi]
        for term in ANALYSIS_TERMS:
            value = analysis_results.get(term, None)
            if isinstance(value, list):
                row.append(', '.join(value))
            else:
                row.append(value)
        writer.writerow(row)

def download_pdf(doi, title, year):
    safe_title = ''.join(e for e in title if e.isalnum() or e.isspace()).replace(' ', '_')
    pdf_url = get_pdf_url(doi)
    
    if pdf_url:
        pdf_path = f"downloads/{safe_title}.pdf"
        try:
            if not os.path.exists('downloads'):
                os.makedirs('downloads')
            wget.download(pdf_url, out=pdf_path)
            print(colored(f"\nDownloaded '{title}.pdf' successfully!", "green"))
            analyze_pdf(f"{safe_title}.pdf")
            with open(f"data/analysisJSONs/{safe_title}_response.json", 'r') as json_file:
                analysis_results = json.load(json_file)
            write_to_csv(title, year, doi, analysis_results)
        except Exception as e:
            print(colored(f"Error processing DOI {doi} (Title: {title}): {e}", "red"))
            failed_dois.append(doi)
    else:
        print(colored(f"Failed to download PDF for DOI: {doi} (Title: {title})", "red"))
        failed_dois.append(doi)

ANALYSIS_TERMS = [
    "Blue infrastructure",
    "blue-green infrastructure",
    "gray infrastructure",
    "water quality",
    "air quality",
    "biodiversity",
    "Stormwater management",
    "Flood-risk management",
    "public health",
    "GI_Examples",
    "Geographic Population Density",
    "Primary Locale",
    "Methodology",
    "Challenges and Limitations"
]

if not os.path.exists('data/downloaded_papers.csv'):
    with open('data/downloaded_papers.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Year", "DOI"] + ANALYSIS_TERMS)

with open('data/real.json', 'r') as file:
    doi_list_data = json.load(file)

failed_dois = []
start_year = 1995
end_year = 2023
processed_dois = []

for _ in tqdm(range(45), desc="Downloading PDFs", unit="pdf"):
    year = start_year
    while year <= end_year:
        papers_for_year = [paper for paper in doi_list_data if paper.get('year') == year and paper['DOI'] not in processed_dois]
        
        if papers_for_year:
            selected_paper = papers_for_year[0]
            download_pdf(selected_paper['DOI'], selected_paper['title'], selected_paper['year'])
            processed_dois.append(selected_paper['DOI'])
            break
        
        year += 1
        if year > end_year:
            year = start_year

if failed_dois:
    with open('data/failed_DOIs.json', 'w') as file:
        json.dump(failed_dois, file)

print(f"Script completed! {len(failed_dois)} DOIs failed to download. Check 'data/failed_DOIs.json' for the list.")
