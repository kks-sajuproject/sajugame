# -*- coding: utf-8 -*-
"""
사주명리 고전 DB 검색 CLI
사용법:
  python3 saju_search.py "正官"                 # 전체에서 검색
  python3 saju_search.py "调候" --book qtbj      # 특정 책만
  python3 saju_search.py "用神 多" --limit 20    # 공백=AND
간체/번체 아무거나 입력해도 됩니다(자동 정규화). 2자 검색 OK.
"""
import sqlite3, sys, argparse, os, re
from opencc import OpenCC
cc = OpenCC('s2t')

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saju_classics.db")

def make_match(query):
    # 공백으로 나눈 각 토큰을 "글자 사이 공백" 구문검색으로, 토큰끼리는 AND
    toks = [t for t in query.strip().split() if t]
    phrases = []
    for t in toks:
        chars = " ".join(cc.convert(t))   # 번체 정규화 + 글자분리
        phrases.append('"%s"' % chars)
    return " AND ".join(phrases)

def search(query, book=None, source=None, limit=15):
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    c = con.cursor()
    where = ["passages_fts MATCH ?"]
    params = [make_match(query)]
    if book:
        where.append("p.book_id = ?"); params.append(book)
    if source:
        where.append("p.source_id = ?"); params.append(source)
    params.append(limit)
    sql = f"""
    SELECT b.title_ko AS book, s.edition AS edition, p.juan AS juan,
           p.section_title AS sect, p.text AS text, bm25(passages_fts) AS score
    FROM passages_fts f
    JOIN passages p ON p.id=f.rowid
    JOIN books b ON b.book_id=p.book_id
    JOIN sources s ON s.source_id=p.source_id
    WHERE {' AND '.join(where)}
    ORDER BY score LIMIT ?"""
    rows = c.execute(sql, params).fetchall()
    con.close()
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--book"); ap.add_argument("--source")
    ap.add_argument("--limit", type=int, default=15)
    a = ap.parse_args()
    rows = search(a.query, a.book, a.source, a.limit)
    print(f"검색어: {a.query}  →  {len(rows)}건\n" + "="*70)
    for i, r in enumerate(rows, 1):
        loc = " · ".join(x for x in [r['book'], r['edition'], r['juan'], r['sect']] if x)
        txt = r['text'].replace("\n", " ")
        if len(txt) > 160: txt = txt[:160] + "…"
        print(f"[{i}] {loc}\n    {txt}\n")

if __name__ == "__main__":
    main()
