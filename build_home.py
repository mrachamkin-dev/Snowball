import os, re

with open('index.html','r',encoding='utf-8') as f: h=f.read()
print("Starting:", len(h))

# 1. Replace snowRise (rising particles) with snowFall (falling flakes)
OLD_ANIM = """@keyframes snowRise {
  0%   { transform: translateY(0);       opacity: 0; }
  8%   { opacity: 1; }
  92%  { opacity: 0.7; }
  100% { transform: translateY(-110vh); opacity: 0; }
}"""

NEW_ANIM = """@keyframes snowFall {
  0%   { transform: translateY(-10px) rotate(0deg);   opacity: 0; }
  5%   { opacity: 1; }
  95%  { opacity: 0.6; }
  100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
}
@keyframes snowRise {
  0%   { transform: translateY(0);       opacity: 0; }
  8%   { opacity: 1; }
  92%  { opacity: 0.7; }
  100% { transform: translateY(-110vh); opacity: 0; }
}"""

if OLD_ANIM in h:
    h = h.replace(OLD_ANIM, NEW_ANIM)
    print("snowFall CSS: ADDED")
else:
    print("snowRise CSS not found - adding snowFall separately")
    h = h.replace(
        "@keyframes ballFloat {",
        "@keyframes snowFall { 0% { transform:translateY(-10px) rotate(0deg);opacity:0; } 5% { opacity:1; } 95% { opacity:0.6; } 100% { transform:translateY(110vh) rotate(360deg);opacity:0; } }\n@keyframes ballFloat {"
    )

# 2. Replace the entire renderHome function with clean redesign
OLD_HOME_START = "function renderHome(app){"
OLD_HOME_END = "function renderType(app){"

start_idx = h.find(OLD_HOME_START)
end_idx = h.find(OLD_HOME_END)

if start_idx > 0 and end_idx > 0:
    NEW_HOME = '''function renderHome(app){
  app.style.background='#0B0906';

  // Falling snow from top
  for(var i=0;i<28;i++){
    var flake=document.createElement('div');
    var sz=1+(i%4);
    var op=0.15+(i%5)*0.06;
    var dur=6+(i%8)*1.4;
    var del=-((i*1.8)%12);
    var left=((i*13+7)%94)+1;
    // Some flakes are slightly bigger and more visible
    var blur=i%5===0?'blur(0.5px)':'';
    flake.style.cssText='position:absolute;top:-10px;border-radius:50%;pointer-events:none;z-index:0;'
      +'width:'+sz+'px;height:'+sz+'px;'
      +'left:'+left+'%;'
      +'background:rgba(194,228,238,'+op+');'
      +(blur?'filter:'+blur+';':'')
      +'animation:snowFall '+dur+'s linear '+del+'s infinite;';
    app.appendChild(flake);
  }

  var wrap=document.createElement('div');
  wrap.style.cssText='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;z-index:1;';
  app.appendChild(wrap);

  // Header - wordmark left, streak right
  var hdr=document.createElement('div');
  hdr.style.cssText='width:100%;padding:52px 24px 0;display:flex;align-items:center;justify-content:space-between;';
  var logo=document.createElement('div');
  logo.className='logo';
  logo.innerHTML='snow<span class="dot">&#9679;</span>ball';
  var streak=document.createElement('div');
  streak.style.cssText='display:flex;align-items:center;gap:6px;cursor:pointer;padding:4px 8px;';
  streak.onclick=function(){go('history');};
  var sball=document.createElement('div');
  sball.className='ball';
  sball.style.cssText='width:12px;height:12px;flex-shrink:0;box-shadow:'+ballShadow(12)+';';
  var snum=document.createElement('span');
  snum.style.cssText='font-family:var(--sans);font-size:12px;color:var(--muted);';
  snum.textContent=getStreak()+' day streak';
  streak.appendChild(sball);streak.appendChild(snum);
  hdr.appendChild(logo);hdr.appendChild(streak);
  wrap.appendChild(hdr);

  // Prompt - center, dominant
  var promptWrap=document.createElement('div');
  promptWrap.style.cssText='flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 36px;text-align:center;';

  var promptEl=document.createElement('div');
  promptEl.id='prompt-text';
  promptEl.style.cssText='font-family:var(--serif);font-size:30px;font-weight:300;font-style:italic;color:var(--cream);line-height:1.3;transition:opacity 0.5s ease;margin-bottom:0;';
  promptEl.textContent='"'+PROMPTS[promptIdx]+'"';
  promptWrap.appendChild(promptEl);
  wrap.appendChild(promptWrap);

  // Snowball - hero, centered, large
  var ballSection=document.createElement('div');
  ballSection.style.cssText='display:flex;flex-direction:column;align-items:center;gap:12px;margin-bottom:52px;cursor:pointer;';
  ballSection.onclick=function(){showInputSheet();};

  // Halo
  var haloWrap=document.createElement('div');
  haloWrap.style.cssText='position:relative;display:flex;align-items:center;justify-content:center;';
  var halo=document.createElement('div');
  halo.style.cssText='position:absolute;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,rgba(194,228,238,0.08) 0%,transparent 70%);animation:haloPulse 3.5s ease-in-out infinite;pointer-events:none;';
  var mainBall=makeBall(128,'ballFloat 4.5s ease-in-out infinite');
  haloWrap.appendChild(halo);
  haloWrap.appendChild(mainBall);
  ballSection.appendChild(haloWrap);

  // Subtle tap hint
  var hint=document.createElement('div');
  hint.style.cssText='font-family:var(--sans);font-size:10px;color:var(--muted);letter-spacing:0.14em;text-transform:uppercase;';
  hint.textContent='tap to begin';
  ballSection.appendChild(hint);

  wrap.appendChild(ballSection);

  // Prompt rotation
  every(function(){
    var el=document.getElementById('prompt-text');
    if(!el)return;
    el.style.opacity='0';
    later(function(){
      promptIdx=(promptIdx+1)%PROMPTS.length;
      var el2=document.getElementById('prompt-text');
      if(el2){el2.textContent='"'+PROMPTS[promptIdx]+'"';el2.style.opacity='1';}
    },500);
  },4800);
}

function showInputSheet(){
  var ov=document.createElement('div');
  ov.style.cssText='position:absolute;inset:0;z-index:20;background:rgba(6,4,2,0.85);display:flex;flex-direction:column;align-items:center;justify-content:flex-end;animation:fadeIn 0.2s ease both;';
  document.getElementById('app').appendChild(ov);

  var sheet=document.createElement('div');
  sheet.style.cssText='width:100%;background:#0B0906;border-radius:24px 24px 0 0;padding:28px 20px 50px;display:flex;flex-direction:column;gap:12px;animation:slideUp 0.35s cubic-bezier(0.34,1.56,0.64,1) both;';

  var title=document.createElement('div');
  title.style.cssText='font-family:var(--serif);font-size:24px;font-weight:300;font-style:italic;color:var(--cream);text-align:center;margin-bottom:4px;';
  title.textContent='How do you want to tell it?';

  var btns=[
    {label:'🎙  Speak it',sub:'just talk',action:function(){ov.remove();go('speak');}},
    {label:'✏️  Type it',sub:'write it out',action:function(){ov.remove();go('type');}},
    {label:'📸  Add your photos',sub:'AI reads them',action:function(){ov.remove();userPhotos=[];go('photos');}},
  ];

  sheet.appendChild(title);
  btns.forEach(function(b){
    var btn=document.createElement('button');
    btn.style.cssText='width:100%;padding:18px 20px;border-radius:16px;border:1px solid var(--dim2);background:rgba(255,255,255,0.03);display:flex;align-items:center;justify-content:space-between;cursor:pointer;';
    var left=document.createElement('div');
    left.style.cssText='font-family:var(--sans);font-size:16px;color:var(--cream);font-weight:400;';
    left.textContent=b.label;
    var right=document.createElement('div');
    right.style.cssText='font-family:var(--sans);font-size:11px;color:var(--muted);';
    right.textContent=b.sub;
    btn.appendChild(left);btn.appendChild(right);
    btn.onclick=b.action;
    sheet.appendChild(btn);
  });

  var cancel=document.createElement('div');
  cancel.style.cssText='font-family:var(--sans);font-size:13px;color:var(--muted);text-align:center;padding:8px 0;cursor:pointer;';
  cancel.textContent='cancel';
  cancel.onclick=function(){ov.remove();};
  sheet.appendChild(cancel);
  ov.appendChild(sheet);
  ov.onclick=function(e){if(e.target===ov)ov.remove();};
}

'''
    h = h[:start_idx] + NEW_HOME + h[end_idx:]
    print("Home screen: REDESIGNED")
else:
    print("renderHome boundaries not found")
    print("start_idx:", start_idx, "end_idx:", end_idx)

# Verify syntax
start = h.find('<script>') + 8
end = h.rfind('</script>')
js = h[start:end]
p=b=0
for c in js:
    if c=='(':p+=1
    elif c==')':p-=1
    elif c=='{':b+=1
    elif c=='}':b-=1
print(f"Syntax: paren={p} brace={b} - {'CLEAN' if p==0 and b==0 else 'BROKEN'}")
print("Size:", len(h))

if p==0 and b==0:
    with open('index.html.new','w',encoding='utf-8') as f: f.write(h)
    os.replace('index.html.new','index.html')
    print("Written safely")
else:
    print("NOT WRITING - syntax broken")
