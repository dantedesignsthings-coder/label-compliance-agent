# 🏷️ Label Compliance Agent V3

**Production-ready label compliance tool for Switzerland (FSV) and EU (1169/2011)**
- ✨ Sticker-ready formatting (copy & paste directly)
- 🟢 Green color scheme  
- ✅ Built-in compliance validation
- 📋 Three-column interface

---

## ✨ What's New in V3

### 1️⃣ Sticker-Ready Formatting
- Output is **already formatted** to fit on small label stickers
- **Copy & paste directly** - no Word formatting needed!
- Compact layout optimized for 40×30mm stickers
- Minimal line breaks and spacing

### 2️⃣ Green Color Scheme
- Modern green gradient (#10b981 - #34d399)
- Better visual hierarchy
- Easier on the eyes

### 3️⃣ Built-in Validation
- **Real-time compliance checking**
- Validates both Switzerland (FSV) and EU (1169/2011) requirements
- Check marks for each mandatory element:
  - ✓ Product Name
  - ✓ Origin Country
  - ✓ Alcohol Content
  - ✓ Volume
  - ✓ Importer Information
  - ✓ Allergen Declarations
  - ✓ Languages
  - ✓ Bold Formatting
  - ✓ Compact Format

---

## 📦 Setup (4 Steps)

### Step 1: Install Dependencies
```bash
pip install flask flask-cors anthropic
```

### Step 2: Set API Key
Get your key from: https://console.anthropic.com

```bash
export ANTHROPIC_API_KEY='sk-ant-your-actual-key-here'
```

**On Windows (Command Prompt):**
```bash
set ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

**On Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY='sk-ant-your-actual-key-here'
```

### Step 3: Start Backend Server
```bash
python server.py
```

You should see:
```
======================================================================
Label Compliance Agent V3 - Backend Server
======================================================================

✓ API key configured
✓ Server starting on http://localhost:5000
✓ Open index.html in your browser

Features:
  • Sticker-ready formatting (copy & paste directly)
  • Green color scheme
  • Compliance validation
  • Switzerland (FSV) + EU (1169/2011)

Press Ctrl+C to stop
======================================================================
```

### Step 4: Open in Browser
Go to: **http://localhost:5000**

---

## 🎯 How to Use

### Left Column: INPUT
1. **Paste your current label text**
2. **Select target markets** (Switzerland, EU, or both)
3. **Click "Generate & Validate"**

### Middle Column: STICKER OUTPUT
- **See sticker-ready format** (white background, compact text)
- **Copy directly** to your sticker printing software
- **No formatting needed** - paste as-is!

### Right Column: VALIDATION
- **Green checkmarks** ✓ for all compliant elements
- **Red X marks** ✕ for missing requirements
- **Summary** showing total compliance score

---

## 📋 Example

**Input:**
```
Savanna Cider
Enthält Sulfite
6% Alkoholgehalt
Importeur: Lekker Roots
Haberweidstrasse 4
8610 Uster-CH
```

**Output (Sticker-Ready):**
```
**Savanna Cidre - Alkoholisches Getränk auf Apfelweinbasis**
Zutaten: Wasser, Apfelsaft aus Konzentrat (vergoren), Zucker, 
Aroma, Zitronensäure, Farbstoff: E150c, Konservierungsstoff: **SULFITE**
**Alkoholgehalt:** 6% vol. **Nettofüllmenge:** 330ml
**Hergestellt in Südafrika** **Importeur:** Lekker Roots, 
Haberweidstrasse 4, 8610 Uster, CH
+41 77 265 2945
**Haltbar bis:** siehe Flasche **Los:** siehe Flasche
```

**Validation Results:**
- ✓ Product Name: Found
- ✓ Origin: Found  
- ✓ Alcohol: Found
- ✓ Volume: Found
- ✓ Importer: Found
- ✓ Allergen Declaration: Found
- ✓ Language: Found
- ✓ Bold Formatting: Applied
- ✓ Compact Format: 8 lines

**Switzerland Compliance: 9/9 checks passed**

---

## 🎨 UI Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    🏷️ LABEL COMPLIANCE V3                    │
├──────────────┬──────────────────┬──────────────────────────┤
│              │                  │                          │
│   INPUT      │  STICKER OUTPUT  │    VALIDATION            │
│              │                  │                          │
│ • Paste text │ • White preview  │ • Real-time checks      │
│ • Markets    │ • Copy button    │ • Checkmarks            │
│ • Generate   │ • Format ready   │ • Compliance score      │
│              │                  │                          │
└──────────────┴──────────────────┴──────────────────────────┘
```

---

## 🔧 Troubleshooting

### Error: "Module not found"
```bash
pip install flask flask-cors anthropic
```

### Error: "ANTHROPIC_API_KEY not set"
```bash
echo $ANTHROPIC_API_KEY
# Should show your key

# If empty:
export ANTHROPIC_API_KEY='sk-ant-...'
```

### Error: "Connection refused"
- ✓ Make sure server is running: `python server.py`
- ✓ Check terminal shows "Server starting on http://localhost:5000"
- ✓ Try refreshing browser (Ctrl+R)

### Error: "Port 5000 already in use"
Edit `server.py`, last line:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

---

## 📱 Advanced Configuration

### Run Server in Background (Mac/Linux)
```bash
python server.py &
```

### Access from Another Computer
Edit `server.py`:
```python
app.run(debug=True, port=5000, host='0.0.0.0')
```

Then access from another PC:
```
http://your-computer-ip:5000
```

### Production Mode
Edit `server.py`:
```python
app.run(debug=False, port=5000)  # Disable debug mode
```

---

## 🎯 Features Breakdown

### ✨ Sticker-Ready Format
- Compact layout (fits 40×30mm labels)
- No extra spacing or blank lines
- Optimized text size
- Direct copy-paste compatibility

### 🟢 Green Color Scheme  
- Primary: `#10b981` (Emerald)
- Light: `#34d399` (Mint)
- Dark: `#059669` (Forest)
- Modern gradient buttons
- Professional appearance

### ✅ Smart Validation
- Checks 9 mandatory elements
- Real-time feedback
- Pass/fail indicators
- Compliance percentage
- Actionable feedback

---

## 📋 Supported Markets

### 🇨🇭 Switzerland (FSV)
✓ German + French required
✓ Origin country statement
✓ Importer address in Switzerland
✓ Alcohol format (X% vol.)
✓ Allergen declarations
✓ Net volume
✓ Complete ingredients list

### 🇪🇺 EU (1169/2011)
✓ Destination language
✓ Origin country
✓ Responsible person/importer
✓ Alcohol format (X% vol.)
✓ Complete ingredients
✓ Allergen declarations
✓ Nutrition information
✓ Net volume

---

## 🎓 Files

```
label-compliance-v3/
├── index.html           ← Web interface (open in browser)
├── server.py            ← Backend server (run this)
├── requirements.txt     ← Python dependencies
└── README.md            ← This file
```

---

## 🚀 Quick Reference

| Action | Command |
|--------|---------|
| Install packages | `pip install flask flask-cors anthropic` |
| Set API key | `export ANTHROPIC_API_KEY='sk-ant-...'` |
| Start server | `python server.py` |
| Open interface | Go to `http://localhost:5000` |
| Stop server | Press `Ctrl+C` |

---

## 📞 Support

### Check Server Status
Look for "✓ Server starting on http://localhost:5000" in terminal

### Validate Your Setup
- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip list | grep flask`
- [ ] API key valid at console.anthropic.com
- [ ] Server running and showing ready status
- [ ] Browser can reach http://localhost:5000

### Common Fixes
1. Restart server: `Ctrl+C` then `python server.py`
2. Clear browser cache: `Ctrl+Shift+Delete`
3. Try different port: Change 5000 in server.py and index.html
4. Verify API key is valid and has credits

---

## ✅ Checklist

- [ ] All files downloaded
- [ ] Dependencies installed
- [ ] API key set
- [ ] Server running
- [ ] Browser opened to http://localhost:5000
- [ ] Can generate labels
- [ ] Can validate output
- [ ] Can copy to clipboard

---

## 🎉 You're Ready!

Everything is production-ready. Just:
1. Set API key
2. Run `python server.py`
3. Open http://localhost:5000
4. Paste label and generate!

**Enjoy V3!** 🚀

---

## 📄 License

MIT License - Use freely for any purpose

---

## 🤝 Contributing

Upload to GitHub and share with the community!

---

**Version 3.0** - Sticker Ready • Green Theme • Built-in Validation
