from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

products = [
    # Mobile Phones - cheaper, flash sale store
    {"id": 1, "name": "iPhone 15", "brand": "Apple", "category": "Mobile", "price": 69999, "original_price": 89900, "discount": 22, "rating": 4.7, "stock": "Only 3 Left!", "offer": "No Cost EMI Available", "urgency": True},
    {"id": 2, "name": "Samsung Galaxy S24", "brand": "Samsung", "category": "Mobile", "price": 71000, "original_price": 79999, "discount": 11, "rating": 4.6, "stock": "In Stock", "offer": "Instant ₹4,000 Bank Cashback", "urgency": False},
    {"id": 3, "name": "OnePlus 12", "brand": "OnePlus", "category": "Mobile", "price": 59999, "original_price": 69999, "discount": 14, "rating": 4.5, "stock": "Only 5 Left!", "offer": "Exchange Bonus ₹3,000", "urgency": True},
    {"id": 4, "name": "Redmi Note 13 Pro", "brand": "Xiaomi", "category": "Mobile", "price": 21999, "original_price": 27999, "discount": 21, "rating": 4.3, "stock": "In Stock", "offer": "Free OTG Cable", "urgency": False},

    # Laptops - slightly higher than ElectroStore
    {"id": 5, "name": "MacBook Air M2", "brand": "Apple", "category": "Laptop", "price": 92900, "original_price": 99900, "discount": 7, "rating": 4.8, "stock": "In Stock", "offer": "No Cost EMI 12 Months", "urgency": False},
    {"id": 6, "name": "Dell XPS 15", "brand": "Dell", "category": "Laptop", "price": 162900, "original_price": 174900, "discount": 7, "rating": 4.6, "stock": "Only 2 Left!", "offer": "Free Dell Wireless Mouse", "urgency": True},
    {"id": 7, "name": "HP Pavilion 15", "brand": "HP", "category": "Laptop", "price": 58990, "original_price": 69990, "discount": 16, "rating": 4.2, "stock": "In Stock", "offer": "₹2,000 Cashback on HDFC Card", "urgency": False},
    {"id": 8, "name": "Lenovo IdeaPad Slim 5", "brand": "Lenovo", "category": "Laptop", "price": 54990, "original_price": 64990, "discount": 15, "rating": 4.3, "stock": "In Stock", "offer": "Free Laptop Bag Worth ₹1,500", "urgency": False},

    # Air Conditioners
    {"id": 9, "name": "Daikin 1.5 Ton 5 Star AC", "brand": "Daikin", "category": "AC", "price": 40999, "original_price": 47990, "discount": 15, "rating": 4.7, "stock": "Only 4 Left!", "offer": "Free Installation + Extended Warranty", "urgency": True},
    {"id": 10, "name": "Voltas 1.5 Ton 3 Star AC", "brand": "Voltas", "category": "AC", "price": 31500, "original_price": 37990, "discount": 17, "rating": 4.4, "stock": "In Stock", "offer": "Exchange Old AC - Get ₹2,000 Off", "urgency": False},

    # Televisions
    {"id": 11, "name": "Sony Bravia 55 inch 4K", "brand": "Sony", "category": "TV", "price": 74999, "original_price": 89990, "discount": 17, "rating": 4.7, "stock": "Only 2 Left!", "offer": "Free Soundbar Worth ₹4,999", "urgency": True},
    {"id": 12, "name": "LG OLED 65 inch 4K", "brand": "LG", "category": "TV", "price": 144990, "original_price": 169990, "discount": 15, "rating": 4.8, "stock": "In Stock", "offer": "No Cost EMI 24 Months", "urgency": False},
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
    app.run(port=8082, debug=True)