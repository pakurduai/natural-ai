import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Remove feather script
content = content.replace('<script src="https://unpkg.com/feather-icons"></script>', '')
content = content.replace('feather.replace();', '')

# Icons SVGs
svg_leaf = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13v-5a2 2 0 0 1 2-2h5a7 7 0 0 1 7 7v0a7 7 0 0 1-7 7Z"></path><path d="M11 20V10"></path></svg>'
svg_bell = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>'
svg_user = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>'
svg_drop = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path></svg>'
svg_home = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>'
svg_scan = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7V5a2 2 0 0 1 2-2h2"></path><path d="M17 3h2a2 2 0 0 1 2 2v2"></path><path d="M21 17v2a2 2 0 0 1-2 2h-2"></path><path d="M7 21H5a2 2 0 0 1-2-2v-2"></path></svg>'
svg_meals = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>'
svg_pie = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>'
svg_moon = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>'
svg_chevron = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>'
svg_arrow = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>'
svg_help = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>'
svg_image = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>'
svg_check = '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>'
svg_save = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>'
svg_lock = '<svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>'

content = content.replace('<i data-feather="feather" class="brand-icon"></i>', f'<span class="brand-icon">{svg_leaf}</span>')
content = content.replace('<i data-feather="bell"></i>', svg_bell)
content = content.replace('<i data-feather="user"></i>', svg_user)
content = content.replace('<i data-feather="droplet" style="width:18px; height:18px;"></i>', svg_drop)
content = content.replace('<i data-feather="home"></i>', svg_home)
content = content.replace('<i data-feather="maximize"></i>', svg_scan)
content = content.replace('<i data-feather="list"></i>', svg_meals)
content = content.replace('<i data-feather="pie-chart" style="color:var(--accent)"></i>', f'<span style="color:var(--accent)">{svg_pie}</span>')
content = content.replace('<i data-feather="moon" style="color:var(--text-dim)"></i>', f'<span style="color:var(--text-dim)">{svg_moon}</span>')
content = content.replace('<i data-feather="chevron-right" style="width:16px; color:var(--text-dim)"></i>', f'<span style="color:var(--text-dim)">{svg_chevron}</span>')
content = content.replace('<i data-feather="arrow-left"></i>', svg_arrow)
content = content.replace('<i data-feather="help-circle" style="color:var(--text-dim)"></i>', f'<span style="color:var(--text-dim)">{svg_help}</span>')
content = content.replace('<i data-feather="image"></i>', svg_image)
content = content.replace('<i data-feather="check-circle" style="width:12px; height:12px;"></i>', svg_check)
content = content.replace('<i data-feather="save"></i>', svg_save)
content = content.replace('<i data-feather="lock" style="width:48px; height:48px; color:var(--text-dim)"></i>', f'<span style="color:var(--text-dim)">{svg_lock}</span>')

# Fix FAB vs Scan Button
# Remove FAB from dashboard
content = re.sub(r'<!-- Floating Action Button for Scan -->.*?</a>', '', content, flags=re.DOTALL)
content = re.sub(r'<a href="#scanner" id="fab-scan".*?</a>', '', content, flags=re.DOTALL)

# Add SCAN FOOD button below Recent Meals
scan_btn = f'''
<div style="padding: 0 20px; margin-bottom: 30px;">
  <a href="#scanner" class="btn-primary" style="text-decoration: none;">
    {svg_scan} SCAN FOOD
  </a>
</div>
'''
content = content.replace('</div>\n    </div>\n\n    <!-- SCANNER SCREEN -->', f'</div>\n{scan_btn}\n    </div>\n\n    <!-- SCANNER SCREEN -->')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated index.html to use inline SVGs and correct buttons.")
