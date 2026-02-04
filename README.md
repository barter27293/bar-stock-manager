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

## Local Development

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
   export FLASK_DEBUG=true
   ```
5. Update `NOTION_DATABASE_ID` in `app.py` with your database ID
6. Run the app:
   ```bash
   python3 app.py
   ```
7. Open http://localhost:5000

## Production Deployment (Ploi.io / VPS)

### 1. Clone to server
```bash
cd /home/ploi
git clone https://github.com/barter27293/bar-stock-manager.git
cd bar-stock-manager
```

### 2. Setup environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p logs
```

### 3. Set environment variables
Add to your server environment or `.env` file:
```
NOTION_API_KEY=your_notion_api_key
```

### 4. Supervisor (process manager)
Copy `supervisor.conf` to `/etc/supervisor/conf.d/bar-stock-manager.conf` and update paths if needed.
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start bar-stock-manager
```

### 5. Nginx (reverse proxy)
Copy `nginx.conf` to `/etc/nginx/sites-available/bar-stock-manager` and update the domain.
```bash
sudo ln -s /etc/nginx/sites-available/bar-stock-manager /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. SSL (optional but recommended)
```bash
sudo certbot --nginx -d bar.yourdomain.com
```

## Ploi.io Quick Setup

1. Add new site in Ploi with your domain
2. Connect GitHub repo: `barter27293/bar-stock-manager`
3. Add environment variable: `NOTION_API_KEY`
4. Add daemon in Ploi:
   - Command: `/home/ploi/{site}/venv/bin/gunicorn app:app -c gunicorn.conf.py`
   - Directory: `/home/ploi/{site}`
5. Deploy!

## Notion Database Schema

Your Notion database needs these properties:
- **Name** (title)
- **Quantity** (number)
- **Category** (select)
- **Main Bottle %** (number)

## Tech Stack

- Flask
- Gunicorn (production server)
- Notion API
- Vanilla JS + CSS
