import streamlit as st
from pdf2docx import Converter
import os
import uuid

st.set_page_config(page_title="PDF to Word Converter", layout="centered")

st.title("📄 PDF to Word Converter")
st.markdown("Convert your PDF to an editable Word document. **Free & Online!**")

uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

if uploaded_file:
    file_id = str(uuid.uuid4())
    input_pdf_path = f"/tmp/{file_id}.pdf"
    output_docx_path = f"/tmp/{file_id}.docx"

    with open(input_pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    st.info("Converting... Please wait ⏳")
    try:
        cv = Converter(input_pdf_path)
        cv.convert(output_docx_path, start=0, end=None)
        cv.close()

        with open(output_docx_path, "rb") as f:
            st.success("✅ Conversion complete!")
            st.download_button("⬇️ Download Word File", f, file_name="converted.docx")

        os.remove(input_pdf_path)
        os.remove(output_docx_path)

    except Exception as e:
        st.error(f"❌ Error during conversion: {e}")
