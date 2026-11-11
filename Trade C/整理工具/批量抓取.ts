import fs from 'node:fs';
import {spawn} from 'node:child_process';
const base=process.cwd();
const {connectChrome}=await import(base+'/.agents/skills/baoyu-url-to-markdown/scripts/vendor/baoyu-fetch/src/browser/chrome-launcher.ts');
const conn=await connectChrome({headless:false});
const endpoint=conn.origin || conn.browserWsUrl;
const ids=[...new Set([...JSON.parse(fs.readFileSync('交易技术分析/Trade C/原始抓取/复盘检索清单.json','utf8')),...fs.readFileSync('交易技术分析/Trade C/原始抓取/补充检索清单.txt','utf8').trim().split(/\s+/)])] as string[];
let cursor=0,done=0;
async function worker(){while(cursor<ids.length){const id=ids[cursor++];const out='交易技术分析/Trade C/原始抓取/'+id+'.json';if(fs.existsSync(out)){const old=JSON.parse(fs.readFileSync(out,'utf8'));if(old.document?.publishedAt && old.document?.content?.length){done++;continue;}fs.copyFileSync(out,out+'.failed-backup');}
const args=['-y','bun','.agents/skills/baoyu-url-to-markdown/scripts/vendor/baoyu-fetch/src/cli.ts','https://x.com/TradercBTC/status/'+id,'--cdp-url',endpoint,'--adapter','generic','--timeout','12000','--format','json','--output',out,'--download-media','--media-dir','交易技术分析/Trade C/原始抓取/'+id];
const code=await new Promise<number|null>(resolve=>{const log=fs.createWriteStream('交易技术分析/Trade C/原始抓取/'+id+'.log');const p=spawn('npx',args,{stdio:['ignore','pipe','pipe']});p.stdout.pipe(log);p.stderr.pipe(log);const tm=setTimeout(()=>p.kill('SIGTERM'),55000);p.on('close',c=>{clearTimeout(tm);log.end();resolve(c);});});done++;console.log(done+'/'+ids.length,id,code);
}}
try {await Promise.all([worker(),worker()]);}finally{await conn.close();}
