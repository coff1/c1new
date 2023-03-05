# -*- coding: UTF-8 -*-
import io
import PyPDF2
import docx
import pandas as pd
from source.myclass.mylog import mylog

def extract_text_from_pdf_content(content,url):
    try:
        # Create a file-like object to pass to PyPDF2
        pdf_file = io.BytesIO(content)

        # Create a PyPDF2 object to extract text from the content
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize a string to store the extracted text
        extracted_text = ""

        # Loop through each page in the PDF and extract the text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text()

        # Return the extracted text
        return extracted_text
    except BaseException:
        message = "extract_text_from_pdf_content error, url : {}".format(url)
        mylog().error(message)
        return ""



def extract_text_from_docx_content(content,url):
    try:
        doc = docx.Document(io.BytesIO(content))
        text = [para.text for para in doc.paragraphs]
        return '\n'.join(text)
    except BaseException:
        message = "extract_text_from_docx_content error, url : {}".format(url)
        mylog().error(message)
        return ""


def extract_text_from_excel_content(content,url):
    try:
        xls = pd.read_excel(io.BytesIO(content))
        return xls.to_string()
    except BaseException:
        message = "extract_text_from_excel_content error, url : {}".format(url)
        mylog().error(message)
        return ""



def extract_text_from_text_content(content,url):
    try:
        return content.decode("UTF-8")
    except BaseException:
        try:
            return content.decode("ANSI")
        except BaseException:
            try:
                return content.decode("ASCII")
            except BaseException:
                try:
                    return content.decode("UNICODE")
                except BaseException:
                    try:
                        return content.decode("GB2312")
                    except BaseException:
                        try:
                            return content.decode("UTF-6")
                        except BaseException:
                            message = "extract_text_from_text_content error, url : {}".format(url)
                            mylog().error(message)
                            return ""
                        

def extract_text_from_all_kinds_content(content,type,url):
    type_in_natural_language=type
    if "text" in type_in_natural_language:
        return extract_text_from_text_content(content,url)
    if type_in_natural_language == "document-pdf":
        return extract_text_from_pdf_content(content,url)
    if type_in_natural_language == "document-excel":
        return extract_text_from_excel_content(content,url)
    if type_in_natural_language == "document-docx":
        return extract_text_from_docx_content(content,url)
    # 尝试解析漏网之鱼
    message = "extract_text_from_all_kinds_content pass:{}".format(url)
    mylog().error(message)
    return ""