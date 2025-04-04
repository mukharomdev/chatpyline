# my_package/validation.py
import importlib
import sys

def validate_exports(package_name: str):
    """Memvalidasi semua ekspor dalam package"""
    package = importlib.import_module(package_name)
    
    if not hasattr(package, '__all__'):
        print(f"⚠️ {package_name} tidak memiliki __all__")
        return False
    
    errors = []
    for export in package.__all__:
        try:
            getattr(package, export)
        except AttributeError:
            errors.append(export)
    
    if errors:
        print(f"❌ Ekspor tidak valid di {package_name}: {errors}")
        return False
    
    print(f"✅ Semua ekspor di {package_name} valid")
    return True

if __name__ == '__main__':
    sys.exit(0 if validate_exports('app') else 1)