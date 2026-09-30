# 直播排期查询

查询飞书排期表中指定日期的带货者、跟播人和开播时间，区分已排班、固定日应播但待确认、表内休息。

## 安装与使用

```bash
git clone https://github.com/DaJunn/wavekol-live-schedule.git ~/.agents/skills/wavekol-live-schedule
cd ~/.agents/skills/wavekol-live-schedule
python3 bin/query-schedule.py 2026-10-08
```

也可对 AI 说：「查明天谁开播、谁跟播」或「汇总这周排期」。多日查询逐日运行后汇总。

## 需要什么

Python 3、已登录的 `lark-cli` 用户身份，以及默认飞书排期表的访问权限。无需浏览器桥接；其他团队需在脚本中配置自己的表并核对结构。

## 使用边界

只读查询。脚本按月页签读取到第 80 行，不读取颜色或自动处理合并单元格；空白、错位、跨年和星期不符需核对源表，不能直接判为不播或确定开播。

完整流程与表结构见 [SKILL.md](SKILL.md)。更多技能见 [DaJunn](https://github.com/DaJunn)。
