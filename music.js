// Snowball Procedural Music Engine
// Generates ambient background music by genre using Web Audio API
// No files, no licensing, works instantly

var SnowballMusic = (function(){
  var ctx = null;
  var masterGain = null;
  var activeNodes = [];
  var fadeInterval = null;

  function init(){
    if(ctx){if(ctx.state==='suspended')ctx.resume();return;}
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    masterGain = ctx.createGain();
    masterGain.gain.value = 0;
    masterGain.connect(ctx.destination);
    ctx.resume();
  }

  function stop(){
    if(fadeInterval) clearInterval(fadeInterval);
    if(!masterGain) return;
    masterGain.gain.setTargetAtTime(0, ctx.currentTime, 0.5);
    setTimeout(function(){
      activeNodes.forEach(function(n){ try{ n.stop(); }catch(e){} });
      activeNodes = [];
    }, 1000);
  }

  function fadeIn(duration){
    masterGain.gain.cancelScheduledValues(ctx.currentTime);
    masterGain.gain.setValueAtTime(0, ctx.currentTime);
    masterGain.gain.setTargetAtTime(0.32, ctx.currentTime, duration/3);
  }

  function osc(freq, type, gainVal, startTime, detune){
    var o = ctx.createOscillator();
    var g = ctx.createGain();
    o.type = type || 'sine';
    o.frequency.value = freq;
    if(detune) o.detune.value = detune;
    g.gain.value = gainVal || 0.3;
    o.connect(g);
    g.connect(masterGain);
    o.start(startTime || 0);
    activeNodes.push(o);
    return {osc:o, gain:g};
  }

  function lfo(target, param, rate, depth, offset){
    var l = ctx.createOscillator();
    var lg = ctx.createGain();
    l.frequency.value = rate;
    lg.gain.value = depth;
    l.connect(lg);
    lg.connect(target[param]);
    l.start(0);
    activeNodes.push(l);
    return l;
  }

  // ── DRAMATIC ────────────────────────────────────────────────────────────────
  function playDramatic(){
    init();
    // Deep rumble
    var bass = osc(55, 'sine', 0.4);
    lfo(bass, 'gain', 0.08, 0.15, 0);
    // Mid tension
    var mid = osc(110, 'triangle', 0.15);
    lfo(mid.osc, 'frequency', 0.05, 2, 0);
    // High shimmer
    var high = osc(440, 'sine', 0.04);
    lfo(high.gain, 'gain', 0.3, 0.03, 0);
    // Second pad
    var pad = osc(82.4, 'sine', 0.2, 0, 5);
    lfo(pad.gain, 'gain', 0.12, 0.1, 0);
    fadeIn(3);
  }

  // ── FUNNY ───────────────────────────────────────────────────────────────────
  function playFunny(){
    init();
    // Bouncy pluck simulation
    var notes = [261.6, 329.6, 392, 329.6, 261.6, 392, 440, 392];
    var bpm = 120;
    var beat = 60/bpm;
    notes.forEach(function(freq, i){
      var t = ctx.currentTime + i * beat * 0.5;
      var o = ctx.createOscillator();
      var g = ctx.createGain();
      o.type = 'triangle';
      o.frequency.value = freq;
      g.gain.setValueAtTime(0.25, t);
      g.gain.exponentialRampToValueAtTime(0.001, t + beat * 0.4);
      o.connect(g);
      g.connect(masterGain);
      o.start(t);
      o.stop(t + beat * 0.5);
      activeNodes.push(o);
    });
    // Loop the pattern
    var loopInterval = setInterval(function(){
      if(!ctx || activeNodes.length === 0) { clearInterval(loopInterval); return; }
      notes.forEach(function(freq, i){
        try{
          var t = ctx.currentTime + i * beat * 0.5;
          var o2 = ctx.createOscillator();
          var g2 = ctx.createGain();
          o2.type = 'triangle';
          o2.frequency.value = freq;
          g2.gain.setValueAtTime(0.2, t);
          g2.gain.exponentialRampToValueAtTime(0.001, t + beat * 0.4);
          o2.connect(g2);
          g2.connect(masterGain);
          o2.start(t);
          o2.stop(t + beat * 0.5);
          activeNodes.push(o2);
        }catch(e){}
      });
    }, notes.length * beat * 500);
    activeNodes.push({stop:function(){clearInterval(loopInterval);}});
    // Warm bass
    var bass = osc(130.8, 'sine', 0.2);
    lfo(bass.gain, 'gain', 0.5, 0.1, 0);
    fadeIn(1.5);
  }

  // ── ROMANTIC ────────────────────────────────────────────────────────────────
  function playRomantic(){
    init();
    // Warm pad - major chord
    var root = osc(261.6, 'sine', 0.25);    // C4
    var third = osc(329.6, 'sine', 0.18);   // E4
    var fifth = osc(392, 'sine', 0.15);     // G4
    var octave = osc(130.8, 'sine', 0.22);  // C3
    // Slow filter sweep effect via gain LFO
    lfo(root.gain, 'gain', 0.07, 0.1, 0);
    lfo(third.gain, 'gain', 0.05, 0.08, 0);
    lfo(fifth.gain, 'gain', 0.06, 0.07, 0);
    // Gentle shimmer
    var shimmer = osc(784, 'sine', 0.04);
    lfo(shimmer.gain, 'gain', 0.25, 0.03, 0);
    fadeIn(4);
  }

  // ── ACTION ──────────────────────────────────────────────────────────────────
  function playAction(){
    init();
    // Driving pulse
    var bpm = 140;
    var beat = 60/bpm;
    function pulse(){
      try{
        if(activeNodes.length === 0) return;
        var t = ctx.currentTime;
        var o = ctx.createOscillator();
        var g = ctx.createGain();
        o.type = 'sawtooth';
        o.frequency.value = 55;
        g.gain.setValueAtTime(0.3, t);
        g.gain.exponentialRampToValueAtTime(0.001, t + beat * 0.3);
        o.connect(g);
        g.connect(masterGain);
        o.start(t);
        o.stop(t + beat * 0.4);
        activeNodes.push(o);
      }catch(e){}
    }
    pulse();
    var pulseInt = setInterval(pulse, beat * 1000);
    activeNodes.push({stop:function(){clearInterval(pulseInt);}});
    // Tension layer
    var tension = osc(110, 'sawtooth', 0.08);
    lfo(tension.osc, 'frequency', 0.3, 5, 0);
    // High urgency
    var high = osc(880, 'sine', 0.04);
    lfo(high.gain, 'gain', 2, 0.03, 0);
    fadeIn(1);
  }

  // ── TRAGIC ──────────────────────────────────────────────────────────────────
  function playTragic(){
    init();
    // Single low tone, very sparse
    var low = osc(55, 'sine', 0.3);
    lfo(low.gain, 'gain', 0.04, 0.2, 0);
    // Minor third above
    var minor = osc(65.4, 'sine', 0.15);  // slightly detuned for sadness
    lfo(minor.gain, 'gain', 0.06, 0.05, 0);
    // Very faint high note
    var high = osc(220, 'sine', 0.06);
    lfo(high.osc, 'frequency', 0.02, 1, 0);
    lfo(high.gain, 'gain', 0.1, 0.04, 0);
    fadeIn(5);
  }

  // ── TRIUMPHANT ──────────────────────────────────────────────────────────────
  function playTriumphant(){
    init();
    // Building major chord
    var root = osc(130.8, 'sine', 0.28);   // C3
    var fifth = osc(196, 'sine', 0.2);     // G3
    var octave = osc(261.6, 'sine', 0.18); // C4
    var high = osc(392, 'sine', 0.12);     // G4
    // Slow swell
    lfo(root.gain, 'gain', 0.06, 0.15, 0);
    lfo(fifth.gain, 'gain', 0.08, 0.12, 0);
    lfo(octave.gain, 'gain', 0.1, 0.1, 0);
    // Rising shimmer
    var shimmer = osc(523.2, 'sine', 0.06);
    lfo(shimmer.gain, 'gain', 0.15, 0.05, 0);
    fadeIn(3);
  }

  function play(genre){
    stop();
    if(ctx&&ctx.state==='suspended')ctx.resume();
    setTimeout(function(){
      try{
        switch(genre){
          case 'dramatic':    playDramatic();    break;
          case 'funny':       playFunny();       break;
          case 'romantic':    playRomantic();    break;
          case 'action':      playAction();      break;
          case 'tragic':      playTragic();      break;
          case 'triumphant':  playTriumphant();  break;
          default:            playDramatic();    break;
        }
      }catch(e){ console.log('Music error:', e); }
    }, 100);
  }

  function unlock(){if(!ctx){ctx=new(window.AudioContext||window.webkitAudioContext)();masterGain=ctx.createGain();masterGain.gain.value=0;masterGain.connect(ctx.destination);}if(ctx.state==='suspended')ctx.resume();}
  return { play:play, stop:stop, unlock:unlock };
})();
