import os, re

with open('index.html','r',encoding='utf-8') as f: h=f.read()
print(f"Starting: {len(h)} chars")

# ── FEATURE 1: Throw button dominant ─────────────────────────────────────────
THROW_BTN = (
    '<button id="btn-throw" style="width:100%;padding:22px;border-radius:20px;border:none;'
    'background:var(--gold);color:var(--black);font-family:var(--sans);font-size:20px;'
    'font-weight:700;letter-spacing:0.06em;text-transform:uppercase;display:flex;'
    'align-items:center;justify-content:center;gap:14px;'
    'box-shadow:0 8px 40px rgba(229,180,68,0.5);cursor:pointer;">'
    '<span style="font-size:28px;">\u2744\ufe0f</span> Throw It Into the World</button>'
    '<div style="display:flex;gap:8px;margin-top:10px;">'
    '<button id="btn-home" style="flex:1;padding:12px 4px;border-radius:13px;border:1px solid var(--dim2);background:rgba(255,255,255,0.03);display:flex;align-items:center;justify-content:center;cursor:pointer;"><span style="font-size:18px;">\U0001f3e0</span></button>'
    '<button id="btn-roll" style="flex:1;padding:12px 4px;border-radius:13px;border:1px solid var(--dim2);background:rgba(255,255,255,0.03);display:flex;align-items:center;justify-content:center;cursor:pointer;"><span style="font-size:18px;">\U0001f501</span></button>'
    '<button id="btn-cap" style="flex:1;padding:12px 4px;border-radius:13px;border:1px solid var(--dim2);background:rgba(255,255,255,0.03);display:flex;align-items:center;justify-content:center;cursor:pointer;"><span style="font-size:18px;">\U0001f4cb</span></button>'
    '<button id="btn-record" style="flex:1;padding:12px 4px;border-radius:13px;border:1px solid var(--dim2);background:rgba(255,255,255,0.03);display:flex;align-items:center;justify-content:center;cursor:pointer;"><span style="font-size:18px;">\U0001f3ac</span></button>'
    '</div>'
)

idx = h.find('<button id="btn-throw"')
if idx > 0:
    container_start = h.rfind('<div style="display:flex;gap:', 0, idx)
    btn_end_marker = h.find('</div>', h.find('Throw It', idx))
    # find the end of outer container
    outer_end = h.find('</div>', btn_end_marker + 1) + 6
    if container_start > 0:
        h = h[:container_start] + THROW_BTN + h[outer_end:]
        print("Feature 1: Throw button DONE")
    else:
        print("Feature 1: using fallback")
        end = h.find('</button>', idx) + 9
        h = h[:idx] + THROW_BTN + h[end:]
else:
    print("Feature 1: btn-throw not found")

# ── FEATURE 2: Hook fade after 4s ────────────────────────────────────────────
if 'hook-overlay' not in h:
    h = h.replace(
        'padding:80px 32px 220px;text-align:center;pointer-events:none;"',
        'padding:80px 32px 220px;text-align:center;pointer-events:none;" id="hook-overlay"'
    )
    print("Feature 2a: hook-overlay id added")

if 'hookFaded' not in h:
    OLD_PLAY = "playBtn.onclick=()=>{"
    NEW_PLAY = (
        "later(()=>{"
        "const ho=document.getElementById('hook-overlay');"
        "if(ho){ho.style.transition='opacity 1.2s ease';ho.style.opacity='0';}"
        "},4000);\n"
        "playBtn.onclick=()=>{"
    )
    if OLD_PLAY in h:
        h = h.replace(OLD_PLAY, NEW_PLAY)
        print("Feature 2b: Hook fade DONE")
    else:
        print("Feature 2b: playBtn not found")

# ── FEATURE 3: 6 scenes ───────────────────────────────────────────────────────
if 'aftermath' not in h:
    six_scenes = (
        '"scenes":['
        '{"beat":"opening - establish world","imagePrompt":"Specific cinematic moment. 35mm film dramatic natural lighting photorealistic no text."},'
        '{"beat":"tension begins","imagePrompt":"Specific cinematic moment. 35mm film dramatic natural lighting photorealistic no text."},'
        '{"beat":"conflict peak","imagePrompt":"Specific cinematic moment. 35mm film dramatic natural lighting photorealistic no text."},'
        '{"beat":"turning point","imagePrompt":"Specific cinematic moment. 35mm film dramatic natural lighting photorealistic no text."},'
        '{"beat":"resolution","imagePrompt":"Specific cinematic moment. 35mm film dramatic natural lighting photorealistic no text."},'
        '{"beat":"aftermath","imagePrompt":"Specific cinematic moment. 35mm film dramatic natural lighting photorealistic no text."}]'
    )
    h = re.sub(r'"scenes":\[(?:\{"beat":"[^"]*","imagePrompt":"[^"]*"\},?){1,4}\]', six_scenes, h, count=1)
    print("Feature 3: 6 scenes DONE:", "aftermath" in h)

# ── FEATURE 4: History & streak ───────────────────────────────────────────────
if 'getHistory' not in h:
    HIST = (
        "\nfunction getHistory(){"
        "try{return JSON.parse(localStorage.getItem('sb_history')||'[]');}"
        "catch(e){return [];}}\n"

        "function saveToHistory(s){"
        "var hist=getHistory();"
        "var e={id:Date.now(),date:new Date().toISOString(),"
        "hook:s.hook,location:s.location,caption:s.caption,"
        "images:s.images,audioUrl:s.audioUrl,shared:false};"
        "hist.unshift(e);if(hist.length>50)hist.pop();"
        "localStorage.setItem('sb_history',JSON.stringify(hist));"
        "return e;}\n"

        "function getStreak(){"
        "var hist=getHistory();if(!hist.length)return 0;"
        "var days=new Set(hist.map(function(h){return h.date.slice(0,10);}));"
        "var streak=0;var d=new Date();"
        "for(var i=0;i<365;i++){"
        "var ds=d.toISOString().slice(0,10);"
        "if(days.has(ds)){streak++;d.setDate(d.getDate()-1);}else break;}"
        "return streak;}\n"

        "function renderHistory(app){"
        "app.style.background='#0B0906';"
        "var hist=getHistory();"
        "var wrap=document.createElement('div');"
        "wrap.style.cssText='position:absolute;inset:0;display:flex;flex-direction:column;overflow:hidden;';"
        "app.appendChild(wrap);"
        "var hdr=document.createElement('div');"
        "hdr.style.cssText='padding:52px 24px 16px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;';"
        "hdr.innerHTML='<button id=\"hback\" style=\"color:var(--muted);font-family:var(--sans);font-size:13px;background:none;border:none;cursor:pointer;\">\u2190 Back</button>"
        "<div style=\"font-family:var(--serif);font-size:19px;font-weight:600;color:var(--cream);\">snow<span style=\"color:var(--gold);\">\u25cf</span>ball</div>"
        "<div style=\"width:50px;\"></div>';"
        "wrap.appendChild(hdr);"
        "document.getElementById('hback').onclick=function(){go('home');};"
        "var streak=getStreak();"
        "var shared=hist.filter(function(h){return h.shared;}).length;"
        "var stats=document.createElement('div');"
        "stats.style.cssText='padding:0 24px 16px;display:flex;gap:12px;flex-shrink:0;';"
        "[['\u2744\ufe0f',streak+' day streak'],['\U0001f4d6',hist.length+' stories'],['\U0001f4e4',shared+' shared']]"
        ".forEach(function(item){"
        "var d=document.createElement('div');"
        "d.style.cssText='flex:1;background:rgba(255,255,255,0.04);border:1px solid var(--dim2);border-radius:14px;padding:12px 8px;display:flex;flex-direction:column;align-items:center;gap:4px;';"
        "d.innerHTML='<span style=\"font-size:20px;\">'+item[0]+'</span>"
        "<span style=\"font-family:var(--sans);font-size:11px;color:var(--muted);text-align:center;\">'+item[1]+'</span>';"
        "stats.appendChild(d);});"
        "wrap.appendChild(stats);"
        "var list=document.createElement('div');"
        "list.style.cssText='flex:1;overflow-y:auto;padding:0 20px 40px;display:flex;flex-direction:column;gap:10px;';"
        "wrap.appendChild(list);"
        "if(!hist.length){"
        "list.innerHTML='<div style=\"font-family:var(--serif);font-size:18px;font-style:italic;color:var(--muted);text-align:center;margin-top:60px;\">No stories yet. Tell your first one.</div>';"
        "}else{"
        "hist.forEach(function(entry){"
        "var card=document.createElement('div');"
        "card.style.cssText='background:rgba(255,255,255,0.03);border:1px solid var(--dim2);border-radius:16px;overflow:hidden;display:flex;cursor:pointer;min-height:80px;';"
        "var thumb=document.createElement('div');"
        "thumb.style.cssText='width:80px;flex-shrink:0;background:#1a1410;position:relative;overflow:hidden;';"
        "if(entry.images&&entry.images[0]){"
        "var ti=document.createElement('img');ti.src=entry.images[0];"
        "ti.style.cssText='width:100%;height:100%;object-fit:cover;';"
        "thumb.appendChild(ti);}"
        "var info=document.createElement('div');"
        "info.style.cssText='flex:1;padding:14px;display:flex;flex-direction:column;justify-content:center;gap:4px;overflow:hidden;';"
        "var hookEl=document.createElement('div');"
        "hookEl.style.cssText='font-family:var(--serif);font-size:15px;font-style:italic;color:var(--cream);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;';"
        "hookEl.textContent=entry.hook||'Untitled';"
        "var metaEl=document.createElement('div');"
        "metaEl.style.cssText='font-family:var(--sans);font-size:10px;color:var(--muted);';"
        "var dd=new Date(entry.date);"
        "metaEl.textContent=dd.toLocaleDateString('en-US',{month:'short',day:'numeric'})+(entry.shared?' \u00b7 Shared':'');"
        "info.appendChild(hookEl);info.appendChild(metaEl);"
        "card.appendChild(thumb);card.appendChild(info);"
        "card.onclick=function(){story=entry;go('playback');};"
        "list.appendChild(card);});}}\n"
    )
    h = h.replace("function render(){", HIST + "\nfunction render(){")
    print("Feature 4: History DONE")

# ── FEATURE 5: Wire history route + real streak ───────────────────────────────
if 'history:renderHistory' not in h:
    h = h.replace(
        '{home:renderHome,type:renderType,speak:renderSpeak,photos:renderPhotos,building:renderBuilding,playback:renderPlayback,error:renderError}',
        '{home:renderHome,type:renderType,speak:renderSpeak,photos:renderPhotos,history:renderHistory,building:renderBuilding,playback:renderPlayback,error:renderError}'
    )
    print("Feature 5a: History route DONE")

# Make streak badge real + tappable
if 'getStreak()' not in h:
    h = h.replace(
        '>3 day streak<',
        '>${getStreak()} day streak<'
    )
    h = h.replace(
        'border-radius:20px;padding:6px 13px;">',
        'border-radius:20px;padding:6px 13px;cursor:pointer;" onclick="go(\'history\')">'
    )
    print("Feature 5b: Real streak DONE")

# ── FEATURE 6: Auto-save to history ──────────────────────────────────────────
if 'saveToHistory' in h:
    for old in [
        "story={...shaped,images,audioUrl};later(()=>go('playback'),600);",
        "story=Object.assign({},shaped,{images:images,audioUrl:audioUrl});later(()=>go('playback'),600);"
    ]:
        if old in h and h.count('saveToHistory(story)') < 2:
            h = h.replace(old, old.replace("later(", "saveToHistory(story);later("), 1)
            print("Feature 6: Auto-save DONE")

# ── WRITE SAFELY ─────────────────────────────────────────────────────────────
with open('index.html.new','w',encoding='utf-8') as f: f.write(h)
os.replace('index.html.new','index.html')
print(f"\nFinal: {len(h)} chars")
print("Throw dominant:", "Throw It Into the World" in h)
print("Hook fade:", "hook-overlay" in h)
print("6 scenes:", "aftermath" in h)
print("History:", "getHistory" in h)
print("Real streak:", "getStreak()" in h)
print("Auto-save:", "saveToHistory" in h)
print("History route:", "history:renderHistory" in h)
