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

# 1. Prompts
h=re.sub(r"const PROMPTS=\[.*?\];",
    "const PROMPTS=['Tell your best story.','What happened to you that nobody would believe?','What is the funniest thing that has ever happened to you?','What is a chapter of your life most people do not know about?','What is the moment that completely changed everything?','What is the wildest thing you have ever gotten away with?','What did you do that you are somehow still not sorry about?','If your life were a movie what is the scene everyone would remember?','What happened the night everything went sideways in the best way?','What is the story your friends always beg you to tell?'];",
    h,count=1,flags=re.DOTALL)
print("Prompts:", "Tell your best story" in h)

# 2. Timer CSS
if "rollBall" not in h:
    h=h.replace("@keyframes imgReveal { from { opacity: 0; } to { opacity: 1; } }",
        "@keyframes imgReveal { from { opacity: 0; } to { opacity: 1; } } @keyframes rollBall { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }")
    print("rollBall CSS:", "rollBall" in h)

# 3. Timer logic
OLD_T="secs++;timerEl.textContent=String(Math.floor(secs/60)).padStart(2,'0')+':'+String(secs%60).padStart(2,'0');"
NEW_T="secs++;timerEl.textContent=secs+'s';var rb=document.getElementById('roll-ball');if(rb&&rb.parentElement){var pct=Math.min(secs/60,1);var tw=Math.max(rb.parentElement.offsetWidth-24,100);rb.style.left=Math.round(pct*tw)+'px';var sz=18+Math.round(pct*18);rb.style.width=sz+'px';rb.style.height=sz+'px';rb.style.animationPlayState=listening?'running':'paused';rb.style.animationDuration=Math.max(0.3,1-pct*0.7)+'s';if(secs>=30){rb.style.filter='drop-shadow(0 0 6px gold)';timerEl.style.color='var(--gold)';}if(secs>=60){var db=document.getElementById('done-btn');if(db&&transcript.length>20){db.click();}}}"
if OLD_T in h:
    h=h.replace(OLD_T,NEW_T)
    print("Timer: UPGRADED")

# 4. Ball track HTML
if "roll-ball" not in h:
    OLD_D='<div style="width:100%;padding:0 20px 44px;"><button id="done-btn"'
    NEW_D='<div style="width:100%;padding:0 20px 12px;"><div style="position:relative;height:36px;margin-bottom:10px;"><div style="position:absolute;bottom:8px;left:0;right:0;height:2px;background:rgba(255,255,255,0.06);border-radius:1px;"></div><div style="position:absolute;bottom:4px;left:50%;width:50%;height:10px;background:rgba(229,180,68,0.10);border-radius:5px;"></div><div id="roll-ball" class="ball" style="position:absolute;bottom:0;left:0;width:18px;height:18px;transition:left 1s linear,width 0.5s,height 0.5s;box-shadow:inset -2px -2px 5px rgba(0,0,0,0.28),inset 1px 1px 3px rgba(255,255,255,0.68),0 2px 8px rgba(0,0,0,0.4);animation:rollBall 1s linear infinite paused;"></div><div style="position:absolute;bottom:0;right:0;font-family:var(--sans);font-size:10px;color:var(--muted);">60s max</div></div></div><div style="width:100%;padding:0 20px 44px;"><button id="done-btn"'
    if OLD_D in h:
        h=h.replace(OLD_D,NEW_D)
        print("Ball track: ADDED")

# 5. Timer display
h=h.replace('<div id="timer" style="font-family:var(--sans);font-size:14px;font-weight:300;color:var(--muted);letter-spacing:0.12em;font-variant-numeric:tabular-nums;">00:00</div>',
    '<div id="timer" style="font-family:var(--sans);font-size:13px;font-weight:300;color:var(--muted);letter-spacing:0.12em;">0s</div>')

# 6. Genre state
if 'currentGenre' not in h:
    h=h.replace("let screen='home',promptIdx=0,rawStory='',story=null,errorMsg='',userPhotos=[];",
        "let screen='home',promptIdx=0,rawStory='',story=null,errorMsg='',userPhotos=[],currentGenre=null,forcedGenre=null;")

# 7. Genre picker
if 'showGenrePicker' not in h:
    GPICKER="""
function showGenrePicker(){
  var ov=document.createElement('div');
  ov.style.cssText='position:absolute;inset:0;z-index:25;background:rgba(6,4,2,0.92);display:flex;flex-direction:column;align-items:center;justify-content:flex-end;';
  document.getElementById('app').appendChild(ov);
  var sheet=document.createElement('div');
  sheet.style.cssText='width:100%;background:#0B0906;border-radius:24px 24px 0 0;padding:24px 20px 44px;display:flex;flex-direction:column;gap:12px;animation:slideUp 0.35s cubic-bezier(0.34,1.56,0.64,1) both;';
  var title=document.createElement('div');
  title.style.cssText='font-family:var(--serif);font-size:22px;font-weight:300;font-style:italic;color:var(--cream);';
  title.textContent='Tell it a different way';
  var sub=document.createElement('div');
  sub.style.cssText='font-family:var(--sans);font-size:12px;color:var(--muted);';
  sub.textContent='Same story. Different feel. Rebuilt in seconds.';
  sheet.appendChild(title);sheet.appendChild(sub);
  var grid=document.createElement('div');
  grid.style.cssText='display:grid;grid-template-columns:1fr 1fr;gap:10px;';
  var genres=[
    {id:'funny',em:'Funny',desc:'Bigger laughs'},
    {id:'dramatic',em:'Dramatic',desc:'Weight and stakes'},
    {id:'romantic',em:'Romantic',desc:'Warmth and longing'},
    {id:'action',em:'Action',desc:'Urgency and motion'},
    {id:'tragic',em:'Tragic',desc:'Beauty in the loss'},
    {id:'triumphant',em:'Triumphant',desc:'The comeback arc'}
  ];
  genres.forEach(function(g){
    var btn=document.createElement('button');
    var isCur=g.id===(currentGenre||'');
    btn.style.cssText='padding:16px 12px;border-radius:16px;cursor:pointer;text-align:left;display:flex;flex-direction:column;gap:4px;border:1px solid '+(isCur?'var(--gold)':'var(--dim2)')+';background:'+(isCur?'rgba(229,180,68,0.12)':'rgba(255,255,255,0.03)')+';';
    var nm=document.createElement('span');nm.textContent=g.em;nm.style.cssText='font-family:var(--sans);font-size:14px;font-weight:600;color:'+(isCur?'var(--gold)':'var(--cream)')+';';
    var ds=document.createElement('span');ds.textContent=g.desc;ds.style.cssText='font-family:var(--sans);font-size:10px;color:var(--muted);';
    btn.appendChild(nm);btn.appendChild(ds);
    btn.onclick=function(){ov.remove();if(g.id===currentGenre)return;forcedGenre=g.id;story=null;go('building');};
    grid.appendChild(btn);
  });
  sheet.appendChild(grid);
  var cancel=document.createElement('button');
  cancel.style.cssText='font-family:var(--sans);font-size:13px;color:var(--muted);background:none;border:none;cursor:pointer;';
  cancel.textContent='Keep this version';
  cancel.onclick=function(){ov.remove();};
  sheet.appendChild(cancel);
  ov.appendChild(sheet);
  ov.onclick=function(e){if(e.target===ov)ov.remove();};
}
"""
    h=h.replace("function render(){",GPICKER+"\nfunction render(){")
    print("Genre picker: ADDED")

# 8. Genre-aware shapeStory
if 'genreHint' not in h:
    h=h.replace("async function shapeStory(raw){",
        "async function shapeStory(raw,genreHint){if(genreHint){raw=raw+' [Shape this as a '+genreHint+' story using that genre structure]';}")
    h=h.replace("const shaped=await shapeStory(rawStory);",
        "const shaped=await shapeStory(rawStory,forcedGenre);currentGenre=shaped.genre||forcedGenre||null;forcedGenre=null;")
    print("Genre-aware shapeStory: DONE")

# 9. Try another feel UI
if 'Try another feel' not in h:
    OLD_CAP="document.getElementById('cap-txt').onclick=()=>navigator.clipboard?.writeText(story.caption||'').catch(()=>{})}"
    NEW_CAP="document.getElementById('cap-txt').onclick=()=>navigator.clipboard?.writeText(story.caption||'').catch(()=>{});var gb=document.createElement('div');gb.style.cssText='margin-top:12px;display:flex;align-items:center;justify-content:space-between;';var gs=document.createElement('span');gs.style.cssText='font-family:var(--sans);font-size:11px;color:var(--muted);';gs.textContent=currentGenre?('Shaped as: '+currentGenre.charAt(0).toUpperCase()+currentGenre.slice(1)):'';var gbtn=document.createElement('button');gbtn.style.cssText='font-family:var(--sans);font-size:11px;color:var(--ice);background:none;border:none;cursor:pointer;';gbtn.textContent='Try another feel';gbtn.onclick=function(){showGenrePicker();};gb.appendChild(gs);gb.appendChild(gbtn);var opEl=document.getElementById('opts');if(opEl)opEl.appendChild(gb);}"
    if OLD_CAP in h:
        h=h.replace(OLD_CAP,NEW_CAP)
        print("Try another feel: ADDED")

# 10. History
if 'getHistory' not in h:
    HIST="function getHistory(){try{return JSON.parse(localStorage.getItem('sb_history')||'[]');}catch(e){return [];}}\nfunction saveToHistory(s){var hist=getHistory();var e={id:Date.now(),date:new Date().toISOString(),hook:s.hook,location:s.location,caption:s.caption,images:s.images,audioUrl:s.audioUrl,shared:false};hist.unshift(e);if(hist.length>50)hist.pop();localStorage.setItem('sb_history',JSON.stringify(hist));return e;}\nfunction getStreak(){var hist=getHistory();if(!hist.length)return 0;var days=new Set(hist.map(function(h){return h.date.slice(0,10);}));var streak=0;var d=new Date();for(var i=0;i<365;i++){var ds=d.toISOString().slice(0,10);if(days.has(ds)){streak++;d.setDate(d.getDate()-1);}else{break;}}return streak;}\nfunction renderHistory(app){app.style.background='#0B0906';var hist=getHistory();var wrap=document.createElement('div');wrap.style.cssText='position:absolute;inset:0;display:flex;flex-direction:column;overflow:hidden;';app.appendChild(wrap);var hdr=document.createElement('div');hdr.style.cssText='padding:52px 24px 16px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;';var bb=document.createElement('button');bb.style.cssText='color:var(--muted);font-family:var(--sans);font-size:13px;background:none;border:none;cursor:pointer;';bb.textContent='Back';bb.onclick=function(){go('home');};var ld=document.createElement('div');ld.className='logo';ld.style.fontSize='19px';ld.innerHTML='snow<span class=\"dot\">&#9679;</span>ball';var sp=document.createElement('div');sp.style.width='50px';hdr.appendChild(bb);hdr.appendChild(ld);hdr.appendChild(sp);wrap.appendChild(hdr);var list=document.createElement('div');list.style.cssText='flex:1;overflow-y:auto;padding:0 20px 40px;display:flex;flex-direction:column;gap:10px;';wrap.appendChild(list);if(!hist.length){list.innerHTML='<div style=\"font-family:var(--serif);font-size:18px;font-style:italic;color:var(--muted);text-align:center;margin-top:60px;\">No stories yet. Tell your first one.</div>';}else{hist.forEach(function(entry){var card=document.createElement('div');card.style.cssText='background:rgba(255,255,255,0.03);border:1px solid var(--dim2);border-radius:16px;overflow:hidden;display:flex;cursor:pointer;min-height:80px;';var thumb=document.createElement('div');thumb.style.cssText='width:80px;flex-shrink:0;background:#1a1410;overflow:hidden;';if(entry.images&&entry.images[0]){var ti=document.createElement('img');ti.src=entry.images[0];ti.style.cssText='width:100%;height:100%;object-fit:cover;';thumb.appendChild(ti);}var info=document.createElement('div');info.style.cssText='flex:1;padding:14px;display:flex;flex-direction:column;justify-content:center;gap:4px;overflow:hidden;';var he=document.createElement('div');he.style.cssText='font-family:var(--serif);font-size:15px;font-style:italic;color:var(--cream);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;';he.textContent=entry.hook||'Untitled';var me=document.createElement('div');me.style.cssText='font-family:var(--sans);font-size:10px;color:var(--muted);';var dd=new Date(entry.date);me.textContent=dd.toLocaleDateString('en-US',{month:'short',day:'numeric'});info.appendChild(he);info.appendChild(me);card.appendChild(thumb);card.appendChild(info);card.onclick=function(){story=entry;go('playback');};list.appendChild(card);});}})\n"
    h=h.replace("function render(){",HIST+"\nfunction render(){")
    h=h.replace('{home:renderHome,type:renderType,speak:renderSpeak,photos:renderPhotos,building:renderBuilding,playback:renderPlayback,error:renderError}','{home:renderHome,type:renderType,speak:renderSpeak,photos:renderPhotos,history:renderHistory,building:renderBuilding,playback:renderPlayback,error:renderError}')
    h=h.replace('>3 day streak<','>${getStreak()} day streak<')
    print("History: ADDED")

# Verify
p,b=check(h)
print(f"\nSyntax: paren={p} brace={b} - {'CLEAN' if p==0 and b==0 else 'BROKEN - NOT WRITING'}")
if p==0 and b==0:
    with open('index.html.new','w',encoding='utf-8') as f: f.write(h)
    os.replace('index.html.new','index.html')
    print("Written. Size:",len(h))
