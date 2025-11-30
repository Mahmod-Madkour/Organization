"""
Standalone script to run Django server in a separate thread.
Uses external DB and static path from settings for safe updates.
"""

import threading
from wsgiref.simple_server import make_server
import os
import sys

# Add project base to Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Organization.settings")

import django
from django.core.wsgi import get_wsgi_application

# Initialize Django
django.setup()

# Server host and port
HOST = "127.0.0.1"
PORT = 8000

def run_django():
    """Run Django WSGI application in simple HTTP server."""
    application = get_wsgi_application()
    httpd = make_server(HOST, PORT, application)
    print(f"Running Django on http://{HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    # Run Django in a background thread
    t = threading.Thread(target=run_django)
    t.daemon = True
    t.start()

    # Keep main thread alive until user presses ENTER
    input("Press ENTER to stop...\n")
