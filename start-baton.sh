#!/bin/bash
cd baton/static/baton/app || exit
# Start servers in background and open browser after brief delay
(npm run dev:all &) && sleep 5 && xdg-open http://localhost:8000/admin || open http://localhost:8000/admin

# Keep script running
wait
