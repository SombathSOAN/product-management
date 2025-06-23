from datetime import datetime
from typing import Optional, List
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Table, Column, String, DateTime, MetaData

# Assume database and metadata objects are already initialized elsewhere
from database import database  # adjust import as needed

# Ensure DATABASE_URL is defined for engine creation
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/product_db")

metadata = MetaData()

branch_table = Table(
    "branches",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String),
    Column("image_url", String),
    Column("lat_long", String),
    Column("location_name", String),
    Column("phone_number", String),
    Column("email", String),
    Column("telegram_link", String),
    Column("description", String),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
)

class Branch(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    image_url: Optional[str] = None
    lat_long: Optional[str] = None
    location_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    telegram_link: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

router = APIRouter()

@router.post("/branches", response_model=Branch)
async def create_branch(branch: Branch):
    query = branch_table.insert().values(**branch.dict())
    await database.execute(query)
    return branch

@router.put("/branches/{branch_id}", response_model=Branch)
async def update_branch(branch_id: str, updated: Branch):
    query = branch_table.select().where(branch_table.c.id == branch_id)
    row = await database.fetch_one(query)
    if row is None:
        raise HTTPException(status_code=404, detail="Branch not found.")

    updated_data = updated.dict()
    updated_data["created_at"] = row["created_at"]
    updated_data["updated_at"] = datetime.utcnow()

    update_query = branch_table.update().where(branch_table.c.id == branch_id).values(**updated_data)
    await database.execute(update_query)
    return updated

@router.get("/branches", response_model=List[Branch])
async def list_branches():
    query = branch_table.select()
    rows = await database.fetch_all(query)
    return [Branch(**dict(row)) for row in rows]

@router.get("/branches/{branch_id}", response_model=Branch)
async def get_branch(branch_id: str):
    query = branch_table.select().where(branch_table.c.id == branch_id)
    row = await database.fetch_one(query)
    if row is None:
        raise HTTPException(status_code=404, detail="Branch not found.")
    return Branch(**dict(row))

@router.delete("/branches/{branch_id}")
async def delete_branch(branch_id: str):
    query = branch_table.select().where(branch_table.c.id == branch_id)
    row = await database.fetch_one(query)
    if row is None:
        raise HTTPException(status_code=404, detail="Branch not found.")
    delete_query = branch_table.delete().where(branch_table.c.id == branch_id)
    await database.execute(delete_query)
    return {"message": "Branch deleted successfully."}