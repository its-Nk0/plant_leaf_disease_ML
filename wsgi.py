"""
WSGI entry point for production deployment
Used by gunicorn, uwsgi, or other WSGI servers
"""
from app import app

if __name__ == "__main__":
    app.run()
