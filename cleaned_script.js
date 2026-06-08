
    

    // --- DATA LAYER ---
        const DEFAULT_FOODS = [
      { id: 1, name: "Berry Oatmeal", kcal: 400, p: 18, c: 54, f: 15, img: "data:image/png;base64,...[TRUNCATED]...", fallback: "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=200" },
      { id: 2, name: "Grilled Chicken Bowl", kcal: 560, p: 38, c: 62, f: 16, img: "data:image/png;base64,...[TRUNCATED]...", fallback: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=200" },
      { id: 3, name: "Blueberry Smoothie", kcal: 230, p: 10, c: 32, f: 6, img: "data:image/png;base64,...[TRUNCATED]...", fallback: "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=200" },
      { id: 4, name: "Avocado Toast", kcal: 310, p: 9, c: 30, f: 17, img: "data:image/png;base64,...[TRUNCATED]...", fallback: "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2?w=200" },
      { id: 5, name: "Baked Salmon", kcal: 380, p: 42, c: 8, f: 22, img: "data:image/png;base64,...[TRUNCATED]...", fallback: "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=200" },
      { id: 6, name: "Caesar Salad", kcal: 290, p: 14, c: 18, f: 19, img: "data:image/png;base64,...[TRUNCATED]...", fallback: "https://images.unsplash.com/photo-1512852939750-1305098529bf?w=200" },
      { id: 7, name: "Banana Pancakes", kcal: 340, p: 12, c: 52, f: 10, img: "data:image/png;base64,...[TRUNCATED]...", fallback: "https://images.unsplash.com/photo-1528207776546-365bb710ee93?w=200" },
      { id: 8, name: "Greek Yogurt Bowl", kcal: 220, p: 20, c: 28, f: 4, img: "data:image/png;base64,...[TRUNCATED]...", fallback: "https://images.unsplash.com/photo-1488477181228-c84b34b8e007?w=200" },
      { id: 9, name: "Quinoa Power Bowl", kcal: 420, p: 16, c: 58, f: 14, img: "data:image/png;base64,...[TRUNCATED]...", fallback: "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=200" },
      { id: 10, name: "Veggie Stir Fry", kcal: 280, p: 11, c: 38, f: 9, img: "data:image/png;base64,...[TRUNCATED]...", fallback: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=200" }
    ];

    const GOALS = { kcal: 2200, p: 150, c: 200, f: 65 };

    function initDB() {
      // Force clear old localstorage cache once to ensure new Base64 images are loaded
      if (!localStorage.getItem('foods_base64_v11')) {
        localStorage.clear();
        localStorage.setItem('foods_base64_v11', 'true');
      }

      // Force update foods to load the new local images automatically
      localStorage.setItem('foods', JSON.stringify(DEFAULT_FOODS));
      
      let logs = localStorage.getItem('logs') ? JSON.parse(localStorage.getItem('logs')) : [];
      if (!Array.isArray(logs)) {
        logs = [];
      }
      // Clean null or corrupted entries
      logs = logs.filter(l => l && typeof l === 'object');

      if (logs.length === 0) {
        // Pre-populate with exactly the 5 logs to match the Meal History screenshot
        const today = new Date();
        
        const d1 = new Date(today); d1.setHours(8, 30, 0, 0); // 08:30 AM
        const d2 = new Date(today); d2.setHours(12, 45, 0, 0); // 12:45 PM
        const d3 = new Date(today); d3.setHours(15, 15, 0, 0); // 03:15 PM
        const d4 = new Date(today); d4.setHours(17, 0, 0, 0);  // 05:00 PM
        const d5 = new Date(today); d5.setHours(19, 30, 0, 0); // 07:30 PM
        
        logs = [
          { ...DEFAULT_FOODS[0], date: d1.toISOString() },
          { ...DEFAULT_FOODS[1], date: d2.toISOString() },
          { ...DEFAULT_FOODS[2], date: d3.toISOString() },
          { ...DEFAULT_FOODS[3], date: d4.toISOString() },
          { ...DEFAULT_FOODS[4], date: d5.toISOString() }
        ];
        localStorage.setItem('logs', JSON.stringify(logs));
      } else {
        // Map and update fallback URLs based on name matches
        let updated = false;
        const normalizeName = (name) => {
          if (!name) return "";
          return name.toLowerCase().replace(/_/g, " ").trim();
        };

        logs = logs.map(l => {
          // Validate date
          if (!l.date || isNaN(new Date(l.date).getTime())) {
            l.date = new Date().toISOString();
            updated = true;
          }
          
          // Normalize name and find match
          const matchingFood = DEFAULT_FOODS.find(f => normalizeName(f.name) === normalizeName(l.name));
          if (matchingFood) {
            // Update image to base64 if it's currently a relative path or not matching
            if (l.img !== matchingFood.img || !l.img.startsWith('data:image')) {
              l.img = matchingFood.img;
              l.fallback = 'meal_0.png';
              updated = true;
            }
            // Ensure nutrient values are valid numbers
            if (typeof l.kcal !== 'number') { l.kcal = matchingFood.kcal; updated = true; }
            if (typeof l.p !== 'number') { l.p = matchingFood.p; updated = true; }
            if (typeof l.c !== 'number') { l.c = matchingFood.c; updated = true; }
            if (typeof l.f !== 'number') { l.f = matchingFood.f; updated = true; }
          } else {
            // If it's a legacy entry without matching food, verify it has essential fields
            if (!l.img || !l.img.startsWith('data:image') || typeof l.kcal !== 'number') {
              const defaultFood = DEFAULT_FOODS[0];
              l.name = defaultFood.name;
              l.img = defaultFood.img;
              l.fallback = 'meal_0.png';
              l.kcal = defaultFood.kcal;
              l.p = defaultFood.p;
              l.c = defaultFood.c;
              l.f = defaultFood.f;
              updated = true;
            }
          }
          return l;
        });

        if (updated) {
          localStorage.setItem('logs', JSON.stringify(logs));
        }
      }
    }
    initDB();

    function safeDateString(dateVal) {
      if (!dateVal) return "Unknown Date";
      const d = new Date(dateVal);
      return isNaN(d.getTime()) ? "Unknown Date" : d.toDateString();
    }

    function safeTimeString(dateVal) {
      if (!dateVal) return "00:00";
      const d = new Date(dateVal);
      return isNaN(d.getTime()) ? "00:00" : d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }

    function safeDateTimeString(dateVal) {
      if (!dateVal) return "Unknown Time";
      const d = new Date(dateVal);
      return isNaN(d.getTime()) ? "Unknown Time" : d.toLocaleString([], {month:'short', day:'numeric', hour: '2-digit', minute:'2-digit'});
    }

    function getMealType(dateVal) {
      if (!dateVal) return "Meal";
      const d = new Date(dateVal);
      if (isNaN(d.getTime())) return "Meal";
      const hour = d.getHours();
      if (hour >= 5 && hour < 11) return "Breakfast";
      if (hour >= 11 && hour < 15) return "Lunch";
      if (hour >= 15 && hour < 19) return "Snack";
      return "Dinner";
    }

    function getFoods() { return JSON.parse(localStorage.getItem('foods')) || []; }
    function getLogs() { return JSON.parse(localStorage.getItem('logs')) || []; }
    function saveLog(log) {
      const logs = getLogs();
      logs.unshift(log);
      localStorage.setItem('logs', JSON.stringify(logs));
      updateDashboard();
      renderHistory();
    }

    // --- ROUTING ---
    function handleRoute() {
      const hash = window.location.hash || '#dashboard';
      document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      
      const targetScreen = document.getElementById('screen-' + hash.replace('#', ''));
      if(targetScreen) targetScreen.classList.add('active');
      
      const targetNav = document.getElementById('nav-' + hash.replace('#', ''));
      if(targetNav) targetNav.classList.add('active');

      const fab = document.getElementById('fab-scan');
      if (fab) {
        if(hash === '#dashboard') fab.style.display = 'flex';
        else fab.style.display = 'none';
      }
      
      if(hash === '#dashboard') updateDashboard();
      if(hash === '#history') renderHistory();
      if(hash === '#admin') renderAdmin();
      
      // Stop camera if leaving scanner
      if(hash !== '#scanner' && window.localStream) {
        window.localStream.getTracks().forEach(track => track.stop());
        document.getElementById('camera-stream').srcObject = null;
      } else if (hash === '#scanner') {
        startCamera();
        const defaultFood = DEFAULT_FOODS.find(f => f.id === 2) || DEFAULT_FOODS[1];
        pendingScan = { ...defaultFood, date: new Date().toISOString() };
        
        const previewImg = document.getElementById('scanned-img-preview');
        previewImg.src = defaultFood.img;
        previewImg.style.display = 'block';
        
        const resImg = document.getElementById('res-img');
        resImg.src = defaultFood.img;
        document.getElementById('res-name').innerText = defaultFood.name;
        document.getElementById('res-cal').innerText = defaultFood.kcal;
        document.getElementById('res-p').innerText = defaultFood.p + 'g';
        document.getElementById('res-c').innerText = defaultFood.c + 'g';
        document.getElementById('res-f').innerText = defaultFood.f + 'g';
        
        const pPercent = defaultFood.kcal > 0 ? Math.round((defaultFood.p * 4 / defaultFood.kcal) * 100) : 0;
        const cPercent = defaultFood.kcal > 0 ? Math.round((defaultFood.c * 4 / defaultFood.kcal) * 100) : 0;
        const fPercent = defaultFood.kcal > 0 ? Math.round((defaultFood.f * 9 / defaultFood.kcal) * 100) : 0;
        document.getElementById('res-p-pct').innerText = 'P ' + pPercent + '%';
        document.getElementById('res-c-pct').innerText = 'C ' + cPercent + '%';
        document.getElementById('res-f-pct').innerText = 'F ' + fPercent + '%';
        
        document.getElementById('scan-result').classList.add('show');
        document.getElementById('scanner-laser').style.display = 'block';
      }
    }
    window.addEventListener('hashchange', handleRoute);

    // --- DASHBOARD ---
    function updateDashboard() {
      const logs = getLogs();
      // Filter for today
      const todayLogs = logs.filter(l => safeDateString(l.date) === safeDateString(new Date()));
      
      let tKcal = 0, tP = 0, tC = 0, tF = 0;
      todayLogs.forEach(l => { tKcal += l.kcal; tP += l.p; tC += l.c; tF += l.f; });
      
      // Update rings
      const setRing = (id, val, max, maxOffset) => {
        const ring = document.getElementById(id);
        const percent = Math.min(val / max, 1);
        ring.style.strokeDashoffset = maxOffset - (maxOffset * percent);
      };
      
      setRing('main-ring', tKcal, GOALS.kcal, 700);
      document.getElementById('dash-remaining').innerText = Math.max(0, GOALS.kcal - tKcal);
      document.getElementById('dash-consumed').innerText = `${tKcal.toLocaleString()} kcal consumed`;
      
      setRing('ring-p', tP, GOALS.p, 160); document.getElementById('val-p').innerText = tP;
      setRing('ring-c', tC, GOALS.c, 160); document.getElementById('val-c').innerText = tC;
      setRing('ring-f', tF, GOALS.f, 160); document.getElementById('val-f').innerText = tF;
      
      // Recent Meals
      const list = document.getElementById('dash-recent-meals');
      list.innerHTML = '';
      todayLogs.slice(0, 3).forEach(l => {
        const timeStr = safeTimeString(l.date);
        list.innerHTML += `
          <div class="meal-card">
            <img src="${l.img}" onerror="this.onerror=null; this.src='${l.fallback || 'meal_0.png'}';" class="meal-img">
            <div class="meal-info">
              <div class="meal-name">${l.name}</div>
              <div class="meal-meta">${getMealType(l.date)} • ${timeStr}</div>
            </div>
            <div class="meal-cal">${l.kcal} <span style="color:var(--text-dim)"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></span></div>
          </div>
        `;
      });
      if(todayLogs.length === 0) {
        list.innerHTML = '<p style="color:var(--text-dim); font-size:12px; padding: 10px;">No meals logged today.</p>';
      }
      
    }

    // --- SCANNER ---
    let pendingScan = null;

    async function startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        document.getElementById('camera-stream').srcObject = stream;
        window.localStream = stream;
      } catch (err) {
        console.log("Camera access denied or unavailable", err);
      }
    }

    document.getElementById('file-upload').addEventListener('change', function(e) {
      if(e.target.files && e.target.files[0]) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          const img = document.getElementById('scanned-img-preview');
          img.src = evt.target.result;
          img.style.display = 'block';
          simulateScan(evt.target.result);
        }
        reader.readAsDataURL(e.target.files[0]);
      }
    });

    function simulateScan(imgSrc) {
      setTimeout(() => {
        
        // Pick a random food from DB
        const foods = getFoods();
        const food = foods[Math.floor(Math.random() * foods.length)];
        
        pendingScan = { ...food, img: imgSrc || food.img, date: new Date().toISOString() };
        
        const resImg = document.getElementById('res-img');
        resImg.src = pendingScan.img;
        resImg.onerror = function() {
          this.onerror = null;
          if (pendingScan && pendingScan.fallback) {
            this.src = pendingScan.fallback;
          }
        };
        document.getElementById('res-name').innerText = pendingScan.name;
        document.getElementById('res-cal').innerText = pendingScan.kcal;
        document.getElementById('res-p').innerText = pendingScan.p + 'g';
        document.getElementById('res-c').innerText = pendingScan.c + 'g';
        document.getElementById('res-f').innerText = pendingScan.f + 'g';
        
        const pPercent = pendingScan.kcal > 0 ? Math.round((pendingScan.p * 4 / pendingScan.kcal) * 100) : 0;
        const cPercent = pendingScan.kcal > 0 ? Math.round((pendingScan.c * 4 / pendingScan.kcal) * 100) : 0;
        const fPercent = pendingScan.kcal > 0 ? Math.round((pendingScan.f * 9 / pendingScan.kcal) * 100) : 0;
        document.getElementById('res-p-pct').innerText = 'P ' + pPercent + '%';
        document.getElementById('res-c-pct').innerText = 'C ' + cPercent + '%';
        document.getElementById('res-f-pct').innerText = 'F ' + fPercent + '%';
        
        document.getElementById('scan-result').classList.add('show');
        
        // Scroll to result
        document.getElementById('screen-scanner').scrollTop = document.getElementById('screen-scanner').scrollHeight;
      }, 1500);
    }

    document.getElementById('btn-save-log').addEventListener('click', () => {
      if(pendingScan) {
        saveLog(pendingScan);
        pendingScan = null;
        window.location.hash = '#dashboard';
      }
    });

    // --- HISTORY ---
    let currentTab = 'today';
    function setTab(tab) {
      currentTab = tab;
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      event.target.classList.add('active');
      renderHistory();
    }

    function renderHistory() {
      const logs = getLogs();
      let filtered = [];
      const now = new Date();
      
      if(currentTab === 'today') {
        filtered = logs.filter(l => safeDateString(l.date) === safeDateString(now));
      } else if(currentTab === 'week') {
        const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        filtered = logs.filter(l => { const d = new Date(l.date); return !isNaN(d.getTime()) && d >= weekAgo; });
      } else {
        filtered = logs;
      }

      let tKcal = 0;
      filtered.forEach(l => tKcal += l.kcal);
      
      document.getElementById('hist-consumed').innerText = tKcal.toLocaleString();
      document.getElementById('hist-remaining').innerText = Math.max(0, GOALS.kcal - tKcal).toLocaleString();

      const list = document.getElementById('history-list');
      list.innerHTML = '';
      filtered.forEach(l => {
        const timeStr = safeTimeString(l.date);
        list.innerHTML += `
          <div class="history-card">
            <img src="${l.img}" onerror="this.onerror=null; this.src='${l.fallback || 'meal_0.png'}';">
            <div class="h-info">
              <div class="h-title">${l.name}</div>
              <div class="h-meta">${getMealType(l.date)} • ${timeStr}</div>
              <div class="h-macros">P: ${l.p}g &nbsp;•&nbsp; C: ${l.c}g &nbsp;•&nbsp; F: ${l.f}g</div>
            </div>
            <div class="h-cal">
              <span class="h-cal-val">${l.kcal}</span>
              <span class="h-cal-lbl">kcal</span>
            </div>
          </div>
        `;
      });
      if(filtered.length === 0) {
        list.innerHTML = '<p style="text-align:center; color:var(--text-dim); margin-top: 40px;">No meals found.</p>';
      }
    }

    // --- ADMIN ---
    function checkAdmin() {
      const pwd = document.getElementById('admin-pwd').value;
      if(pwd === 'admin123') {
        document.getElementById('admin-login').style.display = 'none';
        document.getElementById('admin-panel').style.display = 'block';
        renderAdmin();
      } else {
        alert("Incorrect password");
      }
    }

    function renderAdmin() {
      // populate food table
      const foods = getFoods();
      const fTable = document.querySelector('#admin-food-table tbody');
      fTable.innerHTML = '';
      foods.forEach(f => {
        fTable.innerHTML += `<tr><td>${f.name}</td><td>${f.kcal}</td><td>${f.p}</td><td>${f.c}</td><td>${f.f}</td><td><button class="admin-btn">Edit</button></td></tr>`;
      });

      // populate log table
      const logs = getLogs();
      const lTable = document.querySelector('#admin-log-table tbody');
      lTable.innerHTML = '';
      logs.forEach(l => {
        const timeStr = safeDateTimeString(l.date);
        lTable.innerHTML += `<tr><td>${timeStr}</td><td>${l.name}</td><td>${l.kcal}</td></tr>`;
      });
    }

    function resetDB() {
      localStorage.setItem('foods', JSON.stringify(DEFAULT_FOODS));
      renderAdmin();
      alert("Database reset to defaults.");
    }

    function clearLogs() {
      if(confirm("Are you sure you want to clear all user logs?")) {
        localStorage.setItem('logs', JSON.stringify([]));
        renderAdmin();
      }
    }

    // --- THEME TOGGLE ---
    function toggleTheme() {
      const app = document.getElementById('app');
      const isLight = app.classList.toggle('light-theme');
      document.body.classList.toggle('light-theme', isLight);
      localStorage.setItem('theme', isLight ? 'light' : 'dark');
    }

    // Restore saved theme on load
    (function restoreTheme() {
      const saved = localStorage.getItem('theme');
      if (saved === 'light') {
        document.getElementById('app').classList.add('light-theme');
        document.body.classList.add('light-theme');
      }
    })();

    // Initial render
    handleRoute();

  