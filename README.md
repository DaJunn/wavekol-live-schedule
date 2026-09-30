# wavekol-live-schedule

**海外带货者直播排期查询** —— 一句话查某天谁开播、跟播人是谁、开播时间，自动处理合并单元格

让 AI agent（DSH / Codex / Claude Code 等）使用。

## 解决什么问题

之前想知道「明天谁开播、谁跟播」，得翻飞书排期表、对日期列、还容易看错合并单元格。

现在一句话就能查，脚本自动定位月页签、按日期算列、读跟播人和开播时间，并用「固定直播日」交叉核对防止读错。

## 前置依赖

1. **kimi-webbridge daemon** 在跑：
   ```bash
   ~/.kimi-webbridge/bin/kimi-webbridge status   # 要 running:true + extension_connected:true
   ```
   没装：`curl -fsSL https://cdn.kimi.com/webbridge/install.sh | bash`
2. **Chrome 已登录对应后台**。本系列只复用你自己已打开的标签页，**不代登录**。
3. **飞书表《海外主播排期-小浪花》的访问权限**（数据源就是这张表）

## 安装

```bash
git clone https://github.com/DaJunn/wavekol-live-schedule.git \
  ~/.agents/skills/wavekol-live-schedule
```

## 触发方式

```bash
python3 ~/.agents/skills/wavekol-live-schedule/bin/query-schedule.py            # 默认查【明天】
python3 ~/.agents/skills/wavekol-live-schedule/bin/query-schedule.py 2026-10-08 # 查指定日期
```

问「这周/这几天」时，把 7 个日期各跑一次再汇总——**别只跑一天当一周**。


触发词：「明天谁开播」、「X 月 X 号谁播」、「这周谁有播」、「排期表看一下」

## 说明

- 输出分三档：✅ 已排跟播人开播 / 🟡 按固定日应播但跟播栏空（待排班）/ ❌ 不播
- 单元格空白**不是「不播」**，是跟播未填，标黄提醒
- 脚本报「列星期不符 / token 失效」时别信结果，要人工核对

## 相关

- 完整技能合集见飞书文档《AI减负视频号运营技能合集》
- 更多 skill：https://github.com/DaJunn
