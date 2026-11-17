#!/usr/bin/env python3
"""Sinh ảnh minh hoạ bằng Gemini (Vertex AI) từ file jobs.json.
python gen_images.py jobs.json <thư-mục-ra> [--model gemini-3-pro-image] [--sa /đường/dẫn/service-account.json]
jobs.json: [{"id":"hero_shield","aspect":"4:3","prompt":"..."}]   (ảnh đã có thì bỏ qua)
Khoá: --sa hoặc biến môi trường MISA_GEMINI_SA. KHÔNG in, KHÔNG chép, KHÔNG gửi nội dung khoá ra ngoài."""
import argparse, base64, json, os, sys
from concurrent.futures import ThreadPoolExecutor
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
ap = argparse.ArgumentParser(); ap.add_argument('jobs'); ap.add_argument('out')
ap.add_argument('--model', default='gemini-3-pro-image')
ap.add_argument('--sa', default=os.environ.get('MISA_GEMINI_SA'))
a = ap.parse_args()
if not a.sa or not os.path.exists(a.sa): sys.exit('Không thấy file service account (dùng --sa hoặc MISA_GEMINI_SA)')
cred = service_account.Credentials.from_service_account_file(a.sa, scopes=['https://www.googleapis.com/auth/cloud-platform']); cred.refresh(Request())
PROJ = json.load(open(a.sa))['project_id']
os.makedirs(a.out, exist_ok=True)
def gen(j):
    out = os.path.join(a.out, j['id'] + '.png')
    if os.path.exists(out): return
    url = f'https://aiplatform.googleapis.com/v1/projects/{PROJ}/locations/global/publishers/google/models/{a.model}:generateContent'
    body = {'contents': [{'role': 'user', 'parts': [{'text': j['prompt']}]}],
            'generationConfig': {'responseModalities': ['IMAGE'], 'imageConfig': {'aspectRatio': j.get('aspect', '1:1')}}}
    for _ in range(2):
        r = requests.post(url, headers={'Authorization': 'Bearer ' + cred.token}, json=body, timeout=300)
        if r.status_code == 200:
            for c in r.json().get('candidates', []):
                for p in c.get('content', {}).get('parts', []):
                    if 'inlineData' in p: open(out, 'wb').write(base64.b64decode(p['inlineData']['data'])); print('OK', j['id']); return
        print('lỗi', j['id'], r.status_code, r.text[:200])
with ThreadPoolExecutor(4) as ex: list(ex.map(gen, json.load(open(a.jobs))))
