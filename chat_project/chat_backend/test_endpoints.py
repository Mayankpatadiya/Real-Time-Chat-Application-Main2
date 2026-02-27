import requests

s = requests.Session()
base = 'http://127.0.0.1:8000'

# Test 1: Login page
r = s.get(base + '/login/')
has_form = 'csrfmiddlewaretoken' in r.text
print('1. GET /login/ => %d (has form: %s)' % (r.status_code, has_form))

# Test 2: Login POST
csrf = r.text.split('csrfmiddlewaretoken')[1].split('value="')[1].split('"')[0]
r = s.post(base + '/login/', data={
    'username': 'filetest',
    'password': 'FileTest@1234',
    'csrfmiddlewaretoken': csrf
}, allow_redirects=True)
print('2. POST /login/ => %d (url: %s)' % (r.status_code, r.url))
print('   Has contact items: %s' % ('contact-item' in r.text))
print('   Has attachBtn: %s' % ('attachBtn' in r.text))
print('   Has fileInput: %s' % ('fileInput' in r.text))
print('   Has uploadPreview: %s' % ('uploadPreview' in r.text))
print('   Has lightbox: %s' % ('lightbox' in r.text))
print('   Has doUpload fn: %s' % ('doUpload' in r.text))

# Test 3: Chat page (user id 1)
r = s.get(base + '/chat/1/')
print('3. GET /chat/1/ => %d' % r.status_code)
print('   Has sendBtn: %s' % ('sendBtn' in r.text))
print('   Has file upload: %s' % ('doUpload' in r.text))
print('   Has openLightbox: %s' % ('openLightbox' in r.text))
print('   Has chat-img-thumb: %s' % ('chat-img-thumb' in r.text))
print('   Has file-card: %s' % ('file-card' in r.text))

# Test 4: Profile page
r = s.get(base + '/profile/')
print('4. GET /profile/ => %d' % r.status_code)

# Test 5: Create group page
r = s.get(base + '/groups/new/')
print('5. GET /groups/new/ => %d' % r.status_code)

# Test 6: Upload endpoint (no file = 400)
csrf2 = r.text.split('csrfmiddlewaretoken')[1].split('value="')[1].split('"')[0]
r = s.post(base + '/upload/', data={'csrfmiddlewaretoken': csrf2})
print('6. POST /upload/ (no file) => %d (expected 400)' % r.status_code)
print('   Response: %s' % r.text)

# Test 7: Upload endpoint with file
import io
csrf3 = csrf2
files = {'file': ('test.txt', io.BytesIO(b'Hello test file'), 'text/plain')}
r = s.post(base + '/upload/', data={'csrfmiddlewaretoken': csrf3, 'chat_id': '1', 'caption': 'test file upload'}, files=files)
print('7. POST /upload/ (with file, chat_id=1) => %d' % r.status_code)
print('   Response: %s' % r.text)

# Test 8: Upload image
files2 = {'file': ('test.png', io.BytesIO(b'\x89PNG\r\n\x1a\n' + b'\x00' * 100), 'image/png')}
r = s.post(base + '/upload/', data={'csrfmiddlewaretoken': csrf3, 'chat_id': '1', 'caption': 'test image'}, files=files2)
print('8. POST /upload/ (with image, chat_id=1) => %d' % r.status_code)
print('   Response: %s' % r.text)

print('\nAll endpoint tests completed!')
