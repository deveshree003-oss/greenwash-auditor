from backend.core import llm
from backend.core.config import GROQ_API_KEY
import requests, json

print('groq_client present:', llm.groq_client is not None)
print('Configured GROQ_MODEL:', llm.GROQ_MODEL)

url = 'https://api.groq.com/v1/models'
headers = {'Authorization': f'Bearer {GROQ_API_KEY}', 'Content-Type': 'application/json'}
try:
    r = requests.get(url, headers=headers, timeout=15)
    print('HTTP', r.status_code)
    try:
        data = r.json()
        print(json.dumps(data, indent=2)[:8000])
    except Exception:
        print('Text:', r.text[:8000])
except Exception as e:
    import traceback
    traceback.print_exc()
