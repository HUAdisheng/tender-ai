import sys
sys.path.insert(0, r'd:\clone\tender-ai')
import importlib
modules = [
    'app.common.security',
    'app.api.v1.files',
    'app.storage.rustfs',
    'app.services.file_service',
    'app.main',
]
for m in modules:
    importlib.import_module(m)
print('IMPORT_OK')
