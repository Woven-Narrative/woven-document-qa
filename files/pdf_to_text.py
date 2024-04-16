import os
from tqdm import tqdm
import ftfy
import PyPDF2

def pdf_to_text(pdf_dir, txt_dir):
    #This function creates txt files from the PDFs
    txt_files = []
    pdf_files = []
    for pdf_file in os.listdir(pdf_dir):
        pdf_files.append(pdf_file[:-4])
    for txt_file in os.listdir(txt_dir):
        txt_files.append(txt_file[:-4])

    #remove any items in the txt_files from the pdf_files
    download_files = [x for x in pdf_files if x not in set(txt_files)]

    for file in tqdm(download_files):
            pdf_filename = os.path.join(pdf_dir,file+".pdf")
            pdfFileObj = open(pdf_filename, 'rb')
            pdfReader= PyPDF2.PdfReader(pdfFileObj)
            num_pages = len(pdfReader.pages)
            count = 0
            text = ""

            while count < num_pages:
                pageObj = pdfReader.pages[count]
                count += 1
                text += pageObj.extract_text()

            if text != "":
                ftfy_text = ftfy.fix_text(text)
                txt_filename = os.path.join(txt_dir, file[:-4])
                with open(txt_filename+".txt", 'w',encoding='utf-8') as the_file:
                    the_file.write(ftfy_text)

input = r'/home/thomas/Documents/WOVEN/langchain-ask-the-doc/pdf'
out = r'/home/thomas/Documents/WOVEN/langchain-ask-the-doc/text'
pdf_to_text(input, out)