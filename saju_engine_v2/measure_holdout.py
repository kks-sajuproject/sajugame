# -*- coding: utf-8 -*-
"""(b) 월령 외 격취 규칙 홀드아웃 검증.
   命例 격국라벨을 train/test 분할 → 규칙 변형별 계열 정확도 → 과적합 없이 향상되는 규칙 선택."""
import json, re, random
from saju_engine import HIDDEN, GAN_WX, ZHI_WX
from geukguk import sipsin, GEUK_MAP, WANG, GO

NORM={"정관격":"정관격","칠살격":"칠살격","편관격":"칠살격","정인격":"정인격","인수격":"정인격","편인격":"편인격",
 "식신격":"식신격","상관격":"상관격","정재격":"정재격","편재격":"편재격","건록격":"건록격","록겁격":"양인격","월겁격":"양인격","양인격":"양인격"}
BROAD={"재격":{"정재격","편재격"},"관격":{"정관격","칠살격"},"인수격":{"정인격","편인격"}}
GROUP={"정관격":"관성","칠살격":"관성","정재격":"재성","편재격":"재성","정인격":"인성","편인격":"인성","식신격":"식상","상관격":"식상","건록격":"비겁","양인격":"비겁"}
LABG={**{k:GROUP[NORM[k]] for k in NORM},"재격":"재성","관격":"관성","인수격":"인성","식신생재":"식상"}
SS_GEUK={"정관":"정관격","편관":"칠살격","정인":"정인격","편인":"편인격","식신":"식신격","상관":"상관격","정재":"정재격","편재":"편재격","비견":"건록격","겁재":"양인격"}
LABELS=list(NORM)+list(BROAD)+["식신생재"]
def find_label(t):
    f=[g for g in LABELS if g in t]; return sorted(f,key=len,reverse=True)[0] if f else None
def pof(r):
    p={"year":r["year"],"month":r["month"],"day":r["day"]}
    if r["hour"]:p["hour"]=r["hour"]
    return p
def grp_of_gan(dg,gan): return GROUP.get(SS_GEUK.get(sipsin(dg,gan)))

def rooted_gan(pillars, gan):
    """gan의 오행이 지지(지장간 전체)에 통근했는가."""
    w=GAN_WX[gan]
    for k in pillars:
        for h in HIDDEN[pillars[k][1]]:
            if GAN_WX[h]==w: return True
    return False

def predict(pillars, variant):
    """규칙별 격(계열) 예측."""
    dg=pillars["day"][0]; mz=pillars["month"][1]; hid=HIDDEN[mz]
    others=[pillars[k][0] for k in pillars if k!="day"]
    tou=[h for h in hid if h in others]
    # 월령 기본격
    if mz in WANG: base=hid[0]
    elif mz in GO: base=tou[0] if tou else hid[0]
    else: base=hid[0] if (hid[0] in others or not tou) else tou[0]
    base_grp=grp_of_gan(dg,base)
    if variant=="base":
        return base_grp
    if variant=="officer":   # 천간에 관살 투간시 관살격 우선
        for g in others:
            if sipsin(dg,g) in ("편관","정관"): return "관성"
        return base_grp
    if variant=="strong_tg": # 월령격이 비겁이거나, 천간에 통근한 관/재/인 투간시 그것 우선
        if base_grp=="비겁":
            pri={"편관":5,"정관":5,"정재":4,"편재":4,"정인":3,"편인":3,"식신":2,"상관":2}
            best=None
            for g in others:
                ss=sipsin(dg,g)
                if ss in pri and rooted_gan(pillars,g) and (best is None or pri[ss]>pri[best[1]]):
                    best=(GROUP[SS_GEUK[ss]],ss)
            if best: return best[0]
        return base_grp
    if variant=="officer_rooted":  # 천간에 통근한 관살 투간시 우선(통근 조건)
        for g in others:
            if sipsin(dg,g) in ("편관","정관") and rooted_gan(pillars,g): return "관성"
        return base_grp

def acc(cases, variant):
    ok=0
    for r,lab in cases:
        pred=predict(pof(r),variant)
        if pred==LABG.get(lab): ok+=1
    return ok/len(cases) if cases else 0

def main():
    d=json.load(open("mingli_dataset.json",encoding="utf-8"))
    cases=[]
    for r in d:
        lab=find_label(r["title"]) or find_label(r["context"])
        if lab and not lab.startswith("종"): cases.append((r,lab))
    random.seed(42); random.shuffle(cases)
    half=len(cases)//2; train=cases[:half]; test=cases[half:]
    print(f"케이스 {len(cases)} → train {len(train)} / test {len(test)}\n")
    print(f"{'규칙':16s}{'train':>8s}{'test':>8s}  과적합여부")
    for v in ["base","officer","officer_rooted","strong_tg"]:
        tr,te=acc(train,v),acc(test,v)
        flag="일반화 OK" if te>=acc(test,"base") else "test 하락"
        print(f"{v:16s}{tr*100:7.1f}%{te*100:7.1f}%  {flag}")
    # 전체 정확도(최종 후보)
    print("\n전체(176) 계열 정확도:")
    for v in ["base","officer","officer_rooted","strong_tg"]:
        print(f"  {v:16s}{acc(cases,v)*100:.1f}%")

if __name__=="__main__":
    main()
