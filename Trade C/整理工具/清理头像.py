# -*- coding: utf-8 -*-
from pathlib import Path
import re
ROOT=Path('交易技术分析/Trade C')
def strip_avatar(text):
    # 仅匹配用户指定作者头像，保留图表及引用者名称/来源链接。
    image=r'!\[[^\]]*\]\([^\s)]*E5MklIEP[^\s)]*\)'
    text=re.sub(r'\[\s*'+image+r'\s*\]\([^\s)]+\)', '', text)
    text=re.sub(image, '', text)
    text=re.sub(r'!\[\[[^\]\n]*E5MklIEP[^\]\n]*\]\]', '', text)
    return text

def cleanup():
    removed=changed=0
    for p in ROOT.rglob('*E5MklIEP*'):
        if p.is_file() and p.suffix.lower() in {'.jpg','.jpeg','.png','.webp'}:
            p.unlink();removed+=1
    for p in ROOT.rglob('*.md'):
        old=p.read_text();new=strip_avatar(old)
        if new!=old:p.write_text(new);changed+=1
    return removed,changed
if __name__=='__main__':print('已删除头像、已清理笔记：',cleanup())
