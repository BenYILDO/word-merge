"""Streamlit app to merge Word documents without losing formatting."""

import io
from typing import Iterable

import streamlit as st
from docx import Document
from docxcompose.composer import Composer


def merge_documents(doc_files: Iterable[io.BytesIO]) -> bytes:
    """Return merged Word document bytes for the given docx files."""
    docs = list(doc_files)
    base = Document(docs[0])
    composer = Composer(base)
    for doc_file in docs[1:]:
        composer.append(Document(doc_file))
    output = io.BytesIO()
    composer.save(output)
    output.seek(0)
    return output.read()

st.set_page_config(page_title="Word Birleştirici")

st.title("Word Dosyası Birleştirici")

uploaded_files = st.file_uploader(
    "Word dosyaları yükleyin",
    type="docx",
    accept_multiple_files=True,
)

if uploaded_files:
    st.subheader("Sıralama")
    order_map = {}
    for idx, f in enumerate(uploaded_files):
        order_map[f.name] = st.number_input(
            f"Sıra: {f.name}",
            min_value=1,
            max_value=len(uploaded_files),
            value=idx + 1,
            step=1,
            key=f"order_{f.name}",
        )

    if st.button("Birleştir"):
        sorted_files = sorted(uploaded_files, key=lambda x: order_map[x.name])
        merged_data = merge_documents(sorted_files)
        st.success("Birleştirme tamamlandı!")
        st.download_button(
            "Sonuç dosyasını indir",
            data=merged_data,
            file_name="birlesik.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
