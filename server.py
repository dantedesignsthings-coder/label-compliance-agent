#!/usr/bin/env python3
"""
Label Compliance Agent V3 - Fixed Backend Server
Better error handling and CORS support
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from anthropic import Anthropic
import os
import sys

# Check for API key first
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    print("\n" + "="*70)
    print("❌ ERROR: ANTHROPIC_API_KEY environment variable not set!")
    print("="*70)
    print("\nSet it with:")
    print("  Mac/Linux: export ANTHROPIC_API_KEY='sk-ant-...'")
    print("  Windows CMD: set ANTHROPIC_API_KEY=sk-ant-...")
    print("  Windows PowerShell: $env:ANTHROPIC_API_KEY='sk-ant-...'")
    print("\nThen run: python server.py")
    print("="*70 + "\n")
    sys.exit(1)

app = Flask(__name__)

# Better CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize Anthropic
try:
    client = Anthropic(api_key=api_key)
except Exception as e:
    print(f"\n❌ Error initializing Anthropic: {str(e)}\n")
    sys.exit(1)

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Label Compliance Agent V3</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; background: linear-gradient(135deg, #0f172a 0%, #0d1629 50%, #1a2332 100%); color: #f1f5f9; margin: 0; padding: 40px; text-align: center; }
        .box { max-width: 600px; margin: 0 auto; background: rgba(16, 185, 129, 0.1); border: 2px solid #10b981; border-radius: 12px; padding: 30px; }
        h1 { color: #34d399; font-size: 28px; margin: 0 0 10px 0; }
        p { color: #cbd5e1; font-size: 14px; margin: 8px 0; }
        .code { background: rgba(15, 23, 42, 0.9); padding: 12px; border-radius: 8px; border-left: 3px solid #10b981; font-family: monospace; font-size: 13px; margin: 15px 0; text-align: left; }
        a { color: #34d399; text-decoration: none; font-weight: bold; }
        a:hover { text-decoration: underline; }
        .success { color: #10b981; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <h1>✅ Server Running!</h1>
        <p class="success">Backend is ready at http://localhost:5000</p>
        <p style="margin: 20px 0;">Open <strong>index.html</strong> in your browser</p>
        <p style="color: #f59e0b; margin-top: 20px;">⚠️ Make sure you opened index.html from http://localhost:5000, not file:// path</p>
    </div>
</body>
</html>'''

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})

@app.route('/api/generate-swiss', methods=['POST', 'OPTIONS'])
def generate_swiss():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        prompt = f'''Generate a STICKER-READY Swiss beverage label from this text:
{text}

REQUIREMENTS:
- NO extra blank lines between sections
- Minimal spacing (compact format)
- Short, tight lines to fit 40x30mm sticker
- German AND French required
- Use **text** for bold headers and important info
- ALLERGENS IN CAPITALS AND BOLD (e.g., **SULFITE**)
- Format must be copypasteable as-is to sticker software
- Maximum 8-10 lines total

Output format (compact, no extras):
**Product Name - Category**
Zutaten: ingredients, Konservierungsstoff: **ALLERGEN**
**Alkoholgehalt:** X% vol. **Nettofüllmenge:** Xml
**Hergestellt in Country** **Importeur:** Name, Address, Postal, City
Phone
**Haltbar bis:** info **Los:** info

Output ONLY the label text. Nothing else.'''

        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        output = message.content[0].text.strip()
        return jsonify({'output': output}), 200
        
    except Exception as e:
        return jsonify({'error': f'Generation error: {str(e)}'}), 500

@app.route('/api/generate-eu', methods=['POST', 'OPTIONS'])
def generate_eu():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        prompt = f'''Generate a STICKER-READY EU beverage label from this text:
{text}

REQUIREMENTS:
- NO extra blank lines between sections
- Minimal spacing (compact format)
- Short, tight lines to fit 40x30mm sticker
- English language
- Use **text** for bold headers and important info
- ALLERGENS IN CAPITALS AND BOLD (e.g., **SULFITE**)
- Format must be copypasteable as-is to sticker software
- Maximum 8-10 lines total

Output format (compact, no extras):
**Product Name - Category**
Ingredients: ingredients, Preservative: **ALLERGEN**
**Alcohol:** X% vol. **Volume:** Xml
**Manufactured in Country** **Importer:** Name, Address, Postal, City
Phone
**Best before:** info **Batch:** info

Output ONLY the label text. Nothing else.'''

        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        output = message.content[0].text.strip()
        return jsonify({'output': output}), 200
        
    except Exception as e:
        return jsonify({'error': f'Generation error: {str(e)}'}), 500

@app.route('/api/validate-swiss', methods=['POST', 'OPTIONS'])
def validate_swiss():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        text = data.get('text', '').lower()
        
        checks = []
        mandatory = {
            'Product Name': ['product', 'name', 'cidre', 'cider'],
            'Origin': ['hergestellt', 'switzerland', 'südafrika'],
            'Alcohol': ['%', 'vol'],
            'Volume': ['ml'],
            'Importer': ['importeur', 'address'],
            'Allergen': ['sulfite', 'allergen', 'enthält'],
            'Language': ['zutaten', 'deutsch'],
        }
        
        for element, keywords in mandatory.items():
            found = any(kw.lower() in text for kw in keywords)
            checks.append({'pass': found, 'message': f'{element}: {"✓ Found" if found else "✗ Missing"}'})
        
        has_bold = '**' in text
        checks.append({'pass': has_bold, 'message': f'Bold Formatting: {"✓ Applied" if has_bold else "✗ Not applied"}'})
        
        lines = len([l for l in text.split('\n') if l.strip()])
        compact = lines <= 10
        checks.append({'pass': compact, 'message': f'Compact Format: {"✓ Optimal" if compact else "✗ Too long"}'})
        
        passed = sum(1 for c in checks if c['pass'])
        total = len(checks)
        
        return jsonify({
            'checks': checks,
            'summary': f'Switzerland: {passed}/{total} checks passed',
            'compliant': passed == total
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate-eu', methods=['POST', 'OPTIONS'])
def validate_eu():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        text = data.get('text', '').lower()
        
        checks = []
        mandatory = {
            'Product Name': ['product', 'beverage', 'cider'],
            'Origin': ['manufactured', 'origin'],
            'Alcohol': ['%', 'vol'],
            'Volume': ['ml'],
            'Importer': ['importer', 'address'],
            'Allergen': ['sulfite', 'allergen'],
            'Language': ['ingredients', 'english'],
        }
        
        for element, keywords in mandatory.items():
            found = any(kw.lower() in text for kw in keywords)
            checks.append({'pass': found, 'message': f'{element}: {"✓ Found" if found else "✗ Missing"}'})
        
        has_bold = '**' in text
        checks.append({'pass': has_bold, 'message': f'Bold Formatting: {"✓ Applied" if has_bold else "✗ Not applied"}'})
        
        lines = len([l for l in text.split('\n') if l.strip()])
        compact = lines <= 10
        checks.append({'pass': compact, 'message': f'Compact Format: {"✓ Optimal" if compact else "✗ Too long"}'})
        
        passed = sum(1 for c in checks if c['pass'])
        total = len(checks)
        
        return jsonify({
            'checks': checks,
            'summary': f'EU: {passed}/{total} checks passed',
            'compliant': passed == total
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🏷️  Label Compliance Agent V3 - Backend Server")
    print("="*70)
    print("\n✅ API key: CONFIGURED")
    print("✅ Flask: READY")
    print("✅ CORS: ENABLED")
    print("\n🌐 Server starting on http://localhost:5000")
    print("\n📝 Next steps:")
    print("  1. Open http://localhost:5000 in your browser")
    print("  2. Or open index.html and make sure to access it from http://localhost:5000")
    print("\n⚠️  IMPORTANT: Use http://localhost:5000, NOT file:// path")
    print("\n✨ Features:")
    print("  • Sticker-ready formatting")
    print("  • Green color scheme")
    print("  • Real-time validation")
    print("  • Switzerland (FSV) + EU (1169/2011)")
    print("\n⏹️  Press Ctrl+C to stop server")
    print("="*70 + "\n")
    
    app.run(debug=False, port=5000, host='127.0.0.1')
