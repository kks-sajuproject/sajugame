# -*- coding: utf-8 -*-
"""고전 9책 번역(translations_*.json)에서 命例(사주팔자+인물+격국+결과)를 추출해
   테스트셋 mingli_dataset.json 으로 정규화한다. 2단계 '테스트 사주 대조'의 기초 데이터.

   命例 표기 두 형식 통합:
     A) 슬래시형  "壬 丁 丙 壬 / 寅 未 寅 辰"  (干4 / 支4, 년월일시 순)   ← zpgj·zpzq
     B) 60갑자쌍형 "壬寅·丁未·丙寅·壬辰"        (·또는 공백 구분)          ← zpzqpz·spt·glm
   결과 레코드: book, passage_id, title, pillars(8자), 사주(년월일시), person, shishen, result_tags, context
"""
import json, glob, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
GAN = "甲乙丙丁戊己庚辛壬癸"; ZHI = "子丑寅卯辰巳午未申酉戌亥"

PAT_A = re.compile(rf"([{GAN}])\s*·?\s*([{GAN}])\s*·?\s*([{GAN}])\s*·?\s*([{GAN}])"
                   rf"\s*/\s*([{ZHI}])\s*·?\s*([{ZHI}])\s*·?\s*([{ZHI}])\s*·?\s*([{ZHI}])")
PAT_B = re.compile(rf"([{GAN}][{ZHI}])[\s·]+([{GAN}][{ZHI}])[\s·]+([{GAN}][{ZHI}])[\s·]+([{GAN}][{ZHI}])")

# 인물/관직/결과 키워드 (한국어 번역문 구조 대응)
# 인물명 형식: "명례 — 여길보 학사:", "철보(鐵保) 명조", "오정방(伍廷芳)의 명조", "朱文公:", "高太尉 명"
P_LABEL = re.compile(r"명례\s*[—\-–]\s*([^:：·\]〔「]{1,14}?)\s*[:：]")
P_HANGUL_HANJA = re.compile(r"([가-힣]{2,6}\([一-鿿]{1,4}\))\s*(?:의\s*)?(?:명조|명례|사주|명|造)")
P_HANJA = re.compile(r"([一-鿿]{2,5})\s*(?:命조|명조|命|公|相|尚書|侍郎)")
ANON   = re.compile(r"(某男命|某女命|남명|여명|어떤 남자|어떤 여자|某男|某女|男命|女命)")
OFFICE = ["狀元","状元","장원","丞相","승상","宰相","재상","尚書","상서","侍郎","시랑","參政","참정","御史","어사",
          "知府","知縣","太尉","태위","평장","太傅","태부","國公","會元","榜眼","榜안","提台","運使","員外","원외",
          "太僕","節度使","절도사","統制","巡撫","순무","總兵","閣老","각로","主席","주석","總理","총리","督軍",
          "總統","총통","部長","부장","軍長","군장","公","侯","伯","學士","학사","太守","태수","刺史","자사"]
RESULT = {
 "大貴":["大貴","대귀","극귀","크게 귀","지극히 귀","일품","一品","극품","최고","재상","승상","장원","상서"],
 "富":["大富","대부","거부","큰 부자","치부","발재","發財","부유","부자","巨富","資財"],
 "貴":["貴格","貴顯","귀현","현귀","귀하","발귀","높은 벼슬","청귀","顯達","현달","출세","과거 급제","登科","등과"],
 "貧":["貧","빈천","가난","빈한","걸식","乞丐","거지","빈궁","곤궁","落魄","낙백"],
 "賤":["賤","천하","下賤","미천","노복","下役"],
 "夭":["夭","요절","일찍 죽","단명","수가 짧","요사","早死","早夭","橫死","횡사"],
 "壽":["壽","장수","오래 살","향년","수를 누","高壽","고수","享壽"],
 "克妻":["克妻","극처","상처","아내를 잃","喪妻"], "克夫":["克夫","극부","상부","남편을 잃","喪夫"],
 "克子":["克子","극자","損子","후사가 없","무자","無子","자식을 잃","자식이 없"],
 "離婚":["離婚","이혼","재가","개가"],
 "殘疾":["殘疾","잔질","맹인","실명","失明","폐질","불구","聾","귀머거리","벙어리","질병","병약"],
}
SHISHEN = re.compile(r"(정관|편관|칠살|정인|편인|식신|상관|정재|편재|비견|겁재|양인|건록|록겁|"
                     r"正官|偏官|七殺|正印|偏印|食神|傷官|正財|偏財|比肩|劫財|羊刃)")

def find_person(b, mstart):
    pre = b[max(0, mstart-45):mstart]
    m = P_LABEL.search(pre)
    if m: return m.group(1).strip()
    m = None
    for mm in P_HANGUL_HANJA.finditer(pre): m = mm
    if m: return m.group(1).strip()
    m = None
    for mm in P_HANJA.finditer(pre): m = mm
    if m and not any(c in GAN+ZHI for c in m.group(1)): return m.group(1).strip()
    am = ANON.search(pre)
    return am.group(1) if am else None

def norm_pillars(groups, kind):
    if kind == "A":   # 干4 支4 → 년월일시
        g = groups
        return [g[0]+g[4], g[1]+g[5], g[2]+g[6], g[3]+g[7]]
    else:             # 60갑자쌍 4
        return list(groups)

def extract():
    out = []
    seen = set()
    for f in sorted(glob.glob(os.path.join(HERE, "translations_*.json"))):
        if f.endswith(".bak"): continue
        book = os.path.basename(f)[len("translations_"):-len(".json")]
        data = json.load(open(f, encoding="utf-8"))
        for k, v in data.items():
            b, title = v["b"], v.get("t","")
            for kind, pat in (("A",PAT_A),("B",PAT_B)):
                for m in pat.finditer(b):
                    # 대운/세운 나열의 干支는 命例 사주가 아니므로 제외
                    pre12 = b[max(0, m.start()-12):m.start()]
                    if re.search(r"(대운|大運|歲運|행운|行運|운\s*[:：]|運\s*[:：])", pre12):
                        continue
                    pil = norm_pillars(m.groups(), kind)
                    pillars = "".join(pil)
                    key = (book, k, pillars)
                    if key in seen: continue
                    seen.add(key)
                    ctx = b[max(0,m.start()-35):m.end()+70]
                    # 인물명
                    person = find_person(b, m.start())
                    # 십신 표기 동반
                    shishen = bool(SHISHEN.search(ctx))
                    # 관직 (중복 제거, 한글/한자 동의어 정리)
                    offices = sorted({o for o in OFFICE if o in (person or "")+ctx}, key=len, reverse=True)
                    # 결과 태그
                    tags = [r for r,kws in RESULT.items() if any(w in ctx for w in kws)]
                    out.append({
                        "book": book, "passage_id": int(k), "title": title,
                        "pillars": pillars,
                        "year": pil[0], "month": pil[1], "day": pil[2], "hour": pil[3],
                        "person": person, "offices": offices,
                        "shishen_marked": shishen, "result_tags": tags,
                        "context": ctx.replace("\n"," ").strip(),
                    })
    out.sort(key=lambda r:(r["book"], r["passage_id"]))
    json.dump(out, open(os.path.join(HERE,"mingli_dataset.json"),"w",encoding="utf-8"),
              ensure_ascii=False, indent=1)
    # 통계
    from collections import Counter
    print(f"총 命例: {len(out)}")
    print("책별:", dict(Counter(r['book'] for r in out)))
    print("인물명 동반:", sum(1 for r in out if r['person']))
    print("관직 명시:", sum(1 for r in out if r['offices']))
    print("십신표기:", sum(1 for r in out if r['shishen_marked']))
    print("결과태그 동반:", sum(1 for r in out if r['result_tags']))
    return out

if __name__ == "__main__":
    extract()
