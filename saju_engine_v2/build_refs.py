# -*- coding: utf-8 -*-
"""[2C] 단일 HTML용 고전 근거 테이블 생성. saju_full.db(한국어 FTS)에서
   격국·십신·신살·강약·용신·조후 키워드별 대표 구절을 추출해 refs_table.json 으로.
   웹앱은 분석 결과의 격국/신살에 맞춰 이 구절을 근거로 표시(서버 없이)."""
import json, os
from saju_report import search_classics

HERE = os.path.dirname(os.path.abspath(__file__))
KEYWORDS = [
 # 격국
 "정관격","칠살격","정인격","편인격","식신격","상관격","정재격","편재격","건록격","양인격",
 "종재격","종살격","종아격","화격",
 # 강약·용신·조후
 "신강","신약","중화","용신","조후","억부",
 # 십신
 "정관","칠살","정인","편인","식신","상관","정재","편재","비견","겁재",
 # 신살
 "천을귀인","역마","도화","화개","양인","문창","건록","괴강","백호","공망","천덕","월덕",
 # 영역(질병·육친·재물·성정)
 "질병","육친","처","자식","부귀","빈천","수명","성정","재성","관성","인성","식상",
]

def main():
    table = {}
    for kw in KEYWORDS:
        blk = search_classics([kw], limit=2)
        refs = []
        if blk:
            for ref in blk[0]["refs"]:
                refs.append({"book": ref["book"], "title": ref["title"],
                             "snippet": ref["snippet"][:150], "full": ref.get("full","")})
        if refs: table[kw] = refs
    json.dump(table, open(os.path.join(HERE,"refs_table.json"),"w",encoding="utf-8"),
              ensure_ascii=False, separators=(",",":"))
    n = sum(len(v) for v in table.values())
    print(f"refs_table.json: 키워드 {len(table)}개, 구절 {n}개, "
          f"{round(os.path.getsize(os.path.join(HERE,'refs_table.json'))/1024,1)}KB")
    for k in ["칠살격","신약","천을귀인","조후"]:
        if k in table: print(f"  [{k}] {table[k][0]['book']} · {table[k][0]['snippet'][:40]}…")

if __name__ == "__main__":
    main()
