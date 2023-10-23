import requests
import os
import json
from tqdm import tqdm
from termcolor import colored

# Constants
API_KEY = 'ask_3351fe619beda014a7b025c95598543f'
PDF_FOLDER = 'downloads'
QUESTIONS_FOLDER = 'questions'
UPLOAD_ENDPOINT = 'https://api.askyourpdf.com/v1/api/upload'
CHAT_ENDPOINT = 'https://api.askyourpdf.com/v1/chat/{}'

headers = {
    'x-api-key': API_KEY
}

def get_response_for_prompt(pdf_file, prompt):
    file_path = os.path.join(PDF_FOLDER, pdf_file)
    with open(file_path, 'rb') as file:
        response = requests.post(UPLOAD_ENDPOINT, headers=headers, files={'file': file})
        if response.status_code == 201:
            doc_id = response.json().get('docId')
            chat_data = [{"sender": "User", "message": prompt}]
            chat_response = requests.post(CHAT_ENDPOINT.format(doc_id), headers=headers, json=chat_data)
            if chat_response.status_code == 200:
                return chat_response.json().get('answer', {}).get('message')
    return None

def analyze_pdf(pdf_file):
    """Analyze a single PDF using the AskYourPDF API and store the results in a JSON."""
    combined_response = {}
    
    # Progress bar initialization
    with tqdm(total=2, desc=f"Processing {pdf_file}", position=0, leave=True) as pbar:
        
        # Analysis
        for question_file in sorted(os.listdir(QUESTIONS_FOLDER)):
            with open(os.path.join(QUESTIONS_FOLDER, question_file), 'r') as file:
                prompt = file.read().strip()
                response = get_response_for_prompt(pdf_file, prompt)
                if response:
                    combined_response.update(json.loads(response))
        
        pbar.update(1)
        pbar.set_description("Checking work")
        
        # Double-checking the analysis (can be expanded upon if needed)
        for question_file in sorted(os.listdir(QUESTIONS_FOLDER)):
            with open(os.path.join(QUESTIONS_FOLDER, question_file), 'r') as file:
                prompt = file.read().strip()
                response = get_response_for_prompt(pdf_file, prompt)
                if response:
                    combined_response.update(json.loads(response))
        
        pbar.update(1)
        
        # Save the combined response into a JSON file
        json_filename = f"data/analysisJSONs/{os.path.splitext(pdf_file)[0]}_response.json"
        with open(json_filename, 'w') as json_file:
            json.dump(combined_response, json_file, indent=4)
        
        print(colored(f"Analysis successful! Saved combined chat response for {pdf_file} in {json_filename}", "green"))
