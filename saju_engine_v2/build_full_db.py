# -*- coding: utf-8 -*-
"""원문 DB(saju_classics.db) + 번역(translations_*.json 9책)을 통합한 saju_full.db 생성.
   ⚠ 마운트 파일시스템은 sqlite 저널 쓰기가 막혀 있어 /tmp(정상 fs)에서 빌드 후 복사한다.
   결과: passages(원문) + translations(passage_id,book_id,t,b) + translations_fts(한국어 전문검색).
   재실행 시 마운트의 기존 saju_full.db는 삭제 불가하므로, 먼저 수동 정리하거나 새 이름을 쓸 것.
"""
import sqlite3, json, glob, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "saju_classics.db")
TMP  = "/tmp/saju_full_build.db"
OUT  = os.path.join(HERE, "saju_full.db")

def build():
    shutil.copy(SRC, TMP)
    con = sqlite3.connect(TMP)
    con.execute("""CREATE TABLE IF NOT EXISTS translations(
        passage_id INTEGER PRIMARY KEY, book_id TEXT, t TEXT, b TEXT,
        FOREIGN KEY(passage_id) REFERENCES passages(id))""")
    total = 0
    for f in sorted(glob.glob(os.path.join(HERE, "translations_*.json"))):
        if f.endswith(".bak"): continue
        book = os.path.basename(f)[len("translations_"):-len(".json")]
        data = json.load(open(f, encoding="utf-8"))
        rows = [(int(k), book, v.get("t",""), v.get("b","")) for k,v in data.items()]
        con.executemany("INSERT OR REPLACE INTO translations VALUES(?,?,?,?)", rows)
        total += len(rows)
    con.execute("CREATE INDEX IF NOT EXISTS idx_tr_book ON translations(book_id)")
    con.execute("DROP TABLE IF EXISTS translations_fts")
    con.execute("CREATE VIRTUAL TABLE translations_fts USING fts5("
                "t, b, content='translations', content_rowid='passage_id', tokenize='unicode61')")
    con.execute("INSERT INTO translations_fts(rowid,t,b) SELECT passage_id,t,b FROM translations")
    con.commit()
    tr = con.execute("SELECT count(*) FROM translations").fetchone()[0]
    ps = con.execute("SELECT count(*) FROM passages").fetchone()[0]
    miss = con.execute("SELECT count(*) FROM passages p LEFT JOIN translations t "
                       "ON t.passage_id=p.id WHERE t.passage_id IS NULL").fetchone()[0]
    con.close()
    shutil.copy(TMP, OUT)
    print(f"translations={tr} / passages={ps} / 미번역={miss}  →  {OUT} "
          f"({round(os.path.getsize(OUT)/1048576,2)}MB)")

if __name__ == "__main__":
    build()
