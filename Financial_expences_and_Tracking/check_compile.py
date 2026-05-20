import py_compile, glob
files = glob.glob('*.py') + glob.glob('services/*.py') + glob.glob('db/*.py') + glob.glob('tests/*.py')
for f in files:
    py_compile.compile(f, doraise=True)
print('py_compile OK')
