# Bar Stock Manager 🍸

A visual bar inventory tracker synced with Notion.

## Features

- **Visual bottle display** with fill level indicators
- **Dynamic color coding** — red (< 25%), orange, green (80%+)
- **Category filtering** — quickly filter by spirit type
- **Quantity badges** — shows +1, +2 when you have backup bottles
- **Slider controls** — adjust fill levels with instant visual feedback
- **Mobile optimized** — 3+ bottles per row on mobile
- **Notion sync** — all data stored in your Notion database

## Setup

1. Clone the repo
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your Notion API key:
   ```bash
   export NOTION_API_KEY="your_notion_api_key"
   ```
5. Update `NOTION_DATABASE_ID` in `app.py` with your database ID
6. Run the app:
   ```bash
   python3 app.py
   ```
7. Open http://localhost:5000

## Notion Database Schema

Your Notion database needs these properties:
- **Name** (title)
- **Quantity** (number)
- **Category** (select)
- **Main Bottle %** (number)

## Tech Stack

- Flask
- Notion API
- Vanilla JS + CSS
