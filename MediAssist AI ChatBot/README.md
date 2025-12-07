# 🏥 **AI Healthcare Assistant**
End-to-End Medical Q&A System with Fine-Tuned LLMs + RAG

This project is a HIPAA-aligned AI Healthcare Assistant that answers non-emergency medical questions, explains prescriptions, and supports chronic care guidance.
We built the system end-to-end - from raw data processing to fine-tuning LLMs, evaluating them, building a RAG module, and deploying on Google Cloud.

## 🚀 Key Features

End-to-end ETL pipeline for cleaning and preparing medical datasets

Fine-tuned four medical LLMs: MedLlama3, BioMistral-7B, MedAlpaca, Meditron

Evaluation using FCS, LLM-as-Judge, and clinical relevance checks

Selected MedLlama as the final backend model

RAG system built using a Pediatrics textbook for grounded medical answers

Prescription upload + explanation with OCR

HIPAA-aligned safety guardrails

Deployed on Google Cloud (backend + storage + inference)

## 📚 Datasets Used

MIMIC-III / MIMIC-IV

MedQuAD

iCliniq

PubMedQA

Pediatrics textbook (for RAG)

## 🧠 System Workflow (Simplified)

ETL Pipeline cleans and processes medical datasets

Fine-tuning of four LLMs on curated medical data

Evaluation → MedLlama chosen based on safety & accuracy

RAG Module uses pediatric textbook chunks for reference

Chatbot handles medical Q&A + prescription clarification

Deployment on Google Cloud for secure and scalable access

## 🖥️ Demo & Code

🎥 Demo video attached in the repository

📦 Full implementation available in this repo
