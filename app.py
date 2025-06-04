import streamlit as st
from PIL import Image
import pytesseract
import pdfplumber
from transformers import pipeline
from fpdf import FPDF
import os

summarizer = pipeline("summarization")

st.set_page_config(page_title="AI Summarizer", layout="centered")

st.title("🧠 AI Summarizer - Text/Image/PDF")
st.markdown("Upload an image or PDF. Get summary instantly!")

uploaded_file = st.file_uploader("Upload an Image or PDF", type=["png", "jpg", "jpeg", "pdf"])
output_text = ""

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            full_text = "\n".join(pages)
    else:
        image = Image.open(uploaded_file)
        full_text = pytesseract.image_to_string(image)

    if full_text.strip():
        with st.spinner("Summarizing..."):
            output = summarizer(full_text, max_length=120, min_length=30, do_sample=False)
            output_text = output[0]["summary_text"]
            st.subheader("🔍 Summary:")
            st.write(output_text)

            if st.button("📋 Copy Summary"):
                st.code(output_text, language="text")

            pdf_button = st.download_button(
                label="⬇️ Download as PDF",
                data=FPDF(),
                file_name="summary.pdf",
                mime="application/pdf"
            )
    else:
        st.error("No text detected.")
