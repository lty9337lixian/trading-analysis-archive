# -*- coding: utf-8 -*-
from pathlib import Path
import json,collections
root=Path('交易技术分析/Trade C');rows=json.loads((root/'整理工具/归档目录.json').read_text());months=collections.defaultdict(list)
for r in rows:months[r['date'][:7]].append(r)
text='''---
title: Trade C交易学习索引
source: https://x.com/TradercBTC
date: 2026-09-06
---

# Trade C交易学习索引

账号：**trader-c（@TradercBTC）**。整理时间范围：**2026-01-01—2026-09-06**，日期统一按北京时间排列。

## 学习入口

- [[01-Trade C交易思路详解]]：从市场背景、结构、入场、风险到退出，串联案例与学习步骤。
- [[02-Trade C方法演变与易误读点]]：保留不同阶段的规则变化、原文矛盾与统计边界。
- [[04-Trade C读图与复盘术语速查]]：常见缩写与读图过程。
- [[06-MSKR第三方推理与交易框架对照]]：新增第三方状态与约束思路，区分已知与推断。
- [[07-MSKR第三方推理原稿]]：用户提供原稿，未经核实。
- [[05-独立Agent审查与修复记录]]：本轮发现的问题、修复与审查边界。
- [[03-检索范围与归档核对]]：检索路径、实际覆盖、图片和正文的限制。

下方按发布时间从早到晚排列。每条笔记含原帖链接、作者正文及可获取附图。**原帖归档与编辑总结分开**；只发布图表或视频链接的记录，不擅自补写未见到的交易理由。

'''
text+=f'当前已生成 **{len(rows)}条原帖笔记**。\n\n'
for month,rs in sorted(months.items()):
 text+=f'## {month}（{len(rs)}条）\n\n'
 for r in rs:text+=f"- {r['date'][5:10]} {r['date'][11:16]} · [[{r['name']}|{r['title']}]]\n"
 text+='\n'
(root/'00-Trade C交易学习索引.md').write_text(text)
print('indexed',len(rows))
