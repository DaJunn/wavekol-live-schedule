#!/usr/bin/env python3
# 查海外主播直播排期：给定日期(默认明天) -> 输出当天开播主播/跟播人/时间
import sys, json, subprocess, datetime, re

SHEET_TOKEN = "MpCXswDMHhgTuKtyGyacxcpXncb"  # 海外主播排期-小浪花（wiki UR0Gwg3K0i2Vvjk9ud7c10Qin6f 解析所得）
NOPLAY = {"/", "休", "x", "X", "无"}

def lark(args):
    r = subprocess.run(["lark-cli"]+args, capture_output=True, text=True)
    try: return json.loads(r.stdout)
    except: 
        sys.stderr.write(r.stdout[:500]+r.stderr[:500]); return {}

def col_letter(n):  # 1->A
    s=""
    while n>0: n,r=divmod(n-1,26); s=chr(65+r)+s
    return s

def celltxt(v):
    if v is None: return ""
    if isinstance(v,list):
        return "".join(seg.get("text","") for seg in v if isinstance(seg,dict)).replace("\n"," ").strip()
    return str(v).replace("\n"," ").strip()

def main():
    # 目标日期
    if len(sys.argv)>1 and re.match(r"\d{4}-\d{2}-\d{2}", sys.argv[1]):
        d = datetime.date.fromisoformat(sys.argv[1])
    else:
        d = datetime.date.today() + datetime.timedelta(days=1)
    wk = ["周一","周二","周三","周四","周五","周六","周日"][d.weekday()]
    month = d.month; day = d.day
    # 找月页签
    info = lark(["sheets","+info","--spreadsheet-token",SHEET_TOKEN])
    sheets = info.get("data",{}).get("sheets",{}).get("sheets",[])
    sid=None
    for s in sheets:
        t=s.get("title","")
        if t==f"{month}月":
            sid=s.get("sheet_id"); break
    if not sid:
        print(f"没找到「{month}月」页签"); return
    col = day + 2          # C=1号 -> 列号 = day+2
    cl = col_letter(col)
    # 读 A:目标列 (含B开播时间)
    rng = f"{sid}!A3:{cl}80"
    rd = lark(["sheets","+read","--spreadsheet-token",SHEET_TOKEN,"--range",rng])
    rows = rd.get("data",{}).get("valueRange",{}).get("values",[])
    if not rows: print("读取失败"); return
    # 校验列对不对：第4行(索引1)该列应=星期
    wk_cell = celltxt(rows[1][col-1]) if len(rows)>1 and len(rows[1])>=col else ""
    warn = "" if wk_cell==wk else f"  ⚠️列星期({wk_cell})与目标({wk})不符,表结构可能变,请核对"
    print(f"📅 {d.isoformat()} {wk}  (排期表 {month}月 / {cl}列){warn}\n")
    play=[]; rest=[]; blank=[]
    for r in rows[2:]:
        name = celltxt(r[0]) if len(r)>0 else ""
        if not name or name.startswith("北京") or len(name)>14 or name in("主播","开播时间"): continue
        tm = celltxt(r[1]) if len(r)>1 else ""
        # 固定直播日(在开播时间列文本里)
        fixed = re.search(r"固定[直播日时间]*[:：]?\s*([一二三四五六日、,，\s]+)", tm)
        fixedset = set(re.findall("[一二三四五六日]", fixed.group(1))) if fixed else set()
        cell = celltxt(r[col-1]) if len(r)>=col else ""
        wkc = wk[1]  # 周X 的 X
        if cell and not any(cell.startswith(x) for x in NOPLAY) and "休" not in cell and "请假" not in cell:
            play.append((name, cell, tm.split("固定")[0].strip()[:40]))
        elif cell in NOPLAY or "休" in cell or "请假" in cell:
            rest.append((name, cell))
        else:  # 空白 -> 用固定日推断
            if fixedset and wkc in fixedset:
                blank.append((name, tm.split("固定")[0].strip()[:40]))
    print("✅ 开播（已排跟播人）：")
    for n,gen,t in play: print(f"  · {n}  跟播:{gen}  {t}")
    if not play: print("  （无）")
    if blank:
        print("\n🟡 按固定直播日应播、但跟播栏空（待排班确认）：")
        for n,t in blank: print(f"  · {n}  {t}")
    if rest:
        print("\n❌ 不播：", "、".join(n for n,_ in rest))
    print("\n注：表有合并单元格,机读跟播人可能错位;以「固定直播日+颜色」为准,存疑请人工瞄一眼。")

main()
