#web: gunicorn main:app  --preload --timeout 10
web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}