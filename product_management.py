### Version 11.1, Fixed Image Search
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
import PIL.Image as Image
import io
import pandas as pd
import io
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl, ValidationError
from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone
from pydantic import validator
import os
from dotenv import load_dotenv
import databases
import sqlalchemy
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Table, MetaData, or_, func, and_, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
import re
import urllib.parse
import aiohttp  # Using aiohttp instead of requests for async
from io import BytesIO


# Timezone utility functions
def to_aware(dt):
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt

def to_naive(dt):
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:OoPOlzJfLMJpYCkXqvvfpNHDuoObQzWC@postgres.railway.internal:5432/railway")

# FIX 1: CORRECT DATABASE URL FOR RAILWAY
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Database connection
metadata = MetaData()
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)

# Product Table
data_table = Table(
    "products",
    metadata,
    Column("id", String, primary_key=True),
    Column("barcode", String, index=True),
    Column("name", String, index=True),
    Column("price", Float),
    Column("unit", String),
    Column("tags", ARRAY(String)),
    Column("thumbnail_url", String),
    Column("gallery_urls", ARRAY(String)),
    Column("quantity", Integer),
    Column("stock_visibility", String),
    Column("display_price", Boolean, default=True, server_default=sqlalchemy.sql.expression.true(), index=True),
    Column("featured", Boolean, index=True),
    Column("todays_deal", Boolean, index=True),
    Column("telegram", String),
    Column("phone", String),
    Column("social_link", String),
    Column("meta_name", String),
    Column("meta_description", String),
    Column("meta_image", String),
    Column("published", Boolean, default=True, index=True),
    Column("created_at", DateTime, index=True),
    Column("updated_at", DateTime),
    # New review columns
    Column("review_count", Integer, default=0),
    Column("average_rating", Float, default=0.0)
)

# Banner Table
banner_table = Table(
    "banners",
    metadata,
    Column("id", String, primary_key=True),
    Column("banner_url", String),
    Column("button_text", String, nullable=True),
    Column("button_url", String, nullable=True),
    Column("description", String, nullable=True),
    Column("start_end_date", ARRAY(DateTime)),
    Column("status", Boolean, default=True),
    Column("created_at", DateTime),
    Column("updated_at", DateTime)
)

# Search Log Table
search_log_table = Table(
    "search_logs",
    metadata,
    Column("id", String, primary_key=True),
    Column("query_text", String, index=True),
    Column("clicked_product_id", String, index=True, nullable=True),
    Column("searched_at", DateTime)
)

# User Location Table
user_location_table = Table(
    "user_locations",
    metadata,
    Column("id", String, primary_key=True),
    Column("user_id", String, index=True),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("timestamp", DateTime),
    Column("created_at", DateTime)
)

# Review Table
review_table = Table(
    "reviews",
    metadata,
    Column("id", String, primary_key=True),
    Column("product_id", String, ForeignKey("products.id"), index=True),
    Column("user_id", String, index=True),
    Column("rating", Integer),
    Column("comment", String),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)

app = FastAPI(
    title="Product Management API",
    description="API for managing products, banners, user locations, and reviews",
    version="1.1.1"  # Updated version
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint for Railway
@app.get("/")
async def root():
    return {"message": "Product Management API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "product-management-api"}

@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(engine)
    
    # Check and add missing columns to products table
    with engine.connect() as connection:
        # Check for display_price
        display_price_exists = connection.execute(
            sqlalchemy.text(
                "SELECT EXISTS (SELECT 1 FROM information_schema.columns "
                "WHERE table_name = 'products' AND column_name = 'display_price')"
            )
        ).scalar()
        
        if not display_price_exists:
            connection.execute(
                sqlalchemy.text(
                    "ALTER TABLE products ADD COLUMN display_price BOOLEAN DEFAULT TRUE"
                )
            )
        
        # Check for review_count
        review_count_exists = connection.execute(
            sqlalchemy.text(
                "SELECT EXISTS (SELECT 1 FROM information_schema.columns "
                "WHERE table_name = 'products' AND column_name = 'review_count')"
            )
        ).scalar()
        
        if not review_count_exists:
            connection.execute(
                sqlalchemy.text(
                    "ALTER TABLE products ADD COLUMN review_count INTEGER DEFAULT 0"
                )
            )
        
        # Check for average_rating
        avg_rating_exists = connection.execute(
            sqlalchemy.text(
                "SELECT EXISTS (SELECT 1 FROM information_schema.columns "
                "WHERE table_name = 'products' AND column_name = 'average_rating')"
            )
        ).scalar()
        
        if not avg_rating_exists:
            connection.execute(
                sqlalchemy.text(
                    "ALTER TABLE products ADD COLUMN average_rating FLOAT DEFAULT 0.0"
                )
            )
        
        connection.commit()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    barcode: str
    name: str
    price: float
    unit: str
    tags: List[str]
    thumbnail_url: HttpUrl
    gallery_urls: List[HttpUrl]
    quantity: int
    stock_visibility: str = Field(..., pattern="^(show_quantity|show_text|hide)$")
    display_price: bool = True
    featured: bool = False
    todays_deal: bool = False
    telegram: Optional[str] = None
    phone: Optional[str] = None
    social_link: Optional[str] = None
    meta_name: Optional[str] = None
    meta_description: Optional[str] = None
    meta_image: Optional[str] = None
    published: bool = True
    # New review fields
    review_count: int = 0
    average_rating: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @validator("created_at", "updated_at", pre=True, always=True)
    def ensure_timezone(cls, v):
        if v is None:
            return datetime.now(timezone.utc)
        if isinstance(v, str):
            try:
                dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                dt = datetime.now(timezone.utc)
        else:
            dt = v
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    class Config:
        json_schema_extra = {
            "example": {
                "id": "f2a4e1b2-293a-4a34-a3bb-5593c20fdf6a",
                "barcode": "1234567890123",
                "name": "Premium Coffee",
                "price": 4.5,
                "unit": "bottle",
                "tags": ["coffee", "beverage"],
                "thumbnail_url": "https://example.com/thumb.jpg",
                "gallery_urls": ["https://example.com/img1.jpg"],
                "quantity": 100,
                "stock_visibility": "show_quantity",
                "featured": True,
                "todays_deal": False,
                "telegram": "https://t.me/product123",
                "phone": "012345678",
                "social_link": "https://facebook.com/brandpage",
                "meta_name": "Premium Coffee - 100% Arabica",
                "meta_description": "Get your day started with our Premium Coffee.",
                "meta_image": "https://example.com/meta.jpg",
                "published": True,
                "review_count": 15,
                "average_rating": 4.7,
                "created_at": "2025-06-16T05:50:30.733Z",
                "updated_at": "2025-06-16T05:50:30.733Z"
            }
        }

class SearchLog(BaseModel):
    query_text: str
    clicked_product_id: Optional[str] = None

class Banner(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    banner_url: HttpUrl
    button_text: Optional[str] = None
    button_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    start_end_date: List[datetime] = Field(default_factory=list)
    status: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserLocation(BaseModel):
    user_id: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @validator("timestamp", pre=True, always=True)
    def ensure_timestamp_timezone(cls, v):
        if v is None:
            return datetime.now(timezone.utc)
        if isinstance(v, str):
            try:
                dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                dt = datetime.now(timezone.utc)
        else:
            dt = v
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "timestamp": "2025-06-20T08:29:00.000Z"
            }
        }

class UserLocationResponse(BaseModel):
    id: str
    user_id: str
    latitude: float
    longitude: float
    timestamp: datetime
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Review(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    product_id: str
    user_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @validator("created_at", "updated_at", pre=True, always=True)
    def ensure_timezone(cls, v):
        if v is None:
            return datetime.now(timezone.utc)
        if isinstance(v, str):
            try:
                dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                dt = datetime.now(timezone.utc)
        else:
            dt = v
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    class Config:
        json_schema_extra = {
            "example": {
                "id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
                "product_id": "f2a4e1b2-293a-4a34-a3bb-5593c20fdf6a",
                "user_id": "user_12345",
                "rating": 5,
                "comment": "Excellent product! Would buy again.",
                "created_at": "2025-06-20T10:30:00.000Z",
                "updated_at": "2025-06-20T10:30:00.000Z"
            }
        }

async def update_product_review_stats(product_id: str):
    # Calculate new review stats
    stats_query = sqlalchemy.select(
        func.count().label("review_count"),
        func.avg(review_table.c.rating).label("average_rating")
    ).where(review_table.c.product_id == product_id)
    
    stats = await database.fetch_one(stats_query)
    
    # Update product
    update_query = (
        data_table.update()
        .where(data_table.c.id == product_id)
        .values(
            review_count=stats["review_count"],
            average_rating=float(stats["average_rating"]) if stats["average_rating"] else 0.0
        )
    )
    await database.execute(update_query)

# API: Track User Location
@app.post("/users/location")
async def track_user_location(location: UserLocation):
    location_data = {
        "id": str(uuid4()),
        "user_id": location.user_id,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "timestamp": to_naive(to_aware(location.timestamp)),
        "created_at": to_naive(datetime.now(timezone.utc))
    }
    query = user_location_table.insert().values(**location_data)
    await database.execute(query)
    return {"message": "Location tracked successfully."}

# API: Get User Locations
@app.get("/users/location", response_model=List[UserLocationResponse])
async def get_user_locations(
        user_id: Optional[str] = Query(None, description="Filter by user ID"),
        start_date: Optional[datetime] = Query(None, description="Start date for filtering (UTC)"),
        end_date: Optional[datetime] = Query(None, description="End date for filtering (UTC)"),
        skip: int = Query(0, ge=0, description="Pagination offset"),
        limit: int = Query(100, le=1000, description="Pagination limit")
):
    query = user_location_table.select()
    if user_id:
        query = query.where(user_location_table.c.user_id == user_id)
    if start_date or end_date:
        conditions = []
        if start_date:
            start_naive = to_naive(to_aware(start_date))
            conditions.append(user_location_table.c.timestamp >= start_naive)
        if end_date:
            end_naive = to_naive(to_aware(end_date))
            conditions.append(user_location_table.c.timestamp <= end_naive)
        query = query.where(and_(*conditions))
    query = query.offset(skip).limit(limit)
    rows = await database.fetch_all(query)
    locations = []
    for row in rows:
        location = dict(row)
        location["timestamp"] = to_aware(location["timestamp"])
        location["created_at"] = to_aware(location["created_at"])
        locations.append(UserLocationResponse(**location))
    return locations

# API: Search Products
@app.get("/products/search", response_model=List[Product])
async def search_products(q: str = Query(..., min_length=1)):
    await database.execute(
        search_log_table.insert().values(
            id=str(uuid4()),
            query_text=q,
            searched_at=to_naive(datetime.now(timezone.utc))
        )
    )
    search_query = data_table.select().where(
        and_(
            data_table.c.published == True,
            or_(
                data_table.c.name.ilike(f"%{q}%"),
                func.array_to_string(data_table.c.tags, ' ').ilike(f"%{q}%")
            )
        )
    )
    rows = await database.fetch_all(search_query)
    products = []
    for row in rows:
        try:
            row_data = dict(row)
            if row_data.get("gallery_urls"):
                fixed_urls = []
                for url in row_data["gallery_urls"]:
                    try:
                        HttpUrl(url)
                        fixed_urls.append(url)
                    except:
                        fixed_urls.append(fix_invalid_url(url))
                row_data["gallery_urls"] = fixed_urls
            if row_data.get("thumbnail_url"):
                try:
                    HttpUrl(row_data["thumbnail_url"])
                except:
                    row_data["thumbnail_url"] = fix_invalid_url(row_data["thumbnail_url"])
            products.append(Product(**row_data))
        except Exception as e:
            print(f"Error processing product {row['id']}: {str(e)}")
            continue
    return products

# FIXED API: Search Products by Image with optimized matching
@app.post("/products/search-by-image", response_model=List[Product])
async def search_products_by_image(file: UploadFile = File(...)):
    try:
        import imagehash
        from PIL import Image as PILImage
        from PIL import UnidentifiedImageError
    except ImportError as e:
        print(f"CRITICAL: Required libraries missing - {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Image processing libraries not installed. Install with: pip install pillow imagehash"
        )
    
    # Read uploaded image
    try:
        contents = await file.read()
        if not contents:
            return []
            
        image_stream = BytesIO(contents)
        try:
            uploaded_image = PILImage.open(image_stream)
            # Convert to RGB and resize for consistent processing
            if uploaded_image.mode != 'RGB':
                uploaded_image = uploaded_image.convert('RGB')
                
            # Resize to standard size for better matching
            uploaded_image = uploaded_image.resize((300, 300))
        except UnidentifiedImageError:
            return []
        
        # Generate hash for uploaded image
        uploaded_hash = imagehash.phash(uploaded_image)
        print(f"DEBUG: Uploaded image hash: {uploaded_hash}")
    except Exception as e:
        print(f"ERROR: Failed to process uploaded image - {str(e)}")
        return []

    # Get all products with thumbnails
    query = data_table.select().where(data_table.c.thumbnail_url != None)
    rows = await database.fetch_all(query)
    
    if not rows:
        return []
    
    similar_products = []
    threshold = int(os.getenv("IMAGE_HASH_THRESHOLD", 30))  # Increased default threshold
    
    print(f"Comparing against {len(rows)} products with threshold {threshold}")
    
    # Use a single HTTP session for all requests
    async with aiohttp.ClientSession() as session:
        for row in rows:
            try:
                product = dict(row)
                thumbnail_url = fix_invalid_url(product.get("thumbnail_url"))
                
                if not thumbnail_url:
                    continue
                    
                # Fetch product image
                try:
                    async with session.get(thumbnail_url, timeout=10) as response:
                        if response.status != 200:
                            continue
                            
                        img_data = await response.read()
                        if not img_data:
                            continue
                            
                        try:
                            imported_image = PILImage.open(BytesIO(img_data))
                            # Preprocess product image
                            if imported_image.mode != 'RGB':
                                imported_image = imported_image.convert('RGB')
                            imported_image = imported_image.resize((300, 300))
                        except UnidentifiedImageError:
                            continue
                            
                        imported_hash = imagehash.phash(imported_image)
                        distance = abs(uploaded_hash - imported_hash)
                        
                        # Add all products within threshold
                        if distance <= threshold:
                            print(f"Match found! Product: {product['name']} (ID: {product['id']}), Distance: {distance}")
                            similar_products.append({
                                "product": Product(**product),
                                "distance": distance
                            })
                except Exception as e:
                    continue
            except Exception as e:
                continue
    
    # Sort by distance (lowest distance = best match)
    similar_products.sort(key=lambda x: x["distance"])
    
    # Log final matches
    print(f"Found {len(similar_products)} similar products within threshold")
    
    # Return top 10 matches or all if less than 10
    max_results = min(10, len(similar_products))
    return [item["product"] for item in similar_products[:max_results]]

# # FIXED API: Search Products by Image with enhanced logging
# @app.post("/products/search-by-image", response_model=List[Product])
# async def search_products_by_image(file: UploadFile = File(...)):
#     # Check if required libraries are installed
#     try:
#         import imagehash
#         from PIL import Image as PILImage
#         from PIL import UnidentifiedImageError
#     except ImportError as e:
#         print(f"Missing required libraries: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail="Image processing libraries not installed. Install with: pip install pillow imagehash"
#         )

#     # Read and validate uploaded image
#     try:
#         contents = await file.read()
#         if not contents:
#             raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
#         image_stream = BytesIO(contents)
#         try:
#             uploaded_image = PILImage.open(image_stream)
#             # Convert to RGB if necessary
#             if uploaded_image.mode != 'RGB':
#                 uploaded_image = uploaded_image.convert('RGB')
#         except UnidentifiedImageError:
#             raise HTTPException(status_code=400, detail="Unsupported image format")
        
#         uploaded_hash = imagehash.phash(uploaded_image)
#         print(f"Uploaded image hash: {uploaded_hash}")
#     except Exception as e:
#         print(f"Error processing uploaded image: {str(e)}")
#         raise HTTPException(
#             status_code=400,
#             detail=f"Error processing uploaded image: {str(e)}"
#         )

#     # Get all products with thumbnails
#     query = data_table.select().where(data_table.c.thumbnail_url != None)
#     rows = await database.fetch_all(query)
    
#     similar_products = []
#     threshold = int(os.getenv("IMAGE_HASH_THRESHOLD", 15))  # Configurable threshold
    
#     print(f"Comparing against {len(rows)} products with threshold {threshold}")
    
#     # Use a single HTTP session for all requests
#     async with aiohttp.ClientSession() as session:
#         for i, row in enumerate(rows):
#             product = dict(row)
#             thumbnail_url = fix_invalid_url(product.get("thumbnail_url"))
            
#             if not thumbnail_url:
#                 print(f"Skipping product {product['id']} - no thumbnail URL")
#                 continue
                
#             try:
#                 # Fetch product image
#                 async with session.get(thumbnail_url, timeout=10) as response:
#                     if response.status != 200:
#                         print(f"Failed to fetch {thumbnail_url}: HTTP {response.status}")
#                         continue
                        
#                     img_data = await response.read()
#                     if not img_data:
#                         print(f"Empty image data for {thumbnail_url}")
#                         continue
                        
#                     try:
#                         imported_image = PILImage.open(BytesIO(img_data))
#                         # Convert to RGB if necessary
#                         if imported_image.mode != 'RGB':
#                             imported_image = imported_image.convert('RGB')
#                     except UnidentifiedImageError:
#                         print(f"Unsupported image format for {thumbnail_url}")
#                         continue
                        
#                     imported_hash = imagehash.phash(imported_image)
#                     distance = abs(uploaded_hash - imported_hash)
                    
#                     print(f"Product {product['id']} - Distance: {distance}, Hash: {imported_hash}")
                    
#                     if distance <= threshold:
#                         print(f"Match found! Product: {product['name']} (ID: {product['id']}), Distance: {distance}")
#                         similar_products.append(Product(**product))
#             except Exception as e:
#                 print(f"Error processing product {product['id']}: {str(e)}")
    
#     print(f"Found {len(similar_products)} similar products")
#     return similar_products

# API: List Products
@app.get("/products", response_model=List[Product])
async def list_products(
        published_only: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
):
    query = data_table.select()
    if published_only is True:
        query = query.where(data_table.c.published == True)
    elif published_only is False:
        query = query.where(data_table.c.published == False)
    query = query.offset(skip).limit(limit)
    rows = await database.fetch_all(query)
    products = []
    for row in rows:
        try:
            row_data = dict(row)
            if row_data.get("gallery_urls"):
                fixed_urls = []
                for url in row_data["gallery_urls"]:
                    try:
                        HttpUrl(url)
                        fixed_urls.append(url)
                    except:
                        fixed_urls.append(fix_invalid_url(url))
                row_data["gallery_urls"] = fixed_urls
            if row_data.get("thumbnail_url"):
                try:
                    HttpUrl(row_data["thumbnail_url"])
                except:
                    row_data["thumbnail_url"] = fix_invalid_url(row_data["thumbnail_url"])
            products.append(Product(**row_data))
        except Exception as e:
            print(f"Error processing product {row['id']}: {str(e)}")
            continue
    return products

def fix_invalid_url(url):
    if url.startswith("%20") or url.startswith("/"):
        base = "https://www.dahoughengenterprise.com"
        return urllib.parse.urljoin(base, url.lstrip("/"))
    if " " in url:
        return url.replace(" ", "%20")
    if not url.startswith("http"):
        return f"https://{url}"
    return url

# API: Create Product
@app.post("/products", response_model=Product)
async def create_product(product: Product):
    product_dict = product.dict()
    product_dict["id"] = str(uuid4())
    if not product_dict.get("meta_name"):
        product_dict["meta_name"] = f"Buy {product_dict['name']} Online"
    if not product_dict.get("meta_description"):
        product_dict["meta_description"] = (
            f"Order {product_dict['name']} now for just ${product_dict['price']:.2f}. Fast delivery."
        )
    if not product_dict.get("meta_image"):
        product_dict["meta_image"] = str(product_dict["thumbnail_url"])
    product_dict["created_at"] = to_naive(to_aware(product.created_at))
    product_dict["updated_at"] = to_naive(to_aware(product.updated_at))
    product_dict["thumbnail_url"] = str(product_dict["thumbnail_url"])
    product_dict["gallery_urls"] = [str(u) for u in product_dict["gallery_urls"]]
    query = data_table.insert().values(**product_dict)
    await database.execute(query)
    return product

# API: Get Product by ID
@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    query = data_table.select().where(data_table.c.id == product_id)
    row = await database.fetch_one(query)
    if row is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    return Product(**dict(row))

# API: Update Product
@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, updated: Product):
    query = data_table.select().where(data_table.c.id == product_id)
    row = await database.fetch_one(query)
    if row is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    updated_dict = updated.dict()
    if not updated_dict.get("meta_name"):
        updated_dict["meta_name"] = f"Buy {updated_dict['name']} Online"
    if not updated_dict.get("meta_description"):
        updated_dict[
            "meta_description"] = f"Order {updated_dict['name']} now for just ${updated_dict['price']:.2f}. Fast delivery."
    if not updated_dict.get("meta_image"):
        updated_dict["meta_image"] = str(updated_dict["thumbnail_url"])
    updated_dict["updated_at"] = to_naive(datetime.now(timezone.utc))
    updated_dict["created_at"] = to_naive(to_aware(row["created_at"]))
    updated_dict["thumbnail_url"] = str(updated_dict["thumbnail_url"])
    updated_dict["gallery_urls"] = [str(url) for url in updated_dict["gallery_urls"]]
    update_query = data_table.update().where(data_table.c.id == product_id).values(**updated_dict)
    await database.execute(update_query)
    return updated

# API: Delete Product
@app.delete("/products/{product_id}")
async def delete_product(product_id: str):
    query = data_table.select().where(data_table.c.id == product_id)
    row = await database.fetch_one(query)
    if row is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    # Delete associated reviews first
    await database.execute(review_table.delete().where(review_table.c.product_id == product_id))
    # Then delete the product
    delete_query = data_table.delete().where(data_table.c.id == product_id)
    await database.execute(delete_query)
    return {"message": "Product and its reviews deleted successfully."}

# API: Delete Products by Name
@app.delete("/products/delete/by-name")
async def delete_products_by_name(name: str):
    # Find products to delete
    query = data_table.select().where(data_table.c.name.ilike(f"%{name}%"))
    products = await database.fetch_all(query)
    # Delete reviews for these products
    for product in products:
        await database.execute(
            review_table.delete().where(review_table.c.product_id == product["id"])
        )
    # Delete products
    delete_query = data_table.delete().where(data_table.c.name.ilike(f"%{name}%"))
    result = await database.execute(delete_query)
    return {"message": f"Deleted {result} products and their reviews with name like: {name}"}

# API: Log Search Click
@app.post("/products/search/click")
async def log_search_click(log: SearchLog):
    log_query = search_log_table.insert().values(
        id=str(uuid4()),
        query_text=log.query_text,
        clicked_product_id=log.clicked_product_id,
        searched_at=to_naive(datetime.now(timezone.utc))
    )
    await database.execute(log_query)
    return {"message": "Search click logged."}

# API: Get Search Suggestions
@app.get("/products/search/suggestions", response_model=List[str])
async def suggest_search_keywords(q: Optional[str] = Query(None), limit: int = 10):
    if not q:
        return []
    query = (
        sqlalchemy.select(search_log_table.c.query_text, func.count().label("count"))
        .group_by(search_log_table.c.query_text)
        .order_by(func.count().desc())
        .limit(limit)
    )
    rows = await database.fetch_all(query)
    return [row["query_text"] for row in rows if q.upper() in row["query_text"].upper()][:limit]

# API: Get Trending Search Keywords
@app.get("/products/search/trending", response_model=List[str])
async def trending_search_keywords(limit: int = 10):
    query = (
        sqlalchemy.select(search_log_table.c.query_text, func.count().label("count"))
        .group_by(search_log_table.c.query_text)
        .order_by(func.count().desc())
        .limit(limit)
    )
    rows = await database.fetch_all(query)
    return [row["query_text"] for row in rows]

# API: Import Products
@app.post("/products/import")
async def import_products_excel(file: UploadFile = File(...)):
    contents = await file.read()
    file_stream = io.BytesIO(contents)
    try:
        xls = pd.ExcelFile(file_stream)
        df = None
        for sheet_name in xls.sheet_names:
            sheet_df = pd.read_excel(xls, sheet_name)
            if 'Barcode' in sheet_df.columns:
                df = sheet_df
                break
        if df is None:
            raise HTTPException(status_code=400, detail="No valid product data sheet found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    imported = 0
    skipped = 0
    errors = []
    for idx, row in df.iterrows():
        try:
            row = row.where(pd.notnull(row), None)
            row_index = idx + 2
            product_dict = {
                "id": str(uuid4()),
                "barcode": str(row.get("Barcode", "")).strip(),
                "name": row.get("Name", ""),
                "price": float(row.get("Price", 0)),
                "unit": row.get("Unit", ""),
                "tags": row.get("Tags", "").split(",") if row.get("Tags") else [],
                "thumbnail_url": fix_invalid_url(row.get("Thumbnail URL", "")),
                "gallery_urls": [fix_invalid_url(row.get("Gallery URLs", ""))] if row.get("Gallery URLs") else [],
                "quantity": int(row.get("Quantity", 0)),
                "stock_visibility": row.get("Stock Visibility", "show_quantity"),
                "display_price": bool(row.get("Display Price", True)),
                "featured": bool(row.get("Featured", False)),
                "todays_deal": bool(row.get("Today's Deal", False)),
                "telegram": str(row.get("Telegram", "")).strip(),
                "phone": str(row.get("Phone", "")).strip(),
                "social_link": str(row.get("Social Link", "")).strip(),
                "meta_name": row.get("Meta Name") or f"Buy {row.get('Name')} Online",
                "meta_description": row.get(
                    "Meta Description") or f"Order {row.get('Name')} now for just ${row.get('Price')}. Fast delivery.",
                "meta_image": row.get("Meta Image") or row.get("Thumbnail URL", ""),
                "published": str(row.get("Published", "true")).strip().lower() in ["true", "1", "yes"],
                "review_count": 0,
                "average_rating": 0.0,
                "created_at": to_naive(datetime.now(timezone.utc)),
                "updated_at": to_naive(datetime.now(timezone.utc))
            }
            product_obj = Product(**product_dict)
            product_for_db = product_obj.dict()
            product_for_db["created_at"] = to_naive(product_for_db["created_at"])
            product_for_db["updated_at"] = to_naive(product_for_db["updated_at"])
            query = data_table.insert().values(**product_for_db)
            await database.execute(query)
            imported += 1
        except ValidationError as e:
            error_msg = f"Row {row_index}: Validation error - {str(e)}"
            print(error_msg)
            errors.append(error_msg)
            skipped += 1
        except Exception as e:
            error_msg = f"Row {row_index}: Other error - {str(e)}"
            print(error_msg)
            errors.append(error_msg)
            skipped += 1
    response = {"message": f"Imported {imported} products.", "skipped": skipped}
    if errors:
        response["errors"] = errors[:10]
    return response

@app.post("/products/fix-all")
async def fix_all_products():
    query = data_table.select()
    rows = await database.fetch_all(query)
    fixed_count = 0
    errors = []
    for row in rows:
        try:
            product = dict(row)
            needs_update = False
            if product.get("thumbnail_url"):
                try:
                    HttpUrl(product["thumbnail_url"])
                except:
                    fixed_url = fix_invalid_url(product["thumbnail_url"])
                    if fixed_url != product["thumbnail_url"]:
                        product["thumbnail_url"] = fixed_url
                        needs_update = True
            if product.get("gallery_urls"):
                fixed_urls = []
                changed = False
                for url in product["gallery_urls"]:
                    try:
                        HttpUrl(url)
                        fixed_urls.append(url)
                    except:
                        fixed_url = fix_invalid_url(url)
                        fixed_urls.append(fixed_url)
                        changed = True
                if changed:
                    product["gallery_urls"] = fixed_urls
                    needs_update = True
            if product.get("meta_image"):
                try:
                    HttpUrl(product["meta_image"])
                except:
                    fixed_url = fix_invalid_url(product["meta_image"])
                    if fixed_url != product["meta_image"]:
                        product["meta_image"] = fixed_url
                        needs_update = True
            if needs_update:
                update_query = (
                    data_table.update()
                    .where(data_table.c.id == product["id"])
                    .values(
                        thumbnail_url=product["thumbnail_url"],
                        gallery_urls=product["gallery_urls"],
                        meta_image=product.get("meta_image", "")
                    )
                )
                await database.execute(update_query)
                fixed_count += 1
        except Exception as e:
            errors.append(f"Product {product.get('id')}: {str(e)}")
    return {
        "message": f"Fixed URLs for {fixed_count} products",
        "errors": errors
    }

@app.post("/products/fix-gallery-urls")
async def fix_invalid_gallery_urls():
    query = data_table.select()
    rows = await database.fetch_all(query)
    fixed_count = 0
    errors = []
    for row in rows:
        try:
            product = dict(row)
            gallery_urls = product["gallery_urls"]
            if not gallery_urls:
                continue
            parsed_urls = gallery_urls if isinstance(gallery_urls, list) else [gallery_urls]
            valid_urls = []
            for url in parsed_urls:
                try:
                    HttpUrl(url)
                    valid_urls.append(url)
                except:
                    if url.startswith("http") and " " in url:
                        valid_urls.append(url.replace(" ", "%20"))
                    else:
                        valid_urls.append(url)
            if parsed_urls != gallery_urls:
                update_query = (
                    data_table.update()
                    .where(data_table.c.id == product["id"])
                    .values(gallery_urls=valid_urls)
                )
                await database.execute(update_query)
                fixed_count += 1
        except Exception as e:
            errors.append(f"Product {product.get('id')}: {str(e)}")
    return {
        "message": f"Fixed gallery URLs for {fixed_count} products",
        "errors": errors
    }

# API: Create Banner
@app.post("/banners", response_model=Banner)
async def create_banner(banner: Banner):
    banner_data = banner.dict()
    banner_data["banner_url"] = str(banner.banner_url)
    if banner.button_url:
        banner_data["button_url"] = str(banner.button_url)
    if banner_data.get("start_end_date"):
        banner_data["start_end_date"] = [to_naive(dt) for dt in banner_data["start_end_date"]]
    banner_data["created_at"] = to_naive(banner.created_at)
    banner_data["updated_at"] = to_naive(banner.updated_at)
    query = banner_table.insert().values(**banner_data)
    await database.execute(query)
    return banner

# API: List Banners
@app.get("/banners", response_model=List[Banner])
async def list_banners():
    query = banner_table.select()
    rows = await database.fetch_all(query)
    return [Banner(**dict(row)) for row in rows]

# API: Update Banner
@app.put("/banners/{banner_id}", response_model=Banner)
async def update_banner(banner_id: str, banner: Banner):
    query = banner_table.select().where(banner_table.c.id == banner_id)
    row = await database.fetch_one(query)
    if row is None:
        raise HTTPException(status_code=404, detail="Banner not found.")
    updated_data = banner.dict()
    updated_data["banner_url"] = str(banner.banner_url)
    if banner.button_url:
        updated_data["button_url"] = str(banner.button_url)
    if updated_data.get("start_end_date"):
        updated_data["start_end_date"] = [to_naive(dt) for dt in updated_data["start_end_date"]]
    updated_data["created_at"] = row["created_at"]
    updated_data["updated_at"] = to_naive(datetime.now(timezone.utc))
    update_query = banner_table.update().where(banner_table.c.id == banner_id).values(**updated_data)
    await database.execute(update_query)
    return banner

# Debug Endpoint
@app.get("/products/debug")
async def debug_products():
    query = data_table.select()
    rows = await database.fetch_all(query)
    return {"total_products": len(rows), "sample": [dict(row) for row in rows[:5]]}

# ========== REVIEW ENDPOINTS ========== #

@app.post("/products/{product_id}/reviews", response_model=Review)
async def create_review(product_id: str, review: Review):
    # Verify product exists
    product_query = data_table.select().where(data_table.c.id == product_id)
    product = await database.fetch_one(product_query)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Prepare review data
    review_data = review.dict()
    review_data["id"] = str(uuid4())
    review_data["product_id"] = product_id
    review_data["created_at"] = to_naive(review.created_at)
    review_data["updated_at"] = to_naive(review.updated_at)
    
    # Insert review
    query = review_table.insert().values(**review_data)
    await database.execute(query)
    
    # Update product review stats
    await update_product_review_stats(product_id)
    
    return review

@app.get("/products/{product_id}/reviews", response_model=List[Review])
async def get_product_reviews(
    product_id: str,
    min_rating: Optional[int] = Query(None, ge=1, le=5),
    max_rating: Optional[int] = Query(None, ge=1, le=5),
    sort_by: Optional[str] = Query("newest", description="Sort by: newest, oldest, highest, lowest"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    # Verify product exists
    product_query = data_table.select().where(data_table.c.id == product_id)
    product = await database.fetch_one(product_query)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Build query
    query = review_table.select().where(review_table.c.product_id == product_id)
    
    # Apply rating filters
    if min_rating:
        query = query.where(review_table.c.rating >= min_rating)
    if max_rating:
        query = query.where(review_table.c.rating <= max_rating)
    
    # Apply sorting
    if sort_by == "newest":
        query = query.order_by(review_table.c.created_at.desc())
    elif sort_by == "oldest":
        query = query.order_by(review_table.c.created_at.asc())
    elif sort_by == "highest":
        query = query.order_by(review_table.c.rating.desc())
    elif sort_by == "lowest":
        query = query.order_by(review_table.c.rating.asc())
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    rows = await database.fetch_all(query)
    return [Review(**dict(row)) for row in rows]

@app.get("/reviews", response_model=List[Review])
async def get_all_reviews(
    product_id: Optional[str] = None,
    user_id: Optional[str] = None,
    min_rating: Optional[int] = Query(None, ge=1, le=5),
    max_rating: Optional[int] = Query(None, ge=1, le=5),
    sort_by: Optional[str] = Query("newest", description="Sort by: newest, oldest, highest, lowest"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    query = review_table.select()
    
    # Apply filters
    if product_id:
        query = query.where(review_table.c.product_id == product_id)
    if user_id:
        query = query.where(review_table.c.user_id == user_id)
    if min_rating:
        query = query.where(review_table.c.rating >= min_rating)
    if max_rating:
        query = query.where(review_table.c.rating <= max_rating)
    
    # Apply sorting
    if sort_by == "newest":
        query = query.order_by(review_table.c.created_at.desc())
    elif sort_by == "oldest":
        query = query.order_by(review_table.c.created_at.asc())
    elif sort_by == "highest":
        query = query.order_by(review_table.c.rating.desc())
    elif sort_by == "lowest":
        query = query.order_by(review_table.c.rating.asc())
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    rows = await database.fetch_all(query)
    return [Review(**dict(row)) for row in rows]

@app.get("/reviews/{review_id}", response_model=Review)
async def get_review(review_id: str):
    query = review_table.select().where(review_table.c.id == review_id)
    row = await database.fetch_one(query)
    if not row:
        raise HTTPException(status_code=404, detail="Review not found")
    return Review(**dict(row))

@app.put("/reviews/{review_id}", response_model=Review)
async def update_review(review_id: str, updated_review: Review):
    # Get existing review
    query = review_table.select().where(review_table.c.id == review_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Prepare update data
    update_data = updated_review.dict()
    update_data["updated_at"] = to_naive(datetime.now(timezone.utc))
    update_data["created_at"] = existing["created_at"]  # Preserve original creation time
    
    # Update review
    update_query = (
        review_table.update()
        .where(review_table.c.id == review_id)
        .values(**update_data)
    )
    await database.execute(update_query)
    
    # Update product stats
    await update_product_review_stats(existing["product_id"])
    
    return updated_review

@app.delete("/reviews/{review_id}")
async def delete_review(review_id: str):
    # Get review to get product ID
    query = review_table.select().where(review_table.c.id == review_id)
    review = await database.fetch_one(query)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Delete the review
    await database.execute(review_table.delete().where(review_table.c.id == review_id))
    
    # Update product stats
    await update_product_review_stats(review["product_id"])
    
    return {"message": "Review deleted successfully"}
