# -*- coding: utf-8 -*-
"""
saju_classics.db -> 자체완결형 HTML 뷰어(saju_viewer.html) 생성
- 데이터를 HTML에 내장하므로 서버/인터넷 없이 더블클릭만으로 동작
- 간체/번체 정규화 검색용 s2t 맵, 용어 해설(해석) 용어집 내장
"""
import os, json, sqlite3
from opencc import OpenCC
s2t = OpenCC('s2t'); t2s = OpenCC('t2s')

HERE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(HERE, "saju_classics.db")
TPL  = os.path.join(HERE, "viewer_template.html")
OUT  = os.path.join(HERE, "saju_viewer.html")

con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
c = con.cursor()

books = [dict(r) for r in c.execute(
    "SELECT book_id,title_zh,title_ko,author,dynasty,category,description FROM books")]
sources = [dict(r) for r in c.execute(
    "SELECT source_id,book_id,edition,source_type,note,char_count,passage_count FROM sources")]
passages = [dict(r) for r in c.execute(
    "SELECT id,source_id,book_id,seq,juan,section_no,section_title,text FROM passages ORDER BY source_id,seq")]
con.close()

# ---- 번역 병합 (translations*.json: {passage_id: {t:절제목, b:본문}}) ----
import re, glob
TRANS = {}
for tf in sorted(glob.glob(os.path.join(HERE, "translations*.json"))):
    TRANS.update(json.load(open(tf, encoding="utf-8")))
# PDF 추출 머리말 흔적 제거(원문 표시용)
def clean_src(t):
    t = re.sub(r'-?\s*\d+\s*/\s*27\s*-?\s*子平真诠-沈孝瞻原著', '', t)
    t = t.replace('子平真诠-沈孝瞻原著', '')
    t = re.sub(r'目录-1/27-', '', t)
    return t.strip()
translated_sources = set()
for p in passages:
    key = str(p["id"])
    if key in TRANS:
        p["tr"] = TRANS[key]["b"]
        p["title_tr"] = TRANS[key]["t"]
        p["text"] = clean_src(p["text"])
        translated_sources.add(p["source_id"])
tr_count = {}
for p in passages:
    if p.get("tr"):
        tr_count[p["source_id"]] = tr_count.get(p["source_id"], 0) + 1
for s in sources:
    s["has_tr"] = s["source_id"] in translated_sources
    s["tr_count"] = tr_count.get(s["source_id"], 0)

# 책 정렬: 분류/시대 순으로 보기 좋게(원하면 조정)
order = ["yhzp","zpzq","zpzqpz","dts","qtbj","spt","glm","zpgj","hym"]
books.sort(key=lambda b: order.index(b["book_id"]) if b["book_id"] in order else 99)

# ---- s2t 맵: 코퍼스+제목에 등장하는 글자 중 변환되는 것만 ----
chars = set()
for p in passages:
    chars.update(p["text"])
    if p["section_title"]: chars.update(p["section_title"])
s2t_map = {}
for ch in chars:
    t = s2t.convert(ch)
    if t != ch and len(t) == 1:
        s2t_map[ch] = t

# ---- 용어 해설(해석) 용어집: 번체 키로 작성 후 간체 키 자동 추가 ----
G = {
 "比肩":{"ko":"비견","desc":"일간과 오행·음양이 같은 십신. 형제·동료·경쟁자. 자기 세력을 뜻함."},
 "劫財":{"ko":"겁재","desc":"일간과 오행은 같고 음양이 다른 십신. 형제·동업·재물 다툼. 재(財)를 빼앗는 성분."},
 "食神":{"ko":"식신","desc":"일간이 생(生)하는 같은 음양의 십신. 의식주·재능·표현·장수(壽). 순한 설기."},
 "傷官":{"ko":"상관","desc":"일간이 생하는 다른 음양의 십신. 재능·표현·반항. 정관을 극해 '상관견관'을 꺼림."},
 "偏財":{"ko":"편재","desc":"일간이 극(剋)하는 같은 음양의 십신. 유동적 재물·사업·부친·이성."},
 "正財":{"ko":"정재","desc":"일간이 극하는 다른 음양의 십신. 고정적 재물·정처(正妻)·성실."},
 "偏官":{"ko":"편관(칠살)","desc":"일간을 극하는 같은 음양의 십신. 七殺. 권력·위엄·억제. 제복(制伏)되면 귀(貴)."},
 "七殺":{"ko":"칠살","desc":"편관의 별칭. 일간을 극하는 같은 음양 성분. 식상의 제복이나 인성의 화살(化殺)을 요함."},
 "正官":{"ko":"정관","desc":"일간을 극하는 다른 음양의 십신. 명예·지위·직장·법도. 자평 격국의 핵심."},
 "偏印":{"ko":"편인(효신)","desc":"일간을 생하는 같은 음양의 십신. 梟神. 편중된 학문·종교·계모. 식신을 극함."},
 "正印":{"ko":"정인","desc":"일간을 생하는 다른 음양의 십신. 印綬. 학문·문서·모친·보호."},
 "印綬":{"ko":"인수","desc":"정인의 별칭. 일간을 생하여 보호하는 성분. 학문·문서·귀인."},
 "用神":{"ko":"용신","desc":"사주의 중심을 잡는 가장 긴요한 오행/십신. 격국·억부·조후로 정함. 명리 해석의 핵심."},
 "喜神":{"ko":"희신","desc":"용신을 돕는 성분. 용신과 함께 길(吉)로 작용."},
 "忌神":{"ko":"기신","desc":"용신을 해치는 성분. 흉(凶)으로 작용."},
 "格局":{"ko":"격국","desc":"월령(月令)을 중심으로 사주의 틀을 분류한 것. 자평진전의 기본 체계."},
 "調候":{"ko":"조후","desc":"한난조습(寒暖燥濕)의 기후 균형을 맞추는 용신론. 궁통보감(난강망)의 근간."},
 "通關":{"ko":"통관","desc":"서로 상극하는 두 오행 사이를 이어 기를 흐르게 하는 중간 오행."},
 "月令":{"ko":"월령","desc":"태어난 달의 지지(月支). 격국과 왕쇠 판단의 기준이 되는 '제강(提綱)'."},
 "提綱":{"ko":"제강","desc":"월령(月支)의 별칭. 사주의 강령. 격국 판단의 출발점."},
 "日主":{"ko":"일주(일간)","desc":"태어난 날의 천간. 명(命)의 주체. 본인을 상징."},
 "身強":{"ko":"신강","desc":"일간의 세력이 강한 상태. 보통 극설(剋洩)하는 용신을 씀."},
 "身弱":{"ko":"신약","desc":"일간의 세력이 약한 상태. 보통 생부(生扶)하는 용신을 씀."},
 "從格":{"ko":"종격","desc":"일간이 극히 약해 강한 세력에 따라가는 특수격. 억부의 예외."},
 "五行":{"ko":"오행","desc":"木火土金水. 만물을 구성하는 다섯 기운. 상생·상극으로 작용."},
 "天干":{"ko":"천간","desc":"甲乙丙丁戊己庚辛壬癸 열 글자. 하늘의 기운."},
 "地支":{"ko":"지지","desc":"子丑寅卯辰巳午未申酉戌亥 열둘. 땅의 기운, 지장간을 품음."},
 "藏干":{"ko":"장간(지장간)","desc":"지지 속에 감추어진 천간. 격국·용신 판단의 근거."},
}
glossary = {}
for k,v in G.items():
    glossary[k] = v
    ks = t2s.convert(k)            # 간체 키도 추가(본문 간체 표기 매칭용)
    if ks != k: glossary[ks] = v

# ---- 주입 ----
def inject(tpl, key, obj):
    js = json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")
    return tpl.replace(key, js)

with open(TPL, encoding="utf-8") as f:
    html = f.read()
html = inject(html, "__DATA__", {"books":books,"sources":sources,"passages":passages})
html = inject(html, "__S2T__", s2t_map)
html = inject(html, "__GLOSSARY__", glossary)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("books:%d sources:%d passages:%d s2t:%d glossary:%d"
      % (len(books),len(sources),len(passages),len(s2t_map),len(glossary)))
print("size: %.2f MB -> %s" % (os.path.getsize(OUT)/1e6, OUT))
