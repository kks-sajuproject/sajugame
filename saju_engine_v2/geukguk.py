# -*- coding: utf-8 -*-
"""③ 격국·용신 자동 판정. 팔자(년월일시 干支) 직접 입력 → 격국·강약·용신.
   命例는 생년월일 없이 팔자만 있으므로 compute()가 아닌 팔자 기반으로 판정한다.
   격국 = 월령 지장간 중 천간 투출자의 십신(투출 없으면 월령 본기).
"""
from saju_engine import (sipsin, strength, HIDDEN, GAN, ZHI, GAN_WX, ZHI_WX,
                         GAN_YIN, SHENG, KE, GAN_HE)

GEUK_MAP = {"정관":"정관격","편관":"칠살격","정인":"정인격","편인":"편인격","식신":"식신격",
            "상관":"상관격","정재":"정재격","편재":"편재격","비견":"건록격","겁재":"양인격"}

def to_pillars(year, month, day, hour=None):
    p = {"year":year, "month":month, "day":day}
    if hour: p["hour"] = hour
    return p

# 인원사령(人元司令) — 절입 후 (지장간, 일수)
SILYEONG = {
 "子":[("壬",10),("癸",20)], "丑":[("癸",9),("辛",3),("己",18)], "寅":[("戊",7),("丙",7),("甲",16)],
 "卯":[("甲",10),("乙",20)], "辰":[("乙",9),("癸",3),("戊",18)], "巳":[("戊",7),("庚",7),("丙",16)],
 "午":[("丙",10),("己",9),("丁",11)], "未":[("丁",9),("乙",3),("己",18)], "申":[("戊",7),("壬",7),("庚",16)],
 "酉":[("庚",10),("辛",20)], "戌":[("辛",9),("丁",3),("戊",18)], "亥":[("戊",7),("甲",5),("壬",18)],
}
def saryeong(zhi, days):
    """절입 후 경과일(days)로 당령 지장간 반환."""
    acc = 0
    for g, d in SILYEONG[zhi]:
        acc += d
        if days < acc: return g
    return SILYEONG[zhi][-1][0]

WANG     = set("子午卯酉")   # 사왕지: 본기 고정
GO       = set("辰戌丑未")   # 사고지: 투출자 우선(잡기격), 없으면 본기
SHENG_ZHI= set("寅申巳亥")   # 사생지: 본기 우선

def geukguk(pillars, days=None):
    """격국 판정. days(절입 후 경과일)가 있으면 사령신 우선(웹앱), 없으면 투출/본기(命例).
       왕지: 본기 고정 / 고지: (사령 또는)투출 우선 / 생지: 본기 우선."""
    day_gan = pillars["day"][0]
    month_zhi = pillars["month"][1]
    hidden = HIDDEN[month_zhi]                         # 본기·중기·여기
    other_gans = [pillars[k][0] for k in pillars if k != "day"]
    tou = [h for h in hidden if h in other_gans]       # 월령 투출
    if month_zhi in WANG:
        geuk_gan = hidden[0]                           # 왕지: 본기 고정
    elif days is not None:
        geuk_gan = saryeong(month_zhi, days)           # 사령신(생일 기반·정밀)
    elif month_zhi in GO:
        geuk_gan = tou[0] if tou else hidden[0]        # 고지: 투출 우선
    else:                                              # 생지: 본기 우선
        geuk_gan = hidden[0] if (hidden[0] in other_gans or not tou) else tou[0]
    ss = sipsin(day_gan, geuk_gan)
    # 투출한 타 지장간(본기 외)의 십신 — 겸격/투출 정보
    tou_extra = [(g, sipsin(day_gan, g)) for g in tou if g != geuk_gan]
    return {"geuk": GEUK_MAP.get(ss), "ss": ss, "geuk_gan": geuk_gan,
            "투출": bool(tou), "투간": tou, "투출겸": tou_extra, "월령장간": hidden, "월지유형":
            ("왕지" if month_zhi in WANG else "고지" if month_zhi in GO else "생지")}

def yongsin(pillars):
    """부억 용신(1차). 신강→억부(관·재·식상), 신약→부조(인·비). 극단시 종격 표시."""
    day_gan = pillars["day"][0]
    st = strength(day_gan, pillars, pillars["month"][1])
    dw = GAN_WX[day_gan]
    yin = [k for k,v in SHENG.items() if v==dw][0]     # 인성 오행
    food = SHENG[dw]                                    # 식상 오행
    wealth = KE[dw]                                     # 재성 오행
    officer = [k for k,v in KE.items() if v==dw][0]     # 관살 오행
    if st["verdict"] == "신강":
        yong = [("관살",officer), ("재성",wealth), ("식상",food)]
        note = "신강 → 극·설하는 관살/재성/식상이 용신"
    elif st["verdict"] == "신약":
        yong = [("인성",yin), ("비겁",dw)]
        note = "신약 → 생·부하는 인성/비겁이 용신"
        if st["score"] <= -6:
            note = "극신약 → 종격(從) 가능성 (재/관/식상 세력에 순종)"
    else:
        yong = [("통관·조후",None)]
        note = "중화 → 통관/조후 위주 정밀판단 필요"
    return {"verdict": st["verdict"], "score": st["score"],
            "yongsin": yong, "note": note}

def power_profile(pillars):
    """일간 기준 오행 세력(비겁·인성·식상·재성·관살) 집계 — 천간 + 지지 본기."""
    dg = pillars["day"][0]; dw = GAN_WX[dg]
    yin = [k for k,v in SHENG.items() if v==dw][0]; food = SHENG[dw]; wealth = KE[dw]
    officer = [k for k,v in KE.items() if v==dw][0]
    cnt = {"비겁":0,"인성":0,"식상":0,"재성":0,"관살":0}
    items = []
    for k in pillars:
        items.append(pillars[k][0]); items.append(HIDDEN[pillars[k][1]][0])
    items.remove(dg)   # 일간 자신 1개 제외
    for c in items:
        w = GAN_WX[c]
        if w==dw: cnt["비겁"]+=1
        elif w==yin: cnt["인성"]+=1
        elif w==food: cnt["식상"]+=1
        elif w==wealth: cnt["재성"]+=1
        elif w==officer: cnt["관살"]+=1
    return cnt

def rooted(pillars):
    """일간이 지지에 통근했는가 — 지지 지장간 전체에 비겁/인성 오행이 있으면 뿌리 있음."""
    dg = pillars["day"][0]; dw = GAN_WX[dg]
    yin = [k for k,v in SHENG.items() if v==dw][0]
    for k in pillars:
        for h in HIDDEN[pillars[k][1]]:
            if GAN_WX[h] in (dw, yin): return True
    return False

def check_hua(pillars):
    """화기격: 일간이 인접(월/시)간과 천간합 + 합화오행이 월령 본기."""
    dg = pillars["day"][0]
    neighbors = [pillars["month"][0]] + ([pillars["hour"][0]] if "hour" in pillars else [])
    for n in neighbors:
        key = "".join(sorted([dg,n], key=GAN.index))
        if key in GAN_HE and ZHI_WX[pillars["month"][1]] == GAN_HE[key]:
            return GAN_HE[key]
    return None

def _gan_rooted(pillars, gan):
    """gan의 오행이 지지(지장간 전체)에 통근했는가 — 부유(浮)한 천간 배제용."""
    w = GAN_WX[gan]
    return any(GAN_WX[h] == w for k in pillars for h in HIDDEN[pillars[k][1]])

def alt_geuk(pillars):
    """월령이 비겁(건록/양인)일 때 타주에서 격 취함. 통근한 관살>재>인>식상 우선.
       (홀드아웃 검증: 통근 조건이 train 53.5%/test 51.2%로 base 대비 향상·과적합 아님)."""
    dg = pillars["day"][0]
    others = [pillars[k][0] for k in pillars if k!="day"]
    pri = {"편관":5,"정관":5,"정재":4,"편재":4,"정인":3,"편인":3,"식신":2,"상관":2}
    best = None
    for g in others:
        ss = sipsin(dg, g)
        if ss in pri and _gan_rooted(pillars, g) and (best is None or pri[ss] > pri[best[1]]):
            best = (GEUK_MAP[ss], ss)
    return best

def geuk_candidates(pillars, days=None):
    """격이 갈릴 수 있는 사주의 복수 후보(사령/본기/투출 기준)를 반환."""
    dg = pillars["day"][0]; mz = pillars["month"][1]; hid = HIDDEN[mz]
    others = [pillars[k][0] for k in pillars if k != "day"]
    tou = [h for h in hid if h in others]
    cands = []
    def add(gan, basis):
        ss = sipsin(dg, gan); gk = GEUK_MAP.get(ss)
        if gk and not any(c["geuk"] == gk for c in cands):
            cands.append({"geuk": gk, "ss": ss, "gan": gan, "basis": basis})
    if mz in WANG:
        add(hid[0], "본기(왕지 고정)")
    else:
        if days is not None: add(saryeong(mz, days), "사령(司令)")
        add(hid[0], "월령 본기")
        for t in tou:
            if t != hid[0]: add(t, "투출(透出)")
    return cands

def classify(pillars, days=None):
    """격국 종합 판정: 화기격 → 종격 → 정격(월령/사령) 순. days=절입후 경과일(사령용)."""
    dg = pillars["day"][0]
    st = strength(dg, pillars, pillars["month"][1])
    prof = power_profile(pillars)
    support = prof["비겁"] + prof["인성"]
    drain = prof["식상"] + prof["재성"] + prof["관살"]
    # 1) 화기격
    hua = check_hua(pillars)
    if hua and support <= 2:
        return {"type":"화기격", "geuk":hua+"화격", "strength":st, "profile":prof,
                "note":f"일간이 인접 천간과 합하여 {hua}로 化"}
    # 2) 종격 (극신약 설극종속 / 극신강 인비종왕)
    if st["score"] <= -4.5 and support <= 1 and not rooted(pillars):
        dom = max([("종재격",prof["재성"]),("종살격",prof["관살"]),("종아격",prof["식상"])], key=lambda x:x[1])
        return {"type":"종격", "geuk":dom[0], "strength":st, "profile":prof,
                "note":"일간이 무근·고립 → 왕한 세력에 종속"}
    if st["score"] >= 6 and drain <= 1:
        return {"type":"종격", "geuk":"종왕격" if prof["비겁"]>=prof["인성"] else "종강격",
                "strength":st, "profile":prof, "note":"인비가 극왕 → 왕신을 따름"}
    # 3) 정격
    g = geukguk(pillars, days)
    note = None
    if g["geuk"] in ("건록격","양인격"):
        alt = alt_geuk(pillars)
        if alt:
            g = {**g, "geuk":alt[0], "ss":alt[1]}; note = "월령이 비겁 → 타주에서 격 취함"
    cands = geuk_candidates(pillars, days)
    return {"type":"정격", "geuk":g["geuk"], "ss":g["ss"], "geukguk":g,
            "strength":st, "profile":prof, "note":note, "candidates":cands}

JOHU = {  # 궁통보감 요지 — 월령(계절)별 조후용신
 "亥":("火","해월 수왕·한랭 → 火로 조후·해동"), "子":("火","자월 한기 극성 → 火 조후 긴요"),
 "丑":("火","축월 동토 → 火로 해동, 木 보조"), "寅":("火","인월 초봄 여한 → 火로 발영(發榮)"),
 "卯":("火","묘월 목왕 → 火로 수기를 설하여 빛냄"), "辰":("木","진월 토왕 → 木으로 소토(疏土)"),
 "巳":("水","사월 화기 시작 → 水로 조후"), "午":("水","오월 염열 → 水 조후 필수"),
 "未":("水","미월 조토·염열 → 水·木으로 윤택"), "申":("火","신월 금왕 → 火로 단련"),
 "酉":("火","유월 금왕 → 火로 단련"), "戌":("火","술월 조토 → 火·水로 한난 조절"),
}
def johu(pillars):
    return JOHU.get(pillars["month"][1], (None, "환절기 → 억부·격국 위주"))

def analyze(year, month, day, hour=None, days=None):
    p = to_pillars(year, month, day, hour)
    c = classify(p, days); y = yongsin(p); jh = johu(p)
    return {"pillars": p, "classify": c, "geukguk": c.get("geukguk", {"geuk":c["geuk"]}),
            "yongsin": y, "johu": {"wuxing": jh[0], "note": jh[1]}}

if __name__ == "__main__":
    # 증국번 辛未己亥丙辰庚寅
    r = analyze("辛未","己亥","丙辰","庚寅")
    print("증국번:", r["geukguk"]["geuk"], "/", r["yongsin"]["verdict"], r["yongsin"]["note"])
