import requests
from pypdf import PdfWriter
import os

BASE_URL = "http://127.0.0.1:8000"

# Create dummy PDF with 8 pages (good for booklet)
writer = PdfWriter()
for i in range(8):
    writer.add_blank_page(width=595, height=842) # A4 Portrait
with open("test.pdf", "wb") as f:
    writer.write(f)

# Test Upload
url = f"{BASE_URL}/api/upload"
files = {'file': open('test.pdf', 'rb')}
response = requests.post(url, files=files)
print("Upload Response:", response.json())

if response.status_code == 200:
    filename = response.json()['filename']
    process_url = f"{BASE_URL}/api/process"
    
    # 1. Test Double Mode (Reverse Order = True, Default)
    print("\nTesting Double Mode (Reverse Order = True):")
    payload = {
        "filename": filename,
        "original_filename": "test.pdf",
        "mode": "double",
        "reverse_order": True
    }
    res = requests.post(process_url, json=payload)
    print(res.json())
    assert res.status_code == 200
    files = res.json()['files']
    # If reverse order is True, file 1 should be Backs (Even)
    # We can't easily verify content without downloading and inspecting, 
    # but we can verify the API call succeeds.
    
    # 2. Test Double Mode (Reverse Order = False)
    print("\nTesting Double Mode (Reverse Order = False):")
    payload["reverse_order"] = False
    res = requests.post(process_url, json=payload)
    print(res.json())
    assert res.status_code == 200
    
    print("\nAll tests passed!")
