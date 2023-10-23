import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm
import wget

def get_clean_pdf_url(url):
    # Ensures the PDF URL is clean and ends with '.pdf'
    return url.split(".pdf")[0] + ".pdf"

def get_pdf_url(doi):
    # Fetches the PDF URL from Sci-Hub using the DOI
    response = requests.get(f"https://sci-hub.se/{doi}")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    embed_tag = soup.find('embed', id='pdf')
    if embed_tag:
        src = embed_tag['src']
        
        # Convert src to string if it's not
        if not isinstance(src, str):
            src = str(src)
        
        # Handling different URL formats
        if src.startswith("//"):
            src = "https:" + src
        elif src.startswith("/downloads/"):
            src = "https://sci-hub.se" + src

        cleaned_src = get_clean_pdf_url(src)
        return cleaned_src
    return None

def download_pdf(doi, title):
    # Replaces non-alphanumeric characters in title with underscores for safe file naming
    safe_title = ''.join(e for e in title if e.isalnum() or e.isspace()).replace(' ', '_')
    pdf_url = get_pdf_url(doi)
    
    if pdf_url:
        pdf_path = f"downloads/{safe_title}.pdf"
        try:
            # Creates 'downloads' directory if it doesn't exist
            if not os.path.exists('downloads'):
                os.makedirs('downloads')

            # Use wget to download the file
            wget.download(pdf_url, out=pdf_path)
            print(f"\nDownloaded '{title}.pdf' successfully!")

        except Exception as e:
            print(f"Error processing DOI {doi} (Title: {title}): {e}")
            failed_dois.append(doi)

    else:
        print(f"Failed to download PDF for DOI: {doi} (Title: {title})")
        failed_dois.append(doi)

# Load DOIs from JSON
with open('data/example.json', 'r') as file:
    doi_list_data = json.load(file)

failed_dois = []

# Loop through all DOIs in the JSON and download them
for entry in tqdm(doi_list_data, desc="Downloading PDFs", unit="pdf"):
    doi = entry['DOI']
    title = entry['title']
    download_pdf(doi, title)

# Save failed DOIs to a JSON file in the 'data' directory
if failed_dois:
    with open('data/failed_DOIs.json', 'w') as file:
        json.dump(failed_dois, file)

print(f"Script completed! {len(failed_dois)} DOIs failed to download. Check 'data/failed_DOIs.json' for the list.")
