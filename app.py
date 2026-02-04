from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import requests

app = Flask(__name__)

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID = "561ebe67a3514f7187c362cb1f5ba89d"

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

CATEGORIES = ["Gin", "Whiskey", "Vodka", "Rum", "Tequila", "Brandy", "Liqueur", "Wine", "Beer", "Other"]


def fetch_bottles_from_notion():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    response = requests.post(url, headers=NOTION_HEADERS)

    if response.status_code == 200:
        data = response.json()
        bottles = []
        for page in data["results"]:
            props = page["properties"]
            name = props.get("Name", {}).get("title", [{}])[0].get("plain_text", "N/A")
            quantity = props.get("Quantity", {}).get("number", 0) or 0
            category_data = props.get("Category", {}).get("select")
            category = category_data.get("name") if category_data else "Other"
            main_bottle_pct = props.get("Main Bottle %", {}).get("number", 0) or 0
            
            bottles.append({
                "id": page["id"],
                "name": name,
                "quantity": quantity,
                "category": category,
                "main_bottle_pct": main_bottle_pct
            })
        return bottles
    else:
        print(f"Error fetching from Notion: {response.status_code} - {response.text}")
        return []


def add_bottle_to_notion(name, quantity, category, main_bottle_pct):
    url = "https://api.notion.com/v1/pages"
    new_page_data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": name}}]},
            "Quantity": {"number": int(quantity)},
            "Category": {"select": {"name": category}},
            "Main Bottle %": {"number": int(main_bottle_pct)}
        }
    }
    response = requests.post(url, headers=NOTION_HEADERS, json=new_page_data)
    return response.status_code == 200


def update_bottle_in_notion(page_id, name, quantity, category, main_bottle_pct):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    update_data = {
        "properties": {
            "Name": {"title": [{"text": {"content": name}}]},
            "Quantity": {"number": int(quantity)},
            "Category": {"select": {"name": category}},
            "Main Bottle %": {"number": int(main_bottle_pct)}
        }
    }
    response = requests.patch(url, headers=NOTION_HEADERS, json=update_data)
    return response.status_code == 200


def delete_bottle_from_notion(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    # Archive the page (Notion doesn't truly delete)
    response = requests.patch(url, headers=NOTION_HEADERS, json={"archived": True})
    return response.status_code == 200


@app.route('/')
def index():
    bottles = fetch_bottles_from_notion()
    # Group by category
    categories_dict = {}
    for bottle in bottles:
        cat = bottle["category"]
        if cat not in categories_dict:
            categories_dict[cat] = []
        categories_dict[cat].append(bottle)
    return render_template('index.html', categories_dict=categories_dict, all_categories=CATEGORIES)


@app.route('/add', methods=['GET', 'POST'])
def add_bottle():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form.get('quantity', 0)
        category = request.form.get('category', 'Other')
        main_bottle_pct = request.form.get('main_bottle_pct', 100)
        if add_bottle_to_notion(name, quantity, category, main_bottle_pct):
            return redirect(url_for('index'))
    return render_template('add_bottle.html', categories=CATEGORIES)


@app.route('/edit/<page_id>', methods=['GET', 'POST'])
def edit_bottle(page_id):
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form.get('quantity', 0)
        category = request.form.get('category', 'Other')
        main_bottle_pct = request.form.get('main_bottle_pct', 100)
        if update_bottle_in_notion(page_id, name, quantity, category, main_bottle_pct):
            return redirect(url_for('index'))
    
    # Fetch current bottle data
    bottles = fetch_bottles_from_notion()
    bottle = next((b for b in bottles if b["id"] == page_id), None)
    if not bottle:
        return redirect(url_for('index'))
    return render_template('edit_bottle.html', bottle=bottle, categories=CATEGORIES)


@app.route('/delete/<page_id>', methods=['POST'])
def delete_bottle(page_id):
    delete_bottle_from_notion(page_id)
    return redirect(url_for('index'))


@app.route('/api/update_percentage/<page_id>', methods=['POST'])
def update_percentage(page_id):
    """AJAX endpoint to quickly update bottle percentage"""
    data = request.get_json()
    pct = data.get('percentage', 100)
    
    # Get current bottle data first
    bottles = fetch_bottles_from_notion()
    bottle = next((b for b in bottles if b["id"] == page_id), None)
    if bottle:
        update_bottle_in_notion(page_id, bottle['name'], bottle['quantity'], bottle['category'], pct)
        return jsonify({"success": True})
    return jsonify({"success": False}), 404


if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0')
