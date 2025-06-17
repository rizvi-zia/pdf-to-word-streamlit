import streamlit as st
from pdf2docx import Converter
import os
import uuid

st.set_page_config(page_title="Document Toolkit", layout="centered")

# --- Sidebar Navigation ---
st.sidebar.title("📚 Document Toolkit")
tool = st.sidebar.radio("Choose a tool", [
    "PDF to Word",
    "Word to PDF",
    "Compress PDF",
    "JPG to PDF",
    "PDF to JPG"
])

# --- Tool: PDF to Word ---
def pdf_to_word():
    st.title("📄 PDF to Word Converter")
    st.markdown("Convert your PDF to an editable Word document. **Free & Online!**")
    uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if uploaded_file:
        file_id = str(uuid.uuid4())
        input_pdf = f"/tmp/{file_id}.pdf"
        output_docx = f"/tmp/{file_id}.docx"

        with open(input_pdf, "wb") as f:
            f.write(uploaded_file.read())

        st.info("🔄 Converting...")
        try:
            cv = Converter(input_pdf)
            cv.convert(output_docx)
            cv.close()

            with open(output_docx, "rb") as f:
                st.success("✅ Done!")
                st.download_button("⬇️ Download Word File", f, file_name="converted.docx")

            os.remove(input_pdf)
            os.remove(output_docx)
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- Tool: Word to PDF (placeholder) ---
def word_to_pdf():
    st.title("📝 Word to PDF Converter")
    st.markdown("Convert DOCX to PDF. **Coming soon...**")

# --- Tool: Compress PDF (placeholder) ---
def compress_pdf():
    st.title("📉 Compress PDF")
    st.markdown("Reduce PDF file size. **Coming soon...**")

# --- Tool: JPG to PDF (placeholder) ---
def jpg_to_pdf():
    st.title("🖼 JPG to PDF Converter")
    st.markdown("Convert JPG images into PDF. **Coming soon...**")

# --- Tool: PDF to JPG (placeholder) ---
def pdf_to_jpg():
    st.title("🧾 PDF to JPG Converter")
    st.markdown("Turn your PDF into image files. **Coming soon...**")

# --- Router ---
if tool == "PDF to Word":
    pdf_to_word()
elif tool == "Word to PDF":
    word_to_pdf()
elif tool == "Compress PDF":
    compress_pdf()
elif tool == "JPG to PDF":
    jpg_to_pdf()
elif tool == "PDF to JPG":
    pdf_to_jpg()
