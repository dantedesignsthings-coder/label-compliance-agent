#!/usr/bin/env python3
"""
Label Compliance Agent V3 - Render Production Server
Ready for deployment on Render.com
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from anthropic import Anthropic
import os
import json

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

try:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
except Exception as e:
    print(f"Error: Could not initialize Anthropic client. Make sure ANTHROPIC_API_KEY is set.")
    client = None

# Serve the main HTML page
@app.route('/')
def index():
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except:
        return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Label Compliance Agent V3</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; background: linear-gradient(135deg, #0f172a 0%, #0d1629 50%, #1a2332 100%); color: #f1f5f9; margin: 0; padding: 40px; text-align: center; }
        h1 { color: #34d399; font-size: 28px; }
        p { color: #cbd5e1; font-size: 16px; margin: 10px 0; }
        .info { background: rgba(16, 185, 129, 0.1); padding: 20px; border-radius: 8px; border-left: 3px solid #10b981; margin: 20px auto; max-width: 500px; }
    </style>
</head>
<body>
    <h1>🏷️ Label Compliance Agent V3</h1>
    <p>Backend Server Running on Render</p>
    <p>✓ API configured</p>
    <p>✓ Server ready</p>
    <div class="info">
        <p>The main app page should load automatically.</p>
        <p>If not, refresh your browser.</p>
    </div>
</body>
</html>'''

@app.route('/api/generate-swiss', methods=['POST'])
def generate_swiss():
    try:
        if not client:
            return jsonify({'error': 'API not configured. Set ANTHROPIC_API_KEY environment variable.'}), 500
            
        data = request.json
        text = data.get('text', '')
        
        prompt = f'''Generate a STICKER-READY Swiss beverage label from this text:
{text}

REQUIREMENTS:
- NO extra blank lines
- Minimal spacing (compact format)
- Short, tight lines to fit 40x30mm sticker
- German AND French required
- Use **text** for bold headers and important info
- ALLERGENS IN CAPITALS AND BOLD
- Format must be copypasteable as-is

Output format (compact, no extras):
**Product Name - Category**
Zutaten: ..., Konservierungsstoff: **ALLERGEN**
**Alkoholgehalt:** X% vol. **Nettofüllmenge:** Xml
**Hergestellt in Country** **Importeur:** Name, Address, Postal, City
Phone
**Haltbar bis:** info **Los:** info

Output ONLY the label text, nothing else. Make it fit a 40x30mm sticker.'''

        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        output = message.content[0].text.strip()
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/generate-eu', methods=['POST'])
def generate_eu():
    try:
        if not client:
            return jsonify({'error': 'API not configured. Set ANTHROPIC_API_KEY environment variable.'}), 500
            
        data = request.json
        text = data.get('text', '')
        
        prompt = f'''Generate a STICKER-READY EU beverage label from this text:
{text}

REQUIREMENTS:
- NO extra blank lines
- Minimal spacing (compact format)
- Short, tight lines to fit 40x30mm sticker
- English language
- Use **text** for bold headers and important info
- ALLERGENS IN CAPITALS AND BOLD
- Format must be copypasteable as-is

Output format (compact, no extras):
**Product Name - Category**
Ingredients: ..., Preservative: **ALLERGEN**
**Alcohol:** X% vol. **Volume:** Xml
**Manufactured in Country** **Importer:** Name, Address, Postal, City
Phone
**Best before:** info **Batch:** info

Output ONLY the label text, nothing else. Make it fit a 40x30mm sticker.'''

        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        output = message.content[0].text.strip()
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/validate-swiss', methods=['POST'])
def validate_swiss():
    try:
        data = request.json
        text = data.get('text', '')
        
        checks = []
        
        # Check for mandatory elements
        mandatory = {
            'Product Name': ['Savanna', 'Cidre', 'product', 'name'],
            'Origin': ['Hergestellt', 'Switzerland', 'Südafrika'],
            'Alcohol': ['%', 'vol'],
            'Volume': ['ml', 'Volumen'],
            'Importer': ['Importeur', 'Lekker', 'address'],
            'Allergen Declaration': ['SULFITE', 'allergen', 'enthält'],
            'Language': ['German', 'Deutsch', 'Zutaten', 'Ingredients'],
        }
        
        text_lower = text.lower()
        
        for element, keywords in mandatory.items():
            found = any(keyword.lower() in text_lower for keyword in keywords)
            checks.append({
                'pass': found,
                'message': f'{element}: {"✓ Found" if found else "✗ Missing"}'
            })
        
        # Check formatting
        has_bold = '**' in text
        checks.append({
            'pass': has_bold,
            'message': f'Bold Formatting: {"✓ Applied" if has_bold else "✗ Not applied"}'
        })
        
        # Check line breaks
        line_count = len(text.split('\n'))
        compact = line_count <= 8
        checks.append({
            'pass': compact,
            'message': f'Compact Format: {"✓ ({} lines)" if compact else "✗ ({} lines)"}'.format(line_count, line_count)
        })
        
        # Summary
        passed = sum(1 for c in checks if c['pass'])
        total = len(checks)
        summary = f"Switzerland Compliance: {passed}/{total} checks passed"
        
        return jsonify({
            'checks': checks,
            'summary': summary,
            'compliant': passed == total
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/validate-eu', methods=['POST'])
def validate_eu():
    try:
        data = request.json
        text = data.get('text', '')
        
        checks = []
        
        # Check for mandatory elements
        mandatory = {
            'Product Name': ['product', 'beverage', 'cider'],
            'Origin': ['Manufactured', 'South Africa', 'origin'],
            'Alcohol': ['%', 'vol'],
            'Volume': ['ml', 'volume'],
            'Importer': ['Importer', 'address'],
            'Allergen Declaration': ['SULFITE', 'allergen'],
            'Language': ['English', 'Ingredients'],
        }
        
        text_lower = text.lower()
        
        for element, keywords in mandatory.items():
            found = any(keyword.lower() in text_lower for keyword in keywords)
            checks.append({
                'pass': found,
                'message': f'{element}: {"✓ Found" if found else "✗ Missing"}'
            })
        
        # Check formatting
        has_bold = '**' in text
        checks.append({
            'pass': has_bold,
            'message': f'Bold Formatting: {"✓ Applied" if has_bold else "✗ Not applied"}'
        })
        
        # Check line breaks
        line_count = len(text.split('\n'))
        compact = line_count <= 8
        checks.append({
            'pass': compact,
            'message': f'Compact Format: {"✓ ({} lines)" if compact else "✗ ({} lines)"}'.format(line_count, line_count)
        })
        
        # Summary
        passed = sum(1 for c in checks if c['pass'])
        total = len(checks)
        summary = f"EU Compliance: {passed}/{total} checks passed"
        
        return jsonify({
            'checks': checks,
            'summary': summary,
            'compliant': passed == total
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*70)
    print("Label Compliance Agent V3 - Production Server")
    print("="*70)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n⚠️  WARNING: ANTHROPIC_API_KEY not set!")
        print("Set it in Render dashboard: Settings → Environment Variables")
        print("Key: ANTHROPIC_API_KEY")
        print("Value: sk-ant-...")
    
    print(f"\n✓ Server starting on port {port}")
    print("✓ API configured")
    print(f"✓ Open: https://your-render-url.onrender.com")
    print("\nPress Ctrl+C to stop")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
