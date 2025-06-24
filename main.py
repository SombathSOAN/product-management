#!/usr/bin/env python3
"""
Main entry point for the FastAPI application.
Direct import to avoid Railway auto-detection issues.
"""

# Direct import from product_management module
from product_management import app

# Export app for uvicorn
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)