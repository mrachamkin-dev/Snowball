async function recordStoryVideo(story,onProgress,onDone,onError){
  try{
    var W=1080,H=1920,FPS=30;
    var canvas=document.createElement('canvas');
    canvas.width=W;canvas.height=H;
    var ctx=canvas.getContext('2d');
    function loadImg(src){return new Promise(function(res){var img=new Image();img.crossOrigin='anonymous';img.onload=function(){res(img)};img.onerror=function(){res(null)};img.src=src;});}
    onProgress(5,'Loading images...');
    var imgs=[];
    for(var i=0;i<(story.images||[]).length;i++){imgs.push(await loadImg(story.images[i]));}
    onProgress(15,'Loading audio...');
    var audioCtx=new(window.AudioContext||window.webkitAudioContext)();
    var audioResp=await fetch(story.audioUrl);
    var audioBuffer=await audioCtx.decodeAudioData(await audioResp.arrayBuffer());
    var dur=audioBuffer.duration;
    var stream=canvas.captureStream(FPS);
    var audioDest=audioCtx.createMediaStreamDestination();
    stream.addTrack(audioDest.stream.getAudioTracks()[0]);
    var mime=MediaRecorder.isTypeSupported('video/mp4;codecs=avc1')?'video/mp4;codecs=avc1':MediaRecorder.isTypeSupported('video/mp4')?'video/mp4':MediaRecorder.isTypeSupported('video/webm;codecs=vp9,opus')?'video/webm;codecs=vp9,opus':'video/webm';
    var recorder=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:8000000});
    var chunks=[];
    recorder.ondataavailable=function(e){if(e.data.size>0)chunks.push(e.data);};
    var SF="'Cormorant Garamond',Georgia,serif";
    var SS="'Plus Jakarta Sans',system-ui,sans-serif";
    function drawFrame(t){
      var ic=imgs.length||1;var spi=dur/ic;
      var ii=Math.min(Math.floor(t/spi),ic-1);var it=(t%spi)/spi;
      var img=imgs[ii];
      if(img){
        var ks=1.0+it*0.08;var kx=(ii%2===0?-1:1)*it*0.02*W;var ky=(ii%2===0?-1:1)*it*0.02*H;
        var sc=Math.max(W/img.width,H/img.height)*ks;
        var sw=img.width*sc;var sh=img.height*sc;
        ctx.drawImage(img,(W-sw)/2+kx,(H-sh)/2+ky,sw,sh);
      }else{ctx.fillStyle='#0B0906';ctx.fillRect(0,0,W,H);}
      ctx.fillStyle='rgba(0,0,0,0.45)';ctx.fillRect(0,0,W,H);
      var tg=ctx.createLinearGradient(0,0,0,300);tg.addColorStop(0,'rgba(0,0,0,0.7)');tg.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=tg;ctx.fillRect(0,0,W,300);
      var bg=ctx.createLinearGradient(0,H-500,0,H);bg.addColorStop(0,'rgba(0,0,0,0)');bg.addColorStop(1,'rgba(0,0,0,0.92)');ctx.fillStyle=bg;ctx.fillRect(0,H-500,W,500);
      ctx.fillStyle='rgba(238,232,220,0.55)';ctx.font='38px '+SF;ctx.textAlign='left';ctx.fillText('snow●ball',60,100);
      var ho=t<1.5?t/1.5:(t<3.5?1:(t<5?1-(t-3.5)/1.5:0));ctx.globalAlpha=ho;
      if(story.location){ctx.fillStyle='#E5B444';ctx.font='500 30px '+SS;ctx.textAlign='center';ctx.fillText((story.location||'').toUpperCase(),W/2,H/2-90);}
      ctx.fillStyle='#EEE8DC';ctx.font='300 72px '+SF;ctx.textAlign='center';
      var words=(story.hook||'').split(' ');var line='';var lines=[];var maxW=W-120;
      for(var wi=0;wi<words.length;wi++){var test=line+(line?' ':'')+words[wi];if(ctx.measureText(test).width>maxW&&line){lines.push(line);line=words[wi];}else{line=test;}}
      if(line)lines.push(line);
      var lh=82;var sy=H/2-(lines.length*lh)/2+30;
      for(var li=0;li<lines.length;li++)ctx.fillText(lines[li],W/2,sy+li*lh);
      ctx.globalAlpha=1;ctx.fillStyle='rgba(238,232,220,0.28)';ctx.font='34px '+SF;
      ctx.textAlign='right';ctx.fillText('snow\u25cfball',W-60,H-80);ctx.textAlign='left';
    }
    onProgress(20,'Recording...');recorder.start(100);
    var src=audioCtx.createBufferSource();src.buffer=audioBuffer;
    src.connect(audioDest);src.connect(audioCtx.destination);
    var t0=performance.now();src.start(0);
    await new Promise(function(resolve){
      function tick(){
        var el=(performance.now()-t0)/1000;
        if(el>=dur){drawFrame(dur-0.01);resolve();return;}
        drawFrame(el);
        onProgress(Math.round(20+(el/dur)*70),'Recording '+Math.round(el)+'s / '+Math.round(dur)+'s...');
        requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    });
    recorder.stop();onProgress(95,'Saving...');
    await new Promise(function(r){setTimeout(r,600);});
    var blob=new Blob(chunks,{type:mime});
    var ext2=mime.includes('mp4')?'mp4':'webm';onDone(URL.createObjectURL(blob),ext2);
  }catch(err){onError(err.message||'Recording failed');}
}

function showRecordingModal(story,onVideoReady){
  var ov=document.createElement('div');
  ov.style.cssText='position:absolute;inset:0;z-index:30;background:rgba(6,4,2,0.97);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;padding:32px;';
  document.getElementById('app').appendChild(ov);
  ov.innerHTML='<div style="font-family:Georgia,serif;font-size:26px;font-weight:300;font-style:italic;color:#EEE8DC;text-align:center;">Creating your video...</div><div id="rec-sub" style="font-size:13px;color:#635850;text-align:center;">Loading...</div><div style="width:100%;height:4px;background:rgba(255,255,255,0.08);border-radius:2px;overflow:hidden;"><div id="rec-fill" style="height:100%;background:linear-gradient(to right,#E5B444,#C2E4EE);width:0%;transition:width 0.4s ease;border-radius:2px;"></div></div><button onclick="this.parentElement.remove()" style="font-size:13px;color:#635850;background:none;border:none;cursor:pointer;">Cancel</button>';
  recordStoryVideo(story,
    function(pct,msg){var f=document.getElementById('rec-fill'),s=document.getElementById('rec-sub');if(f)f.style.width=pct+'%';if(s)s.textContent=msg;},
    function(url,ext){
      if(onVideoReady){onVideoReady(url,ext);ov.remove();return;}
      ov.innerHTML='';ov.style.gap='20px';
      var ball=document.createElement('div');ball.className='ball';
      ball.style.cssText='width:60px;height:60px;flex-shrink:0;animation:ballFloat 3s ease-in-out infinite;box-shadow:inset -8px -7px 18px rgba(0,0,0,0.28),inset 4px 4px 10px rgba(255,255,255,0.68),0 8px 26px rgba(0,0,0,0.52),0 0 26px rgba(194,228,238,0.42);';
      var title=document.createElement('div');title.style.cssText='font-family:Georgia,serif;font-size:26px;font-weight:300;font-style:italic;color:#EEE8DC;text-align:center;';title.textContent='Your video is ready';
      var dl=document.createElement('a');dl.href=url;dl.download='snowball.'+ext;
      dl.style.cssText='width:100%;padding:18px;border-radius:18px;background:#E5B444;color:#060402;font-size:16px;font-weight:600;text-align:center;text-decoration:none;display:block;';
      dl.textContent='\u2b07\ufe0f  Save Video';
      var sh=document.createElement('button');
      sh.style.cssText='width:100%;padding:16px;border-radius:18px;border:1px solid #2A2318;background:rgba(255,255,255,0.03);color:#EEE8DC;font-size:15px;cursor:pointer;';
      sh.textContent='\ud83d\udce4  Share via...';
      sh.onclick=async function(){try{var r=await fetch(url);var b=await r.blob();var f=new File([b],'snowball.'+ext,{type:b.type});if(navigator.canShare&&navigator.canShare({files:[f]})){await navigator.share({files:[f],title:'My Snowball Story',text:story.caption||''});}else{dl.click();}}catch(e){dl.click();}};
      var bk=document.createElement('button');
      bk.style.cssText='font-size:13px;color:#635850;background:none;border:none;cursor:pointer;';
      bk.textContent='\u2190 Back to story';bk.onclick=function(){ov.remove();};
      ov.appendChild(ball);ov.appendChild(title);ov.appendChild(dl);ov.appendChild(sh);ov.appendChild(bk);
    },
    function(err){var s=document.getElementById('rec-sub');if(s)s.textContent='Error: '+err;}
  );
}
