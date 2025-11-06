"""Test premium GUI"""
import sys
import traceback

try:
    from gui_premium import WebPConverterPremiumGUI
    print("Import successful!")
    app = WebPConverterPremiumGUI()
    print("App created successfully!")
    app.run()
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
