#!/usr/bin/env python3
"""
Label Compliance Agent V3 - Render Production Server (Fixed)
"""

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from anthropic import Anthropic

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Anthropic client
try:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("WARNING: ANTHROPIC_API_KEY not set!")
    client = Anthropic(api_key=api_key)
except Exception as e:
    print(f"Error initializing Anthropic: {e}")
    client = None

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Serve the main HTML file"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return '''<!DOCTYPE html>
<html>
<head>
    <title>Label Compliance Agent V3</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #f1f5f9; margin: 0; padding: 40px; text-align: center; }
        h1 { color: #34d399; }
        p { color: #cbd5e1; }
    </style>
</head>
<body>
    <h1>🏷️ Label Compliance Agent V3</h1>
    <p>Server is running...</p>
    <p>If you see this, the backend is working!</p>
</body>
</html>'''

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'api_configured': client is not None
    })

@app.route('/api/generate-swiss', methods=['POST'])
def generate_swiss():
    """Generate Swiss-compliant label"""
    try:
        if not client:
            return jsonify({'error': 'API not configured'}), 500
        
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        prompt = f'''Generate a STICKER-READY Swiss beverage label from this text:
{text}

REQUIREMENTS:
- NO extra blank lines
- Minimal spacing (compact format)
- Short, tight lines to fit 40x30mm sticker
- German AND French required
- Use **text** for bold headers
- ALLERGENS IN CAPITALS AND BOLD
- Sticker-ready format

Output ONLY the label text, nothing else.'''
        
        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        output = message.content[0].text.strip()
        return jsonify({'output': output})
    
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 400

@app.route('/api/generate-eu', methods=['POST'])
def generate_eu():
    """Generate EU-compliant label"""
    try:
        if not client:
            return jsonify({'error': 'API not configured'}), 500
        
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        prompt = f'''Generate a STICKER-READY EU beverage label from this text:
{text}

REQUIREMENTS:
- NO extra blank lines
- Minimal spacing (compact format)
- Short, tight lines to fit 40x30mm sticker
- English language
- Use **text** for bold headers
- ALLERGENS IN CAPITALS AND BOLD
- Sticker-ready format

Output ONLY the label text, nothing else.'''
        
        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        output = message.content[0].text.strip()
        return jsonify({'output': output})
    
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 400

@app.route('/api/validate-swiss', methods=['POST'])
def validate_swiss():
    """Validate Swiss compliance"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        checks = []
        text_lower = text.lower()
        
        # Mandatory checks
        checks.append({
            'pass': 'product' in text_lower or 'cidre' in text_lower,
            'message': 'Product Name: ✓ Found' if 'product' in text_lower or 'cidre' in text_lower else 'Product Name: ✗ Missing'
        })
        
        checks.append({
            'pass': 'hergestellt' in text_lower or 'manufactured' in text_lower,
            'message': 'Origin: ✓ Found' if 'hergestellt' in text_lower or 'manufactured' in text_lower else 'Origin: ✗ Missing'
        })
        
        checks.append({
            'pass': '%' in text and 'vol' in text_lower,
            'message': 'Alcohol: ✓ Found' if '%' in text and 'vol' in text_lower else 'Alcohol: ✗ Missing'
        })
        
        checks.append({
            'pass': 'ml' in text_lower or 'volume' in text_lower,
            'message': 'Volume: ✓ Found' if 'ml' in text_lower or 'volume' in text_lower else 'Volume: ✗ Missing'
        })
        
        checks.append({
            'pass': 'importeur' in text_lower,
            'message': 'Importer: ✓ Found' if 'importeur' in text_lower else 'Importer: ✗ Missing'
        })
        
        checks.append({
            'pass': 'sulfite' in text_lower or 'allergen' in text_lower,
            'message': 'Allergens: ✓ Found' if 'sulfite' in text_lower or 'allergen' in text_lower else 'Allergens: ✗ Missing'
        })
        
        checks.append({
            'pass': '**' in text,
            'message': 'Bold Formatting: ✓ Applied' if '**' in text else 'Bold Formatting: ✗ Not applied'
        })
        
        passed = sum(1 for c in checks if c['pass'])
        total = len(checks)
        
        return jsonify({
            'checks': checks,
            'summary': f'Switzerland: {passed}/{total} checks passed',
            'compliant': passed == total
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/validate-eu', methods=['POST'])
def validate_eu():
    """Validate EU compliance"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        checks = []
        text_lower = text.lower()
        
        # Mandatory checks
        checks.append({
            'pass': 'product' in text_lower or 'beverage' in text_lower,
            'message': 'Product Name: ✓ Found' if 'product' in text_lower or 'beverage' in text_lower else 'Product Name: ✗ Missing'
        })
        
        checks.append({
            'pass': 'manufactured' in text_lower,
            'message': 'Origin: ✓ Found' if 'manufactured' in text_lower else 'Origin: ✗ Missing'
        })
        
        checks.append({
            'pass': '%' in text and 'vol' in text_lower,
            'message': 'Alcohol: ✓ Found' if '%' in text and 'vol' in text_lower else 'Alcohol: ✗ Missing'
        })
        
        checks.append({
            'pass': 'ml' in text_lower or 'volume' in text_lower,
            'message': 'Volume: ✓ Found' if 'ml' in text_lower or 'volume' in text_lower else 'Volume: ✗ Missing'
        })
        
        checks.append({
            'pass': 'importer' in text_lower,
            'message': 'Importer: ✓ Found' if 'importer' in text_lower else 'Importer: ✗ Missing'
        })
        
        checks.append({
            'pass': 'sulfite' in text_lower or 'allergen' in text_lower,
            'message': 'Allergens: ✓ Found' if 'sulfite' in text_lower or 'allergen' in text_lower else 'Allergens: ✗ Missing'
        })
        
        checks.append({
            'pass': '**' in text,
            'message': 'Bold Formatting: ✓ Applied' if '**' in text else 'Bold Formatting: ✗ Not applied'
        })
        
        passed = sum(1 for c in checks if c['pass'])
        total = len(checks)
        
        return jsonify({
            'checks': checks,
            'summary': f'EU: {passed}/{total} checks passed',
            'compliant': passed == total
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/fix-label', methods=['POST'])
def fix_label():
    """Auto-fix non-compliant label"""
    try:
        if not client:
            return jsonify({'error': 'API not configured'}), 500
        
        data = request.get_json()
        text = data.get('text', '')
        market = data.get('market', 'switzerland')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if market == 'switzerland':
            prompt = f'''You are a Swiss label expert. Fix this incomplete label to be 100% compliant with FSV requirements.

Original: {text}

Generate a COMPLETE, STICKER-READY label with:
- Product name + category
- Origin: "Hergestellt in..."
- Alcohol: "X% vol."
- Complete ingredients
- **ALLERGENS IN CAPITALS AND BOLD**
- Volume: "XXXml"
- Importer with full Swiss address
- Phone
- Shelf life info
- German AND French

Use **text** for bold. Make it compact, sticker-ready.
Output ONLY the label, nothing else.'''
        else:
            prompt = f'''You are an EU label expert. Fix this incomplete label to be 100% compliant with 1169/2011.

Original: {text}

Generate a COMPLETE, STICKER-READY label with:
- Product name + category
- Origin: "Manufactured in..."
- Alcohol: "X% vol."
- Complete ingredients
- **ALLERGENS IN CAPITALS AND BOLD**
- Volume: "XXXml"
- Importer with full address
- Phone
- Shelf life info
- English language

Use **text** for bold. Make it compact, sticker-ready.
Output ONLY the label, nothing else.'''
        
        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        output = message.content[0].text.strip()
        return jsonify({'output': output})
    
    except Exception as e:
        return jsonify({'error': f'Fix failed: {str(e)}'}), 400

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
