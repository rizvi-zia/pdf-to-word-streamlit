import streamlit as st
from pdf2docx import Converter
from fpdf import FPDF
from PIL import Image
import fitz  # PyMuPDF
import os
import uuid

st.set_page_config(page_title="Document Toolkit", layout="centered")

# --- Sidebar Navigation ---
st.sidebar.title("📚 Document Toolkit")
tool = st.sidebar.radio("Choose a tool", [
    "PDF to Word",
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

# --- Tool: JPG to PDF ---
def jpg_to_pdf():
    st.title("🖼 JPG to PDF Converter")
    st.markdown("Convert JPG images into a single PDF document.")
    uploaded_files = st.file_uploader("Upload JPG images", type=["jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        images = []
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file).convert("RGB")
            images.append(image)

        if images:
            pdf_path = f"/tmp/{uuid.uuid4()}.pdf"
            images[0].save(pdf_path, save_all=True, append_images=images[1:])

            with open(pdf_path, "rb") as f:
                st.success("✅ PDF created!")
                st.download_button("⬇️ Download PDF", f, file_name="images.pdf")

            os.remove(pdf_path)

# --- Tool: PDF to JPG ---
def pdf_to_jpg():
    st.title("🧾 PDF to JPG Converter")
    st.markdown("Turn your PDF pages into high-quality JPG images.")
    uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if uploaded_file:
        pdf_path = f"/tmp/{uuid.uuid4()}.pdf"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        try:
            pdf = fitz.open(pdf_path)
            for page_number in range(len(pdf)):
                page = pdf.load_page(page_number)
                pix = page.get_pixmap()
                img_path = f"/tmp/page_{page_number + 1}.jpg"
                pix.save(img_path)
                with open(img_path, "rb") as img_file:
                    st.download_button(f"⬇️ Download Page {page_number + 1} as JPG", img_file, file_name=f"page_{page_number + 1}.jpg")
                os.remove(img_path)
            os.remove(pdf_path)
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- Router ---
if tool == "PDF to Word":
    pdf_to_word()
elif tool == "JPG to PDF":
    jpg_to_pdf()
elif tool == "PDF to JPG":
    pdf_to_jpg()
