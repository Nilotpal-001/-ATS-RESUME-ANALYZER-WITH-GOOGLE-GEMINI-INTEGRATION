import io
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
    
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    

def get_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:

    ##convert pdf to img
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

    #convert to bytes

        img_bytes_arr= io.BytesIO()
        first_page.save(img_bytes_arr,format='JPEG')
        img_bytes_arr=img_bytes_arr.getvalue()
    
        pdf_parts = [
            {
                "mime_type": "image/jpeg" ,
                "data": base64.b64encode(img_bytes_arr).decode() #encode to base64
            }
        ]
        return pdf_parts
    else:  
        raise FileNotFoundError("No file uploaded")
    

    ##streamlit app

st.set_page_config(page_title="ATS resume analyzer")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description:", key="input")
uploaded_file=st.file_uploader("upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("uploaded successfully")

submit1=st.button("Tell me about the Resume")
submit2=st.button("Resume Accuracy")
submit3=st.button("Required Keywords")
submit4=st.button("Ways to improve my Skills")


input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("please upload resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_response(input_prompt2,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("please upload resume")










