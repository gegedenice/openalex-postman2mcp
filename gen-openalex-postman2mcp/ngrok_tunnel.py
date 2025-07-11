
import ngrok
import os
import time
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("NGROK_AUTHTOKEN"):
    raise ValueError("NGROK_AUTHTOKEN is not set in the environment variables.")

listener = ngrok.forward(3333, authtoken=os.getenv("NGROK_AUTHTOKEN"), subdomain="mcp")
# Output ngrok url to console
print(f"Ingress established at {listener.url()}")
# Keep the listener alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing listener")
