#!/usr/bin/env python3
"""每天从 titles.txt 随机抽取 10 条，生成美区 Apple ID 风格表格"""

import random
import datetime
import re
import os
import sys

SAMPLE_SIZE = 10
TZ = datetime.timezone(datetime.timedelta(hours=8))
REGIONS = ["美区", "港区", "日区", "台区", "韩区"]

def random_time(today: datetime.date) -> str:
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    day = today - datetime.timedelta(days=1) if random.random() < 0.3 else today
    return f"{day.isoformat()} {hour:02d}:{minute:02d}:{second:02d}"

def main():
    today = datetime.datetime.now(TZ).date()

    if not os.path.exists("titles.txt"):
        sys.exit("❌ 找不到 titles.txt")

    with open("titles.txt", encoding="utf-8") as f:
        titles = [line.strip() for line in f if line.strip()]

    if len(titles) < SAMPLE_SIZE:
        sys.exit(f"❌ 标题数量不足 {SAMPLE_SIZE} 个")

    selected = random.sample(titles, SAMPLE_SIZE)

    lines = [
        f"> 🍎 **{today.isoformat()} 已更新 · 今日 {len(selected)} 个公开共享账号**",
        "> （本表每天 0:00 自动随机更新，账号已打码显示）",
        "",
        "| 地区 | 账号(打码) | 密码 | 来源检测时间 |",
        "| --- | --- | --- | --- |",
    ]

    for title in selected:
        region = random.choice(REGIONS)
        account = title[:42] + "..." if len(title) > 42 else title
        account = account.replace("|", "\\|")
        lines.append(f"| {region} | `{account}` | `••••••••` | {random_time(today)} |")

    lines += [
        "",
        f"> 数据来源：本仓库 titles.txt（共 {len(titles)} 条） · 每日自动随机抽取",
        "",
        "想要稳定独享账号请点击下方购买按钮。",
    ]

    new_section = "\n".join(lines)

    with open("README.md", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!-- DAILY:START -->\n(.*?)\n<!-- DAILY:END -->"
    match = re.search(pattern, content, re.S)
    if not match:
        sys.exit("❌ README.md 缺少 <!-- DAILY:START --> 和 <!-- DAILY:END --> 标记")

    new_content = content[:match.start(1)] + new_section + content[match.end(1):]

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ 已更新 {today.isoformat()}，生成了 {len(selected)} 条记录")

if __name__ == "__main__":
    main()
