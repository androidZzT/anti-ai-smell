#!/usr/bin/env python3
"""anti-ai-smell —— 中文去 AI 味 linter。

扫一份中文稿子，标出 AI 味词汇（生造词/翻译腔/戏剧化/宏大官腔/套话）和 AI 味句式，
并给出母语者真正会说的「人话」替代。

用法：
    python3 lint.py <file> [<file> ...]
    python3 lint.py --list                # 打印整张词表
    python3 lint.py <file> --soft-ok      # 只有 hard 级命中才非零退出

退出码：0 = 未命中 hard 级；1 = 命中 hard 级（宏大官腔 / 套话）。
soft 级（生造/翻译腔/戏剧化/带味字/句式）只提示，不影响退出码。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "ai-flavor-words.json")

C = {"red": "\033[31m", "yellow": "\033[33m", "green": "\033[32m",
     "dim": "\033[2m", "bold": "\033[1m", "cyan": "\033[36m", "off": "\033[0m"}


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def list_table(db):
    for cat in db["categories"]:
        sev = "hard" if cat["severity"] == "hard" else "soft"
        print(f"\n{C['bold']}{cat['title']}{C['off']} [{sev}] — {cat['desc']}")
        for it in cat["words"]:
            en = f" ({it['en']})" if it.get("en") else ""
            human = " / ".join(it["human"])
            note = f"  {C['dim']}// {it['note']}{C['off']}" if it.get("note") else ""
            print(f"  {C['yellow']}{it['w']}{C['off']}{en}  →  {C['green']}{human}{C['off']}{note}")
    print(f"\n{C['bold']}句式{C['off']} [soft]")
    for p in db["syntax_patterns"]:
        print(f"  {C['yellow']}{p['title']}{C['off']}  →  {C['green']}{p['hint']}{C['off']}")


def scan(text, db):
    """返回 (hits, hard_count)。hits: list of dict。"""
    hits = []
    hard = 0
    for cat in db["categories"]:
        is_hard = cat["severity"] == "hard"
        for it in cat["words"]:
            w = it["w"]
            n = text.count(w)
            if n:
                hits.append({"kind": "word", "cat": cat["title"], "hard": is_hard,
                             "w": w, "en": it.get("en", ""), "n": n,
                             "human": it["human"], "note": it.get("note", "")})
                if is_hard:
                    hard += n
    for p in db["syntax_patterns"]:
        m = re.findall(p["regex"], text)
        if m:
            hits.append({"kind": "syntax", "cat": "句式", "hard": False,
                         "w": p["title"], "en": "", "n": len(m),
                         "human": [p["hint"]], "note": ""})
    return hits, hard


def report(path, hits, hard):
    name = os.path.basename(path)
    if not hits:
        print(f"{C['green']}✓{C['off']} {name}  干净")
        return
    total = sum(h["n"] for h in hits)
    tag = f"{C['red']}✗{C['off']}" if hard else f"{C['yellow']}⚠{C['off']}"
    print(f"\n{tag} {C['bold']}{name}{C['off']}  命中 {total} 处（hard {hard}）")
    order = {}
    for h in hits:
        order.setdefault(h["cat"], []).append(h)
    for cat, items in order.items():
        print(f"  {C['cyan']}{cat}{C['off']}")
        for h in items:
            en = f" ({h['en']})" if h["en"] else ""
            human = " / ".join(h["human"])
            note = f"  {C['dim']}// {h['note']}{C['off']}" if h["note"] else ""
            print(f"    {C['yellow']}{h['w']}{C['off']}{en} ×{h['n']}  →  "
                  f"{C['green']}{human}{C['off']}{note}")


def main(argv):
    db = load()
    if "--list" in argv:
        list_table(db)
        return 0
    soft_ok = "--soft-ok" in argv
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 0
    total_hard = 0
    for path in files:
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"{C['red']}无法读取 {path}: {e}{C['off']}")
            continue
        hits, hard = scan(text, db)
        total_hard += hard
        report(path, hits, hard)
    print()
    if total_hard and not soft_ok:
        print(f"{C['red']}hard 级命中 {total_hard} 处（宏大官腔 / 套话），建议清零。{C['off']}")
        return 1
    print(f"{C['green']}无 hard 级命中。soft 级按语境自行判断。{C['off']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
