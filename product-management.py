from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Tuple
from uuid import uuid4
from datetime import datetime
import os
from dotenv import load_dotenv
import databases
import sqlalchemy
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Table, MetaData, or_, func
from sqlalchemy.dialects.postgresql import ARRAY

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/product_db")

# Database connection
metadata = MetaData()
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)

# Product Table
data_table = Table(
    "products",
    metadata,
    Column("id", String, primary_key=True),
    Column("barcode", String),
    Column("name", String),
    Column("price", Float),
    Column("unit", String),
    Column("tags", ARRAY(String)),
    Column("thumbnail_url", String),
    Column("gallery_urls", ARRAY(String)),
    Column("quantity", Integer),
    Column("stock_visibility", String),
    Column("featured", Boolean),
    Column("todays_deal", Boolean),
    Column("telegram", String),
    Column("phone", String),
    Column("social_link", String),
    Column("created_at", DateTime),
    Column("updated_at", DateTime)
)

# Search Log Table
search_log_table = Table(
    "search_logs",
    metadata,
    Column("id", String, primary_key=True),
    Column("query_text", String),
    Column("searched_at", DateTime),
    Column("clicked_product_id", String, nullable=True)
)

# Banner Table
banner_table = Table(
    "banners",
    metadata,
    Column("id", String, primary_key=True),
    Column("banner_url", String),
    Column("button_text", String),
    Column("button_url", String),
    Column("description", String),
    Column("start_end_date", ARRAY(DateTime)),
    Column("status", Boolean),
    Column("created_at", DateTime),
    Column("updated_at", DateTime)
)

metadata.create_all(engine)

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Pydantic Model
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
    featured: bool = False
    todays_deal: bool = False
    telegram: Optional[str] = None
    phone: Optional[str] = None
    social_link: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# API: Search Product with Logging (must appear before /{product_id})
@app.get("/products/search", response_model=List[Product])
async def search_products(q: str = Query(..., min_length=1)):
    await database.execute(
        search_log_table.insert().values(
            id=str(uuid4()),
            query_text=q,
            searched_at=datetime.utcnow()
        )
    )

    search_query = data_table.select().where(
        or_(
            data_table.c.name.ilike(f"%{q}%"),
            func.array_to_string(data_table.c.tags, ' ').ilike(f"%{q}%")
        )
    )
    rows = await database.fetch_all(search_query)
    return [Product(**dict(row)) for row in rows]

# API: List Products
@app.get("/products", response_model=List[Product])
async def list_products():
    query = data_table.select()
    rows = await database.fetch_all(query)
    return [Product(**dict(row)) for row in rows]

# API: Create Product
@app.post("/products", response_model=Product)
async def create_product(product: Product):
    product_dict = product.dict()
    insert_data = {
        **product_dict,
        "thumbnail_url": str(product_dict["thumbnail_url"]),
        "gallery_urls": [str(url) for url in product_dict["gallery_urls"]]
    }
    query = data_table.insert().values(**insert_data)
    await database.execute(query)
    return product

# API: Create Banner
@app.post("/banners", response_model=Banner)
async def create_banner(banner: Banner):
    banner_data = banner.dict()
    banner_data["banner_url"] = str(banner.banner_url)
    if banner.button_url:
        banner_data["button_url"] = str(banner.button_url)
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
    updated_data["updated_at"] = datetime.utcnow()
    updated_data["created_at"] = row["created_at"]
    updated_data["banner_url"] = str(banner.banner_url)
    if banner.button_url:
        updated_data["button_url"] = str(banner.button_url)

    update_query = banner_table.update().where(banner_table.c.id == banner_id).values(**updated_data)
    await database.execute(update_query)
    return banner

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
    updated_dict["updated_at"] = datetime.utcnow()
    updated_dict["created_at"] = row["created_at"]
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
    delete_query = data_table.delete().where(data_table.c.id == product_id)
    await database.execute(delete_query)
    return {"message": "Product deleted successfully."}

# API: Log Search Click
@app.post("/products/search/click")
async def log_search_click(log: SearchLog):
    log_query = search_log_table.insert().values(
        id=str(uuid4()),
        query_text=log.query_text,
        clicked_product_id=log.clicked_product_id,
        searched_at=datetime.utcnow()
    )
    await database.execute(log_query)
    return {"message": "Search click logged."}

# API: Log Raw Search Query Only
@app.post("/products/search/log")
async def log_search_text_only(log: SearchLog):
    log_query = search_log_table.insert().values(
        id=str(uuid4()),
        query_text=log.query_text,
        clicked_product_id=None,
        searched_at=datetime.utcnow()
    )
    await database.execute(log_query)
    return {"message": "Search query logged."}
