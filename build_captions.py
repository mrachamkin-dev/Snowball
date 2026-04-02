import os, re

with open('index.html','r',encoding='utf-8') as f: h=f.read()
print("Starting:", len(h))

def check(code):
    s=code.find('<script>')+8; e=code.rfind('</script>')
    js=code[s:e]; p=b=0
    for c in js:
        if c=='(':p+=1
        elif c==')':p-=1
        elif c=='{':b+=1
        elif c=='}':b-=1
    return p,b

# ── FEATURE 1: Add tagline above prompt on home screen ───────────────────────
OLD_PROMPT_EL = (
    "var promptEl=document.createElement('div');\n"
    "  promptEl.id='prompt-text';\n"
    "  promptEl.style.cssText='font-family:var(--serif);font-size:34px;font-weight:300;font-style:italic;color:var(--cream);line-height:1.3;transition:opacity 0.5s ease;margin-bottom:0;';\n"
    "  promptEl.textContent='\"'+PROMPTS[promptIdx]+'\"';\n"
    "  promptWrap.appendChild(promptEl);"
)

NEW_PROMPT_EL = (
    "var tagline=document.createElement('div');\n"
    "  tagline.style.cssText='font-family:var(--sans);font-size:12px;font-weight:500;color:var(--muted);letter-spacing:0.18em;text-transform:uppercase;margin-bottom:20px;';\n"
    "  tagline.textContent='Tell your story. We\\'ll make it viral.';\n"
    "  promptWrap.appendChild(tagline);\n"
    "  var promptEl=document.createElement('div');\n"
    "  promptEl.id='prompt-text';\n"
    "  promptEl.style.cssText='font-family:var(--serif);font-size:34px;font-weight:300;font-style:italic;color:var(--cream);line-height:1.3;transition:opacity 0.5s ease;margin-bottom:0;';\n"
    "  promptEl.textContent='\"'+PROMPTS[promptIdx]+'\"';\n"
    "  promptWrap.appendChild(promptEl);"
)

if OLD_PROMPT_EL in h:
    h = h.replace(OLD_PROMPT_EL, NEW_PROMPT_EL)
    print("Tagline: ADDED")
else:
    print("Prompt element pattern not found - trying simpler approach")
    # Try finding just the promptEl creation
    idx = h.find("promptEl.id='prompt-text'")
    if idx > 0:
        # Find start of this var statement
        start_idx = h.rfind("var promptEl=", 0, idx)
        # Find the appendChild call after
        end_idx = h.find("promptWrap.appendChild(promptEl);", idx) + len("promptWrap.appendChild(promptEl);")
        old_block = h[start_idx:end_idx]
        new_block = (
            "var tagline=document.createElement('div');"
            "tagline.style.cssText='font-family:var(--sans);font-size:12px;font-weight:500;color:var(--muted);letter-spacing:0.18em;text-transform:uppercase;margin-bottom:20px;';"
            "tagline.textContent='Tell your story. We\\'ll make it viral.';"
            "promptWrap.appendChild(tagline);"
            + old_block
        )
        h = h[:start_idx] + new_block + h[end_idx:]
        print("Tagline: ADDED via index")

# ── FEATURE 2: Word-by-word captions synced to audio ─────────────────────────
# Add caption overlay to playback HTML
OLD_HOOK_OVERLAY = '<div style="position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 32px 220px;text-align:center;pointer-events:none;" id="hook-overlay">'

NEW_HOOK_OVERLAY = (
    '<div style="position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 32px 220px;text-align:center;pointer-events:none;" id="hook-overlay">'
)

# Add caption overlay after hook overlay closing div - find the right spot
CAPTION_OVERLAY = (
    '<div id="caption-overlay" style="position:absolute;bottom:170px;left:0;right:0;z-index:4;'
    'padding:0 24px;text-align:center;pointer-events:none;display:none;">'
    '<div id="caption-word" style="font-family:var(--sans);font-size:22px;font-weight:700;'
    'color:#ffffff;text-shadow:0 2px 8px rgba(0,0,0,0.9),0 0 20px rgba(0,0,0,0.7);'
    'letter-spacing:0.02em;line-height:1.2;'
    'animation:captionPop 0.15s cubic-bezier(0.34,1.56,0.64,1) both;"></div></div>'
)

# Add caption CSS
if 'captionPop' not in h:
    h = h.replace(
        '@keyframes snowFall{',
        '@keyframes captionPop{0%{transform:scale(0.85);opacity:0}100%{transform:scale(1);opacity:1}} @keyframes snowFall{'
    )
    print("Caption CSS: ADDED")

# Add caption overlay to playback HTML before opts div
OLD_OPTS_DIV = '<div id="opts" style="display:none;position:absolute;bottom:0'
if CAPTION_OVERLAY not in h and OLD_OPTS_DIV in h:
    h = h.replace(OLD_OPTS_DIV, CAPTION_OVERLAY + OLD_OPTS_DIV)
    print("Caption overlay HTML: ADDED")

# Add caption JS logic after audio setup in renderPlayback
OLD_AUDIO_SETUP = "audio.onended=()=>{playing=false;playBtn.textContent='▶';if(imgTimer)clearInterval(imgTimer);showImg(0)};"
NEW_AUDIO_SETUP = (
    "audio.onended=()=>{playing=false;playBtn.textContent='▶';if(imgTimer)clearInterval(imgTimer);showImg(0);"
    "var co=document.getElementById('caption-overlay');if(co)co.style.display='none';};\n"
    # Caption word display logic
    "var captionWords=[];var captionTimer=null;\n"
    "function startCaptions(narration){\n"
    "  var co=document.getElementById('caption-overlay');\n"
    "  if(!co||!narration)return;\n"
    "  co.style.display='block';\n"
    "  var words=narration.split(/\\s+/).filter(function(w){return w.length>0;});\n"
    "  if(!words.length)return;\n"
    "  var dur=audio.duration||20;\n"
    "  var wpt=(dur/words.length)*1000;\n"
    "  var wi=0;\n"
    "  var cw=document.getElementById('caption-word');\n"
    "  function showWord(){\n"
    "    if(wi>=words.length||!playing){return;}\n"
    "    if(cw){cw.style.animation='none';void cw.offsetWidth;cw.textContent=words[wi];cw.style.animation='captionPop 0.15s cubic-bezier(0.34,1.56,0.64,1) both';}\n"
    "    wi++;\n"
    "    captionTimer=setTimeout(showWord,wpt);\n"
    "  }\n"
    "  showWord();\n"
    "}\n"
)

if OLD_AUDIO_SETUP in h and 'startCaptions' not in h:
    h = h.replace(OLD_AUDIO_SETUP, NEW_AUDIO_SETUP)
    print("Caption JS: ADDED")

# Start captions when play begins
OLD_PLAY = "audio.play().then(()=>{playing=true;playBtn.textContent='⏸'}).catch(()=>{})"
NEW_PLAY = "audio.play().then(()=>{playing=true;playBtn.textContent='⏸';if(story&&story.narration)startCaptions(story.narration);}).catch(()=>{})"
if OLD_PLAY in h and 'startCaptions' in h:
    h = h.replace(OLD_PLAY, NEW_PLAY)
    print("Captions start on play: WIRED")

# Stop captions on pause
OLD_PAUSE = "audio.pause();playing=false;playBtn.textContent='▶'"
NEW_PAUSE = "audio.pause();playing=false;playBtn.textContent='▶';if(captionTimer){clearTimeout(captionTimer);captionTimer=null;}"
if OLD_PAUSE in h:
    h = h.replace(OLD_PAUSE, NEW_PAUSE)
    print("Captions pause: WIRED")

# ── VERIFY ────────────────────────────────────────────────────────────────────
p, b = check(h)
print(f"\nSyntax: paren={p} brace={b} - {'CLEAN' if p==0 and b==0 else 'BROKEN'}")
print("Size:", len(h))
print("Tagline:", "Tell your story. We" in h)
print("Caption overlay:", "caption-overlay" in h)
print("captionPop CSS:", "captionPop" in h)
print("startCaptions:", "startCaptions" in h)

if p==0 and b==0:
    with open('index.html.new','w',encoding='utf-8') as f: f.write(h)
    os.replace('index.html.new','index.html')
    print("Written safely")
else:
    print("NOT WRITING - syntax broken")
