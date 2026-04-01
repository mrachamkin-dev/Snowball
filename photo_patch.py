with open('index.html','r',encoding='utf-8') as f: h=f.read()

# Check what we're working with
print("File size:", len(h), "chars")
print("Has old SYS:", "cinematic story editor trained on McKee" in h)
print("Has shapeStoryFromPhotos:", "shapeStoryFromPhotos" in h)
print("Has photo pipeline:", "setProg(15)" in h)

# 1. Upgrade main story system prompt
OLD1 = 'const SYS=`You are a cinematic story editor trained on McKee, Harmon Story Circle, and the But/Therefore rule. Given a raw personal story, return ONLY a valid JSON object \u2014 no markdown, no backticks. {"hook":"One sentence under 12 words. Present tense. Drops into the action.","location":"Place \u00b7 Time. Under 8 words.","narration":"First-person. 90-130 words. Starts with hook. Warm, cinematic.","scenes":[{"beat":"scene","imagePrompt":"Cinematic 35mm film photography, golden hour lighting, shallow depth of field, photorealistic, award-winning composition, vivid colors, emotionally evocative, no text, no watermarks."},{"beat":"scene","imagePrompt":"Cinematic 35mm film photography, golden hour lighting, shallow depth of field, photorealistic, award-winning composition, vivid colors, emotionally evocative, no text, no watermarks."},{"beat":"scene","imagePrompt":"Cinematic 35mm film photography, golden hour lighting, shallow depth of field, photorealistic, award-winning composition, vivid colors, emotionally evocative, no text, no watermarks."},{"beat":"scene","imagePrompt":"Cinematic 35mm film photography, golden hour lighting, shallow depth of field, photorealistic, award-winning composition, vivid colors, emotionally evocative, no text, no watermarks."}],"caption":"TikTok caption + 4 hashtags. Under 160 chars."}`'

NEW1 = '''const SYS=`You are a viral story editor trained on McKee, Harmon Story Circle, and TikTok scroll psychology. Given a raw personal story, return ONLY a valid JSON object no markdown no backticks.

HOOK: Must stop a thumb mid-scroll in 3 seconds. Use one of: Confession ("I did something I will never admit"), Contradiction ("The worst moment was also the best"), Stakes ("Everything I built was about to disappear"), Intrigue ("Nobody in that room knew what was happening"). Be specific to this story. Under 12 words. Present tense.

IMAGE PROMPTS: Describe ONE specific cinematic moment with exact location, time of day, specific action, emotional atmosphere. 35mm film, shallow depth of field, dramatic natural lighting, photorealistic, no text.

{"hook":"Scroll-stopping hook under 12 words","location":"Specific place and time under 8 words","narration":"First-person 90-130 words. Opens with hook verbatim. Builds with But/Therefore. Cinematic and specific.","hookImagePrompt":"Cinematic image perfectly matching the hook emotion. FIRST thing viewer sees. 35mm film dramatic photorealistic no text.","scenes":[{"beat":"scene beat","imagePrompt":"Specific cinematic moment. 35mm film dramatic light photorealistic no text."},{"beat":"scene beat","imagePrompt":"Specific cinematic moment. 35mm film dramatic light photorealistic no text."},{"beat":"scene beat","imagePrompt":"Specific cinematic moment. 35mm film dramatic light photorealistic no text."}],"caption":"TikTok caption teases without spoiling + 4 hashtags under 160 chars."}`'''

if OLD1 in h:
    h = h.replace(OLD1, NEW1)
    print("SYS prompt: UPGRADED")
else:
    print("SYS prompt: NOT FOUND - checking variant...")
    if "cinematic story editor trained on McKee" in h:
        import re
        h = re.sub(r'const SYS=`[^`]+`', NEW1, h, count=1)
        print("SYS prompt: UPGRADED via regex")

# 2. Upgrade PHOTO_SYS
OLD2 = "const PHOTO_SYS='You are a cinematic story editor. Analyze the photos and return ONLY valid JSON no markdown. {\"hook\":\"One sentence under 12 words present tense.\",\"location\":\"Place and time under 8 words.\",\"narration\":\"First-person 90-130 words warm cinematic based on what you see in the photos.\",\"caption\":\"TikTok caption 4 hashtags under 160 chars.\"}'"

NEW2 = """const PHOTO_SYS=`You are a viral story editor and visual director. The user has shared real photos from their life.

Analyze each photo for story relevance, visual quality, and emotional impact. Then build the most compelling 4-image visual story using:
- KEEP: High quality photos that serve the story directly (type: user_photo)
- ENHANCE: Low quality or poorly composed photos - use as mood reference for AI recreation (type: ai_from_reference)  
- FILL: Generate AI scenes for story moments not captured in photos (type: ai_generate)

Return ONLY valid JSON no markdown no backticks:
{"hook":"Scroll-stopping hook under 12 words. Confession/Contradiction/Stakes/Intrigue format.","location":"Place and time under 8 words.","narration":"First-person 90-130 words opens with hook warm cinematic specific.","hookImagePrompt":"Image matching hook emotion. 35mm film dramatic photorealistic no text.","caption":"TikTok caption teases + 4 hashtags under 160 chars.","visualPlan":[{"type":"user_photo","photoIndex":0,"reason":"why this works"},{"type":"ai_generate","imagePrompt":"specific cinematic scene. 35mm film dramatic photorealistic no text.","reason":"story gap"},{"type":"ai_from_reference","photoIndex":1,"imagePrompt":"enhanced cinematic version inspired by photo mood. 35mm film photorealistic no text.","reason":"why AI is better"},{"type":"user_photo","photoIndex":2,"reason":"why this works"}]}

visualPlan must have exactly 4 entries in story order.`"""

if OLD2 in h:
    h = h.replace(OLD2, NEW2)
    print("PHOTO_SYS: UPGRADED")
else:
    print("PHOTO_SYS: NOT FOUND - skipping")

# 3. Add executeVisualPlan function after shapeStoryFromPhotos
EXEC_FUNC = """
async function executeVisualPlan(plan,photos,setProgFn){
  const images=[];
  const vp=plan.visualPlan||[];
  const total=vp.length||4;
  for(let i=0;i<vp.length;i++){
    const step=vp[i];
    if(step.type==='user_photo'&&photos[step.photoIndex]){
      images.push(photos[step.photoIndex]);
    } else if(step.type==='ai_generate'||step.type==='ai_from_reference'){
      const url=await generateImage(step.imagePrompt);
      images.push(url);
    }
    if(setProgFn)setProgFn(20+((i+1)/total)*55);
  }
  if(images.length===0)photos.forEach(p=>images.push(p));
  return images;
}"""

if "executeVisualPlan" not in h:
    h = h.replace("function renderPhotos", EXEC_FUNC + "\nfunction renderPhotos")
    print("executeVisualPlan: ADDED")
else:
    print("executeVisualPlan: already exists")

# 4. Upgrade normal building pipeline to use hookImagePrompt
OLD_NORMAL = "setStep(0);setProg(6);const shaped=await shapeStory(rawStory);setProg(22);setStep(1);const images=[];for(let i=0;i<shaped.scenes.length;i++){const url=await generateImage(shaped.scenes[i].imagePrompt);images.push(url);setProg(22+((i+1)/shaped.scenes.length)*52);if(i===0){const card=document.getElementById('preview-card'),img=document.getElementById('preview-img');if(card&&img){img.src=url;card.style.display='block';card.style.animation='imgReveal 0.8s ease both'}}}setStep(2);setProg(78);const audioUrl=await generateSpeech(shaped.narration);setStep(3);setProg(100);story=Object.assign({},shaped,{images:images,audioUrl:audioUrl});later(()=>go('playback'),600);"

NEW_NORMAL = "setStep(0);setProg(6);const shaped=await shapeStory(rawStory);setProg(22);setStep(1);const images=[];if(shaped.hookImagePrompt){const hookUrl=await generateImage(shaped.hookImagePrompt);images.push(hookUrl);const hcard=document.getElementById('preview-card'),himg=document.getElementById('preview-img');if(hcard&&himg){himg.src=hookUrl;hcard.style.display='block';hcard.style.animation='imgReveal 0.8s ease both'}setProg(35);}for(let i=0;i<(shaped.scenes||[]).length;i++){const url=await generateImage(shaped.scenes[i].imagePrompt);images.push(url);setProg(35+((i+1)/((shaped.scenes||[]).length||1))*40);if(i===0&&!shaped.hookImagePrompt){const card2=document.getElementById('preview-card'),img2=document.getElementById('preview-img');if(card2&&img2){img2.src=url;card2.style.display='block';card2.style.animation='imgReveal 0.8s ease both'}}}setStep(2);setProg(78);const audioUrl=await generateSpeech(shaped.narration);setStep(3);setProg(100);story=Object.assign({},shaped,{images:images,audioUrl:audioUrl});later(()=>go('playback'),600);"

if OLD_NORMAL in h:
    h = h.replace(OLD_NORMAL, NEW_NORMAL)
    print("Normal pipeline: UPGRADED with hookImagePrompt")
else:
    print("Normal pipeline: NOT FOUND")

# 5. Upgrade photo pipeline to use executeVisualPlan
OLD_PHOTO = "setStep(0);setProg(20);const shaped=await shapeStoryFromPhotos(userPhotos,rawStory);setProg(78);setStep(2);const audioUrl=await generateSpeech(shaped.narration);setStep(3);setProg(100);story=Object.assign({},shaped,{images:userPhotos,audioUrl:audioUrl});later(()=>go('playback'),600);"
NEW_PHOTO = "setStep(0);setProg(15);const shaped=await shapeStoryFromPhotos(userPhotos,rawStory);setProg(20);setStep(1);const images=await executeVisualPlan(shaped,userPhotos,function(p){setProg(p);});setStep(2);setProg(78);const audioUrl=await generateSpeech(shaped.narration);setStep(3);setProg(100);story=Object.assign({},shaped,{images:images,audioUrl:audioUrl});later(()=>go('playback'),600);"

if OLD_PHOTO in h:
    h = h.replace(OLD_PHOTO, NEW_PHOTO)
    print("Photo pipeline: UPGRADED with executeVisualPlan")
else:
    print("Photo pipeline: NOT FOUND (may already be upgraded)")

with open('index.html','w',encoding='utf-8') as f: f.write(h)
print("\nFinal checks:")
print("  hookImagePrompt:", "hookImagePrompt" in h)
print("  visualPlan:", "visualPlan" in h)
print("  executeVisualPlan:", "executeVisualPlan" in h)
print("  scroll-stopping hook:", "Scroll-stopping hook" in h)
