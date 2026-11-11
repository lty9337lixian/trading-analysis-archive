# -*- coding: utf-8 -*-
from pathlib import Path
import json,re,datetime,shutil
from 清理头像 import strip_avatar, cleanup
ROOT=Path('交易技术分析/Trade C'); RAW=ROOT/'原始抓取'; rows=[]; failures=[]
FIXES=json.loads((ROOT/'整理工具/审查正文修复.json').read_text()) if (ROOT/'整理工具/审查正文修复.json').exists() else {}
OVERRIDES={'2008910015269155202':'SOL：我的计划','2017610785799934206':'alawys short BTC ETH SOL','2021033900835995752':'日经指数：太强了','2046149294454194653':'保本止损通常不是最优选择','2095105306040897680':'BTC的结构非常清晰','2020162816163082257':'黄金：周线趋势与高位箱体交易计划','2054828075410682209':'止损应服从入场前的交易逻辑','2096283788078977071':'固定止盈、趋势与收益右尾的再思考','2096279849002574186':'风险预算与情绪性止盈的区别','2096276990559220157':'出场决策与成本价锚定','2096273573623238881':'压榨利润与控制风险如何平衡','2096187250094850277':'SOL错误复盘：主观剧本与结构失效','2096177695034093668':'BTC错失两次机会：提前离场与跨品种干扰','2096192103445668055':'周度交易自报统计与执行遗漏','2092454165402493086':'复盘普涨山寨（上）','2091716251999690863':'黄金复盘：止损范围与突破后确认','2091718714534359281':'WLD复盘：合理亏损与重复试错','2088599228398665732':'WLD复盘：下跌减弱不等于反转','2088595421597978948':'LDO复盘：周期过小与主观方向','2071444664398311522':'黄金日内交易系统（六月版本）','2039554198124285989':'BTC交易003：从放弃到盈利的思路演变','2006715761864437925':'BTC新年交易计划（图表帖）','2006395058145333754':'跨年最后一笔仓位止盈记录','2077593081243914523':'C哥完整交易系统框架（全量推文版）','2031741978728374674':'恒科周内复盘：EMA50与ATR','2044668276614332423':'修正交易系统定义：三个模块不等于完整系统'}
def maintext(d):
 doc=d.get('document') or {}; b='\n\n'.join(x.get('markdown','') for x in doc.get('content',[]) if x.get('markdown'))
 b=b.split('Only some accounts can reply.')[0]
 # 从主帖发布时间之后截断，避免把其他用户回复混入作者正文。
 id=Path(doc.get('requestedUrl',doc.get('url',''))).name
 if id:
  pat=r'\[\d{1,2}:\d{2}[^\n]*?\]\(https://x\.com/TradercBTC/status/'+re.escape(id)+r'\)[^\n]*'
  m=re.search(pat,b)
  if m:b=b[:m.start()]
 # 删除X悬浮行情卡，卡中现价属于抓取时界面，不是原帖记录。
 b=re.sub(r'-?\s*\[!\[[^\]]*\]\([^\n]+\)\s*\n(?:(?!\n\n).)*?\]\(https://x\.com/search\?[^\n]*src=typeahead_click\)', '', b, flags=re.S)
 b=re.sub(r'^[ \t]*-?[ \t]*\[\s*!\[[^\]]*\]\([^)]+\)\s*[^\[\]]{0,300}\]\(https://x\.com/search\?[^\n]*src=typeahead_click\)', '', b, flags=re.M)
 # 只清理最开头的作者头像与名字，不删除引用帖的作者标识。
 b=re.sub(r'\A\s*-?\s*\[!\[@TradercBTC\]\([^\n]+\)\]\(https://x.com/TradercBTC\)\s*','',b)
 b=re.sub(r'\A\s*\[\s*!\[@TradercBTC\]\([^\n]+\)\s*\]\(https://x.com/TradercBTC\)\s*','',b)
 b=re.sub(r'\A\s*\[trader-c\]\(https://x.com/TradercBTC\)\s*','',b)
 b=re.sub(r'\A\s*\[@TradercBTC\]\(https://x.com/TradercBTC\)\s*','',b)
 b=re.sub(r'^\t', '', b.strip(), flags=re.M)
 if id in FIXES:
  fix=FIXES[id];old=b;b=fix['text']
  if fix.get('previous_as_quote'):
   b+='\n\n### 被引用帖内容（与本帖主文分开）\n\n'+('引用来源：'+fix['quote_source']+'\n\n' if fix.get('quote_source') else '')+old
 if id=='2020162816163082257':
  b=b.replace('[$GOLD](https://x.com/search?q=$GOLD)', '### 被引用帖（2026-02-04，非本帖主文）\n\n引用来源：https://x.com/TradercBTC/status/2018893216653709535\n\n[$GOLD](https://x.com/search?q=$GOLD)',1)
 return strip_avatar(b)
for p in sorted(RAW.glob('*.json')):
 if not p.stem.isdigit():continue
 try:
  d=json.loads(p.read_text());retry=RAW/(p.stem+'.审查重抓.json')
  if retry.exists():d=json.loads(retry.read_text())
  doc=d.get('document') or {};b=maintext(d)
  if d.get('status')!='ok' or not b or re.search(r'Something went wrong|Try reloading|I scream\. You scream',b) or not doc.get('publishedAt'):failures.append(p.stem);continue
  dt=datetime.datetime.fromisoformat(doc['publishedAt'].replace('Z','+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=8)))
  if not ('2026-01-01'<=dt.date().isoformat()<='2026-09-06'):continue
  t=OVERRIDES.get(p.stem)
  if not t:
   h=re.search(r'^\s*#{1,3} (.+)$',b,re.M)
   t=h.group(1) if h else re.sub(r'^trader-c on X: ["“]?','',doc.get('title',''))
   t=t.split('\n')[0];t=re.sub(r'["”]? / X$','',t)
   if 'https://' in t or not t.strip():t='交易思考与记录'
   t=re.sub(r'[/\\:*?"<>|\[\]#]','',t).strip()[:48]
  if 'native' in t or '0x' in t:
   t=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',b.split('\n')[0])[:48]
   t=re.sub(r'[/\\:*?"<>|\[\]#]','',t).strip()
  name=f'{dt:%Y-%m-%d %H%M} {t} {p.stem[-6:]}'
  existing=sorted((ROOT/'复盘与交易记录').glob('* '+p.stem[-6:]))
  if existing and not (ROOT/'复盘与交易记录'/name).exists():name=existing[0].name
  folder=ROOT/'复盘与交易记录'/name;folder.mkdir(parents=True,exist_ok=True)
  media=[]
  for m in (d.get('downloads') or {}).get('replacements',[]):
   if '/profile_images/' in m['url']:continue
   src=Path(m['absolutePath'])
   if not src.exists():continue
   dest=folder/'images'/src.name;dest.parent.mkdir(exist_ok=True)
   if not dest.exists():shutil.copy2(src,dest)
   embed=f'![[交易技术分析/Trade C/复盘与交易记录/{name}/images/{dest.name}]]'
   media.append((m['url'],embed))
   b=re.sub(r'!\[[^\]]*\]\('+re.escape(m['url'])+r'\)',lambda _:embed,b)
  # 通用抓取只把封面放在元数据时，也须嵌到正文。
  extra=[e for u,e in media if e not in b and '/media/' in u]
  if extra:b+='\n\n### 原帖可获取的附图\n\n'+'\n\n'.join(extra)
  # 公开嵌入接口仅用于核对与补齐主帖图片，不用截断文本替换长文。
  sp=RAW/'图片补充'/(p.stem+'.json');own_count=0
  if sp.exists():
   sd=json.loads(sp.read_text());photos=[m.get('media_url_https') for m in sd.get('mediaDetails',[]) if m.get('type')=='photo']
   if not photos:photos=[m.get('url') for m in sd.get('photos',[])]
   def media_key(u):return re.sub(r'\.(?:png|jpg|jpeg|webp)$','',u.split('/media/')[-1].split('?')[0].split(':')[0])
   for number,u in enumerate(photos,1):
    ext=Path(u.split('?')[0]).suffix or '.jpg';src=RAW/'图片补充'/p.stem/f'photo-{number:02d}{ext}'
    if not src.exists():continue
    dest=folder/'images'/src.name;dest.parent.mkdir(exist_ok=True)
    if not dest.exists():shutil.copy2(src,dest)
    embed=f'![[交易技术分析/Trade C/复盘与交易记录/{name}/images/{dest.name}]]';replaced=False
    for old_u,old_e in media:
     if media_key(old_u)==media_key(u) and old_e in b:b=b.replace(old_e,embed);replaced=True
    if not replaced:b+=f'\n\n### 原帖主图 {number}\n\n'+embed
    own_count+=1
  b=re.sub(r"\[(!\[\[[^\n]+?\]\])\]\(https?://[^\s)]+\)", r"\1", b)
  seen_images=set()
  def unique_embed(m):
   if m.group(0) in seen_images:return ''
   seen_images.add(m.group(0));return m.group(0)
  b=re.sub(r'!\[\[[^\n]+?\]\]',unique_embed,b)
  b=re.sub(r'### 原帖(?:可获取的附图|主图 \d+)\s*(?=### |$)','',b)
  # 保留引用链接；图文引自其他帖子时不视为主帖自有图片。
  source='https://x.com/TradercBTC/status/'+p.stem
  note='---\ntitle: '+json.dumps(t,ensure_ascii=False)+'\nsource: '+source+f'\ndate: {dt:%Y-%m-%d}\n---\n\n# '+t+f'\n\n[原帖]({source}) · 发布时间：{dt:%Y-%m-%d %H:%M}（北京时间）\n\n'
  note+='> [!info] 原帖归档\n> 以下是网页抓取的作者正文及页面中的引用内容。交易价格、收益与概率属于作者当时的记录或判断，未当作经审计业绩。图片以本地实际下载内容为准；完整附件请对照原帖。\n\n'
  if p.stem=='2077593081243914523':note+='> [!note] 线程范围\n> “全量推文版”是原帖标题。本页保存线程首帖；评论区的全部分层链接并未完整抓取，不能将本页视为全线程合集。\n\n'
  note+='## 原帖内容\n\n'+b+'\n\n---\n\n返回 [[00-Trade C交易学习索引]] · 结合 [[01-Trade C交易思路详解]] 阅读。\n'
  (folder/(name+'.md')).write_text(note)
  rows.append({'id':p.stem,'date':dt.isoformat(),'title':t,'name':name,'path':str(folder/(name+'.md')),'chars':len(b),'images':len(media),'main_photos':own_count})
 except Exception as e:failures.append(p.stem+':'+str(e))
rows.sort(key=lambda r:(r['date'],r['id']))
(ROOT/'整理工具/归档目录.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps({'archived':len(rows),'failed':failures},ensure_ascii=False))

cleanup()  # 用户要求不保留该作者头像；同步清理抓取副本与旧笔记。
