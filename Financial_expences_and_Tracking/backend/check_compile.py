import py_compile, glob, os, sys

# Resolve project paths
_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_BACKEND_DIR, '..'))

# Collect all Python files from frontend and backend
files = (
    glob.glob(os.path.join(_PROJECT_ROOT, 'frontend', '*.py'))
    + glob.glob(os.path.join(_BACKEND_DIR, '*.py'))
    + glob.glob(os.path.join(_BACKEND_DIR, 'services', '*.py'))
    + glob.glob(os.path.join(_BACKEND_DIR, 'db', '*.py'))
    + glob.glob(os.path.join(_BACKEND_DIR, 'tests', '*.py'))
)
for f in files:
    py_compile.compile(f, doraise=True)
print('py_compile OK')
