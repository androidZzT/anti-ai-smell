<div align="center">
  <img src="docs/hero.png" width="720" alt="anti-ai-smell" style="border-radius: 16px;">

  <h1>anti-ai-smell</h1>
  <p><strong>把 AI 味的中文改成人话 · Turn AI-flavored Chinese back into plain human speech.</strong></p>
  <p><em>A zero-dependency linter + word table + Claude skill. It catches the words AI keeps writing in Chinese, and tells you what a person would actually say.</em></p>

  <p>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-ff7b54?style=flat-square" alt="License: MIT"></a>
    <img src="https://img.shields.io/badge/Python-3-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3">
    <img src="https://img.shields.io/badge/deps-none-1a9e6b?style=flat-square" alt="No dependencies">
    <img src="https://img.shields.io/badge/Claude-Skill-ff7b54?style=flat-square" alt="Claude Skill">
    <a href="https://github.com/androidZzT/anti-ai-smell/stargazers"><img src="https://img.shields.io/github/stars/androidZzT/anti-ai-smell?style=flat-square&color=ff7b54" alt="Stars"></a>
  </p>

  <p>
    <a href="#what-it-does">What</a> &bull;
    <a href="#quick-start">Quick start</a> &bull;
    <a href="#the-word-table">Word table</a> &bull;
    <a href="#two-rules">Rules</a> &bull;
    <a href="#contributing">Contributing</a> &bull;
    <a href="README_CN.md">中文</a>
  </p>
</div>

---

## What it does

AI writes Chinese with a recognizable "smell". It hard-translates English concepts into stiff words no native speaker uses — `门控` (gate), `横切` (cross-cutting), `一等公民` (first-class); it coins words like `切法` and `硬货`; it dresses plain facts in theatrics like `理直气壮的谎` ("a defiant lie"); and it leans on grand officialese — `赋能` (empower), `涌现` (emerge), `不仅仅……而是……` (not just… but…).

Each word is fine on its own. Pile them up and any reader instantly knows: a machine wrote this.

**anti-ai-smell does one thing: it flags those words and gives you the plain version.**

It is a linter plus a word table, and also a [Claude Skill](https://docs.claude.com/en/docs/claude-code/skills). It complements sentence-level de-AI tools that target syntax — those handle sentence structure, this handles the **Chinese word choices**.

<div align="center">
  <img src="docs/lint-demo.png" width="720" alt="lint output" style="border-radius: 12px;">
</div>

---

## Quick start

```bash
git clone https://github.com/androidZzT/anti-ai-smell.git
cd anti-ai-smell

# Scan a draft
python3 lint.py your-article.md

# Print the whole table
python3 lint.py --list
```

Python 3, no third-party dependencies. Exit code `1` on a **hard**-level hit (grand officialese / filler), `0` otherwise — drop it into CI if you like.

---

## The word table

51 words across 6 categories, plus a handful of AI-smell syntax patterns (em-dash overuse, rhetorical questions, "not just… but…", emoji, and more).

| Category | Example | Plain (人话) |
|---|---|---|
| **Coined** 生造词 | 切法 / 硬货 / 打法 | this angle / real substance / approach |
| **Translationese** 翻译腔 | 门控(gate) / 横切(cross-cutting) / 鲁棒(robust) / 一等公民(first-class) | gatekeep / the common part / solid / native support |
| **Theatrical** 戏剧化 | 理直气壮的谎 / 欢快的成功 / 最容易的死法 | reported success but failed / another "success" / where it breaks most easily |
| **Loaded** 带味的字 | 偷师 / 偷凭证 | learn from / steal credentials |
| **Grand / officialese** 宏大官腔 | 赋能 / 涌现 / 不仅仅 / 长出 | help / emerge as a new ability / not just / add |
| **Filler / connectors** 套话 | 值得注意的是 / 此外 / 至关重要 | delete, say it directly / new sentence / key |

Full table: [`data/ai-flavor-words.json`](data/ai-flavor-words.json).

---

## Two rules

**1. Don't replace mechanically.** The linter only flags positions and suggests. Whether and how to change it is up to context. Many words are precise in the right place:

- `门控` is a real term in machine learning (a gating network) and electronics — keep it there.
- `收敛` is a real term in math and iterative algorithms — don't blindly swap it.

The test is one sentence: **would a native speaker actually say this?** If yes, keep it. If no, use the plain column.

**2. Normal jargon is not AI-smell.** Words like `幂等` (idempotent), `编排` (orchestration), `缓存` (cache) that professionals genuinely use are **not** in the table. anti-ai-smell targets *coined / translationese / theatrical / officialese* — not "all technical terms".

---

## Use it as a Claude Skill

Drop the whole directory into `~/.claude/skills/anti-ai-smell/`. Claude will scan Chinese drafts for AI-smell before handing them back. See [`SKILL.md`](SKILL.md).

---

## Contributing

The word table is community-maintained. Found a new AI-smell word? Add it to [`data/ai-flavor-words.json`](data/ai-flavor-words.json) under the right category, or open a PR. The bar: **a native speaker wouldn't say it, but AI keeps writing it.**

```json
{"w": "门控", "en": "gate / gating", "human": ["把关", "卡一道", "网关"], "note": "legit in ML gating / circuits"}
```

---

## Credits

- The syntax-level de-AI thinking draws on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
- The word table grew out of real cases caught over and over in everyday Chinese writing, and keeps growing.

## License

[MIT](LICENSE)
