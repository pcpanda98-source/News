#!/bin/bash
echo "Starting News App..."
exec gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --log-level info
