import os, re

with open('index.html','r',encoding='utf-8') as f: h=f.read()
print(f"Starting: {len(h)} chars")

# ═══════════════════════════════════════════════════════════
# FEATURE: GENRE-AWARE STORY ENGINE
# ═══════════════════════════════════════════════════════════

# 1. Replace the main SYS prompt with genre-aware version
OLD_SYS_START = "const SYS=`You are a viral story editor"
OLD_SYS_END = '`'

# Find and replace the entire SYS constant
sys_start = h.find("const SYS=`")
if sys_start > 0:
    sys_end = h.find("`", sys_start + 11) + 1
    # Make sure we get the full backtick string
    # Find the closing backtick that ends the template literal
    depth = 0
    i = sys_start + 11  # past 'const SYS=`'
    while i < len(h):
        if h[i] == '`':
            sys_end = i + 1
            break
        i += 1
    
    NEW_SYS = '''const GENRES = {
  funny: {
    name: "Funny",
    hook_style: "Absurdist or self-deprecating. Sets up the misdirection.",
    structure: "Setup -> escalating complications -> punchline. Each beat makes it worse before it gets funnier. Use the rule of three.",
    narration_style: "Punchy rhythm. Short sentences build, longer sentence pays off. Self-aware narrator. Slight irony. The humor comes from specific details, not adjectives.",
    image_direction: "Slightly surreal or exaggerated moments. Expressive reactions. Chaotic energy. Warm lighting.",
    voice_note: "Faster pace, lighter touch, slight smirk in the delivery."
  },
  dramatic: {
    name: "Dramatic",
    hook_style: "Stakes something real immediately. The listener must know what could be lost.",
    structure: "Clear before/after. Build specificity — the more particular the detail, the more universal the feeling. The turn must be earned.",
    narration_style: "Measured sentences. Space between thoughts. Concrete sensory details. No rushing to the point — the journey IS the point.",
    image_direction: "High contrast. Weight and stillness. Faces and hands. Dramatic natural light.",
    voice_note: "Slower, deliberate, grave. Pauses matter."
  },
  romantic: {
    name: "Romantic",
    hook_style: "Creates an ache. Something the listener has felt before — longing, recognition, connection.",
    structure: "Longing then connection, or connection then loss. Stretch the sensory moments. Internal experience matters as much as external action.",
    narration_style: "Warmer, slightly breathless. Present-tense moments stretched out. Sensory details over plot mechanics.",
    image_direction: "Golden hour. Intimate framing. Empty spaces that feel full. Two people or the absence of them.",
    voice_note: "Soft, warm, intimate. Like telling a secret."
  },
  action: {
    name: "Action",
    hook_style: "Drops into the middle of something already happening. No setup — just motion.",
    structure: "Scene-to-scene momentum. Every sentence moves forward. No reflection during action — only after. Short declarative sentences.",
    narration_style: "Urgent. Physical. Present tense. Breathless. The narrator is slightly overwhelmed in the best way.",
    image_direction: "Motion, wide angles, physical stakes. Bodies in space. Tension visible in the environment.",
    voice_note: "Faster, urgent, adrenaline. Slight breathlessness."
  },
  tragic: {
    name: "Tragic",
    hook_style: "Contains a shadow of what's coming. The listener senses it before they know it.",
    structure: "Irony is the engine — we know what the narrator didn't yet know. Past tense looking back on present-tense moments. Name the loss clearly.",
    narration_style: "Quiet and deliberate. Beautiful details that hurt more because of what happens. Earned sadness — never manufactured.",
    image_direction: "Beautiful then broken. Light giving way to shadow. Stillness. Emptiness that means something.",
    voice_note: "Quiet, measured, the weight of knowing."
  },
  triumphant: {
    name: "Triumphant",
    hook_style: "Starts at the bottom. Name the lowest point first — the victory only lands if we feel the descent.",
    structure: "Descent then ascent. The lowest point must be named explicitly and specifically. Don't rush to the win — earn it beat by beat.",
    narration_style: "Starts quiet and builds. Specific struggle details make the triumph real. Not inspirational-poster language — real, earned, specific.",
    image_direction: "Darkness giving way to light, literally. Small moments of resilience. The face of someone who made it.",
    voice_note: "Builds from quiet to strong. The emotion is in the restraint, not the volume."
  }
};

const SYS=`You are a viral story editor and genre specialist trained on McKee, Harmon Story Circle, TikTok scroll psychology, and the emotional architecture of the world's best short-form stories.

Given a raw personal story, you must:
1. DETECT the genre (funny/dramatic/romantic/action/tragic/triumphant) from the emotional content
2. Apply that genre's specific structural and tonal rules
3. Return ONLY a valid JSON object — no markdown, no backticks

HOOK RULES (critical — this stops the scroll):
- Funny: absurdist or self-deprecating setup, implies chaos ahead
- Dramatic: stakes something real, names what could be lost  
- Romantic: creates an ache, something the listener has felt
- Action: drops mid-scene, no setup, pure motion
- Tragic: contains a shadow of what's coming
- Triumphant: starts at the bottom, names the lowest point first
Under 12 words. Present tense. No period.

NARRATION RULES by genre:
- Funny: punchy rhythm, short sentences build to longer payoff, specific details not adjectives, slight irony
- Dramatic: measured, space between thoughts, concrete sensory details, earned turns
- Romantic: warm, slightly breathless, stretched sensory moments, internal experience matters
- Action: urgent, physical, present tense, short declarative sentences, bodies in space
- Tragic: quiet and deliberate, beautiful details that hurt more knowing what comes, earned sadness
- Triumphant: starts quiet builds to strong, specific struggle details, never inspirational-poster language

IMAGE RULES: Each prompt describes ONE specific cinematic moment. Include exact location, time of day, specific action, emotional atmosphere. Match genre mood. 35mm film, dramatic natural lighting, photorealistic, no text.

Return this exact JSON structure:
{"genre":"one of: funny/dramatic/romantic/action/tragic/triumphant","hook":"scroll-stopping hook under 12 words","location":"specific place and time under 8 words","narration":"90-130 words. Opens with hook verbatim. Genre-appropriate rhythm and tone. Builds to emotional payoff.","hookImagePrompt":"cinematic image perfectly matching hook emotion. First thing viewer sees. 35mm film dramatic photorealistic no text.","scenes":[{"beat":"opening - establish world","imagePrompt":"specific cinematic moment matching genre mood. 35mm film photorealistic no text."},{"beat":"tension begins","imagePrompt":"specific cinematic moment. 35mm film photorealistic no text."},{"beat":"conflict peak","imagePrompt":"specific cinematic moment. 35mm film photorealistic no text."},{"beat":"turning point","imagePrompt":"specific cinematic moment. 35mm film photorealistic no text."},{"beat":"resolution","imagePrompt":"specific cinematic moment. 35mm film photorealistic no text."},{"beat":"aftermath - emotional landing","imagePrompt":"specific cinematic moment. 35mm film photorealistic no text."}],"caption":"TikTok caption that teases the emotional payoff without spoiling it + 4 hashtags under 160 chars.","voiceId":"Choose best ElevenLabs voice. Consider genre and narrator gender. Options: pNInz6obpgDQGcFmaJgB (Adam-warm male), ErXwobaYiN019PkySvjV (Antoni-narrative male), TxGEqnHWrfWFTfGW9XjX (Josh-deep cinematic male), 21m00Tcm4TlvDq8ikWAM (Rachel-warm female), EXAVITQu4vr4xnSDxMaL (Bella-emotional female), MF3mGyEYCl7XYWbV9V6O (Elli-energetic female). Return only the ID."}`'''

    h = h[:sys_start] + NEW_SYS + h[sys_end:]
    print("Genre system prompt: INSTALLED")
else:
    print("SYS prompt: not found")

# 2. Add genre state variable
if 'currentGenre' not in h:
    h = h.replace(
        "let screen='home',promptIdx=0,rawStory='',story=null,errorMsg='',userPhotos=[];",
        "let screen='home',promptIdx=0,rawStory='',story=null,errorMsg='',userPhotos=[],currentGenre=null,forcedGenre=null;"
    )
    print("Genre state: ADDED")

# 3. Add genre-forcing to shapeStory — if forcedGenre is set, tell Claude to use it
OLD_SHAPE = "async function shapeStory(raw){"
NEW_SHAPE = """async function shapeStory(raw,genreOverride){
  const genreNote = genreOverride
    ? 'IMPORTANT: The user has chosen to reshape this as a ' + genreOverride.toUpperCase() + ' story. Apply that genre\\'s full structural and tonal rules even if the raw story suggests a different genre.'
    : '';
  raw = genreNote ? raw + '\\n\\n' + genreNote : raw;
"""
if OLD_SHAPE in h and 'genreOverride' not in h:
    h = h.replace(OLD_SHAPE, NEW_SHAPE)
    print("shapeStory: genre override ADDED")

# 4. Pass forcedGenre into shapeStory calls
h = h.replace(
    "const shaped=await shapeStory(rawStory);",
    "const shaped=await shapeStory(rawStory,forcedGenre);currentGenre=shaped.genre||null;forcedGenre=null;"
)
print("shapeStory calls: genre aware")

# 5. Add "Try another feel" UI to playback screen
# Add genre selector after the caption panel
OLD_CAP_PANEL_END = (
    "document.getElementById('cap-txt').onclick=()=>navigator.clipboard?.writeText(story.caption||'').catch(()=>{});"
)
NEW_CAP_PANEL_END = (
    "document.getElementById('cap-txt').onclick=()=>navigator.clipboard?.writeText(story.caption||'').catch(()=>{});"
    # Add genre indicator + try another feel
    "const genreBar=document.createElement('div');"
    "genreBar.style.cssText='margin-top:10px;display:flex;align-items:center;justify-content:space-between;padding:0 2px;';"
    "const GENRE_EMOJI={funny:'😂',dramatic:'🎭',romantic:'💛',action:'⚡',tragic:'🌧',triumphant:'🏔'};"
    "const gName=(currentGenre||'cinematic');"
    "const gEmoji=GENRE_EMOJI[gName]||'✨';"
    "genreBar.innerHTML="
    "'<span style=\"font-family:var(--sans);font-size:11px;color:var(--muted);\">'+gEmoji+' Shaped as: '+gName.charAt(0).toUpperCase()+gName.slice(1)+'</span>'"
    "+'<button id=\"btn-genre\" style=\"font-family:var(--sans);font-size:11px;color:var(--ice);background:none;border:none;cursor:pointer;padding:4px 0;\">Try another feel \u2192</button>';"
    "document.getElementById('opts').appendChild(genreBar);"
    "document.getElementById('btn-genre').onclick=()=>showGenrePicker();"
)

if OLD_CAP_PANEL_END in h and 'btn-genre' not in h:
    h = h.replace(OLD_CAP_PANEL_END, NEW_CAP_PANEL_END)
    print("Try another feel UI: ADDED")
else:
    print("Try another feel: pattern not found or already added")

# 6. Add genre picker modal function before render()
GENRE_PICKER = """
function showGenrePicker(){
  const ov=document.createElement('div');
  ov.style.cssText='position:absolute;inset:0;z-index:25;background:rgba(6,4,2,0.95);display:flex;flex-direction:column;align-items:center;justify-content:flex-end;animation:fadeIn 0.2s ease both;';
  document.getElementById('app').appendChild(ov);
  const GENRES_UI=[
    {id:'funny',emoji:'😂',name:'Funny',desc:'Same story, bigger laughs'},
    {id:'dramatic',emoji:'🎭',name:'Dramatic',desc:'Weight and consequence'},
    {id:'romantic',emoji:'💛',name:'Romantic',desc:'Warmth and longing'},
    {id:'action',emoji:'⚡',name:'Action',desc:'Urgency and adrenaline'},
    {id:'tragic',emoji:'🌧',name:'Tragic',desc:'Beauty in the loss'},
    {id:'triumphant',emoji:'🏔',name:'Triumphant',desc:'The comeback arc'},
  ];
  const sheet=document.createElement('div');
  sheet.style.cssText='width:100%;background:#0B0906;border-radius:24px 24px 0 0;padding:24px 20px 44px;display:flex;flex-direction:column;gap:12px;animation:slideUp 0.35s cubic-bezier(0.34,1.56,0.64,1) both;';
  const title=document.createElement('div');
  title.style.cssText='font-family:var(--serif);font-size:22px;font-weight:300;font-style:italic;color:var(--cream);margin-bottom:4px;';
  title.textContent='Tell it a different way';
  const sub=document.createElement('div');
  sub.style.cssText='font-family:var(--sans);font-size:12px;color:var(--muted);margin-bottom:8px;';
  sub.textContent='Same story. Different feel. Rebuilt in seconds.';
  sheet.appendChild(title);sheet.appendChild(sub);
  const grid=document.createElement('div');
  grid.style.cssText='display:grid;grid-template-columns:1fr 1fr;gap:10px;';
  GENRES_UI.forEach(g=>{
    const btn=document.createElement('button');
    const isCurrent=g.id===(currentGenre||'');
    btn.style.cssText='padding:16px 12px;border-radius:16px;border:1px solid '+(isCurrent?'var(--gold)':'var(--dim2)')+';background:'+(isCurrent?'rgba(229,180,68,0.12)':'rgba(255,255,255,0.03)')+';display:flex;flex-direction:column;align-items:flex-start;gap:4px;cursor:pointer;text-align:left;';
    btn.innerHTML='<span style="font-size:22px;">'+g.emoji+'</span>'
      +'<span style="font-family:var(--sans);font-size:14px;font-weight:600;color:'+(isCurrent?'var(--gold)':'var(--cream)')+';">'+g.name+'</span>'
      +'<span style="font-family:var(--sans);font-size:10px;color:var(--muted);">'+g.desc+'</span>';
    btn.onclick=()=>{
      ov.remove();
      if(g.id===currentGenre)return;
      forcedGenre=g.id;
      story=null;
      go('building');
    };
    grid.appendChild(btn);
  });
  sheet.appendChild(grid);
  const cancel=document.createElement('button');
  cancel.style.cssText='font-family:var(--sans);font-size:13px;color:var(--muted);background:none;border:none;cursor:pointer;margin-top:4px;';
  cancel.textContent='Keep this version';
  cancel.onclick=()=>ov.remove();
  sheet.appendChild(cancel);
  ov.appendChild(sheet);
  ov.onclick=e=>{if(e.target===ov)ov.remove();};
}
"""

if 'showGenrePicker' not in h:
    h = h.replace("function render(){", GENRE_PICKER + "\nfunction render(){")
    print("Genre picker modal: ADDED")

# Write safely
with open('index.html.new','w',encoding='utf-8') as f: f.write(h)
os.replace('index.html.new','index.html')

print(f"\nFinal: {len(h)} chars")
print("Genre prompt:", "DETECT the genre" in h)
print("GENRES object:", "const GENRES" in h)
print("Genre state:", "currentGenre" in h)
print("forcedGenre:", "forcedGenre" in h)
print("Genre picker:", "showGenrePicker" in h)
print("Try another feel:", "btn-genre" in h)
print("Genre override in shapeStory:", "genreOverride" in h)
