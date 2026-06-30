# AI LinkedIn Post Generator

An AI-powered LinkedIn Post Generator that creates professional LinkedIn posts using **Large Language Models (LLMs)**, **Few-Shot Learning**, and **Prompt Engineering**.

Users can generate LinkedIn posts by selecting:

* Influencer style
* Topic
* Post length
* Language

The generated post follows the writing style of the selected influencer and is optimized for professional LinkedIn content.

---

# Features

* Generate AI-powered LinkedIn posts
* Mimic writing style of different influencers
* Support multiple post topics
* Generate posts in English and Hinglish
* Choose post length (Short / Medium / Long)
* Few-shot learning for style-based generation
* Fast inference using Groq Cloud API
* Simple and interactive UI with Streamlit

---

# Problem Statement

Writing high-quality LinkedIn posts consistently can be difficult and time-consuming.

This project solves that problem by using Generative AI to automate post creation while maintaining professional tone, structure, and style.

---

# Tech Stack

## Programming Language

* Python

## Frameworks & Libraries

* Streamlit
* LangChain
* Pandas
* Python-dotenv

## AI/LLM

* Llama 3.3 70B Versatile

## API Provider

* Groq Cloud

## Dataset Source

* Kaggle LinkedIn Posts Dataset

---

# Project Architecture

Raw Dataset (Kaggle ZIP)
↓
Data Preprocessing
↓
Metadata Extraction using LLM
↓
Processed JSON Dataset
↓
Few-Shot Example Retrieval
↓
Prompt Engineering
↓
Groq API Call
↓
LLM Response
↓
Generated LinkedIn Post

---

# How It Works

## Step 1: Dataset Collection

The project uses a LinkedIn post dataset from Kaggle containing:

* Influencer names
* LinkedIn post content
* Followers count

---

## Step 2: Data Preprocessing

The raw dataset is cleaned and processed by:

* Extracting ZIP files
* Reading CSV files
* Removing null values
* Selecting unique influencers
* Extracting metadata

Extracted metadata includes:

* Line count
* Language
* Tags

---

## Step 3: Few-Shot Learning

Relevant example posts are retrieved based on:

* Influencer
* Topic
* Length
* Language

These examples are used as context for generation.

---

## Step 4: Prompt Engineering

A structured prompt is created using:

* Selected topic
* Selected length
* Selected language
* Influencer style
* Example posts

This improves output quality.

---

## Step 5: LLM Generation

The prompt is sent to Groq Cloud using API calls.

Model Used:

* Llama 3.3 70B Versatile

The model generates a new LinkedIn post based on user input.

---

# Project Structure

```bash
LinkedIn-Post-Generator/
│
├── data/
│   ├── linkedin_data.zip
│   ├── processed_posts.json
│
├── main.py
├── few_shot.py
├── preprocess.py
├── post_generator.py
├── llm_helper.py
├── requirements.txt
├── .env
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <your-repository-url>
cd LinkedIn-Post-Generator
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in root directory.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Run Application

```bash
streamlit run main.py
```

---

# Sample Inputs

* Influencer: Selected Creator
* Topic: Data Science
* Length: Medium
* Language: English

---

# Sample Output

AI generates a professional LinkedIn post in the selected influencer’s writing style.

Example:

* Professional tone
* Relevant topic
* Structured formatting
* Human-like writing

---

# Challenges Faced

* Understanding prompt engineering
* Maintaining style consistency
* Tag normalization
* Handling LLM output formatting
* Dataset preprocessing

---

# Future Improvements

* Add more influencers
* Improve retrieval system
* Add RAG pipeline
* Deploy on cloud
* Add analytics dashboard
* Improve UI/UX

---

# Learning Outcomes

This project helped me gain hands-on experience in:

* Generative AI
* LLM Integration
* Prompt Engineering
* Few-Shot Learning
* API Handling
* Streamlit Development

---

# Author

**Preeti Saini**
Computer Science Engineer
AI / Software Development Enthusiast
