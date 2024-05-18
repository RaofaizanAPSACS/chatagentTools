# Import required libraries.
import requests
from PyPDF2 import PdfReader



# Function to call the Q/A and Query Document API.
def process_doc_query(text):
    if text != "":
        api_url = "http://localhost:8000/queryDoc"
        payload = {"query": text}
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            answer = response.json()["Answer"]
            answer = "Answer: " + answer
            return answer, ""
        else:
            return "Upload a PDF File to ask queries.", ""


def process_query(text, history):
    
    api_url = "http://localhost:8000/querySearch"  # Replace with your API endpoint URL
    payload = {"query": text}
    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        answer = response.json()["Answer"]

        history.append((text, answer))
        # for char in answer:

        #     history[-1][1] += char
        #     #time.sleep(0.05)
        #     yield history
        return "", history
    else:
        print("Error: Failed to get a response from the API")


# Function to call the upload document API.
def uplaod_doc(file):

    # Reading PDF file.
    text = ""

    # Check whether file is successfully uploaded, then extract text.
    if file is not None:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()

        api_url = "http://localhost:8000/uploadDoc"  
        payload = {"file": text}
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return "File Uploaded Successfully"
        else:
            return "Error: Failed to get a response from the API"
        


# Function for remove PDF API call functionality.
def clear_knowledge_base():
    api_url = "http://localhost:8000/removeDoc" 
    response = requests.get(api_url)
    if response.status_code == 200:
        return "","Answer",""
    else:
        return "Error: Failed to get a response from the API"