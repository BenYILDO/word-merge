diff --git a//dev/null b/streamlit_word_merge.py
index 0000000000000000000000000000000000000000..47fcbd64cf0bee25e9496506650aa1c4d24664e5 100644
--- a//dev/null
+++ b/streamlit_word_merge.py
@@ -0,0 +1,43 @@
+import io
+import streamlit as st
+from docx import Document
+from docxcompose.composer import Composer
+
+st.set_page_config(page_title="Word Birleştirici")
+
+st.title("Word Dosyası Birleştirici")
+
+uploaded_files = st.file_uploader(
+    "Word dosyaları yükleyin",
+    type="docx",
+    accept_multiple_files=True,
+)
+
+if uploaded_files:
+    st.subheader("Sıralama")
+    order_map = {}
+    for idx, f in enumerate(uploaded_files):
+        order_map[f.name] = st.number_input(
+            f"Sıra: {f.name}",
+            min_value=1,
+            max_value=len(uploaded_files),
+            value=idx + 1,
+            step=1,
+            key=f"order_{f.name}",
+        )
+
+    if st.button("Birleştir"):
+        sorted_files = sorted(uploaded_files, key=lambda x: order_map[x.name])
+        base = Document(sorted_files[0])
+        composer = Composer(base)
+        for doc_file in sorted_files[1:]:
+            composer.append(Document(doc_file))
+        output = io.BytesIO()
+        composer.save(output)
+        st.success("Birleştirme tamamlandı!")
+        st.download_button(
+            "Sonuç dosyasını indir",
+            data=output.getvalue(),
+            file_name="birlesik.docx",
+            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
+        )
