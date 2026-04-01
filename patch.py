with open('index.html','r') as f: h=f.read()

# 1. Add userPhotos state
h=h.replace("let screen='home',promptIdx=0,rawStory='',story=null,errorMsg='';","let screen='home',promptIdx=0,rawStory='',story=null,errorMsg='',userPhotos=[];")

# 2. Add photos route
h=h.replace("{home:renderHome,type:renderType,speak:renderSpeak,building:renderBuilding,playback:renderPlayback,error:renderError}","{home:renderHome,type:renderType,speak:renderSpeak,photos:renderPhotos,building:renderBuilding,playback:renderPlayback,error:renderError}")

# 3. Add photos button in home
h=h.replace("btns.appendChild(bs);btns.appendChild(bt);wrap.appendChild(btns);","btns.appendChild(bs);btns.appendChild(bt);const bp=document.createElement('button');bp.className='btn-ghost';bp.innerHTML='\ud83d\udcf8 \u00a0Add your photos';bp.onclick=()=>{userPhotos=[];go('photos')};btns.appendChild(bp);wrap.appendChild(btns);")

# 4. Add photo shape function + renderPhotos before render()
NEW_FUNCS="""
const PHOTO_SYS=`You are a cinematic story editor. The user has shared photos from their life. Analyze what you see and return ONLY valid JSON — no markdown, no backticks.
{"hook":"One sentence under 12 words. Present tense. Based on what you see.","location":"Place and time inferred from photos. Under 8 words.","narration":"First-person narration 90-130 words based on the photos. Warm, cinematic, emotionally resonant.","caption":"TikTok caption + 4 hashtags under 160 chars."}`;

async function shapeStoryFromPhotos(photos,context){
  const content=photos.map(d=>{const[hdr,data]=d.split(',');const mt=hdr.match(/:(.*?);/)[1];return{type:'image',source:{type:'base64',media_type:mt,data}};});
  content.push({type:'text',text:PHOTO_SYS+'\\n\\nUser context: '+context});
  const r=await fetch('/api/claude',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model:'claude-sonnet-4-20250514',max_tokens:1200,messages:[{role:'user',content}]})});
  if(!r.ok)throw new Error('Vision error '+r.status);
  const d=await r.json();
  const text=d.content?.[0]?.text??'';
  const clean=text.replace(/```json\\s*/g,'').replace(/```\\s*/g,'').trim();
  try{return JSON.parse(clean);}catch{const m=clean.match(/\\{[\\s\\S]*\\}/);if(m)return JSON.parse(m[0]);throw new Error('Could not read photos. Try again.');}
}

function renderPhotos(app){
  userPhotos=[];
  app.style.background='#070503';
  const wrap=document.createElement('div');
  wrap.style.cssText='position:absolute;inset:0;display:flex;flex-direction:column;';
  app.appendChild(wrap);
  const hdr=document.createElement('div');
  hdr.style.cssText='padding:52px 24px 0;display:flex;align-items:center;justify-content:space-between;';
  hdr.innerHTML='<button id="phback" style="color:var(--muted);font-family:var(--sans);font-size:13px;padding:4px 0;">\u2190 Back</button><div class="logo" style="font-size:19px;">snow<span class="dot">\u25cf</span>ball</div><div style="width:50px;"></div>';
  wrap.appendChild(hdr);
  document.getElementById('phback').onclick=()=>go('home');
  const info=document.createElement('div');
  info.style.cssText='padding:14px 26px 0;';
  info.innerHTML='<div style="font-family:var(--serif);font-size:24px;font-style:italic;font-weight:300;color:var(--cream);line-height:1.25;">Your photos, your story</div><div style="font-family:var(--sans);font-size:12px;color:var(--muted);margin-top:6px;line-height:1.5;">Add up to 4 photos. AI reads them and writes your narration.</div>';
  wrap.appendChild(info);
  const grid=document.createElement('div');
  grid.style.cssText='display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:16px 20px;flex:1;';
  wrap.appendChild(grid);
  const photoData={};
  for(let i=0;i<4;i++){
    const slot=document.createElement('div');
    slot.id='ph-slot-'+i;
    slot.style.cssText='background:rgba(255,255,255,0.03);border:1.5px dashed var(--dim2);border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;cursor:pointer;position:relative;overflow:hidden;min-height:110px;';
    const icon=document.createElement('span');icon.textContent='\ud83d\udcf7';icon.style.fontSize='24px';
    const lbl=document.createElement('span');lbl.textContent='Add photo';lbl.style.cssText='font-family:var(--sans);font-size:11px;color:var(--muted);';
    const inp=document.createElement('input');inp.type='file';inp.accept='image/*';inp.style.display='none';
    slot.appendChild(icon);slot.appendChild(lbl);slot.appendChild(inp);
    grid.appendChild(slot);
    const idx=i;
    slot.onclick=()=>inp.click();
    inp.onchange=()=>{
      const file=inp.files[0];if(!file)return;
      const reader=new FileReader();
      reader.onload=e=>{
        photoData[idx]=e.target.result;
        slot.innerHTML='';
        const img=document.createElement('img');
        img.src=e.target.result;img.style.cssText='width:100%;height:100%;object-fit:cover;position:absolute;inset:0;';
        const rm=document.createElement('div');
        rm.textContent='\u2715';rm.style.cssText='position:absolute;top:5px;right:5px;width:20px;height:20px;border-radius:50%;background:rgba(0,0,0,0.75);display:flex;align-items:center;justify-content:center;font-size:11px;color:white;cursor:pointer;';
        rm.onclick=e2=>{e2.stopPropagation();delete photoData[idx];slot.innerHTML='';slot.style.border='1.5px dashed var(--dim2)';slot.appendChild(icon);slot.appendChild(lbl);slot.appendChild(inp);slot.onclick=()=>inp.click();updateBtn();};
        slot.appendChild(img);slot.appendChild(rm);slot.style.border='none';
        updateBtn();
      };reader.readAsDataURL(file);
    };
  }
  const ctx=document.createElement('textarea');
  ctx.id='ph-ctx';ctx.placeholder='Optional: describe what happened...';
  ctx.style.cssText='width:100%;height:66px;border-radius:14px;background:rgba(255,255,255,0.03);border:1px solid var(--dim2);color:var(--cream);font-family:var(--serif);font-size:15px;font-style:italic;padding:12px 16px;caret-color:var(--gold);resize:none;outline:none;margin:0 20px;width:calc(100% - 40px);';
  wrap.appendChild(ctx);
  const foot=document.createElement('div');foot.style.cssText='padding:10px 20px 44px;';
  const btn=document.createElement('button');btn.id='ph-btn';btn.className='btn-dim';btn.style.cssText='font-size:16px;font-weight:600;padding:18px;border-radius:18px;width:100%;';btn.textContent='Add at least 1 photo';
  foot.appendChild(btn);wrap.appendChild(foot);
  function updateBtn(){const c=Object.keys(photoData).length;if(c>0){btn.className='btn-gold';btn.textContent='Shape my story \u2744\ufe0f ('+c+' photo'+(c>1?'s':'')+')';}else{btn.className='btn-dim';btn.textContent='Add at least 1 photo';}}
  btn.onclick=()=>{const photos=Object.values(photoData);if(!photos.length)return;userPhotos=photos;rawStory=ctx.value||'Tell the story in these photos.';go('building');};
}
"""

h=h.replace("function render(){",NEW_FUNCS+"\nfunction render(){")

# 5. Modify building pipeline to handle photos
OLD_PIPE="(async()=>{try{setStep(0);setProg(6);const shaped=await shapeStory(rawStory);setProg(22);setStep(1);const images=[];for(let i=0;i<shaped.scenes.length;i++){const url=await generateImage(shaped.scenes[i].imagePrompt);images.push(url);setProg(22+((i+1)/shaped.scenes.length)*52);if(i===0){const card=document.getElementById('preview-card'),img=document.getElementById('preview-img');if(card&&img){img.src=url;card.style.display='block';card.style.animation='imgReveal 0.8s ease both'}}}setStep(2);setProg(78);const audioUrl=await generateSpeech(shaped.narration);setStep(3);setProg(100);story={...shaped,images,audioUrl};later(()=>go('playback'),600)}catch(e){errorMsg=e.message||'Something went wrong.';go('error')}})()"

NEW_PIPE="""(async()=>{try{
if(userPhotos.length>0){
  setStep(0);setProg(20);
  const shaped=await shapeStoryFromPhotos(userPhotos,rawStory);
  setProg(78);setStep(2);
  const audioUrl=await generateSpeech(shaped.narration);
  setStep(3);setProg(100);
  story={...shaped,images:userPhotos,audioUrl};
  later(()=>go('playback'),600);
}else{
  setStep(0);setProg(6);const shaped=await shapeStory(rawStory);setProg(22);setStep(1);const images=[];for(let i=0;i<shaped.scenes.length;i++){const url=await generateImage(shaped.scenes[i].imagePrompt);images.push(url);setProg(22+((i+1)/shaped.scenes.length)*52);if(i===0){const card=document.getElementById('preview-card'),img=document.getElementById('preview-img');if(card&&img){img.src=url;card.style.display='block';card.style.animation='imgReveal 0.8s ease both'}}}setStep(2);setProg(78);const audioUrl=await generateSpeech(shaped.narration);setStep(3);setProg(100);story={...shaped,images,audioUrl};later(()=>go('playback'),600);
}
}catch(e){errorMsg=e.message||'Something went wrong.';go('error')}})()"""

h=h.replace(OLD_PIPE,NEW_PIPE)

with open('index.html','w') as f: f.write(h)
print("Done! Checking key replacements...")
print("userPhotos state:", "userPhotos=[]" in h)
print("photos route:", "photos:renderPhotos" in h)
print("photos button:", "Add your photos" in h)
print("renderPhotos func:", "function renderPhotos" in h)
print("photo pipeline:", "shapeStoryFromPhotos" in h)
