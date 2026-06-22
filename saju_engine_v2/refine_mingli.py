# -*- coding: utf-8 -*-
"""① 命例 인명·생년 고증·정제.
   mingli_dataset.json → 인명에서 관직 접미 분리, 간/번체 인명 번체 통일,
   동일 팔자+동일/포함 인명 병합, 근현대 인물 생몰 매칭 → 신뢰 검증셋 mingli_verify_clean.
"""
import json, re, os
from collections import defaultdict
from opencc import OpenCC

HERE = os.path.dirname(os.path.abspath(__file__))
S2T = OpenCC('s2t')   # 간체→번체

# 관직 접미(인명 끝에 붙어 추출된 것) — 길이 긴 것 우선
OFFICE_SUF = ["都憲","僉事","狀元","状元","丞相","尚書","侍郎","參政","御史","知府","知縣","路分","正郎",
              "朝議","提刑","運使","通判","員外","學士","太守","刺史","防禦","團練","觀察","節度","承宣",
              "龍圖","直閣","閣老","參軍","主簿","縣令","太尉","少卿","評事","寺丞","祭酒","博士","員","公"]
ANON = re.compile(r"^(남명|여명|某|어떤|男命|女命)")

# 근현대/역사 인물 생몰(양력 생년월일) — 명리서 빈출, 엔진 대조 검증용 (지식 기반)
BIRTH = {
 "孫中山":(1866,11,12),"蔣介石":(1887,10,31),"袁世凱":(1859,9,16),"譚嗣同":(1865,3,10),
 "梁啟超":(1873,2,23),"徐世昌":(1855,10,20),"汪精衛":(1883,5,4),"黎元洪":(1864,10,19),
 "朱元璋":(1328,10,21),"毛澤東":(1893,12,26),"周恩來":(1898,3,5),"蔡元培":(1868,1,11),
 "胡適":(1891,12,17),"段祺瑞":(1865,3,6),"馮玉祥":(1882,11,6),"閻錫山":(1883,10,8),
 "吳佩孚":(1874,4,22),"張作霖":(1875,3,19),"陳獨秀":(1879,10,9),"伍廷芳":(1842,7,9),
 "曾國藩":(1811,11,26),"李鴻章":(1823,2,15),"左宗棠":(1812,11,10),"張之洞":(1837,9,2),
 "邵逸夫":(1907,11,19),"杜月笙":(1888,8,22),"張學良":(1901,6,3),"溥儀":(1906,2,7),
 "光緒":(1871,8,14),"乾隆":(1711,9,25),"康有為":(1858,3,19),"宋教仁":(1882,4,5),
 # 생년월일 확실 인물 추가 (엔진 대조로 검증)
 "于右任":(1879,4,11),"陳立夫":(1900,8,21),"胡漢民":(1879,12,9),"戴季陶":(1891,1,6),
 "李宗仁":(1891,8,13),"蔣經國":(1910,4,27),"宋慶齡":(1893,1,27),"何應欽":(1890,4,2),
 "張勛":(1854,9,16),"馮國璋":(1859,1,7),"曹錕":(1862,12,12),"孫傳芳":(1885,4,17),
 "唐紹儀":(1862,1,2),"熊希齡":(1870,7,23),"宋子文":(1894,12,4),"孔祥熙":(1880,9,11),
}

def strip_office(name):
    """인명 끝 관직 접미 분리 → (정인명, [관직])."""
    offs = []
    changed = True
    while changed and len(name) > 2:
        changed = False
        for s in OFFICE_SUF:
            if name.endswith(s) and len(name) - len(s) >= 2:
                offs.append(s); name = name[:-len(s)]; changed = True; break
    return name, offs

def refine():
    d = json.load(open(os.path.join(HERE,"mingli_dataset.json"), encoding="utf-8"))
    # 1) 인명 정제: 익명 분리, 관직 접미 제거, 번체 통일
    named = []
    for r in d:
        p = r.get("person")
        if not p or ANON.match(p): continue
        if not re.search(r"[一-鿿]", p): continue
        # 한글(한자) 병기형이면 한자만 추출
        m = re.search(r"\(([一-鿿]{1,5})\)", p)
        hanja = m.group(1) if m else re.sub(r"[^一-鿿]", "", p)
        if len(hanja) < 2: continue
        clean, offs = strip_office(S2T.convert(hanja))
        r2 = dict(r)
        r2["person_clean"] = clean
        r2["offices"] = sorted(set([S2T.convert(o) for o in r["offices"]] + offs), key=len, reverse=True)
        named.append(r2)
    # 2) 병합: (번체인명, 팔자) 동일 → 1건. 결과정보 풍부한 것 대표.
    groups = defaultdict(list)
    for r in named:
        groups[(r["person_clean"], r["pillars"])].append(r)
    merged = []
    for (name, pil), rs in groups.items():
        best = max(rs, key=lambda r: len(r["result_tags"])*2 + len(r["offices"]) + r["shishen_marked"])
        best = dict(best)
        best["offices"] = sorted({o for r in rs for o in r["offices"]}, key=len, reverse=True)
        best["result_tags"] = sorted({t for r in rs for t in r["result_tags"]})
        best["sources"] = sorted({f"{r['book']}#{r['passage_id']}" for r in rs})
        merged.append(best)
    # 3) 동일 팔자 + 인명 포함관계(朱文 ⊂ 朱文公) → 긴 이름으로 흡수
    by_pil = defaultdict(list)
    for r in merged: by_pil[r["pillars"]].append(r)
    drop = set()
    for pil, rs in by_pil.items():
        for i, a in enumerate(rs):
            for b in rs:
                if a is b or id(a) in drop: continue
                if a["person_clean"] != b["person_clean"] and a["person_clean"] in b["person_clean"]:
                    b["offices"] = sorted(set(b["offices"]) | set(a["offices"]), key=len, reverse=True)
                    b["result_tags"] = sorted(set(b["result_tags"]) | set(a["result_tags"]))
                    b["sources"] = sorted(set(b["sources"]) | set(a["sources"]))
                    drop.add(id(a))
    clean = [r for r in merged if id(r) not in drop]
    # 4) 생몰 매칭 + 엔진 교차검증 (고전팔자 ↔ 생년 계산 년월일주 대조)
    from saju_engine import compute
    for r in clean:
        b = BIRTH.get(r["person_clean"])
        if b:
            r["birth"] = {"y":b[0],"m":b[1],"d":b[2]}
            eng = compute(b[0], b[1], b[2], gender="남")
            ey, em, ed = eng["pillars"]["year"], eng["pillars"]["month"], eng["pillars"]["day"]
            r["engine_pillars"] = f"{ey}·{em}·{ed}"
            r["birth_match"] = sum([ey==r["year"], em==r["month"], ed==r["day"]])
        else:
            r["birth"] = None; r["engine_pillars"] = None; r["birth_match"] = None
    # 같은 인물에 복수 팔자면 birth_match 높은 것만 verified, 나머지는 낮춤
    bybirth = defaultdict(list)
    for r in clean:
        if r["birth"]: bybirth[r["person_clean"]].append(r)
    for nm, rs in bybirth.items():
        mx = max(r["birth_match"] for r in rs)
        for r in rs:
            r["is_primary"] = (r["birth_match"] == mx and mx >= 2)
    # 신뢰등급
    for r in clean:
        if r["birth_match"] is None:   r["grade"] = "unverified"      # 생몰 미상
        elif r["birth_match"] == 3:    r["grade"] = "verified"        # 3주 완전일치
        elif r["birth_match"] == 2:    r["grade"] = "partial"         # 년월 일치(시/일주 이설)
        else:                          r["grade"] = "discrepancy"     # 생년 이설/추출 의심
    clean.sort(key=lambda r:(r["birth"] is None, r["person_clean"]))
    json.dump(clean, open(os.path.join(HERE,"mingli_verify_clean.json"),"w",encoding="utf-8"),
              ensure_ascii=False, indent=1)
    matched = [r for r in clean if r["birth"]]
    from collections import Counter
    print(f"정제 후 고유 命例: {len(clean)}  (병합 전 named {len(named)})")
    print(f"관직 분리 적용: {sum(1 for r in clean if r['offices'])}")
    print(f"생몰 매칭: {len(matched)}  신뢰등급: {dict(Counter(r['grade'] for r in matched))}")
    print(f"\n{'인물':8s}{'고전팔자(년월일)':18s}{'엔진계산':16s}일치  등급")
    for r in sorted(matched, key=lambda r: r['person_clean']):
        cl = f"{r['year']}·{r['month']}·{r['day']}"
        print(f"  {r['person_clean']:6s}{cl:18s}{r['engine_pillars'] or '':16s}{r['birth_match']}/3  {r['grade']}")
    return clean

if __name__ == "__main__":
    refine()
