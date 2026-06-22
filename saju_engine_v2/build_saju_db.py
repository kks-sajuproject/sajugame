# -*- coding: utf-8 -*-
"""
사주명리 고전 자료 DB 빌더
- 입력: saju_origindata/01_text_original/*.txt, 04_pdf_extracted_text/*.txt
- 출력: saju_classics.db (SQLite + FTS5 전문검색)
스키마: books(책) - sources(판본/파일) - passages(권/장/절 + 청크)
"""
import os, re, sqlite3
from opencc import OpenCC
cc_s2t = OpenCC('s2t')  # 간체 -> 번체 정규화

def to_trad(s):
    return cc_s2t.convert(s)

def spaced(s):
    """한자 1글자 단위 색인을 위해 공백 분리(번체 정규화)."""
    return " ".join(to_trad(s))

BASE = "/sessions/elegant-jolly-allen/mnt/cowork1/saju_origindata"
OUT_DIR = "/tmp/saju_build"
os.makedirs(OUT_DIR, exist_ok=True)
DB = os.path.join(OUT_DIR, "saju_classics.db")

# ---------------------------------------------------------------------------
# 1) 책(book) 메타데이터
# ---------------------------------------------------------------------------
BOOKS = [
    # book_id, 한자제목, 한글제목, 저자, 시대, 분류, 설명
    ("spt",  "三命通會", "삼명통회", "萬民英(만민영)", "明",      "종합/백과",   "명대 만민영 편. 명리 백과사전격 대저."),
    ("yhzp", "淵海子平", "연해자평", "徐大升 等",       "宋末~明初","종합",       "자평학 최고(最古) 종합서."),
    ("zpzq", "子平眞詮", "자평진전", "沈孝瞻(심효첨)",  "淸",      "격국론",     "청 건륭 진사 심효첨 원저. 격국론의 표준서."),
    ("zpzqpz","子平眞詮評註","자평진전평주","沈孝瞻 原著·徐樂吾 評註","淸~民國","격국론/주해","서락오 평주본."),
    ("dts",  "滴天髓",   "적천수",   "京圖(傳 劉基)",   "明",      "핵심이론",   "명리 핵심 이론서. 통신론·육친론."),
    ("qtbj", "窮通寶鑑", "궁통보감", "余春台 編(欄江網)","淸",     "조후용신",   "조후(調候) 용신론의 근간. 난강망."),
    ("glm",  "格局論命", "격국론명", "현대",            "현대",    "격국해설",   "현대 격국론 해설서."),
    ("zpgj", "子平格局命法元鑰(上)","자평격국명법원약(상)","慚愧學人","현대","격국해설","현대 격국 명법 해설(상권)."),
    ("hym",  "胡一鳴八字命理","호일명 팔자명리","胡一鳴(호일명)","현대","강의/실전","호일명 팔자명리 강의록."),
]

# ---------------------------------------------------------------------------
# 2) 판본(source) = 파일 매핑
# ---------------------------------------------------------------------------
SOURCES = [
    # source_id, book_id, 판본라벨, 출처유형, 상대경로, 비고
    ("spt_txt",  "spt",  "원문텍스트본",      "원문텍스트", "01_text_original/sanmyeongtonghoe_original.txt", "UTF-8 원문"),
    ("spt_pdf",  "spt",  "PDF추출본",         "PDF추출",   "04_pdf_extracted_text/sanmyeongtonghoe.txt",     "PDF에서 추출"),
    ("yhzp_txt", "yhzp", "원문텍스트본(발췌)", "원문텍스트", "01_text_original/yeonhaejapyeong_original.txt",  "발췌·정리본(약 5.6만자)"),
    ("yhzp_pdf", "yhzp", "PDF추출본",         "PDF추출",   "04_pdf_extracted_text/yeonhaejapyeong.txt",      "PDF에서 추출"),
    ("zpzq_pdf", "zpzq", "심효첨 원저본",      "PDF추출",   "04_pdf_extracted_text/japyeongjinjeon_original.txt", "원저 PDF 추출"),
    ("zpzqpz_pdf","zpzqpz","서락오 평주본",    "PDF추출",   "04_pdf_extracted_text/japyeongjinjeon_annotated.txt","평주 PDF 추출"),
    ("dts_pdf",  "dts",  "PDF추출본",         "PDF추출",   "04_pdf_extracted_text/jeokcheonsu.txt",          "PDF에서 추출"),
    ("qtbj_pdf", "qtbj", "PDF추출본",         "PDF추출",   "04_pdf_extracted_text/gungtongbogam.txt",        "PDF에서 추출"),
    ("glm_txt",  "glm",  "원문텍스트본",      "원문텍스트", "01_text_original/gyeokguknonmyeong.txt",         "UTF-8 원문"),
    ("glm_pdf",  "glm",  "PDF추출본",         "PDF추출",   "04_pdf_extracted_text/gyeokguknonmyeong.txt",    "PDF에서 추출"),
    ("zpgj_pdf", "zpgj", "PDF추출본(상)",     "PDF추출",   "04_pdf_extracted_text/gyeokgukmyeongbeob_wonyak.txt","PDF에서 추출"),
    ("hym_pdf",  "hym",  "PDF추출본",         "PDF추출",   "04_pdf_extracted_text/hoilmyeong_bazimyeongri.txt","PDF에서 추출"),
]

# ---------------------------------------------------------------------------
# 3) 파싱 유틸
# ---------------------------------------------------------------------------
CN_NUM = "一二三四五六七八九十百千零〇兩"

re_juan   = re.compile(r'^[ 　]*卷[' + CN_NUM + r']+')
re_num    = re.compile(r'^[ 　]*[' + CN_NUM + r']{1,4}[、.．]\s*\S')
re_circle = re.compile(r'^[ 　]*[○●◎]')
re_title  = re.compile(r'^[ 　]*[《【][^》】]{1,40}[》】][ 　]*$')
re_junk_url   = re.compile(r'https?://|www\.|ＱＱ|blog|\.com|\.net', re.I)
re_toc_dots   = re.compile(r'[.．·…]{3,}\s*\d*\s*$')   # 목차 점선
re_pageonly   = re.compile(r'^[ 　]*[-—–]?\s*\d{1,4}\s*[-—–]?\s*$')  # 페이지번호만

def clean_line(s):
    return s.replace('﻿', '').rstrip('\n').strip(' 　')

def is_junk(s):
    if not s.strip():
        return True
    if re_toc_dots.search(s):
        return True
    if re_pageonly.match(s):
        return True
    if re_junk_url.search(s):
        return True
    return False

def is_heading(s):
    return bool(re_juan.match(s) or re_circle.match(s) or re_title.match(s) or re_num.match(s))

def heading_label(s):
    return re.sub(r'^[ 　]*[○●◎]\s*', '', s).strip(' 　《》【】')

# 청크 분할: 문장부호(。！？；) 경계로 약 TARGET자 단위
TARGET = 480
def chunk_text(text, target=TARGET):
    text = text.strip()
    if not text:
        return []
    if len(text) <= target * 1.6:
        return [text]
    chunks, buf = [], ""
    parts = re.split(r'(?<=[。！？；!?;])', text)
    for p in parts:
        if not p:
            continue
        if len(buf) + len(p) > target and buf:
            chunks.append(buf)
            buf = p
        else:
            buf += p
    if buf:
        chunks.append(buf)
    return chunks

def parse_file(path):
    """반환: [(juan, section_no, section_title, chunk_no, text)]"""
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.readlines()
    rows = []
    cur_juan = None
    cur_sec_title = None
    sec_no = 0
    buf_lines = []

    def flush():
        nonlocal buf_lines
        if not buf_lines:
            return
        body = "".join(buf_lines)
        buf_lines = []
        for ci, ck in enumerate(chunk_text(body), 1):
            ck = ck.strip()
            if ck:
                rows.append([cur_juan, sec_no, cur_sec_title, ci, ck])

    for ln in raw:
        s = clean_line(ln)
        if is_junk(s):
            continue
        if re_juan.match(s):
            flush()
            cur_juan = s.strip(' 　')
            cur_sec_title = None
            continue
        if is_heading(s):
            flush()
            sec_no += 1
            cur_sec_title = heading_label(s)
            continue
        buf_lines.append(s)
    flush()
    return rows

# ---------------------------------------------------------------------------
# 4) DB 구축
# ---------------------------------------------------------------------------
def build():
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.executescript("""
    
    CREATE TABLE books(
        book_id TEXT PRIMARY KEY,
        title_zh TEXT, title_ko TEXT, author TEXT,
        dynasty TEXT, category TEXT, description TEXT
    );
    CREATE TABLE sources(
        source_id TEXT PRIMARY KEY,
        book_id TEXT REFERENCES books(book_id),
        edition TEXT, source_type TEXT,
        filename TEXT, orig_path TEXT, note TEXT,
        char_count INTEGER, passage_count INTEGER
    );
    CREATE TABLE passages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id TEXT REFERENCES sources(source_id),
        book_id TEXT REFERENCES books(book_id),
        seq INTEGER,
        juan TEXT,
        section_no INTEGER,
        section_title TEXT,
        chunk_no INTEGER,
        text TEXT,
        char_count INTEGER
    );
    CREATE INDEX idx_p_book ON passages(book_id);
    CREATE INDEX idx_p_source ON passages(source_id);
    CREATE INDEX idx_p_sec ON passages(source_id, section_no);
    """)

    cur.executemany("INSERT INTO books VALUES (?,?,?,?,?,?,?)", BOOKS)

    for sid, bid, edition, stype, rel, note in SOURCES:
        path = os.path.join(BASE, rel)
        rows = parse_file(path)
        total_chars = sum(len(r[4]) for r in rows)
        seq = 0
        for juan, sec_no, sec_title, ck_no, text in rows:
            seq += 1
            cur.execute(
                "INSERT INTO passages(source_id,book_id,seq,juan,section_no,section_title,chunk_no,text,char_count)"
                " VALUES (?,?,?,?,?,?,?,?,?)",
                (sid, bid, seq, juan, sec_no, sec_title, ck_no, text, len(text)))
        cur.execute(
            "INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?)",
            (sid, bid, edition, stype, os.path.basename(path), rel, note,
             total_chars, len(rows)))

    # 전문검색: 한자 1글자 단위 + 번체 정규화.
    #  -> 2자 검색어(正官, 调候 등)와 간체/번체 혼용 검색 모두 지원.
    #  fts.body = 공백분리된 번체 본문, fts.title = 공백분리된 번체 절제목
    cur.executescript("""
    CREATE VIRTUAL TABLE passages_fts USING fts5(
        body, title, tokenize='unicode61'
    );
    """)
    for pid, text, sect in cur.execute(
            "SELECT id, text, COALESCE(section_title,'') FROM passages").fetchall():
        cur.execute("INSERT INTO passages_fts(rowid, body, title) VALUES (?,?,?)",
                    (pid, spaced(text), spaced(sect)))

    con.commit()
    stats = cur.execute("""
        SELECT b.title_ko, s.edition, s.passage_count, s.char_count
        FROM sources s JOIN books b ON b.book_id=s.book_id
        ORDER BY b.title_ko
    """).fetchall()
    con.close()
    return stats

if __name__ == "__main__":
    stats = build()
    print("=== 판본별 적재 결과 ===")
    tp = tc = 0
    for ko, ed, pc, cc in stats:
        tp += pc; tc += cc
        print(f"  {ko:18s} | {ed:14s} | chunk {pc:5d} | {cc:8,d}ja")
    print(f"  TOTAL chunk {tp}  chars {tc:,}")
    print("DB:", DB)
