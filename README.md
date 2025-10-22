# Netcore Personalization Demo (Streamlit)

An interactive demo app that showcases how Netcore can personalize user experiences across channels — from browsing analytics to AI-powered product recommendations and personalized emails.

---

## Features

- **Fashion storefront UI**
  - Three categories: **Dresses**, **Tops**, and **Bottoms**
  - Product grids with real images, prices, and discount tags
  - “Quick View” pop-up for product details

- **Live Prediction Widget (right sidebar)**
  - Learns user preferences in real time
  - Tracks category interest, style preference, and discount affinity

- **Store Analytics Widget (top bar)**
  - Collapsible summary for session metrics (dwell time, location, weather, etc.)

- **Personalized Email Preview**
  - Automatically generates an HTML email with:
    - Your brand logo
    - Product recommendations based on user behavior
  - Lets you preview or download the HTML file (`email.html`)

---

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** [Streamlit](https://streamlit.io)
- **Frontend:** Streamlit Components (HTML/CSS for layout and modals)
- **Hosting:** Streamlit Cloud / Localhost

---

## Local Setup

```bash
# 1. Create virtual environment (optional)
python3 -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
