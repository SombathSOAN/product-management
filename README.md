Product Management API - README

Product Management API
=======================

A FastAPI-based backend for managing products, banners, and user search logs — built for e-commerce applications that need SEO metadata, analytics tracking, and smooth product CRUD operations.

Features
--------
- Product CRUD with:
  - Name, price, unit, and tags
  - Quantity and stock visibility
  - SEO metadata (meta title, description, and image)
  - Thumbnail and gallery support
  - Telegram/Phone/Social media links
- Banner management (create, update, list)
- Search logging:
  - Track user queries and clicked products
  - Get top searched keywords for autocomplete/suggestions
- CORS enabled for frontend integration
- PostgreSQL with SQLAlchemy and `databases` async engine

Tech Stack
----------
- Backend: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy Core + `databases`
- Schema Validation: Pydantic
- Environment: `.env` + `python-dotenv`

Setup
-----
1. Clone the project
```
git clone https://github.com/yourname/product-management-api.git
cd product-management-api
```

2. Install dependencies
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure `.env`
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost/product_db
```

4. Run the server
```
uvicorn product-management:app --reload
```

API Endpoints
-------------
Products:
- GET `/products`: List all products
- GET `/products/{id}`: Get product by ID
- POST `/products`: Create product
- PUT `/products/{id}`: Update product
- DELETE `/products/{id}`: Delete product

Search:
- GET `/products/search?q=term`: Search products
- POST `/products/search/click`: Log clicked product from search
- POST `/products/search/log`: Log search term only
- GET `/products/search/suggestions`: Get top searched terms

Banners:
- GET `/banners`: List banners
- POST `/banners`: Create banner
- PUT `/banners/{id}`: Update banner

Example Product JSON
---------------------
{
  "barcode": "1234567890123",
  "name": "Premium Tea",
  "price": 2.5,
  "unit": "box",
  "tags": ["tea", "organic"],
  "thumbnail_url": "https://yourdomain.com/images/tea.jpg",
  "gallery_urls": [
    "https://yourdomain.com/images/tea-1.jpg",
    "https://yourdomain.com/images/tea-2.jpg"
  ],
  "quantity": 20,
  "stock_visibility": "show_quantity",
  "featured": true,
  "todays_deal": false,
  "telegram": "https://t.me/yourchannel",
  "phone": "012 345 6789",
  "social_link": "https://facebook.com/yourpage",
  "meta_name": "Buy Premium Tea Online",
  "meta_description": "Order Premium Tea now for just $2.50. Fast delivery.",
  "meta_image": "https://yourdomain.com/images/tea-meta.jpg"
}

Notes
-----
- Make sure your PostgreSQL table has the correct schema.
- All image/URL fields are validated with `HttpUrl` by Pydantic.

Author
------
Made with 💻 by Sombath Sona

License
-------
MIT — use freely, contribute with credit.


