# 🐛 Troubleshooting Blank Screen

## Quick Fixes for Blank Screen at http://localhost:5173

---

## ✅ Step 1: Check Browser Console

1. Open http://localhost:5173 in your browser
2. Press **F12** or **Right-click → Inspect**
3. Go to the **Console** tab
4. Look for any **red error messages**

### Common Console Errors:

#### Error: "Failed to fetch" or CORS error
**Solution**: Make sure backend is running on port 8000
```bash
# In backend terminal
uvicorn main:app --reload --port 8000
```

#### Error: "Cannot find module" or import errors
**Solution**: Reinstall dependencies
```bash
cd frontend
npm install
```

#### Error: "Unexpected token" or syntax error
**Solution**: Clear cache and restart
```bash
# Stop the dev server (Ctrl+C)
# Delete node_modules/.vite folder
Remove-Item -Recurse -Force node_modules\.vite
# Restart
npm run dev
```

---

## ✅ Step 2: Verify Frontend Server is Running

Check your terminal where you ran `npm run dev`. You should see:

```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### If you don't see this:

1. **Stop the server** (Ctrl+C)
2. **Clear the cache**:
   ```bash
   Remove-Item -Recurse -Force node_modules\.vite
   ```
3. **Restart**:
   ```bash
   npm run dev
   ```

---

## ✅ Step 3: Verify Backend Server is Running

Check your backend terminal. You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Test backend is working:
Open http://localhost:8000/health in your browser

You should see:
```json
{"status":"healthy"}
```

If you get an error, restart the backend:
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

---

## ✅ Step 4: Check Port Conflicts

### Frontend Port (5173) in use?
```bash
# Kill process on port 5173 (Windows)
netstat -ano | findstr :5173
# Note the PID number, then:
taskkill /PID <PID_NUMBER> /F

# Then restart
npm run dev
```

### Backend Port (8000) in use?
```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
# Note the PID number, then:
taskkill /PID <PID_NUMBER> /F

# Then restart
uvicorn main:app --reload --port 8000
```

---

## ✅ Step 5: Complete Fresh Start

If nothing works, do a complete fresh start:

### 1. Stop Everything
- Press **Ctrl+C** in both terminals (frontend and backend)

### 2. Clear Frontend Cache
```bash
cd frontend
Remove-Item -Recurse -Force node_modules\.vite
Remove-Item -Recurse -Force dist
```

### 3. Reinstall Frontend Dependencies (if needed)
```bash
npm install
```

### 4. Restart Backend
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

Wait for: `INFO: Application startup complete.`

### 5. Restart Frontend
Open a new terminal:
```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:5173/`

### 6. Open Browser
- Go to http://localhost:5173
- **Hard refresh**: Press **Ctrl+Shift+R** (or Ctrl+F5)

---

## ✅ Step 6: Check Browser Compatibility

### Recommended Browsers:
- ✅ **Google Chrome** (recommended)
- ✅ **Microsoft Edge**
- ✅ **Firefox**

### Not Recommended:
- ❌ Internet Explorer
- ⚠️ Safari (may have issues)

---

## ✅ Step 7: Check Network Tab

1. Open browser DevTools (F12)
2. Go to **Network** tab
3. Refresh the page (Ctrl+R)
4. Look for failed requests (red items)

### Common Issues:

#### main.jsx fails to load
**Solution**: Clear cache and hard refresh (Ctrl+Shift+R)

#### index.css fails to load
**Solution**: Restart Vite dev server

#### API calls fail (process-audio)
**Solution**: Check backend is running on port 8000

---

## ✅ Step 8: Verify File Structure

Make sure you have these files:

```
frontend/
├── index.html          ✓
├── package.json        ✓
├── vite.config.js      ✓
├── tailwind.config.js  ✓
├── postcss.config.js   ✓
└── src/
    ├── main.jsx        ✓
    ├── App.jsx         ✓
    ├── index.css       ✓
    └── App.css         ✓
```

---

## ✅ Step 9: Check for JavaScript Errors

Open browser console (F12) and look for:

### "Uncaught SyntaxError"
**Solution**: 
```bash
npm install
npm run dev
```

### "Failed to resolve module"
**Solution**:
```bash
Remove-Item -Recurse -Force node_modules
npm install
npm run dev
```

### "Cannot read property of undefined"
**Solution**: Check if backend is running and returning data

---

## ✅ Step 10: Nuclear Option - Complete Reinstall

If NOTHING works:

### 1. Backup your .env file
```bash
copy backend\.env backend\.env.backup
```

### 2. Delete node_modules
```bash
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item -Recurse -Force node_modules\.vite
Remove-Item -Recurse -Force dist
```

### 3. Reinstall everything
```bash
npm install
```

### 4. Restart both servers
```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 5. Open browser with hard refresh
- Go to http://localhost:5173
- Press **Ctrl+Shift+R**

---

## 📞 Still Not Working?

### Check these:

1. ✅ Node.js version: `node --version` (should be 16+)
2. ✅ npm version: `npm --version` (should be 8+)
3. ✅ Python version: `python --version` (should be 3.8+)
4. ✅ Both terminals are open and running
5. ✅ No firewall blocking ports 5173 or 8000
6. ✅ Antivirus not blocking the servers

### Get Detailed Logs:

**Frontend logs:**
```bash
npm run dev -- --debug
```

**Backend logs:**
```bash
uvicorn main:app --reload --port 8000 --log-level debug
```

---

## 🎯 Most Common Solution

**90% of the time, this fixes it:**

1. **Hard refresh** the browser: **Ctrl+Shift+R**
2. **Clear browser cache**: Settings → Clear browsing data
3. **Restart both servers**:
   - Stop with Ctrl+C
   - Start again with the 3+2 commands

---

## ✅ Expected Behavior

When everything works, you should see:

1. **Backend terminal**: `INFO: Application startup complete.`
2. **Frontend terminal**: `Local: http://localhost:5173/`
3. **Browser**: Dark themed interface with "VoiceBot AI" header and a microphone button
4. **Console**: No red errors (F12 → Console tab)

---

## 📝 Quick Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Browser console has no errors (F12)
- [ ] Hard refreshed browser (Ctrl+Shift+R)
- [ ] Using Chrome or Edge browser
- [ ] Both terminals are still open
- [ ] No firewall/antivirus blocking

If all checked ✅ and still blank, share the **console errors** (F12 → Console) for more help!
