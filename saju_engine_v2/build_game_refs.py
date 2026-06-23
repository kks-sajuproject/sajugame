# -*- coding: utf-8 -*-
"""build_game_refs.py — 게임용 고전 근거 추출.
   saju_full.db(한국어 번역 FTS)에서 신살·십신·육친 키워드별 고전 구절을 뽑아
   game_refs.json으로 저장한다. build_game.py가 이를 REFS로 임베드한다.
"""
import sqlite3, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "saju_full.db")
BK = {"glm":"격국론명","spt":"삼명통회","zpgj":"자평격국명법원약","zpzq":"자평진전",
      "zpzqpz":"자평진전평주","hym":"호일명","dts":"적천수","qtbj":"궁통보감","yhzp":"연해자평"}

KEYWORDS = [
 # 신살
 "천을귀인","양인","백호","괴강","도화","역마","화개","공망","문창","건록","천덕","월덕",
 "원진","현침","겁살","재살","천살","망신","장성","반안","육해","칠살","홍염","함지","귀문","천라지망",
 # 십신
 "정관","편관","정재","편재","정인","편인","식신","상관","비견","겁재",
 # 육친/주제
 "처","자식","부모","육친","질병","부귀","수명","성정",
]

def fts_phrase(s): return '"' + s.replace('"','') + '"'

def search(con, kw, limit=3):
    try:
        rows = con.execute("""SELECT t.book_id,t.t,t.b FROM translations_fts f
            JOIN translations t ON t.passage_id=f.rowid
            WHERE translations_fts MATCH ? ORDER BY rank LIMIT ?""",
            (fts_phrase(kw), limit*5)).fetchall()
    except sqlite3.OperationalError:
        rows = []
    seen, out = set(), []
    for bk, title, body in rows:
        if not body: continue
        t = re.sub(r"^〔重出〕","", title or "")
        if "重出" in (title or ""): continue
        key = (bk, t)
        if key in seen: continue
        seen.add(key)
        clean = re.sub(r"\s+", " ", body).strip()
        out.append({"book": BK.get(bk, bk), "title": t,
                    "snippet": clean[:130], "full": clean[:520]})
        if len(out) >= limit: break
    return out

def main():
    con = sqlite3.connect(f"file:{DB}?immutable=1", uri=True)
    refs = {}
    for kw in KEYWORDS:
        r = search(con, kw)
        if r: refs[kw] = r
    con.close()
    out = os.path.join(HERE, "game_refs.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(refs, f, ensure_ascii=False, separators=(",",":"))
    print("wrote", out, "| keywords with refs:", len(refs), "/", len(KEYWORDS))
    print("missing:", [k for k in KEYWORDS if k not in refs])

if __name__ == "__main__":
    main()
