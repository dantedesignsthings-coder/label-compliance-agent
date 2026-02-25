#!/usr/bin/env python3
"""
Label Compliance Agent - Backend Server
This server handles API calls to Claude and serves the HTML interface.
Run with: export ANTHROPIC_API_KEY='sk-ant-...' && python server.py
"""

from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
from anthropic import Anthropic
import os

app = Flask(__name__)
CORS(app)

# Initialize Anthropic client - gets API key from environment variable
try:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
except Exception as e:
    print(f"Error: Could not initialize Anthropic client. Make sure ANTHROPIC_API_KEY is set.")
    print(f"Run: export ANTHROPIC_API_KEY='sk-ant-...'")
    client = None

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Label Compliance Agent</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #0f172a;
            --secondary: #1e293b;
            --accent: #3b82f6;
            --accent-light: #60a5fa;
            --success: #10b981;
            --error: #ef4444;
            --text: #f1f5f9;
            --text-muted: #cbd5e1;
            --border: #334155;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #0d1629 50%, #1a2332 100%);
            color: var(--text);
            min-height: 100vh;
        }

        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(10px); border-bottom: 1px solid var(--border); padding: 20px 0; margin-bottom: 40px; position: sticky; top: 0; z-index: 100; }
        .header-content { display: flex; align-items: center; justify-content: space-between; gap: 20px; }
        .logo { display: flex; align-items: center; gap: 12px; }
        .logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
        .logo-text h1 { font-size: 20px; font-weight: 700; }
        .logo-text p { font-size: 12px; color: var(--text-muted); }
        .status { display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px; font-size: 13px; color: var(--success); }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 40px; }
        @media (max-width: 1024px) { .grid { grid-template-columns: 1fr; } }
        .card { background: rgba(30, 41, 59, 0.9); backdrop-filter: blur(10px); border: 1px solid var(--border); border-radius: 12px; padding: 30px; transition: all 0.3s ease; }
        .card:hover { border-color: var(--accent); box-shadow: 0 0 30px rgba(59, 130, 246, 0.1); }
        .card h2 { font-size: 20px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
        .card-icon { width: 32px; height: 32px; background: rgba(59, 130, 246, 0.2); border-radius: 8px; display: flex; align-items: center; justify-content: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 8px; color: var(--text); }
        textarea { width: 100%; padding: 12px; background: rgba(15, 23, 42, 0.5); border: 1px solid var(--border); border-radius: 8px; color: var(--text); font-family: 'Monaco', 'Courier New', monospace; font-size: 13px; resize: vertical; min-height: 250px; transition: all 0.3s ease; line-height: 1.6; }
        textarea:focus { outline: none; border-color: var(--accent); background: rgba(15, 23, 42, 0.8); box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
        button { padding: 12px 24px; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; display: flex; align-items: center; justify-content: center; gap: 8px; }
        .btn-primary { background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%); color: white; width: 100%; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3); }
        .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .output-section { margin-top: 20px; }
        .output-title { font-size: 14px; font-weight: 600; margin-bottom: 12px; color: var(--accent-light); display: flex; align-items: center; gap: 8px; }
        .output-box { background: rgba(15, 23, 42, 0.5); border: 1px solid var(--border); border-radius: 8px; padding: 20px; line-height: 1.8; font-size: 12px; max-height: 400px; overflow-y: auto; white-space: pre-wrap; word-wrap: break-word; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif; color: var(--text); letter-spacing: 0.3px; }
        .output-box strong { font-weight: 700; color: #ffffff; }
        .copy-btn { padding: 8px 14px; background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%); color: white; border: none; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; margin-top: 10px; transition: all 0.2s ease; }
        .copy-btn:hover { background: linear-gradient(135deg, var(--accent-light) 0%, var(--accent) 100%); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
        .copy-btn:active { transform: translateY(0); }
        .loader { display: inline-block; width: 14px; height: 14px; border: 2px solid rgba(59, 130, 246, 0.3); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.8s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .alert { padding: 12px; border-radius: 8px; margin-bottom: 15px; font-size: 13px; display: none; }
        .alert.show { display: block; animation: slideDown 0.3s ease; }
        @keyframes slideDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
        .alert-success { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: var(--success); }
        .alert-error { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); color: var(--error); }
        .market-selector { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
        .market-checkbox { display: flex; align-items: center; gap: 8px; padding: 10px; background: rgba(15, 23, 42, 0.5); border: 1px solid var(--border); border-radius: 6px; cursor: pointer; transition: all 0.3s ease; }
        .market-checkbox:hover { border-color: var(--accent); }
        .market-checkbox input { cursor: pointer; accent-color: var(--accent); }
        .compliance-note { background: rgba(59, 130, 246, 0.1); border-left: 3px solid var(--accent); padding: 12px; border-radius: 6px; font-size: 12px; color: var(--text-muted); margin-top: 15px; }
        .empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
        .empty-state-icon { font-size: 48px; margin-bottom: 10px; }
        footer { border-top: 1px solid var(--border); padding: 30px 0; text-align: center; color: var(--text-muted); font-size: 12px; margin-top: 60px; }
        a { color: var(--accent-light); text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <div class="logo-icon">🏷️</div>
                    <div class="logo-text">
                        <h1>Label Compliance Agent</h1>
                        <p>Switzerland (FSV) + EU (1169/2011)</p>
                    </div>
                </div>
                <div class="status">
                    <span>✓ Ready</span>
                </div>
            </div>
        </div>
    </header>

    <div class="container">
        <div id="alertContainer"></div>

        <div class="grid">
            <div class="card">
                <h2><div class="card-icon">📝</div> Old Label Text</h2>
                <p style="color: var(--text-muted); font-size: 12px; margin-bottom: 15px;">Paste your current label</p>

                <div class="form-group">
                    <label>Target Markets</label>
                    <div class="market-selector">
                        <label class="market-checkbox">
                            <input type="checkbox" name="market" value="switzerland" checked>
                            <span>🇨🇭 Switzerland</span>
                        </label>
                        <label class="market-checkbox">
                            <input type="checkbox" name="market" value="eu" checked>
                            <span>🇪🇺 EU</span>
                        </label>
                    </div>
                </div>

                <div class="form-group">
                    <label>Current Label Text</label>
                    <textarea id="oldLabelText" placeholder="Paste your current label text here...">Savanna Cider
Enthält Sulfite
6% Alkoholgehalt
Importeur: Lekker Roots
Haberweidstrasse 4
8610 Uster-CH</textarea>
                </div>

                <button class="btn-primary" onclick="updateLabel()" id="updateBtn">
                    <span id="updateBtnText">Generate Compliant Label</span>
                </button>

                <div class="compliance-note">
                    ℹ️ We'll generate properly formatted labels with all required elements, correct capitalization, and allergen declarations in CAPITALS.
                </div>
            </div>

            <div class="card">
                <h2><div class="card-icon">✅</div> Compliant Output</h2>
                <p style="color: var(--text-muted); font-size: 12px; margin-bottom: 15px;">Your verified and formatted label</p>

                <div id="outputContainer" style="display: none;">
                    <div class="output-section" id="swissSection" style="display: none;">
                        <div class="output-title">🇨🇭 Switzerland</div>
                        <div class="output-box" id="swissOutput"></div>
                        <button class="copy-btn" onclick="copyText('swissOutput')">Copy Swiss Label</button>
                    </div>

                    <div class="output-section" id="euSection" style="display: none;">
                        <div class="output-title">🇪🇺 EU</div>
                        <div class="output-box" id="euOutput"></div>
                        <button class="copy-btn" onclick="copyText('euOutput')">Copy EU Label</button>
                    </div>

                    <div class="compliance-note" style="margin-top: 20px;">
                        ✓ Ready to print. All mandatory elements included. Properly formatted with correct text styling and capitalization.
                    </div>
                </div>

                <div id="emptyState" class="empty-state">
                    <div class="empty-state-icon">📋</div>
                    <p>Enter label text and click generate to see compliant output here</p>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <p>⚠️ Always verify final labels with your legal team before printing.</p>
        <p style="margin-top: 10px;">
            <a href="https://www.blv.admin.ch" target="_blank">Switzerland FSV</a> • 
            <a href="https://ec.europa.eu/food" target="_blank">EU Regulations</a>
        </p>
    </footer>

    <script>
        function formatLabelOutput(text) {
            return text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
        }

        async function updateLabel() {
            const text = document.getElementById('oldLabelText').value.trim();
            if (!text) {
                showAlert('Please enter label text', 'error');
                return;
            }

            const markets = getMarkets();
            if (!markets.length) {
                showAlert('Select at least one market', 'error');
                return;
            }

            setLoading('updateBtn', true);

            try {
                if (markets.includes('switzerland')) {
                    const swissResponse = await callBackend('/api/generate-swiss', { text });
                    document.getElementById('swissOutput').innerHTML = formatLabelOutput(swissResponse);
                    document.getElementById('swissSection').style.display = 'block';
                }

                if (markets.includes('eu')) {
                    const euResponse = await callBackend('/api/generate-eu', { text });
                    document.getElementById('euOutput').innerHTML = formatLabelOutput(euResponse);
                    document.getElementById('euSection').style.display = 'block';
                }

                document.getElementById('emptyState').style.display = 'none';
                document.getElementById('outputContainer').style.display = 'block';
                showAlert('Label generated successfully!', 'success');
            } catch (error) {
                showAlert('Error: ' + error.message, 'error');
            } finally {
                setLoading('updateBtn', false);
            }
        }

        async function callBackend(endpoint, data) {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'API request failed');
            }

            const result = await response.json();
            return result.output;
        }

        function getMarkets() {
            return Array.from(document.querySelectorAll('input[name="market"]:checked')).map(el => el.value);
        }

        function setLoading(id, loading) {
            const btn = document.getElementById(id);
            const text = btn.querySelector('span');
            btn.disabled = loading;
            text.innerHTML = loading ? '<span class="loader"></span> Processing...' : 'Generate Compliant Label';
        }

        function showAlert(msg, type) {
            const container = document.getElementById('alertContainer');
            const alert = document.createElement('div');
            alert.className = `alert alert-${type} show`;
            alert.textContent = msg;
            container.appendChild(alert);
            setTimeout(() => {
                alert.classList.remove('show');
                setTimeout(() => alert.remove(), 300);
            }, 4000);
        }

        function copyText(elementId) {
            const element = document.getElementById(elementId);
            if (!element) {
                showAlert('Error: Output not found', 'error');
                return;
            }
            
            const text = element.textContent || element.innerText || '';
            
            if (!text) {
                showAlert('Error: Nothing to copy', 'error');
                return;
            }
            
            navigator.clipboard.writeText(text).then(() => {
                showAlert('✓ Copied to clipboard!', 'success');
            }).catch((err) => {
                showAlert('Failed to copy - try manual select', 'error');
            });
        }
    </script>
</body>
</html>'''

@app.route('/api/generate-swiss', methods=['POST'])
def generate_swiss():
    try:
        if not client:
            return jsonify({'error': 'API not configured. Set ANTHROPIC_API_KEY environment variable.'}), 500
            
        data = request.json
        text = data.get('text', '')
        
        prompt = f'''You are a Swiss beverage label compliance expert (FSV - Foodstuff Act).

Current label: {text}

Generate a COMPLETE Swiss beverage label. Use **text** for bold. Format exactly like:
**Savanna Cidre - Alkoholisches Getränk auf Apfelweinbasis**

Zutaten: ..., Konservierungsstoff: **SULFITE**

**Alkoholgehalt:** X% vol. **Nettofüllmenge:** Xml

**Hergestellt in Country** **Importeur:** Name Address

Phone

**Mindestens haltbar bis:** info **Losnummer:** info

Include both German and French. Make **bold** the product name, section headers, allergens in CAPITALS, and important info.'''

        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return jsonify({'output': message.content[0].text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/generate-eu', methods=['POST'])
def generate_eu():
    try:
        if not client:
            return jsonify({'error': 'API not configured. Set ANTHROPIC_API_KEY environment variable.'}), 500
            
        data = request.json
        text = data.get('text', '')
        
        prompt = f'''You are an EU beverage label compliance expert (Regulation 1169/2011).

Current label: {text}

Generate a COMPLETE EU beverage label. Use **text** for bold. Format exactly like:
**Savanna Cider - Alcoholic Beverage Based on Apple Cider**

Ingredients: ..., Preservative: **SULFITE**

**Alcohol content:** X% vol. **Net volume:** Xml

**Manufactured in Country** **Importer:** Name Address

Phone

**Best before:** info **Batch code:** info

In English. Make **bold** the product name, section headers, allergens in CAPITALS, and important info.'''

        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return jsonify({'output': message.content[0].text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("\n" + "="*70)
    print("Label Compliance Agent - Backend Server")
    print("="*70)
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n❌ ERROR: ANTHROPIC_API_KEY not set!")
        print("\nSet it with:")
        print("  export ANTHROPIC_API_KEY='sk-ant-...'")
        print("\nThen run this script again.")
        exit(1)
    
    print("\n✓ API key configured")
    print("✓ Server starting on http://localhost:5000")
    print("✓ Open your browser to http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
