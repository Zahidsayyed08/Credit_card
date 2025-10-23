# 💳 Credit Card Statement Parser

A **full-stack web application** built with **Flask (Backend)** and **React (Frontend)** that intelligently extracts key financial data from credit card statements using **OCR** and **AI-powered analysis**.

---

## 🚀 Project Overview

The **Credit Card Statement Parser** uses **Optical Character Recognition (OCR)** and **Google Gemini AI** to extract structured financial information from various credit card statement formats (PDFs or images).  
It accurately identifies **5 key data points** across **5 major credit card issuers**.

---

## ✨ Key Features

### 🧾 1. Multi-Format Support
- Supports **PDF (.pdf)**, **JPEG (.jpg, .jpeg)**, and **PNG (.png)** formats  
- Maximum upload size: **10MB**
- Automatic file format detection

### 🧠 2. OCR Technology
- Uses **Tesseract OCR** for image processing  
- **pdfplumber** for PDF text extraction  
- Smart fallback for failed or partial extractions

### 🤖 3. AI-Powered Analysis
- Integrated with **Google Gemini API**  
- Extracts and interprets structured data points  
- Employs **Natural Language Processing (NLP)** for high accuracy  
- Returns well-formatted **JSON** output

### 💳 4. Supported Card Issuers
| Issuer | Sample Variants |
|--------|------------------|
| **Chase** | Sapphire, Freedom, Slate, Ink, Reserve, Preferred |
| **American Express** | Platinum, Gold, Green, Blue, Corporate |
| **Capital One** | Venture, Quicksilver, Savor, Spark |
| **Discover** | It, Chrome, Student, Cashback |
| **Citibank** | Prestige, Costco, Double Cash, Simplicity |

### 📊 5. Extracted Data Points
1. Card Last 4 Digits  
2. Billing Cycle  
3. Payment Due Date  
4. Total Balance  
5. Card Variant / Type  

### 🖥️ 6. User Experience
- Sleek and responsive **React UI**
- **Drag & Drop** file upload  
- Real-time feedback while processing  
- Clear result presentation with error handling  

---

## 🧩 Technology Stack

### 🎨 Frontend
- **React 18**
- **CSS3** (Flexbox / Grid)
- **Fetch API** for backend communication
- Error boundaries and validation

### ⚙️ Backend
- **Flask 2.3** (Python 3.8+)
- **Tesseract OCR**
- **pdfplumber**
- **Pillow** (Image preprocessing)
- **Flask-CORS**
- **Google Generative AI (Gemini)**

### 🌐 APIs
- **Google Gemini API** → AI-based data extraction  
- **Tesseract OCR** → Text extraction from images  

---

## 🔁 Processing Pipeline

```plaintext
User Interface (React)
    ↓
File Selection & Upload
    ↓
Flask Backend Validation
    ↓
OCR Text Extraction (Tesseract / pdfplumber)
    ↓
AI Analysis via Google Gemini
    ↓
Key Data Point Extraction
    ↓
Formatted JSON Response
    ↓
Results Display on UI
    ↓
File Cleanup
