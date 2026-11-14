/* Pre-renders the light-show music from the page's own synth code (site/index.html: AUD + SCORES) with an
   offline Web Audio context, and writes 16-bit WAVs. usage: node render-music.js <index.html> <outdir> [score keys...]  (default: all)
   The page plays these files instead of synthesizing live (too heavy for the projector's CPU). */
const fs=require('fs'),path=require('path'),W=require('node-web-audio-api');
const [,,htmlPath,outDir,...only]=process.argv;
const html=fs.readFileSync(htmlPath,'utf8');
const a=html.indexOf('const mtof='),m=html.indexOf('const PHOENIX_MEL=');
const b=html.indexOf('})();',m)+5;
if(a<0||m<0||b<5)throw new Error('engine block not found');
const src=html.slice(a,b);
const env={window:{},location:{search:''},performance:{now:()=>Date.now()},toast:()=>{},LITE:false,addEventListener:()=>{},setInterval,clearInterval,setTimeout};
const {AUD,SCORES}=new Function(...Object.keys(env),src+';return {AUD,SCORES};')(...Object.values(env));

const LEAD=.1,SR=44100;
function wav(buf,file,level=1){
  const ch=buf.numberOfChannels,n=buf.length,data=[...Array(ch)].map((_,i)=>buf.getChannelData(i));
  let peak=0;for(const d of data)for(let i=0;i<n;i++)peak=Math.max(peak,Math.abs(d[i]));
  const g=peak>0?0.89*level/peak:1; // normalise to about -1 dBFS (times the score's level, e.g. a calmer piece)
  const out=Buffer.alloc(44+n*ch*2);
  out.write('RIFF',0);out.writeUInt32LE(36+n*ch*2,4);out.write('WAVE',8);out.write('fmt ',12);
  out.writeUInt32LE(16,16);out.writeUInt16LE(1,20);out.writeUInt16LE(ch,22);out.writeUInt32LE(SR,24);
  out.writeUInt32LE(SR*ch*2,28);out.writeUInt16LE(ch*2,32);out.writeUInt16LE(16,34);out.write('data',36);out.writeUInt32LE(n*ch*2,40);
  let o=44;for(let i=0;i<n;i++)for(let c=0;c<ch;c++){const v=Math.max(-1,Math.min(1,data[c][i]*g));out.writeInt16LE(Math.round(v*32767),o);o+=2;}
  fs.writeFileSync(file,out);return {peak,gain:g};
}
(async()=>{
  fs.mkdirSync(outDir,{recursive:true});
  for(const [key,score] of Object.entries(SCORES)){
    if(only.length&&!only.includes(key))continue;
    const spb=60/score.bpm/4,len=LEAD+score.steps*spb+3;
    const c=new W.OfflineAudioContext(2,Math.ceil(len*SR),SR);
    AUD.ctx=null;AUD.init(c);
    /* Offline there is no CPU limit: add a proper convolution reverb next to the cheap echoes. */
    const L=Math.floor(SR*2.2),ir=c.createBuffer(2,L,SR);
    for(let k=0;k<2;k++){const d=ir.getChannelData(k);for(let i=0;i<L;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/L,2.6);}
    const conv=c.createConvolver();conv.buffer=ir;const cg=c.createGain();cg.gain.value=.35;AUD.rev.connect(conv);conv.connect(cg);cg.connect(AUD.out);
    const r={aud:true,t0:LEAD,bus:c.createGain(),send:c.createGain(),notes:0,late:0,cues:[]};
    r.bus.connect(AUD.out);r.send.connect(AUD.rev);
    const X=AUD.api(r);
    for(let st=0;st<score.steps;st++)score.at(st,LEAD+st*spb,X);
    const t0=Date.now(),buf=await c.startRendering();
    const file=path.join(outDir,key+'.wav'),info=wav(buf,file,score.level||1);
    console.log(key+': '+score.steps+' steps, '+len.toFixed(1)+' s, '+r.notes+' notes, rendered in '+((Date.now()-t0)/1000).toFixed(1)+' s, peak '+info.peak.toFixed(2)+' -> '+file);
  }
})().catch(e=>{console.error(e);process.exit(1);});
