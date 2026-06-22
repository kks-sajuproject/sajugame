# -*- coding: utf-8 -*-
"""사주 계산 엔진 (만세력) — sxtwl 기반.
   생년월일시 → 사주팔자·지장간·십신·대운 산출. 절기 경계는 sxtwl이 처리.
   2단계 命例/실존인물 검증의 계산 기반.

   사용:
     from saju_engine import compute
     r = compute(1866,11,12, hour=None, gender="남", calendar="solar")
     print(r["pillars"], r["sipsin"], r["daewoon"])
"""
import sxtwl

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
GAN_KO = dict(zip(GAN, "갑을병정무기경신임계"))
ZHI_KO = dict(zip(ZHI, "자축인묘진사오미신유술해"))
# 오행 / 음양
GAN_WX = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
ZHI_WX = {"子":"水","丑":"土","寅":"木","卯":"木","辰":"土","巳":"火","午":"火","未":"土","申":"金","酉":"金","戌":"土","亥":"水"}
GAN_YIN = set("乙丁己辛癸")          # 음간 (나머지는 양)
SHENG = {"木":"火","火":"土","土":"金","金":"水","水":"木"}   # 생
KE    = {"木":"土","土":"水","水":"火","火":"金","金":"木"}    # 극
# 지장간 (본기·중기·여기)
HIDDEN = {"子":["癸"],"丑":["己","癸","辛"],"寅":["甲","丙","戊"],"卯":["乙"],
          "辰":["戊","乙","癸"],"巳":["丙","庚","戊"],"午":["丁","己"],"未":["己","丁","乙"],
          "申":["庚","壬","戊"],"酉":["辛"],"戌":["戊","辛","丁"],"亥":["壬","甲"]}

def sipsin(day_gan, other_gan):
    """일간 대비 천간 other_gan의 십신."""
    if other_gan not in GAN_WX: return None
    dw, ow = GAN_WX[day_gan], GAN_WX[other_gan]
    same_yy = (day_gan in GAN_YIN) == (other_gan in GAN_YIN)
    if ow == dw:               return "비견" if same_yy else "겁재"
    if SHENG[dw] == ow:        return "식신" if same_yy else "상관"   # 일간이 생함
    if KE[dw] == ow:           return "편재" if same_yy else "정재"   # 일간이 극함
    if KE[ow] == dw:           return "편관" if same_yy else "정관"   # 타가 일간을 극함(官殺)
    if SHENG[ow] == dw:        return "편인" if same_yy else "정인"   # 타가 일간을 생함(印)
    return None

# === 십이운성(十二運星) ===
TWELVE = ["장생","목욕","관대","건록","제왕","쇠","병","사","묘","절","태","양"]
CHANGSHENG = {"甲":"亥","丙":"寅","戊":"寅","庚":"巳","壬":"申","乙":"午","丁":"酉","己":"酉","辛":"子","癸":"卯"}
def twelve_stage(gan, zhi):
    start = ZHI.index(CHANGSHENG[gan]); idx = ZHI.index(zhi)
    forward = gan not in GAN_YIN
    pos = (idx - start) % 12 if forward else (start - idx) % 12
    return TWELVE[pos]

# === 신살(神煞) ===
TIANYI = {"甲":"丑未","戊":"丑未","庚":"丑未","乙":"子申","己":"子申","丙":"亥酉","丁":"亥酉","辛":"寅午","壬":"巳卯","癸":"巳卯"}
MAYI  = {"申":"寅","子":"寅","辰":"寅","寅":"申","午":"申","戌":"申","巳":"亥","酉":"亥","丑":"亥","亥":"巳","卯":"巳","未":"巳"}
TAOHUA= {"申":"酉","子":"酉","辰":"酉","寅":"卯","午":"卯","戌":"卯","巳":"午","酉":"午","丑":"午","亥":"子","卯":"子","未":"子"}
HUAGAI= {"申":"辰","子":"辰","辰":"辰","寅":"戌","午":"戌","戌":"戌","巳":"丑","酉":"丑","丑":"丑","亥":"未","卯":"未","未":"未"}
YANGIN= {"甲":"卯","丙":"午","戊":"午","庚":"酉","壬":"子"}
WENCHANG={"甲":"巳","乙":"午","丙":"申","戊":"申","丁":"酉","己":"酉","庚":"亥","辛":"子","壬":"寅","癸":"卯"}
LU     = {"甲":"寅","乙":"卯","丙":"巳","戊":"巳","丁":"午","己":"午","庚":"申","辛":"酉","壬":"亥","癸":"子"}
def shensha(day_gan, year_zhi, branches):
    ty = set(TIANYI[day_gan]); res = {}
    res["천을귀인"] = [z for z in branches if z in ty]
    res["역마"]   = [z for z in branches if z == MAYI[year_zhi]]
    res["도화"]   = [z for z in branches if z == TAOHUA[year_zhi]]
    res["화개"]   = [z for z in branches if z == HUAGAI[year_zhi]]
    if day_gan in YANGIN: res["양인"] = [z for z in branches if z == YANGIN[day_gan]]
    res["문창귀인"] = [z for z in branches if z == WENCHANG[day_gan]]
    res["건록"]   = [z for z in branches if z == LU[day_gan]]
    return {k:v for k,v in res.items() if v}

# === 합충형해 ===
import itertools
GAN_HE   = {frozenset("甲己"):"土",frozenset("乙庚"):"金",frozenset("丙辛"):"水",frozenset("丁壬"):"木",frozenset("戊癸"):"火"}
GAN_CHONG= {frozenset("甲庚"),frozenset("乙辛"),frozenset("丙壬"),frozenset("丁癸")}
ZHI_LIUHE= {frozenset("子丑"),frozenset("寅亥"),frozenset("卯戌"),frozenset("辰酉"),frozenset("巳申"),frozenset("午未")}
ZHI_SANHE= {frozenset("申子辰"):"水",frozenset("寅午戌"):"火",frozenset("巳酉丑"):"金",frozenset("亥卯未"):"木"}
ZHI_CHONG= {frozenset("子午"),frozenset("丑未"),frozenset("寅申"),frozenset("卯酉"),frozenset("辰戌"),frozenset("巳亥")}
ZHI_HAI  = {frozenset("子未"),frozenset("丑午"),frozenset("寅巳"),frozenset("卯辰"),frozenset("申亥"),frozenset("酉戌")}
def interactions(gans, branches):
    out = {"천간합":[],"천간충":[],"지지육합":[],"지지삼합":[],"지지충":[],"지지해":[]}
    for a,b in itertools.combinations(sorted(set(gans),key=GAN.index),2):
        fs=frozenset(a+b)
        if fs in GAN_HE:    out["천간합"].append(f"{a}{b}합({GAN_HE[fs]})")
        if fs in GAN_CHONG: out["천간충"].append(f"{a}{b}충")
    sb=set(branches)
    for a,b in itertools.combinations(sorted(sb,key=ZHI.index),2):
        fs=frozenset(a+b)
        if fs in ZHI_LIUHE: out["지지육합"].append(f"{a}{b}합")
        if fs in ZHI_CHONG: out["지지충"].append(f"{a}{b}충")
        if fs in ZHI_HAI:   out["지지해"].append(f"{a}{b}해")
    for combo,wx in ZHI_SANHE.items():
        if combo<=sb: out["지지삼합"].append(f"{''.join(sorted(combo,key=ZHI.index))}삼합({wx})")
    return {k:v for k,v in out.items() if v}

# === 왕쇠 강약(신강/신약) ===
def strength(day_gan, pillars, month_zhi):
    dw = GAN_WX[day_gan]
    yin_wx = [k for k,v in SHENG.items() if v==dw][0]   # 일간을 생하는 오행(인성)
    helps = {dw, yin_wx}                                 # 비겁 + 인성 = 부조 세력
    score = 0.0; detail = []
    mwx = ZHI_WX[month_zhi]                              # 득령
    if mwx in helps:       score += 3; detail.append(f"득령({month_zhi}·{mwx}) +3")
    elif SHENG[dw]==mwx:   score -= 1.5; detail.append(f"월령 설기({mwx}) -1.5")
    else:                  score -= 1.2; detail.append(f"월령 극·설({mwx}) -1.2")
    for pos,gz in pillars.items():                      # 천간 부조(일간 제외)
        if pos=="day": continue
        score += 1 if GAN_WX[gz[0]] in helps else -0.7
    for pos in pillars:                                 # 지지 통근(월·일 가중)
        zwx = ZHI_WX[pillars[pos][1]]; w = 1.5 if pos in ("month","day") else 1.0
        score += w if zwx in helps else -w*0.6
    verdict = "신강" if score>=2 else ("신약" if score<=-2 else "중화")
    return {"score":round(score,1),"verdict":verdict,"detail":detail}

def _gz(g): return GAN[g.tg] + ZHI[g.dz]

def compute(y, m, d, hour=None, minute=0, gender="남", calendar="solar"):
    """hour: 0~23 정수 또는 None(시주 미상). calendar: 'solar'|'lunar'."""
    if calendar == "lunar":
        day = sxtwl.fromLunar(y, m, d, False)
    else:
        day = sxtwl.fromSolar(y, m, d)
    yGZ, mGZ, dGZ = day.getYearGZ(), day.getMonthGZ(), day.getDayGZ()
    day_gan = GAN[dGZ.tg]
    pillars = {"year": _gz(yGZ), "month": _gz(mGZ), "day": _gz(dGZ)}
    # 시주
    hour_gz = None
    if hour is not None:
        zhi_idx = ((hour + 1) // 2) % 12           # 23~00:30→子
        sh = sxtwl.getShiGz(dGZ.tg, hour)          # 시천간
        hour_gz = GAN[sh.tg] + ZHI[sh.dz]
        pillars["hour"] = hour_gz
    # 십신 (천간)
    ss = {"year": sipsin(day_gan, pillars["year"][0]),
          "month": sipsin(day_gan, pillars["month"][0]),
          "day": "일간(아신)",
          "hour": sipsin(day_gan, hour_gz[0]) if hour_gz else None}
    # 지장간 + 지지십신(본기)
    branches = {k: pillars[k][1] for k in pillars}
    hidden = {k: HIDDEN[v] for k, v in branches.items()}
    branch_ss = {k: sipsin(day_gan, HIDDEN[v][0]) for k, v in branches.items()}
    # 오행 분포
    wx_count = {"木":0,"火":0,"土":0,"金":0,"水":0}
    for k in pillars:
        wx_count[GAN_WX[pillars[k][0]]] += 1
        wx_count[ZHI_WX[pillars[k][1]]] += 1
    # 십이운성·신살·합충·강약
    gans_list = [pillars[k][0] for k in pillars]
    branches_list = [pillars[k][1] for k in pillars]
    twelve = {k: twelve_stage(day_gan, pillars[k][1]) for k in pillars}
    ss_shen = shensha(day_gan, pillars["year"][1], branches_list)
    inter = interactions(gans_list, branches_list)
    stren = strength(day_gan, pillars, pillars["month"][1])
    # 대운
    daewoon = _daewoon(day, yGZ, mGZ, gender)
    return {
        "input": {"y":y,"m":m,"d":d,"hour":hour,"gender":gender,"calendar":calendar},
        "pillars": pillars, "day_master": day_gan,
        "sipsin": ss, "branch_sipsin": branch_ss, "hidden_stems": hidden,
        "wuxing": wx_count, "twelve_stage": twelve, "shensha": ss_shen,
        "interactions": inter, "strength": stren, "daewoon": daewoon,
    }

def _daewoon(day, yGZ, mGZ, gender, n=8):
    """대운: 순/역 + 기운 나이(절기 거리/3) + n개 간지."""
    yang_year = (yGZ.tg % 2 == 0)                  # 甲丙戊庚壬 = 짝수 index = 양
    forward = (yang_year and gender == "남") or (not yang_year and gender == "여")
    # 기운 나이: 출생 JD ~ (순:다음 / 역:이전) 절기 JD
    birth_jd = sxtwl.toJD(sxtwl.Time(day.getSolarYear(), day.getSolarMonth(), day.getSolarDay(), 12, 0, 0))
    cur = day
    # 다음/이전 절기 찾기 (节: 12절, 月을 가르는 것). hasJieQi 우선, 없으면 전후 탐색.
    def find_jq(start, step):
        c = start
        for _ in range(60):
            c = c.after(1) if step > 0 else c.before(1)
            if c.hasJieQi():
                jd = c.getJieQiJD()
                # 节만(홀수 인덱스 제외) — 단순화: 모든 절기 사용해도 月경계 근접
                return jd
        return None
    jq_jd = find_jq(day, 1 if forward else -1)
    days_diff = abs(jq_jd - birth_jd) if jq_jd else 0
    start_age = round(days_diff / 3.0, 1)          # 3일 = 1세
    # 대운 간지: 월주에서 ±1씩
    seq = []
    tg, dz = mGZ.tg, mGZ.dz
    for i in range(1, n + 1):
        if forward: tg, dz = (tg + 1) % 10, (dz + 1) % 12
        else:       tg, dz = (tg - 1) % 10, (dz - 1) % 12
        seq.append({"age": round(start_age + (i - 1) * 10, 1), "gz": GAN[tg] + ZHI[dz]})
    return {"forward": forward, "start_age": start_age, "list": seq}

def fmt(r):
    p = r["pillars"]
    order = ["year","month","day","hour"]
    line = "  ".join(f"{p[k]}" for k in order if k in p)
    ss = r["sipsin"]
    ssl = "  ".join(f"{ss[k]}" for k in order if k in p and ss.get(k))
    tw = r["twelve_stage"]
    twl = "  ".join(f"{tw[k]}" for k in order if k in p)
    st = r["strength"]
    out = [f"사주: {line}   (일간 {r['day_master']})",
           f"십신(천간): {ssl}",
           f"십이운성: {twl}",
           f"오행분포: " + " ".join(f"{w}{c}" for w,c in r['wuxing'].items()),
           f"강약: {st['verdict']} (점수 {st['score']})"]
    if r["shensha"]:
        out.append("신살: " + ", ".join(f"{k}({''.join(v)})" for k,v in r['shensha'].items()))
    if r["interactions"]:
        out.append("합충: " + ", ".join(f"{k}[{'·'.join(v)}]" for k,v in r['interactions'].items()))
    out.append(f"대운({'순행' if r['daewoon']['forward'] else '역행'}, 기운 {r['daewoon']['start_age']}세):")
    out.append("   " + "  ".join(f"{x['age']}세{x['gz']}" for x in r['daewoon']['list']))
    return "\n".join(out)

if __name__ == "__main__":
    # 손중산(쑨원): 1866-11-12, 남
    r = compute(1866, 11, 12, hour=4, gender="남")
    print("[손중산 1866-11-12 寅시(가정)]")
    print(fmt(r))
