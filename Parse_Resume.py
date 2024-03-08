#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 19:18:47 2023

@author: GPT

Updating starting 02/08/24
@author: Gihyeon Kwon
"""
import spacy
import os
import re
import pandas as pd
from PyPDF2 import PdfReader
import fitz  # pip install PyMuPDF
import csv
from fuzzywuzzy import fuzz

#Loads pre-trained model en_core_web_sm
nlp = spacy.load('en_core_web_sm')

#New pdft to text string function using fitz
def extract_info_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    words = text.split()
    text = " ".join(words)
    return text

def extract_resume_info(text):

    doc = nlp(text)


    phone_pattern = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    email_pattern = r"[\w.-]+@[\w.-]+"
    website_pattern = r"\bhttps?://[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/))"

    #total 41 files

    #version 1: 10~ errors. 
    #Gettings the first two words, 
    # doesnt work when name is 3 words or there is a word (like page number) before name
    name = doc[:2].text

    #version 2: 30~ errors with names
    #pre trained model: confuses names with other words
    # names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    # name = names[0] if names else ""

    #8~ errors
    phone = re.search(phone_pattern, text).group(0) if re.search(phone_pattern, text) else None
    #3~ errors
    email = re.search(email_pattern, text).group(0) if re.search(email_pattern, text) else None

    #Website regex does not work at all..
    website = re.search(website_pattern, text).group(0) if re.search(website_pattern, text) else None
    
    return name, phone, email, website

def normalize_text(text):
    """
    Helper for extract_career_info function
    """
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.lower()


def fuzzy_match_colleges(text, colleges, threshold=90):
    """
    Helper for extract_career_info function
    @param threshold : percentage of similarity to look for
    """
    matched_colleges = []
    for college in colleges:
        normalized_college = normalize_text(college)
        match_score = fuzz.ratio(text, normalized_college)
        if match_score > threshold:
            matched_colleges.append(college)
    return matched_colleges

def extract_career_info(text):
    #try 1: didnt work
    # doc = nlp(text)
    # #Regex to get college patterns
    # #Many errors as Regex is not solid.
    # college_pattern = r"(?<!\bEDUCATION\s)(?:\b(?:University|College|Institute|School) of \b\w+|\b\w+ (?:University|College|Institute|School))\b"
    # college = re.search(college_pattern, text).group(0) if re.search(college_pattern,text) else "Null"


    #Try 2, using csv data:
    college_names = set()
    with open("college_names", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            college_names.add(row[1].strip().lower())

    #Option 1: broad
    found_colleges = None
    text_lower = text.lower()  # Convert text to lowercase for case-insensitive matching
    
    for college in college_names:
        if college in text_lower:
            found_colleges = college
            break
    
    return found_colleges

    #Option2 Normalzing text using fuzzywuzzy
    return fuzzy_match_colleges(text, college_names)


# Main function to parse PDF resumes in a folder and save the information in a CSV file
def parse_resumes_in_folder(folder_path, output_csv):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            resume_text = extract_info_from_pdf(pdf_path)
            name, phone, email, website = extract_resume_info(resume_text)
            college = extract_career_info(resume_text)
            # data.append([name, phone, email, website, filename])
            data.append([college, filename])

            

    # Create a pandas DataFrame from the extracted data and save it as a CSV file
    # df = pd.DataFrame(data, columns=["Name", "Cellphone number", "Email", "Website", "file"])
    df = pd.DataFrame(data, columns = ["college", "file"])
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    folder_path = "/Users/gihyeonkwon/Documents/UCSD/Research/Tanner/resumeParsing/research-lab-parsing/resume_samples"
    output_csv = "/Users/gihyeonkwon/Documents/UCSD/Research/Tanner/resumeParsing/research-lab-parsing/resume_data.csv"
    parse_resumes_in_folder(folder_path, output_csv) 
    print("completed")