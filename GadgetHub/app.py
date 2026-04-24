from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

products = [
    # Mobile Phones - mid range pricing
    {"id": 1, "name": "iPhone 15", "brand": "Apple", "category": "Mobile", "price": 75999, "original_price": 89900, "discount": 15, "rating": 4.8, "stock": "In Stock", "offer": "Free 1 Year AppleCare", "delivery": "Free Delivery Tomorrow"},
    {"id": 2, "name": "Samsung Galaxy S24", "brand": "Samsung", "category": "Mobile", "price": 72999, "original_price": 79999, "discount": 9, "rating": 4.7, "stock": "In Stock", "offer": "Flat ₹3,000 Off on Exchange", "delivery": "Free Delivery Tomorrow"},
    {"id": 3, "name": "OnePlus 12", "brand": "OnePlus", "category": "Mobile", "price": 62999, "original_price": 69999, "discount": 10, "rating": 4.6, "stock": "In Stock", "offer": "Buy 2 Get 10% Extra Off", "delivery": "Free Delivery in 2 Days"},
    {"id": 4, "name": "Redmi Note 13 Pro", "brand": "Xiaomi", "category": "Mobile", "price": 23499, "original_price": 27999, "discount": 16, "rating": 4.4, "stock": "Out of Stock", "offer": "", "delivery": ""},

    # Laptops - competitive pricing
    {"id": 5, "name": "MacBook Air M2", "brand": "Apple", "category": "Laptop", "price": 87900, "original_price": 99900, "discount": 12, "rating": 4.9, "stock": "In Stock", "offer": "EMI from ₹7,325/month", "delivery": "Free Delivery Tomorrow"},
    {"id": 6, "name": "Dell XPS 15", "brand": "Dell", "category": "Laptop", "price": 155900, "original_price": 174900, "discount": 11, "rating": 4.7, "stock": "In Stock", "offer": "Extra 5% Off with Axis Card", "delivery": "Free Delivery in 2 Days"},
    {"id": 7, "name": "HP Pavilion 15", "brand": "HP", "category": "Laptop", "price": 59990, "original_price": 69990, "discount": 14, "rating": 4.3, "stock": "In Stock", "offer": "1 Year Accidental Damage Cover", "delivery": "Free Delivery Tomorrow"},
    {"id": 8, "name": "Lenovo IdeaPad Slim 5", "brand": "Lenovo", "category": "Laptop", "price": 56490, "original_price": 64990, "discount": 13, "rating": 4.4, "stock": "In Stock", "offer": "Free Laptop Sleeve", "delivery": "Free Delivery in 2 Days"},

    # Air Conditioners
    {"id": 9, "name": "Daikin 1.5 Ton 5 Star AC", "brand": "Daikin", "category": "AC", "price": 41990, "original_price": 47990, "discount": 13, "rating": 4.8, "stock": "In Stock", "offer": "Free Professional Installation", "delivery": "Delivery in 3-5 Days"},
    {"id": 10, "name": "Voltas 1.5 Ton 3 Star AC", "brand": "Voltas", "category": "AC", "price": 33490, "original_price": 37990, "discount": 12, "rating": 4.5, "stock": "In Stock", "offer": "5 Year Comprehensive Warranty", "delivery": "Delivery in 3-5 Days"},

    # Televisions
    {"id": 11, "name": "Sony Bravia 55 inch 4K", "brand": "Sony", "category": "TV", "price": 76990, "original_price": 89990, "discount": 14, "rating": 4.8, "stock": "In Stock", "offer": "Free HDMI Cable + Wall Mount", "delivery": "Free Delivery in 2 Days"},
    {"id": 12, "name": "LG OLED 65 inch 4K", "brand": "LG", "category": "TV", "price": 147990, "original_price": 169990, "discount": 13, "rating": 4.9, "stock": "In Stock", "offer": "No Cost EMI 18 Months", "delivery": "Delivery in 3-5 Days"},
]

@app.route('/')
def home():
    category = request.args.get('category', 'All')
    if category and category != 'All':
        filtered = [p for p in products if p['category'] == category]
    else:
        filtered = products
    return render_template('index.html', products=filtered, selected_category=category)

@app.route('/api/products')
def get_all_products():
    return jsonify(products)

@app.route('/api/products/search')
def search_products():
    query = request.args.get('q', '').lower()
    results = [p for p in products if query in p['name'].lower() or query in p['brand'].lower() or query in p['category'].lower()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=8083, debug=True)