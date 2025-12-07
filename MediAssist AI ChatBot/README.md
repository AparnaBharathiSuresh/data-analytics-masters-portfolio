🏥 AI Healthcare Assistant
End-to-End HIPAA-Aligned Medical Question Answering System with Fine-Tuned LLMs & RAG

This project implements a complete end-to-end healthcare AI system that helps patients get clear, reliable answers to non-emergency medical questions, understand prescriptions, and receive guidance for chronic care management.
It includes everything from data engineering, LLM fine-tuning, and evaluation, to a Pediatric textbook–based RAG module and Google Cloud deployment.

🚀 Project Highlights

✔ ETL Pipeline for cleaning and processing messy medical datasets

✔ Fine-tuning four domain-specific LLMs (MedLlama3, BioMistral-7B, MedAlpaca, Meditron)

✔ Evaluation using FCS, LLM-as-Judge, Clinical Relevance Scoring

✔ Selected MedLlama as the final backend model

✔ RAG system built using a Pediatrics Textbook for grounded medical responses

✔ Prescription upload with OCR-based interpretation

✔ HIPAA-aligned safety guardrails

✔ Deployed on Google Cloud (Cloud Run / GCE / GCS / Vertex AI)

✔ End-to-end, production-style architecture

🧰 Tech Stack
AI & NLP

MedLlama3

BioMistral-7B

MedAlpaca

Meditron

Transformers (Hugging Face)

Evaluation: FCS, LLM-as-Judge, GEval

Data Engineering

Python

ETL Pipeline

Data cleaning & preprocessing

MIMIC-III / MIMIC-IV

MedQuAD, iCliniq, PubMedQA

RAG

Pediatrics Textbook Knowledge Base

Chunking + Embeddings

FAISS / Vector Store

Context-aware prompting

Deployment

Google Cloud Platform

Cloud Run / Compute Engine

Google Cloud Storage

Secure APIs

Streamlit frontend

📊 Project Architecture
          ┌───────────────────────┐
          │     Raw Medical Data  │
          │ MIMIC, MedQuAD, etc.  │
          └───────────┬───────────┘
                      │ ETL Pipeline
                      ▼
          ┌───────────────────────┐
          │  Cleaned Training Data│
          └───────────┬───────────┘
                      │ Fine-tuning
                      ▼
          ┌───────────────────────┐
          │  Fine-Tuned LLMs      │
          │  MedLlama, etc.       │
          └───────────┬───────────┘
                      │ Evaluation (FCS, LLM-as-Judge)
                      ▼
          ┌───────────────────────┐
          │   Selected Model:     │
          │      MedLlama         │
          └───────────┬───────────┘
                      │ RAG (Pediatrics Textbook)
                      ▼
          ┌───────────────────────┐
          │   AI Medical Assistant │
          │  Q&A + Prescription    │
          │     Explanation        │
          └───────────┬───────────┘
                      │ Deployment
                      ▼
          ┌───────────────────────┐
          │ Google Cloud Platform │
          └───────────────────────┘

📦 Dataset Sources
Dataset	Purpose
MIMIC-III / MIMIC-IV	Clinical language understanding & reasoning
MedQuAD	High-quality medical Q&A
iCliniq	Real-world doctor–patient conversations
PubMedQA	Clinically relevant question answering
Pediatrics Textbook	RAG knowledge base

All datasets were cleaned, anonymized, and processed to comply with HIPAA-aligned practices.

🧪 Model Evaluation

Each model was evaluated on:

FCS (Factuality & Clinical Safety Score)

LLM-as-Judge Score

Clinical Relevance

Hallucination Risk

Readability & Patient-Friendliness

Outcome:
➡️ MedLlama achieved the highest combined score and was selected as the backend model.

📚 RAG System (Pediatrics Textbook)

Extracted high-quality pediatric reference text

Chunked (500–800 tokens) with overlaps

Generated embeddings

Stored in vector database

Retrieved on user queries to ground responses

Ensured clinically consistent and safe pediatric guidance

🖥️ Frontend Features

Clean chat interface (Streamlit)

Prescription file upload

OCR-based extraction

Context-aware medical explanation

Safety disclaimers & emergency escalation messages

☁️ Deployment

The entire system is deployed on Google Cloud, including:

Cloud Run / GCE for backend

Cloud Storage for data

Load-balanced API

Secure endpoints with controlled access

Scalable inference architecture

🎥 Demo & Code

📽 Project Demo Video – included in repository / attachments
💻 Full Source Code – This repository
🧩 Future Improvements

Expand RAG with more st
