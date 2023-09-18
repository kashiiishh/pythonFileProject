from flask import Flask, render_template, request
import magic
import fitz  # PyMuPDF
import docx2txt


app = Flask(__name__)
app.template_folder = 'templates'



from pdfminer.high_level import extract_text
def pdf_to_text(pdf_path):
  return extract_text(pdf_path)























def docx_to_text(docx_path):
  txt=docx2txt.process(docx_path)
  if txt:
    return txt.replace('\t',' ')
  return None

# def pdf_to_text(pdf_path):
#     txt = ""
#     pdf_document = fitz.open(pdf_path)

#     for page_num in range(pdf_document.page_count):
#         page = pdf_document[page_num]
#         txt += page.get_text("txt")

#     pdf_document.close()
#     return txt


def identify_file_type(file):
    print("Reading file content...")
    mime = magic.Magic()
    file_content = file.read()
    print("File content length:", len(file_content))
    file_type = mime.from_buffer(file_content)
    print("Detected file type:", file_type)
    
    return file_type


    
@app.route('/', methods=['GET', 'POST'])
def home():
    # file_path=input("Enter the path to the file: ")
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file:
                file_type = identify_file_type(file)
                if "PDF" in file_type.upper():
                    result = "The file is a PDF."
                    # text=pdf_to_text(file)
                elif "MICROSOFT WORD" in file_type.upper():
                    result = "The file is DOCX."
                    text=docx_to_text(file)
                elif "IMAGE" in file_type.upper():
                    result= "The file is an Image"
                elif "EXCEL" in file_type.upper():
                    result= "The file is an ExcelSheet"
                elif "MICROSOFT POWERPOINT" in file_type.upper():
                    result= "The file is an Power Point"
                elif "MICROSOFT EXCEL" in file_type.upper():
                    result= "The file is an Excel"
                else:
                    result = "The file type is not recognized."
                return render_template('result.html', result=result,text=text)
        except Exception as e:
            print("Error:", e)
            result = "An error occurred while processing the file."
            return render_template('result.html', result=result,text=text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()


