# PaperRAG — Akademik Makale Araştırma Asistanı

[English](README.md) | [Türkçe](README_TR.md)

PaperRAG; akademik PDF'leri ayrıştıran, yöntem ve katkıları inceleyen, atıf ağları kuran, anlamsal sorgular çalıştıran ve literatür özeti oluşturan bir Retrieval-Augmented Generation sistemidir.

## Teknolojiler

- FastAPI ve Uvicorn
- ChromaDB ve Gemini embeddings
- Gemini dil modeli
- PyMuPDF PDF ayrıştırıcısı
- Semantic Scholar entegrasyonu ve çevrimdışı örnek veri desteği
- Streamlit arayüzü

## Kurulum

Python 3.10 veya üzeri gerekir.

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="api_anahtariniz"
```

## Çalıştırma

```bash
python -m backend.main
streamlit run frontend/app.py
```

Arka uç `http://127.0.0.1:8001`, arayüz ise varsayılan Streamlit adresinde çalışır.

## Testler

```bash
pytest tests/
```

