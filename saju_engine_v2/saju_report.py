# -*- coding: utf-8 -*-
"""④ 사주 종합 분석 리포트 (RAG). saju_engine + geukguk + saju_full.db 통합.
   생년월일시 → 팔자·강약·격국·용신·신살·대운 산출 → 특징 키워드로 고전 구절 검색 →
   근거와 함께 종합 리포트 출력. 2단계 4번째 토대 = 4단계(웹 분석)의 핵심 엔진.
"""
import sqlite3, os, re
from saju_engine import compute, fmt, GAN_WX, SHENG, KE
from geukguk import geukguk, yongsin, to_pillars

HERE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(HERE, "saju_full.db")
BK   = {"glm":"격국론명","spt":"삼명통회","zpgj":"자평격국명법원약","zpzq":"자평진전",
        "zpzqpz":"자평진전평주","hym":"호일명","dts":"적천수","qtbj":"궁통보감","yhzp":"연해자평"}

def _fts_phrase(s):
    # FTS5 한국어 구문검색: 토큰 분리 방지 위해 따옴표
    return '"' + s.replace('"', '') + '"'

def search_classics(keywords, limit=3):
    """translations_fts(한국어)에서 키워드별 관련 고전 구절 검색."""
    con = sqlite3.connect(f"file:{DB}?immutable=1", uri=True)
    seen, out = set(), []
    for kw in keywords:
        q = _fts_phrase(kw)
        try:
            rows = con.execute("""SELECT t.book_id, t.t, t.b
                FROM translations_fts f JOIN translations t ON t.passage_id=f.rowid
                WHERE translations_fts MATCH ? ORDER BY rank LIMIT ?""", (q, limit*4)).fetchall()
        except sqlite3.OperationalError:
            rows = []
        hits = []
        for bk, title, body in rows:
            if "重出" in title or "〔重出〕" in (body[:8] if body else ""): continue
            key = (bk, re.sub(r"^〔重出〕", "", title))
            if key in seen: continue
            seen.add(key)
            clean = re.sub(r"\s+", " ", body)
            hits.append({"book": BK.get(bk, bk), "title": re.sub(r"^〔重出〕","",title),
                         "snippet": clean[:120], "full": clean[:700]})
            if len(hits) >= limit: break
        if hits: out.append({"keyword": kw, "refs": hits})
    con.close()
    return out

def report(y, m, d, hour=None, gender="남", calendar="solar"):
    eng = compute(y, m, d, hour=hour, gender=gender, calendar=calendar)
    p = eng["pillars"]
    g = geukguk(p)
    yo = yongsin(p)
    # 검색 키워드: 격국 + 용신 계열 + 강약
    kws = []
    if g["geuk"]: kws.append(g["geuk"])
    if g["ss"]:   kws.append(g["ss"])
    for label, _ in yo["yongsin"][:1]:
        kws.append(label)
    kws.append("용신")
    # 주요 신살 키워드
    for sk in ("천을귀인", "양인", "도화", "역마"):
        if sk in eng["shensha"]: kws.append(sk)
    kws = list(dict.fromkeys(kws))   # 중복 제거, 순서 유지
    refs = search_classics(kws, limit=2)
    return {"engine": eng, "geukguk": g, "yongsin": yo, "keywords": kws, "classics": refs}

def render(r):
    eng = r["engine"]; g = r["geukguk"]; yo = r["yongsin"]
    L = []
    L.append("━━━━━━ 사주 종합 분석 ━━━━━━")
    L.append(fmt(eng))
    L.append("")
    L.append(f"◆ 격국: {g['geuk'] or '(월령기준 미정·외격 검토)'}  "
             f"[월지 {eng['pillars']['month'][1]}·{g['월지유형']}, 격취간 {g['geuk_gan']}({g['ss']})]")
    yong_str = ", ".join(f"{lab}{('('+wx+')') if wx else ''}" for lab, wx in yo["yongsin"])
    L.append(f"◆ 용신(부억 1차): {yong_str}  — {yo['note']}")
    L.append("")
    L.append(f"◆ 고전 근거 (키워드: {', '.join(r['keywords'])})")
    if not r["classics"]:
        L.append("   (관련 구절 미검색)")
    for blk in r["classics"]:
        L.append(f"  · [{blk['keyword']}]")
        for ref in blk["refs"]:
            L.append(f"      〔{ref['book']}〕 {ref['title']}")
            L.append(f"         {ref['snippet']}…")
    L.append("━━━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(L)

if __name__ == "__main__":
    # 증국번 1811-11-26 (verified), 寅시 가정
    print(render(report(1811, 11, 26, hour=4, gender="남")))
