from flask import Flask, jsonify, render_template, request
import requests
from flask_cors import CORS
import pymysql
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Mock Store URLs
STORES = {
    "ElectroStore": "http://localhost:8081",
    "QuickShop": "http://localhost:8082",
    "GadgetHub": "http://localhost:8083"
}

# MySQL Connection
def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        database='pricescout',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Create table if not exists
def init_db():
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    search_query VARCHAR(255),
                    best_store VARCHAR(100),
                    best_price INT,
                    product_name VARCHAR(255),
                    searched_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    brand VARCHAR(100),
                    category VARCHAR(100),
                    electrostore_price INT,
                    quickshop_price INT,
                    gadgethub_price INT,
                    best_store VARCHAR(100),
                    best_price INT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ DB init error: {e}")

def save_search(query, best_store, best_price, product_name):
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO search_history (search_query, best_store, best_price, product_name) VALUES (%s, %s, %s, %s)",
                (query, best_store, best_price, product_name)
            )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Save search error: {e}")

def save_products(products):
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            for p in products:
                prices = {s: p['store_prices'].get(s) for s in STORES}
                valid = {s: pr for s, pr in prices.items() if pr is not None}
                if not valid:
                    continue
                best_store = min(valid, key=valid.get)
                best_price = valid[best_store]
                cursor.execute('''
                    INSERT INTO products (name, brand, category, electrostore_price, quickshop_price, gadgethub_price, best_store, best_price, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        electrostore_price=%s, quickshop_price=%s, gadgethub_price=%s,
                        best_store=%s, best_price=%s, updated_at=%s
                ''', (
                    p['name'], p['brand'], p['category'],
                    prices.get('ElectroStore'), prices.get('QuickShop'), prices.get('GadgetHub'),
                    best_store, best_price, datetime.now(),
                    prices.get('ElectroStore'), prices.get('QuickShop'), prices.get('GadgetHub'),
                    best_store, best_price, datetime.now()
                ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Save products error: {e}")

def fetch_from_stores(query):
    results = {}
    for store_name, base_url in STORES.items():
        try:
            url = f"{base_url}/api/products/search?q={query}"
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                results[store_name] = response.json()
        except Exception as e:
            print(f"⚠️ Could not reach {store_name}: {e}")
            results[store_name] = []
    return results

def merge_results(store_results):
    merged = {}
    for store_name, products in store_results.items():
        for product in products:
            key = product['name']
            if key not in merged:
                merged[key] = {
                    'name': product['name'],
                    'brand': product['brand'],
                    'category': product['category'],
                    'rating': product['rating'],
                    'store_prices': {},
                    'store_data': {}
                }
            merged[key]['store_prices'][store_name] = product['price']
            merged[key]['store_data'][store_name] = product

    # Find best deal for each product
    final = []
    for name, data in merged.items():
        prices = {s: p for s, p in data['store_prices'].items()}
        if prices:
            best_store = min(prices, key=prices.get)
            best_price = prices[best_store]
            data['best_store'] = best_store
            data['best_price'] = best_price
            data['all_stores'] = STORES.keys()
        final.append(data)

    return final

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('index.html', error="Please enter a product to search!")

    store_results = fetch_from_stores(query)
    products = merge_results(store_results)

    if not products:
        return render_template('index.html', error=f"No products found for '{query}'", query=query)

    # Save to DB
    if products:
        best = min(products, key=lambda x: x['best_price'])
        save_search(query, best['best_store'], best['best_price'], best['name'])
        save_products(products)

    return render_template('index.html', products=products, query=query, stores=list(STORES.keys()))

@app.route('/history')
def history():
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM search_history ORDER BY searched_at DESC LIMIT 20")
            history = cursor.fetchall()
        conn.close()
        return render_template('index.html', history=history, show_history=True)
    except:
        return render_template('index.html', history=[], show_history=True)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').strip()
    store_results = fetch_from_stores(query)
    products = merge_results(store_results)
    return jsonify(products)

if __name__ == '__main__':
    init_db()
    app.run(port=8080, debug=True)