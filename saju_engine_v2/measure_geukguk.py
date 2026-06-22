# -*- coding: utf-8 -*-
"""격국 자동판정 정확도 측정 — 命例 문맥에 명시된 격국명 ↔ 엔진 판정 대조."""
import json, re, os
from geukguk import analyze

HERE = os.path.dirname(os.path.abspath(__file__))
# 명시 격국명 → 표준 격으로 정규화
NORM = {"정관격":"정관격","칠살격":"칠살격","편관격":"칠살격","정인격":"정인격","인수격":"정인격",
        "편인격":"편인격","식신격":"식신격","상관격":"상관격","정재격":"정재격","편재격":"편재격",
        "건록격":"건록격","록겁격":"양인격","월겁격":"양인격","양인격":"양인격"}
# 대분류(정/편 미구분) 라벨
BROAD = {"재격":{"정재격","편재격"}, "관격":{"정관격","칠살격"}, "인수격":{"정인격","편인격"}}
LABELS = list(NORM) + list(BROAD) + ["식신생재","종격","종재격","종살격","종아격"]

def find_label(text):
    found = [g for g in LABELS if g in text]
    # 더 구체적인 라벨 우선 (정재격 > 재격)
    for g in sorted(found, key=len, reverse=True):
        return g
    return None

def main():
    d = json.load(open(os.path.join(HERE,"mingli_dataset.json"), encoding="utf-8"))
    cases = []
    for r in d:
        lab = find_label(r["title"]) or find_label(r["context"])
        if lab: cases.append((r, lab))
    # 십신 계열(관성·재성·인성·식상·비겁) 매핑
    GROUP = {"정관격":"관성","칠살격":"관성","정재격":"재성","편재격":"재성",
             "정인격":"인성","편인격":"인성","식신격":"식상","상관격":"식상",
             "건록격":"비겁","양인격":"비겁"}
    LAB_GROUP = {**{k:GROUP[NORM[k]] for k in NORM}, "재격":"재성","관격":"관성",
                 "인수격":"인성","식신생재":"식상"}
    # 정격만 채점 (종격은 별도 — 엔진이 정격 기반이라)
    scored = strict = grp = skip = 0
    misses = []
    for r, lab in cases:
        res = analyze(r["year"], r["month"], r["day"], r["hour"] or None)
        pred = res["classify"]["geuk"]
        scored += 1
        # 종격 라벨은 종격끼리 매칭
        if lab.startswith("종"):
            ok = (pred or "").startswith("종"); gok = ok
            jong_scored = True
        else:
            if lab in NORM:     ok = (pred == NORM[lab])
            elif lab in BROAD:  ok = (pred in BROAD[lab])
            else:               ok = False
            gok = (pred in GROUP and GROUP[pred] == LAB_GROUP.get(lab))
        if ok: strict += 1
        if gok: grp += 1
        if not gok and len(misses) < 10:
            misses.append((r["pillars"], lab, pred, r["title"][:26]))
    print(f"격국명 명시 命例: {len(cases)}  채점 {scored} (종격 포함)")
    print(f"① 엄밀 격 일치(정/편·종격 구분): {strict}/{scored} = {round(100*strict/scored,1)}%")
    print(f"② 십신 계열 일치(관/재/인/식상·종격): {grp}/{scored} = {round(100*grp/scored,1)}%")
    print("\n계열까지 불일치 샘플(월령 외 격취 등 고급규칙 필요):")
    for m in misses:
        print(f"  {m[0]}  고전:{m[1]:6s} 엔진:{str(m[2]):6s}  {m[3]}")

if __name__ == "__main__":
    main()
