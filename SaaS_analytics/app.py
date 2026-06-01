# app.py
"""
SaaS Executive Analytics
Project Root Entrypoint Wrapper.
Delegates execution to frontend/app.py to preserve standard launch commands.
"""

import sys
import os
import runpy

# Dynamic path resolution: Add project root, frontend, and backend folders to search paths
project_root = os.path.dirname(os.path.abspath(__file__))
for path in [project_root, os.path.join(project_root, "frontend"), os.path.join(project_root, "backend")]:
    if path not in sys.path:
        sys.path.append(path)

# Resolve and run the frontend entrypoint script dynamically
frontend_app_path = os.path.join(project_root, "frontend", "app.py")
with open(frontend_app_path, "r", encoding="utf-8") as f:
    code = compile(f.read(), frontend_app_path, 'exec')
    exec(code, globals())

