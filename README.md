# 交易技术分析归档

2026-11-11 上传快照，包含 48k纯白、线索C、Trade C、Z说交易、Keyshotvv 五个文件夹。

笔记、图片、字幕及其他文件保留原始目录结构。36 个 MP4 视频原件放在私有 Release `snapshot-2026-11-11` 的分卷附件中，未转码。`FILE_MANIFEST.json` 记录全部源文件的大小和 SHA-256；`VIDEO_PARTS.json` 记录视频分卷校验值。

## 下载并恢复视频

需要登录拥有此私有仓库访问权限的 GitHub 账号，并安装 GitHub CLI。

```bash
gh repo clone lty9337lixian/trading-analysis-archive
cd trading-analysis-archive
gh release download snapshot-2026-11-11 --repo lty9337lixian/trading-analysis-archive --pattern 'videos.tar.part*' --dir video-parts
cat video-parts/videos.tar.part* | tar -xf -
```

解包后视频回到对应笔记的原始 videos 目录。分卷必须全部下载后再解包。
