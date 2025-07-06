#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add project directory to Python path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

# Set environment variables
os.environ.setdefault('ENVIRONMENT', 'production')
os.environ.setdefault('DEBUG', 'false')

# Database URL setup (you can update it later if needed)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./product_management.db')
os.environ['DATABASE_URL'] = DATABASE_URL

# Thread optimization
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'

# 🚀 Import FastAPI app directly
from product_management import app as application