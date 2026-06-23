# -*- coding: utf-8 -*-
"""build_game.py — 사주 캐릭터 게임 화면 빌더.
   기존 build_webapp.py의 검증된 만세력/분석 JS 엔진을 추출해 재사용하고,
   그 위에 신살 판정 + 캐릭터 게임 UI(상단 캐릭터 영역 + 하단 사주·궁성 표)를 얹어
   자립형 단일 HTML(saju_game.html)을 생성한다.  characters.js를 인라인 포함.
   실행: python3 build_game.py  → saju_game.html
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))

def rd(p):
    with open(os.path.join(HERE, p), encoding="utf-8") as f:
        return f.read()

src = rd("build_webapp.py")

def between(s, start, end, keep_end=True):
    i = s.index(start)
    j = s.index(end, i)
    return s[i: j + (len(end) if keep_end else 0)]

# 1) 만세력+분석 엔진 (상수~analyzeFull)
blockA = between(src,
    'const GAN="甲乙丙丁戊己庚辛壬癸"',
    '/* ============ UI ============ */', keep_end=False)
# 2) 궁(宮) 매핑
gung = re.search(r'const GUNG=\{.*?\};', src, re.S).group(0)
# 3) 용신 길흉(useAvoid·judgeLuck·fortune)
blockB = between(src, 'function useAvoid(s,a)',
    'return {use:[...use],avoid:[...avoid],list,dl};}')

ENGINE = blockA + "\n" + gung + "\n" + blockB

JIEQI = rd("jieqi_table.json")
LUNAR = rd("lunar_table.json")
CHARS = rd("characters.js")
GAME_REFS = rd("game_refs.json")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<meta name="theme-color" content="#1d2433">
<title>사주 캐릭터 — 운세 도감</title>
<style>
:root{--bg:#f4f1ea;--card:#ffffff;--bd:#e5ddcf;--tx:#262320;--sub:#6f6a60;--accent:#7c4dff}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--bg);color:var(--tx);font-family:"Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;line-height:1.6}
.wrap{max-width:920px;margin:0 auto;padding:18px 14px 60px}
h1{font-size:20px;font-weight:700;margin:4px 0 2px;text-align:center}
.tag{text-align:center;color:var(--sub);font-size:13px;margin-bottom:16px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:14px;margin-bottom:16px}
.seg{display:inline-flex;border:1px solid var(--bd);border-radius:10px;overflow:hidden;margin:2px 8px 2px 0}
.seg button{border:0;background:#fff;padding:7px 13px;font-size:13px;cursor:pointer;color:var(--sub)}
.seg button.on{background:var(--accent);color:#fff;font-weight:600}
.frm{display:flex;flex-wrap:wrap;gap:8px;align-items:flex-end}
.fld{display:flex;flex-direction:column;font-size:12px;color:var(--sub)}
.fld select{margin-top:3px;padding:8px 6px;border:1px solid var(--bd);border-radius:9px;font-size:14px;background:#fff;min-width:74px}
.go{margin-top:8px;width:100%;padding:13px;border:0;border-radius:12px;background:linear-gradient(90deg,#5b3df0,#8a5cff);color:#fff;font-size:16px;font-weight:700;cursor:pointer}
.ex{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.ex button{border:1px solid var(--bd);background:#fff;border-radius:20px;padding:6px 12px;font-size:12px;cursor:pointer;color:var(--tx)}
.predbtn{margin-top:8px;width:100%;padding:10px;border:1px dashed var(--accent);background:#f6f2ff;color:#5b3df0;border-radius:11px;font-size:13.5px;font-weight:600;cursor:pointer}
.predhint{font-size:11.5px;color:var(--sub);line-height:1.6}
#predNote{margin-top:6px;font-size:13px;color:#5b3df0;font-weight:600}
.modalov{position:fixed;inset:0;background:rgba(20,16,30,.5);display:flex;align-items:center;justify-content:center;z-index:200;padding:16px}
.modalbox{background:#fff;border-radius:16px;max-width:460px;width:100%;max-height:88vh;overflow:auto;padding:18px}
.modalttl{font-weight:700;font-size:17px;margin-bottom:4px}
.qgrp{margin:14px 0}
.qgrp .ql{font-size:13.5px;font-weight:600;margin-bottom:7px}
.qopt{display:flex;flex-wrap:wrap;gap:6px}
.qopt label{border:1px solid var(--bd);border-radius:10px;padding:7px 11px;font-size:13px;cursor:pointer;background:#fff}
.qopt input{margin-right:5px;vertical-align:middle}
.modalbtns{display:flex;gap:8px;margin-top:16px}
.modalbtns button{flex:1;padding:12px;border:0;border-radius:12px;background:linear-gradient(90deg,#5b3df0,#8a5cff);color:#fff;font-size:15px;font-weight:700;cursor:pointer}
.modalbtns button.ghost{background:#ececf0;color:#444}
.hidden{display:none}
.note{font-size:12px;color:var(--sub);margin-top:8px}

.stagewrap{position:relative;border-radius:16px;overflow:hidden;
  background:radial-gradient(120% 90% at 50% 0%,#2a3350 0%,#1a2034 55%,#141a2c 100%);
  border:1px solid #2a3350;padding:10px 8px 8px}
.stagettl{color:#cdd6f5;font-size:12px;font-weight:600;text-align:center;margin-bottom:7px;letter-spacing:.3px}
.stage{display:flex;flex-wrap:wrap;justify-content:center;gap:6px}
.charcard{width:72px;display:flex;flex-direction:column;align-items:center;cursor:pointer;
  border-radius:12px;padding:4px 3px;transition:transform .15s,background .15s}
.charcard:hover{transform:translateY(-3px)}
.charcard.big{width:88px}
.charcard.sel{background:rgba(255,255,255,.12)}
.charcard svg{filter:drop-shadow(0 3px 5px rgba(0,0,0,.35))}
.charname{color:#eef2ff;font-size:11px;font-weight:600;margin-top:3px;text-align:center;line-height:1.2}
.charrole{font-size:10.5px;margin-top:2px;padding:1px 7px;border-radius:9px}
.r-gil{background:#fff3cf;color:#8a6d12}.r-hyung{background:#ffd8d2;color:#9c2418}
.r-yang{background:#ffe6c4;color:#8a571a}.r-oh{background:#dfeaf7;color:#2a557f}.r-il{background:#e7e2d6;color:#5a5346}
.stag{position:absolute;top:2px;left:8px;font-size:9px;font-weight:700;padding:1px 6px;border-radius:8px;z-index:2}
.s1{background:#dfe0e3;color:#666}.s2{background:#ffd9a8;color:#8a571a}.s3{background:#ffc2b4;color:#b3261e}

#info{margin-top:14px}
.infobox{background:#fff;border:1px solid var(--bd);border-radius:14px;padding:14px}
.infobox h3{margin:0 0 2px;font-size:17px}
.infobox .meta{font-size:12.5px;color:var(--sub);margin-bottom:8px}
.infobox .line{font-size:14px;margin:5px 0;padding-left:22px;position:relative}
.infobox .line b{font-weight:700}
.ic{position:absolute;left:0;top:1px}
.tip-gil{color:#b07d00}.tip-bad{color:#c0392b}.tip-info{color:#2a6a8a}
.infohint{color:var(--sub);font-size:13px;text-align:center;padding:18px}

.pillars{display:flex;gap:8px;justify-content:center;flex-wrap:nowrap;padding:18px 6px 14px}
.relpill{display:inline-flex;align-items:center;gap:5px;border:1.5px solid var(--bd);border-radius:20px;padding:6px 13px;margin:3px;font-size:13px;cursor:pointer;background:#fff;font-weight:600}
.relpill.on{box-shadow:0 0 0 3px rgba(0,0,0,.07);font-weight:700}
#relList.hot{background:#fff7ed;border:1.6px solid #f0a93a;border-radius:12px;padding:8px 6px;animation:relpulse 1.1s ease-in-out 2}
@keyframes relpulse{0%,100%{box-shadow:0 0 0 0 rgba(240,169,58,0)}50%{box-shadow:0 0 0 6px rgba(240,169,58,.22)}}
.sectitle.hot{color:#b3261e}
#summaryBox{margin-top:4px}
.sumwhen{font-size:13px;font-weight:700;color:#6a4ad0;margin-bottom:8px}
.sumitem{font-size:14px;line-height:1.7;padding:7px 11px;margin:5px 0;border-radius:10px;background:#faf7f2;border:1px solid var(--bd)}
.sumitem.sum-good{background:#fff8e6;border-color:#e8cf93}
.sumitem.sum-bad{background:#fff4f1;border-color:#f0b9ad}
.sumitem.sum-mid{background:#f4f6f8;border-color:#d8dee4}
.dggrp{font-size:13px;font-weight:700;color:#3a3a3a;margin:12px 0 7px;border-left:3px solid #c9a227;padding-left:8px}
.dggrid{display:grid;grid-template-columns:1fr;gap:8px}
.dgcard{display:grid;grid-template-columns:58px 1fr;gap:10px;align-items:start;padding:9px 11px;border:1px solid var(--bd);border-radius:12px;background:#fff;cursor:pointer;transition:box-shadow .15s,border-color .15s}
.dgcard:hover{border-color:#c9a227;box-shadow:0 2px 10px rgba(0,0,0,.06)}
.dgtok{width:58px;height:58px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.dgtok svg{width:54px;height:54px}
.dgnm{font-size:13.5px;font-weight:700;line-height:1.35}
.dgbadges{margin:4px 0 5px;display:flex;gap:5px;flex-wrap:wrap}
.dgb{font-size:10.5px;font-weight:700;padding:1px 7px;border-radius:8px}
.dgdesc{font-size:12px;color:#555;line-height:1.55}
.dgfull{grid-column:1/3;display:none;margin-top:8px;border-top:1px dashed var(--bd);padding-top:8px}
@media(min-width:520px){.dggrid{grid-template-columns:1fr 1fr}}
.bigev{color:#d23b2a;font-weight:700}
.sumgrp{font-size:12.5px;font-weight:700;color:#6a4ad0;margin:14px 0 3px}
.sumdesc{font-size:12px;color:#666;line-height:1.6;margin:0 0 6px;padding:6px 9px;background:#f6f4fb;border-radius:8px}
.sumlane{border:1px solid var(--bd);border-radius:14px;overflow:hidden;margin:11px 0;background:#fff}
.lanehd{padding:8px 12px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:2px}
.lanehd .lt{font-size:15px;font-weight:700}
.lanehd .lg{font-size:18px;font-weight:700;margin-left:6px}
.lanehd .lp{font-size:11px;width:100%}
.carow{display:flex;align-items:center;gap:4px;padding:9px 4px 4px}
.carow .nav{flex:0 0 auto;width:32px;height:32px;border-radius:50%;border:1px solid var(--bd);background:#fff;font-size:20px;line-height:1;cursor:pointer;color:#666;padding:0}
.carow .nav:active{transform:scale(.92)}
.carstg{flex:1;display:flex;align-items:center;justify-content:center;gap:5px;min-height:214px;overflow:hidden}
.pcw{flex:0 0 auto;cursor:pointer;transition:opacity .2s}
.pcd{border-radius:12px;overflow:hidden;background:#fff}
.pchd{padding:5px 8px;display:flex;align-items:center;justify-content:space-between;gap:4px}
.pcnm{font-weight:700;line-height:1.25}
.pcst{font-size:10px;letter-spacing:1px;color:#e0a800;flex:0 0 auto}
.pcemb{display:flex;align-items:center;justify-content:center}
.pcemb svg{width:100%;height:100%;display:block}
.pcft{padding:5px 8px 7px}
.pctype{font-size:10px;font-weight:700}
.pcshort{font-size:11px;color:#555;line-height:1.45;margin-top:2px}
.cardots{display:flex;justify-content:center;gap:5px;padding:2px 0 9px}
.cardots i{width:7px;height:7px;border-radius:50%;display:inline-block;transition:background .2s}
@keyframes sumNext{0%{opacity:0;transform:translateX(40px) scale(.94)}60%{opacity:1}100%{opacity:1;transform:none}}
@keyframes sumPrev{0%{opacity:0;transform:translateX(-40px) scale(.94)}60%{opacity:1}100%{opacity:1;transform:none}}
.carstg{position:relative}
.zapfx{position:absolute;pointer-events:none;z-index:7;animation:zapfx .5s ease-out forwards}
@keyframes zapfx{0%{opacity:0;transform:scale(.5)}12%{opacity:1}26%{opacity:.15}42%{opacity:1}60%{opacity:.3}100%{opacity:0;transform:scale(1.2)}}
.zapglow{position:absolute;inset:0;border-radius:12px;box-shadow:0 0 0 3px #ffd54a,0 0 18px 4px rgba(255,179,0,.7);animation:zapglow .5s ease-out forwards;pointer-events:none}
@keyframes zapglow{0%{opacity:0}20%{opacity:1}100%{opacity:0}}
.sechd{display:flex;align-items:flex-start;justify-content:space-between;gap:8px}
.sechd .sectitle{flex:1;margin-top:0}
.sectog{flex:0 0 auto;width:27px;height:27px;border:1px solid var(--bd);background:#fff;border-radius:8px;color:#666;font-size:13px;line-height:1;cursor:pointer;padding:0}
.sectog:active{transform:scale(.9)}
.stagetog{position:absolute;top:8px;right:8px;z-index:6;background:rgba(255,255,255,.85)}
.secbody{overflow:hidden}
#sumModalBox,#sumModalBox *{font-family:"Apple SD Gothic Neo","Malgun Gothic",sans-serif}
#sumModalBox h3{font-size:15px;font-weight:700;margin:10px 0 4px}
#sumModalBox .line{font-size:13.5px;line-height:1.75}
#sumModalBox .meta{font-size:12px;color:var(--sub)}
#sumModalBox .reftitle{font-size:13px}
#sumModalBox .refhead{font-size:12.5px}
#sumModalBox .refsnip,#sumModalBox .reffull{font-size:12.5px;line-height:1.7}
.sumleg{font-size:11.5px;color:var(--sub);margin:2px 0 8px}
.refsec{margin-top:12px;border-top:1px dashed var(--bd);padding-top:10px}
.reftitle{font-size:13px;font-weight:700;margin-bottom:6px}
.refitem{background:#faf7f2;border:1px solid var(--bd);border-radius:10px;padding:8px 10px;margin:5px 0;cursor:pointer}
.refhead{font-size:12.5px;font-weight:600;color:#7a5230}
.refmore{font-size:11px;color:var(--sub);font-weight:400}
.refsnip{font-size:12px;color:var(--sub);margin-top:3px;line-height:1.6}
.reffull{display:none;font-size:12.5px;margin-top:7px;line-height:1.8;color:var(--tx)}
.refitem.open .reffull{display:block}.refitem.open .refsnip{display:none}
.gunghead{display:flex;flex-direction:column;align-items:center;margin-bottom:2px}
.gzrow{display:flex;align-items:center;justify-content:center;gap:4px;margin:3px 0 0}
.gsym{display:inline-flex;line-height:0}
.poscap{font-size:9.5px;color:var(--sub);margin-top:1px}
@media(max-width:560px){.gsym svg{width:28px;height:28px}}
.pcol{flex:1 1 0;min-width:106px;border:1px solid var(--bd);border-radius:14px;background:#fff;
  padding:8px 5px;text-align:center;transition:box-shadow .2s,border-color .2s,transform .2s}
.pcol .gung{font-size:11px;color:var(--sub);font-weight:600}
.pcol .gung small{display:block;font-weight:400;font-size:10px;opacity:.8}
.pcol .ss{font-size:12px;color:#7c4dff;font-weight:600;margin:4px 0 3px}
.gz{width:46px;height:46px;margin:2px auto;border-radius:10px;display:flex;align-items:center;justify-content:center;
  font-size:26px;font-weight:700;color:#fff}
.wx-mok{background:#3aa05a}.wx-hwa{background:#e0574a}.wx-to{background:#cf9a2a}.wx-geum{background:#8b97a1}.wx-su{background:#3f74b8}
.gz.sm{width:30px;height:30px;font-size:16px;border-radius:8px}
.hidn{font-size:11px;color:var(--sub);margin-top:4px;line-height:1.5}
.twf{font-size:11px;color:#8a8378;margin-top:2px}
.daycap{margin-top:4px}
.pcol.hl{transform:translateY(-2px)}
#result{position:relative}
#fxRel,#fxSel{position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;overflow:visible}
#fxRel{z-index:38}#fxSel{z-index:42}
.fxline{fill:none;stroke-width:3.5;stroke-linecap:round;animation:dashflow .8s linear infinite}
@keyframes dashflow{to{stroke-dashoffset:-32}}
.fxdot{animation:fxpulse 1s ease-in-out infinite}
@keyframes fxpulse{0%,100%{opacity:1;stroke-width:3}50%{opacity:.4;stroke-width:5}}
.legend{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;font-size:12px;color:var(--sub);margin-top:10px}
.legend span{display:inline-flex;align-items:center;gap:5px}
.dot{width:11px;height:11px;border-radius:50%;display:inline-block}
.sectitle{font-size:14px;font-weight:700;margin:0 0 8px;color:var(--sub)}
.lrlabel{font-size:12px;color:var(--sub);margin:8px 2px 3px;font-weight:600}
.lrow{display:flex;gap:6px;overflow-x:auto;padding:3px 2px 6px}
.chip{flex:0 0 auto;border:1px solid var(--bd);background:#fff;border-radius:11px;padding:6px 9px;cursor:pointer;text-align:center;font-size:11px;line-height:1.3;min-width:56px}
.chip.on{border-color:var(--accent);box-shadow:0 0 0 2px rgba(124,77,255,.3);background:#f6f2ff}
.chip .cgz{font-size:16px;font-weight:700;letter-spacing:1px}
.luck-good{color:#1f9d55}.luck-bad{color:#d23b2a}.luck-mid{color:#9a8a5a}
.pcol.luck{background:#f5f1ff;border-color:#dcccff}
.pcol .lmk{font-size:12px;font-weight:700;margin-top:3px}
.charcard{position:relative}
.charcard .lk{position:absolute;top:2px;right:8px;background:#7c4dff;color:#fff;font-size:9px;padding:1px 6px;border-radius:8px}
.relchipbg{fill:#1b2233;opacity:.92}.reltext{font-size:11px;font-weight:700}
.stagecols{display:flex;gap:10px;align-items:stretch}
.stagecol{flex:1;min-width:0}
.scolttl{color:#aeb8d8;font-size:12px;font-weight:700;text-align:center;margin-bottom:8px}
.scells{display:flex;flex-wrap:wrap;justify-content:center;gap:5px;min-height:44px}
.stagedivider{width:1px;background:rgba(255,255,255,.16)}
.luckhint{color:#8a93b5;font-size:12px;text-align:center;padding:22px 4px;line-height:1.5}
.chip.indae{outline:2px dashed #9a6aff;outline-offset:2px}
@media(max-width:560px){.gz{width:40px;height:40px;font-size:22px}.charcard{width:60px}.charcard.big{width:72px}.charname{font-size:10px}.stagettl{font-size:11px}}
</style>
</head>
<body>
<div class="wrap">
  <h1>🐾 사주 캐릭터 — 운세 도감</h1>
  <div class="tag">생년월일시를 넣으면 내 사주의 캐릭터(신살)가 나타나요. 캐릭터를 누르면 어느 궁(宮)에 길·흉으로 작용하는지 보여줍니다.</div>

  <div class="card">
    <div id="calSeg" class="seg"><button data-cal="solar" class="on" onclick="setCal('solar')">양력</button><button data-cal="lunar" onclick="setCal('lunar')">음력</button></div>
    <div class="frm" style="margin-top:8px">
      <label class="fld hidden" id="leapWrap">윤달<select id="leap"><option value="0">평달</option><option value="1">윤달</option></select></label>
      <label class="fld">연도<select id="y"></select></label>
      <label class="fld">월<select id="m"></select></label>
      <label class="fld">일<select id="d"></select></label>
      <label class="fld">시<select id="h"></select></label>
      <label class="fld">분<select id="mi"></select></label>
    </div>
    <button type="button" class="predbtn" onclick="openPred()">🕒 태어난 시간을 모르시나요? — 몇 가지 답하고 추정하기</button>
    <div id="predNote"></div>
    <div id="predModal" class="modalov hidden" onclick="if(event.target===this)closePred()">
      <div class="modalbox">
        <div class="modalttl">🕒 태어난 시간 예측</div>
        <div class="predhint" style="margin:2px 0 6px">정확한 출생 기록(병원·부모님 기억)이 가장 좋지만, 모를 땐 아래로 추정해볼 수 있어요. 어디까지나 참고용이에요.</div>
        <div class="qgrp"><div class="ql">1) 혹시 대략의 시간대를 들으신 적 있나요?</div><div class="qopt">
          <label><input type="radio" name="pq1" value="모름" checked>모름</label>
          <label><input type="radio" name="pq1" value="새벽">새벽(3~7시)</label>
          <label><input type="radio" name="pq1" value="아침">아침(7~11시)</label>
          <label><input type="radio" name="pq1" value="한낮">한낮(11~15시)</label>
          <label><input type="radio" name="pq1" value="오후">오후(15~19시)</label>
          <label><input type="radio" name="pq1" value="저녁">저녁(19~23시)</label>
          <label><input type="radio" name="pq1" value="한밤">한밤(23~3시)</label></div></div>
        <div class="qgrp"><div class="ql">2) 평소 생체 리듬은 어떤가요?</div><div class="qopt">
          <label><input type="radio" name="pq2" value="아침형">아침형(일찍 일어남)</label>
          <label><input type="radio" name="pq2" value="중간" checked>중간</label>
          <label><input type="radio" name="pq2" value="저녁형">저녁형(올빼미)</label></div></div>
        <div class="qgrp"><div class="ql">3) 잠잘 때 가장 편한 자세는?</div><div class="qopt">
          <label><input type="radio" name="pq3" value="바로" checked>바로 똑바로 눕는다</label>
          <label><input type="radio" name="pq3" value="옆으로">옆으로(모로) 눕는다</label>
          <label><input type="radio" name="pq3" value="엎드려">엎드리거나 웅크린다</label></div></div>
        <div class="predhint" style="margin:6px 0 0">▾ 아래는 사주(시주)와 대조해 더 정밀하게 보정하는 질문이에요.</div>
        <div class="qgrp"><div class="ql">4) 내 성격에 가장 가까운 것은?</div><div class="qopt">
          <label><input type="radio" name="pq6" value="리더">리더·주도적</label>
          <label><input type="radio" name="pq6" value="예술">예술·감성·몽상</label>
          <label><input type="radio" name="pq6" value="분석">분석·예민·완벽</label>
          <label><input type="radio" name="pq6" value="사교">사교·인기·끼</label>
          <label><input type="radio" name="pq6" value="성실">성실·실속·안정</label>
          <label><input type="radio" name="pq6" value="" checked>모름</label></div></div>
        <div class="qgrp"><div class="ql">5) 노후·말년에 더 끌리는 것은?</div><div class="qopt">
          <label><input type="radio" name="pq5" value="재물">재물·안정</label>
          <label><input type="radio" name="pq5" value="공부">공부·종교·예술</label>
          <label><input type="radio" name="pq5" value="활동">활동·여행·이동</label>
          <label><input type="radio" name="pq5" value="명예">명예·자리·리더</label>
          <label><input type="radio" name="pq5" value="" checked>모름</label></div></div>
        <div class="qgrp"><div class="ql">6) 자녀에 대해 (해당되면)</div><div class="qopt">
          <label><input type="radio" name="pq4" value="가깝다">가깝고 잘 통한다</label>
          <label><input type="radio" name="pq4" value="반듯">반듯·모범적이다</label>
          <label><input type="radio" name="pq4" value="독립">독립적·강하다</label>
          <label><input type="radio" name="pq4" value="" checked>모름/없음</label></div></div>
        <div class="modalbtns"><button onclick="applyPred()">이 추정 시간 넣기</button><button class="ghost" onclick="closePred()">닫기</button></div>
        <div class="predhint" style="margin-top:12px">※ 추정이라 실제와 다를 수 있어요. 사주의 <b>일주·격국</b>은 시와 무관하게 정확하지만, <b>시주(자녀·말년)</b>는 시에 따라 달라집니다.</div>
      </div>
    </div>
    <div style="margin-top:10px">
      <div id="sexSeg" class="seg"><button data-sex="남" class="on" onclick="setSex('남')">남자</button><button data-sex="여" onclick="setSex('여')">여자</button></div>
      <div id="lstSeg" class="seg"><button data-lst="1" class="on" onclick="setLst('1')">진태양시 보정</button><button data-lst="0" onclick="setLst('0')">표준시 그대로</button></div>
    </div>
    <button class="go" onclick="run()">사주 소환</button>
    <button type="button" class="predbtn" style="border-color:#2a9d8f;background:#eafaf5;color:#1d6b5f;margin-top:8px" onclick="toggleBT()">🔎 내 인생 백테스팅 — 실제 사건과 사주 비교해보기</button>
    <div class="ex" id="exBox"></div>
    <div class="note">한국 표준시(KST) 기준. 시(時)를 모르면 "모름"을 선택하면 3주만 분석합니다.</div>
  </div>

  <div id="btCard" class="card hidden">
    <div class="sectitle">🔎 내 인생 백테스팅 — 겪은 일을 입력하면 그 시기 사주 신호와 맞춰봐요</div>
    <div class="predhint">먼저 위에서 「사주 소환」으로 사주를 분석하세요. 연도(필수)·월(선택)·사건 종류·메모를 넣고 「분석하기」를 누르면, 그 시기의 대운·세운(·월운) 신호가 입력한 사건과 얼마나 맞는지 보여드려요.</div>
    <div id="btRows"></div>
    <button type="button" class="predbtn" style="margin-top:6px" onclick="btAddRow()">＋ 사건 추가</button>
    <div style="margin-top:10px"><button class="go" style="margin:0" onclick="btAnalyze()">분석하기</button></div>
    <div id="btResult"></div>
  </div>

  <div id="result" class="hidden">
    <svg id="fxRel" xmlns="http://www.w3.org/2000/svg"></svg>
    <svg id="fxSel" xmlns="http://www.w3.org/2000/svg"></svg>
    <div class="card">
      <div class="sechd"><div class="sectitle">운(運) 선택 — 대운·세운·월운을 누르면 아래 캐릭터와 합·충이 갱신됩니다</div><button class="sectog" onclick="secToggle('sb-luck',this)" aria-expanded="true" aria-label="접기/펼치기">▾</button></div>
      <div class="secbody" id="sb-luck">
        <div class="lrlabel">대운 (10년)</div><div class="lrow" id="daeRow"></div>
        <div class="lrlabel">세운 (해운) <span id="seYearLab" style="font-weight:400"></span></div><div class="lrow" id="seRow"></div>
        <div class="lrlabel">월운 (달운)</div><div class="lrow" id="wolRow"></div>
      </div>
    </div>

    <div class="card">
      <div class="sechd"><div class="sectitle">📋 이 시기 총평 — 무엇을 기대하고 무엇을 조심할까 (큰 사건은 빨강)</div><button class="sectog" onclick="secToggle('sb-sum',this)" aria-expanded="true" aria-label="접기/펼치기">▾</button></div>
      <div class="secbody" id="sb-sum"><div id="summaryBox"><div class="infohint" style="padding:6px">대운·세운·월운을 선택하면 그 시기의 총평이 자동으로 나옵니다.</div></div></div>
    </div>

    <div class="stagewrap">
      <button class="sectog stagetog" onclick="secToggle('sb-stage',this)" aria-expanded="true" aria-label="접기/펼치기">▾</button>
      <div class="stagettl">✦ 내 사주에 깃든 캐릭터 ✦</div>
      <div class="secbody" id="sb-stage">
        <div class="stagecols">
          <div class="stagecol"><div class="scolttl">원국 — 타고난 나</div><div class="scells" id="cellsOrig"></div></div>
          <div class="stagedivider"></div>
          <div class="stagecol"><div class="scolttl">운(運)으로 오는</div><div class="scells" id="cellsLuck"></div></div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="sechd"><div class="sectitle">사주 원국 + 운 · 궁(宮) — 글자 옆 캐릭터가 위 캐릭터 클릭 시 표정·테두리로 반응</div><button class="sectog" onclick="secToggle('sb-gung',this)" aria-expanded="true" aria-label="접기/펼치기">▾</button></div>
      <div class="secbody" id="sb-gung">
        <div class="pillars" id="pillars"></div>
        <div class="legend">
          <span><i class="dot" style="background:#e0b400"></i>길</span>
          <span><i class="dot" style="background:#d98a2a"></i>양면</span>
          <span><i class="dot" style="background:#d23b2a"></i>흉</span>
        </div>
        <div class="sectitle" id="relTitle" style="margin-top:16px">합·충·형·파·해 — 운을 선택하면 표시됩니다</div>
        <div id="relList"><div class="infohint" style="padding:8px">운(대운·세운·월운)을 선택하면 합·충 관계가 여기에 표시됩니다.</div></div>
      </div>
    </div>

    <div id="info"><div class="infohint">위 캐릭터(또는 합·충 칩)를 누르면 상세 설명이 여기에 나타납니다.</div></div>

    <div class="card">
      <div class="sectitle">📖 내 신살 도감 — 지금 내 사주에 뜬 캐릭터 모아보기</div>
      <div id="dogamBox"><div class="infohint" style="padding:8px">사주를 소환하면 원국과 선택한 운에 뜬 캐릭터가 도감으로 모입니다.</div></div>
    </div>
  </div>

  <div id="sumModal" class="modalov hidden" onclick="if(event.target===this)closeSumModal()">
    <div class="modalbox" id="sumModalBox"></div>
  </div>
</div>

<script>__CHARS__</script>
<script>
const JIEQI = __JIEQI__;
const LUNAR = __LUNAR__;
const REFS = __GAMEREFS__;
__ENGINE__
</script>
<script>
/* ===== 신살 판정 + 게임 UI ===== */
document.head.insertAdjacentHTML('beforeend', SAJU_CHARS.style);
const SC = SAJU_CHARS;
const WX_KO={木:'목',火:'화',土:'토',金:'금',水:'수'};
const WXCLASS={木:'wx-mok',火:'wx-hwa',土:'wx-to',金:'wx-geum',水:'wx-su'};
const WXLINE={木:'#3aa05a',火:'#e0574a',土:'#cf9a2a',金:'#8b97a1',水:'#3f74b8'};
// 완전한 지장간(여기·중기·본기 순) — 표시용
const JANGGAN={子:['壬','癸'],丑:['癸','辛','己'],寅:['戊','丙','甲'],卯:['甲','乙'],辰:['乙','癸','戊'],巳:['戊','庚','丙'],午:['丙','己','丁'],未:['丁','乙','己'],申:['戊','壬','庚'],酉:['庚','辛'],戌:['辛','丁','戊'],亥:['戊','甲','壬']};

const SAMHAP_GROUP={申:'水',子:'水',辰:'水',寅:'火',午:'火',戌:'火',巳:'金',酉:'金',丑:'金',亥:'木',卯:'木',未:'木'};
const TWELVE_SS={
 水:{巳:'겁살',午:'재살',未:'천살',申:'지살',酉:'연살',戌:'월살',亥:'망신',子:'장성',丑:'반안',寅:'역마',卯:'육해',辰:'화개'},
 火:{亥:'겁살',子:'재살',丑:'천살',寅:'지살',卯:'연살',辰:'월살',巳:'망신',午:'장성',未:'반안',申:'역마',酉:'육해',戌:'화개'},
 金:{寅:'겁살',卯:'재살',辰:'천살',巳:'지살',午:'연살',未:'월살',申:'망신',酉:'장성',戌:'반안',亥:'역마',子:'육해',丑:'화개'},
 木:{申:'겁살',酉:'재살',戌:'천살',亥:'지살',子:'연살',丑:'월살',寅:'망신',卯:'장성',辰:'반안',巳:'역마',午:'육해',未:'화개'}};
const SS12CHAR={겁살:'겁살',재살:'재살',천살:'천살',지살:'지살',연살:'도화',월살:'월살',망신:'망신살',장성:'장성살',반안:'반안살',역마:'역마',육해:'육해살',화개:'화개'};
const BAEKHO=new Set(['甲辰','乙未','丙戌','丁丑','戊辰','壬戌','癸丑']);
const GWAEGANG=new Set(['庚辰','庚戌','壬辰','戊戌']);
const HYUNCHIM=new Set(['甲申','甲午','辛卯','辛未','戊午','壬午']);
const CHEONDEOK={寅:'丁',卯:'申',辰:'壬',巳:'辛',午:'亥',未:'甲',申:'癸',酉:'寅',戌:'丙',亥:'乙',子:'巳',丑:'庚'};
const WOLDEOK={寅:'丙',午:'丙',戌:'丙',申:'壬',子:'壬',辰:'壬',亥:'甲',卯:'甲',未:'甲',巳:'庚',酉:'庚',丑:'庚'};
const HONGYEOM={甲:'午',乙:'申',丙:'寅',丁:'未',戊:'辰',己:'辰',庚:'戌',辛:'酉',壬:'子',癸:'申'};
const GUIMUN={子酉:'자유귀문',丑午:'축오귀문',寅未:'인미귀문',卯申:'묘신귀문',辰亥:'진해귀문',巳戌:'사술귀문'};
const WONJIN=new Set(['子未','丑午','寅酉','卯申','辰亥','巳戌']);
function ZIDX(g,z){for(let i=0;i<60;i++)if(i%10===GAN.indexOf(g)&&i%12===ZHI.indexOf(z))return i;return 0;}
function gongmangOf(didx){const s=(didx-(didx%10))%12;return [ZHI[(s+10)%12],ZHI[(s+11)%12]];}

function shinsalSet(p,order,dg){
  const branchOf={},stemOf={},gz={};
  order.forEach(k=>{branchOf[k]=p[k][1];stemOf[k]=p[k][0];gz[k]=p[k];});
  const pkByBranch=b=>order.filter(k=>branchOf[k]===b);
  const res=[];const seen={};
  function push(key,targets,note){
    targets=(targets||[]).filter(t=>t&&t.k);
    if(!targets.length)return;
    if(seen[key]){const ex=seen[key];targets.forEach(t=>{if(!ex.targets.some(o=>o.k===t.k&&o.which===t.which))ex.targets.push(t);});return;}
    const e={key,targets,note};seen[key]=e;res.push(e);
  }
  // 12신살 (년지 기준)
  const grp=SAMHAP_GROUP[branchOf.year],tbl=TWELVE_SS[grp];
  order.forEach(k=>{const nm=tbl[branchOf[k]];if(nm)push(SS12CHAR[nm],[{k,which:'z'}],nm+'('+branchOf[k]+')');});
  // 귀인(일간 기준) — 엔진 shensha 활용(주어진 간지 전체)
  const sh=shensha(dg, branchOf.year, order.map(k=>branchOf[k]));
  ['천을귀인','양인','문창귀인','건록'].forEach(name=>{ if(sh[name]) sh[name].forEach(b=>push(name,pkByBranch(b).map(k=>({k,which:'z'})),name)); });
  // 칠살(편관)
  order.forEach(k=>{ if(k!=='day' && sipsin(dg,stemOf[k])==='편관') push('편관칠살',[{k,which:'g'}],'천간 편관'); });
  // 백호·괴강·현침
  order.forEach(k=>{ if(BAEKHO.has(gz[k])) push('백호',[{k,which:'z'}],gz[k]+' 백호'); });
  order.forEach(k=>{ if(GWAEGANG.has(gz[k])) push('괴강',[{k,which:'z'}],gz[k]+' 괴강'); });
  order.forEach(k=>{ if(HYUNCHIM.has(gz[k])) push('현침살',[{k,which:'g'}],gz[k]+' 현침'); });
  // 천덕·월덕 (월지 기준)
  const mb=branchOf.month, cd=CHEONDEOK[mb], wd=WOLDEOK[mb];
  order.forEach(k=>{ if(stemOf[k]===cd)push('천덕귀인',[{k,which:'g'}],'월지 '+mb+' 천덕'); else if(branchOf[k]===cd)push('천덕귀인',[{k,which:'z'}],'월지 '+mb+' 천덕'); });
  order.forEach(k=>{ if(stemOf[k]===wd)push('월덕귀인',[{k,which:'g'}],'월지 '+mb+' 월덕'); });
  // 홍염(일간 기준)
  const hy=HONGYEOM[dg]; if(hy) pkByBranch(hy).forEach(k=>push('홍염살',[{k,which:'z'}],dg+'일간 홍염'));
  // 공망(일주 순공)
  const didx=ZIDX(dg,branchOf.day),gmv=gongmangOf(didx);
  gmv.forEach(b=>{pkByBranch(b).filter(k=>k!=='day').forEach(k=>push('공망',[{k,which:'z'}],'공망 '+b));});
  // 쌍(귀문·원진·천라지망)
  for(let i=0;i<order.length;i++)for(let j=i+1;j<order.length;j++){
    const a1=order[i],a2=order[j],b1=branchOf[a1],b2=branchOf[a2],k1=b1+b2,k2=b2+b1;
    const gmn=GUIMUN[k1]||GUIMUN[k2];
    if(gmn)push(gmn,[{k:a1,which:'z'},{k:a2,which:'z'}],b1+b2+' 귀문');
    if(WONJIN.has(k1)||WONJIN.has(k2))push('원진',[{k:a1,which:'z'},{k:a2,which:'z'}],b1+b2+' 원진');
  }
  const bs=new Set(order.map(k=>branchOf[k]));
  if(bs.has('戌')&&bs.has('亥'))push('천라지망',order.filter(k=>['戌','亥'].includes(branchOf[k])).map(k=>({k,which:'z'})),'戌亥 천라');
  if(bs.has('辰')&&bs.has('巳'))push('천라지망',order.filter(k=>['辰','巳'].includes(branchOf[k])).map(k=>({k,which:'z'})),'辰巳 지망');
  // 역마 진/살 결정
  const GIL=new Set(['천을귀인','천덕귀인','월덕귀인','문창귀인','건록','장성살','반안살']);
  const HG=new Set(['양인','백호','괴강','겁살','재살','천살','육해살','망신살','공망','편관칠살']);
  const hasGil=res.some(e=>GIL.has(e.key)),hasHyung=res.some(e=>HG.has(e.key));
  res.forEach(e=>{ if(e.key==='역마') e.key=(hasGil&&!hasHyung)?'진역마':(hasHyung?'살역마':'진역마'); });
  res.forEach(e=>{e.pillars=[...new Set(e.targets.map(t=>t.k))];});
  return res;
}

// 원소 = 합(삼합·방합·반합·육합)으로 오행이 형성될 때 등장
const SANHAP_E={水:['申','子','辰'],木:['亥','卯','未'],火:['寅','午','戌'],金:['巳','酉','丑']};
const BANGHAP_E={水:['亥','子','丑'],木:['寅','卯','辰'],火:['巳','午','未'],金:['申','酉','戌']};
const WANGJI={水:'子',木:'卯',火:'午',金:'酉'};
const YUKHAP_E={'子丑':'土','寅亥':'木','卯戌':'火','辰酉':'金','巳申':'水','午未':'火'};
const COMBO_ORD={삼합:4,방합:3,반합:2,육합:1};
function elemCombos(brSet){
  const acc={};
  const add=(el,brs,type)=>{if(!brs.every(b=>brSet.has(b)))return;if(!acc[el])acc[el]={brs:new Set(),types:[]};brs.forEach(b=>acc[el].brs.add(b));if(!acc[el].types.includes(type))acc[el].types.push(type);};
  ['水','木','火','金'].forEach(E=>{
    add(E,SANHAP_E[E],'삼합');add(E,BANGHAP_E[E],'방합');
    const w=WANGJI[E],sh=SANHAP_E[E],bh=BANGHAP_E[E];
    add(E,[w,sh[0]],'반합');add(E,[w,sh[2]],'반합');   // 삼합 반합(왕지 포함만)
    add(E,[w,bh[0]],'반합');add(E,[w,bh[2]],'반합');   // 방합 반합(왕지 포함)
  });
  for(const pr in YUKHAP_E){if(brSet.has(pr[0])&&brSet.has(pr[1]))add(YUKHAP_E[pr],[pr[0],pr[1]],'육합');}
  const out={};for(const el in acc){const ts=acc[el].types.slice().sort((a,b)=>COMBO_ORD[b]-COMBO_ORD[a]);out[el]={branches:[...acc[el].brs],types:ts,primary:ts[0]};}
  return out;
}
function spiritSet(P,ord){
  const brSet=new Set(ord.map(k=>P[k][1]));const found=elemCombos(brSet);const out=[];
  for(const E in found){const f=found[E];const targets=[];
    f.branches.forEach(b=>ord.filter(k=>P[k][1]===b).forEach(k=>targets.push({k,which:'z'})));
    if(targets.length>=2)out.push({key:WX_KO[E],hanja:E,combo:f.primary,types:f.types,branches:f.branches,targets});}
  return out;
}

/* === 상세 설명 === */
const SS_INFO={
 천을귀인:{g:'최고의 길신. 어려울 때 귀인·윗사람의 도움을 받습니다.',a:'사람을 통해 풀어가세요. 인맥이 곧 복입니다.'},
 천덕귀인:{g:'하늘이 베푸는 덕. 위기에서 보호받고 흉이 줄어듭니다.',a:'선행과 베풂이 그대로 복으로 돌아옵니다.'},
 월덕귀인:{g:'달의 덕. 온화한 구원과 인덕이 따릅니다.',a:'급할수록 부드럽게. 인덕으로 풀립니다.'},
 문창귀인:{g:'학문·시험·문서운의 길신. 머리가 총명합니다.',a:'공부·자격·글로 승부하면 길합니다.'},
 건록:{g:'안정된 재록(祿). 자기 힘으로 먹고사는 복.',a:'성실함이 곧 재산. 꾸준함이 답입니다.'},
 편관칠살:{b:'칠살. 강한 압박·경쟁·구설이지만 제압하면 큰 권력이 됩니다.',a:'식신·인성으로 제어하면 흉이 권위로 바뀝니다.',d:'나를 강하게 누르는 기운이에요. 잘 다스리면 군인·검경·운동·사업처럼 강단이 필요한 분야에서 큰 권력·성취가 되지만, 못 다스리면 압박·사고·질병·관재로 나타납니다.',w:'신약한데 칠살이 강하거나, 운에서 칠살이 또 들어와 겹칠 때 압박이 커져요. 식신(제압)·인성(설기)이 있으면 길로 바뀝니다.'},
 양인:{b:'지나치게 강한 칼날의 기운. 과격·사고·다툼 주의.',a:'힘을 쓰는 일·전문기술로 돌리면 길합니다.',d:'칼처럼 날카롭고 강한 힘이에요. 결단력·승부욕이 강해 운동·의료(수술)·기술·군경 같은 「힘과 정밀함」이 필요한 일에 어울려요. 다만 과격함·사고·다툼·금전 손실을 조심해야 합니다.',w:'일간이 강한데 양인까지 세거나, 운에서 양인을 충하면(양인충) 사고·다툼수가 커져요.'},
 백호:{b:'피·사고·수술수의 강한 기운.',a:'안전·건강 관리를 철저히. 활인업엔 오히려 길.',d:'피를 보는 일과 연결된 강한 기운이에요. 사고·수술·외상 같은 일을 조심해야 하지만, 의료·군경·정육·미용처럼 「피·칼」을 다루는 활인업에서는 오히려 능력으로 쓰입니다.',w:'백호 글자가 일지·시지에 있고, 운에서 그 글자를 충·형할 때 사고수가 올라와요.'},
 괴강:{b:'극단적이고 강렬한 카리스마. 길흉이 크게 갈립니다.',a:'리더십·전문직에 쓰면 대성. 고집은 화근.',d:'아주 강하고 극단적인 기운이에요. 우두머리 기질·카리스마·결단력이 뛰어나 큰 인물이 많지만, 한번 무너지면 크게 흔들려 길흉의 진폭이 큽니다.',w:'괴강이 일주에 있고 운에서 충을 맞을 때 극단으로 치우치기 쉬워요. 고집을 누그러뜨리면 길합니다.'},
 도화:{b:'매력·인기. 이성운이 강하나 색난 주의.',a:'끼를 예술·서비스·인기업으로 살리면 길.',d:'사람을 끄는 매력과 인기의 기운이에요. 끼·미적 감각이 좋아 연예·예술·서비스·영업에 강점이지만, 이성 문제(색난)나 구설을 조심해야 합니다.',w:'도화 글자가 운에서 합이 되면 이성 인연·인기가 크게 동하고, 충이 되면 구설·관계 변동이 생겨요.'},
 홍염살:{b:'은근한 매혹·끼. 이성의 인기가 많습니다.',a:'매력을 일과 대인관계의 무기로 쓰세요.'},
 화개:{b:'예술·종교·학문의 별. 고독하나 깊은 재능.',a:'혼자 깊이 파는 분야(예술·연구·수행)에서 빛납니다.'},
 역마:{b:'이동·변동수.',a:''},
 진역마:{g:'길한 역마. 이동이 곧 발전 — 해외·무역·영업에 길.',a:'적극적으로 움직이세요. 나갈수록 발전합니다.'},
 살역마:{b:'흉한 역마. 원치 않는 이동·분주하나 실속 없음.',a:'무리한 이동·변동은 자제. 자리를 지키는 게 이득.'},
 지살:{b:'이사·독립·터전의 변동.',a:'주거·환경 변화의 시기. 능동적 이동은 길.'},
 겁살:{b:'빼앗김·강탈·갑작스런 손실수.',a:'보증·투기·과욕 금물. 지키는 데 집중.'},
 재살:{b:'관재·구속·송사의 기운(수옥살).',a:'법규·계약을 철저히. 시비에 휘말리지 마세요.'},
 천살:{b:'거스를 수 없는 천재지변·변고.',a:'대비와 보험. 겸손함이 화를 줄입니다.'},
 월살:{b:'메마름·위축·소모(고초살).',a:'무리한 확장보다 내실. 건강·자금 비축.'},
 망신살:{b:'망신·구설·체면 손상.',a:'언행·처신을 조심. 드러내기보다 신중하게.'},
 육해살:{b:'질병·방해·구설. 일이 더디고 막힙니다.',a:'건강 챙기고 인간관계 갈등을 피하세요.'},
 장성살:{g:'장수의 별. 권위·통솔·리더십.',a:'주도권을 잡는 자리에서 능력을 발휘하세요.'},
 반안살:{g:'안장(말 등). 승진·출세·후원의 기운.',a:'윗사람의 후원을 받아 올라타는 시기.'},
 공망:{b:'비어있음·허무. 해당 궁의 결실이 약해집니다.',a:'기대를 비우고 정신·종교·전문분야로 채우세요.'},
 원진:{b:'까닭 모를 미움·애증. 관계의 불화.',a:'엮인 상대와 거리 조절. 감정 소모를 줄이세요.'},
 천라지망:{b:'그물에 갇힘 — 속박·관재·답답함.',a:'의료·법무·수사·종교 등 활인업엔 오히려 길.'},
 현침살:{b:'바늘처럼 예리함. 구설·날선 말 주의.',a:'침·의술·기술·비평 등 정밀함이 필요한 일엔 길.'},
 자유귀문:{b:'子(물)와 酉(금)의 만남. 신경이 가장 날카로운 축에 속해요.',a:'예민함을 연구·분석·기획으로 쓰면 강점. 충분한 휴식이 약입니다.',d:'머리가 비상하고 직관이 예리해 통찰력이 뛰어나지만, 완벽주의·결벽 성향에 잔걱정과 의심이 많아요. 밤에 생각이 꼬리를 물어 잠을 설치기도 합니다.',w:'가을·겨울에 나서 금수 기운이 강하거나, 운에서 子가 午에·酉가 卯에 충을 맞을 때 예민함이 크게 올라옵니다.'},
 축오귀문:{b:'丑(흙)과 午(불)의 만남. 속으로 화가 끓는 타입이에요.',a:'명상·종교·심리·상담 분야로 풀면 좋아요. 화를 쌓아두지 마세요.',d:'겉으론 차분해 보여도 속으로 울화가 끓어요. 종교·신앙심이 깊고, 참고 참다가 한 번에 폭발하는 기질과 강한 인내가 함께 있습니다.',w:'화·토 기운이 강하거나, 운에서 午가 子충·丑이 未충을 맞고 스트레스가 쌓일 때 발현돼요.'},
 인미귀문:{b:'寅(나무)과 未(흙)의 만남. 자존심과 몰입이 강해요.',a:'몰입력을 한 분야의 전문성으로. 과몰입(집착)은 경계하세요.',d:'자존심과 고집이 강하고 예술적 감수성·몽상 기질이 있어요. 한 가지에 깊이 빠지는 몰입(집착)이 특징입니다.',w:'봄철 목 기운이 강하거나, 운에서 寅이 申충·未가 丑충을 받을 때 두드러져요.'},
 묘신귀문:{b:'卯(나무)와 申(금)이 부딪히는 조합. 예민함과 공격성이 함께 있어요.',a:'손재주·기술·정밀한 일에 길. 규칙적 생활로 신경을 다스리세요.',d:'나무와 금이 서로 부딪쳐 신경질·변덕이 날 수 있지만, 손재주와 기술적 직감이 뛰어나요. 날카로운 분석력이 강점입니다.',w:'금과 목이 서로 강해 부딪칠 때, 운에서 卯酉충·寅申충이 들 때 신경이 곤두서요.'},
 진해귀문:{b:'辰(흙)과 亥(물)의 만남. 여섯 귀문 중 영적 감수성이 가장 강해요.',a:'예지·상상력을 창작·종교·역학·상담으로. 현실도피·우울은 경계.',d:'상상력과 예지력(촉)이 뛰어나고 영적·종교적 감수성이 깊어요. 다만 현실도피·우울감으로 흐르기 쉬워 마음 관리가 필요합니다.',w:'수 기운이 강하거나 화개·인성과 겹칠 때, 운에서 辰戌충·巳亥충이 들 때 깊어져요.'},
 사술귀문:{b:'巳(불)와 戌(흙)의 만남. 의심·집착·추진력이 강해요.',a:'몰입과 추진력을 목표 달성에. 질투·의심은 스스로 다독이세요.',d:'의심·질투·집착이 강하고 속을 잘 안 보이는 비밀스러운 타입이지만, 한번 마음먹으면 강한 추진력을 보입니다.',w:'화 기운이 강하거나, 운에서 巳가 亥충·辰戌충이 들 때 집착·예민함이 커져요.'},
 재고귀인:{g:'재물 창고. 부를 모으고 지키는 복.',a:'저축·부동산·자산관리에 강점.'},
 천주귀인:{g:'식록(食祿). 먹을 복·생활의 안정.',a:'의식주·요식·복지 분야와 인연.'},
 복성귀인:{g:'복록·행운의 별.',a:'낙천적 태도가 복을 키웁니다.'},
 금여:{g:'금수레. 안락·좋은 배우자·후반 영화.',a:'배우자·가정의 덕이 큽니다.'},
 암록:{g:'숨은 복록. 드러나지 않는 귀인의 도움.',a:'보이지 않는 곳에서 도움이 옵니다.'},
 태극귀인:{g:'총명·집중. 시작과 끝을 보는 통찰.',a:'한 분야를 깊이 파면 대성.'},
 학당귀인:{g:'학문·총명·시험운.',a:'학업·연구·교육 분야에 길.'},
 협록:{g:'좌우에서 록을 끼는 든든한 재록.',a:'주변의 협력으로 재물이 안정됩니다.'},
 관귀학관:{g:'학문으로 얻는 관운·승진.',a:'공부가 곧 승진. 자격·시험에 길.'},
 문곡귀인:{g:'문장·예술·지혜의 별.',a:'글·예술·기획으로 빛납니다.'},
 탕화살:{b:'화상·화재·끓는 물 등 사고수.',a:'불·뜨거운 것 취급에 각별히 주의.'},
 목:{b:'木 기운이 과다합니다(자존·고집·확장욕).',a:'설기(식상)·다스림(금)으로 균형을.'},
 화:{b:'火 기운이 과다합니다(열정·조급·과시).',a:'수(水)로 식히고 차분함을 더하세요.'},
 토:{b:'土 기운이 과다합니다(고집·정체).',a:'목(木)으로 소토(疏土), 변화를 주세요.'},
 금:{b:'金 기운이 과다합니다(예리·강경).',a:'화(火)로 단련, 부드러움을 더하세요.'},
 수:{b:'水 기운이 과다합니다(다재·산만).',a:'토(土)로 제방, 집중을 만드세요.'}
};

/* ===== 운→궁→십성→주체 (3차 좁힘) ===== */
function gtype(k,which){
  if(k==='day')return which==='z'?'배우자':'내면';
  if(k==='month')return which==='z'?'가정기반':'가치관';
  if(k==='hour')return which==='z'?'실제자녀':'미래자녀';
  if(k==='year')return which==='z'?'뿌리':'사회상';
  return '내면';
}
const SUBJW={};
const SIPSIN_DOM={정재:'재물·아내',편재:'사업·이성·부친',정관:'직장·명예·남편',편관:'압박·도전·질병',정인:'문서·학업·모친',편인:'기술·종교·눈치',식신:'표현·먹을복·자녀',상관:'재능·구설·자녀',비견:'동료·독립',겁재:'경쟁·손재'};
const SUBJECT_PLAIN={사회상:'남에게 보이는 나(직업·명예)',뿌리:'어린 시절과 집안(조상·고향)',가치관:'배움과 직업관(원칙·이상)',가정기반:'가정과 부모(생활 기반)',내면:'속마음(생각·자아)',배우자:'나 자신과 배우자(결혼)',미래자녀:'말년과 자녀 계획',실제자녀:'자녀와 노년'};
const GUNG_SHORT={사회상:'사회적 나·명예',뿌리:'어린시절·집안',가치관:'배움·직업관',가정기반:'가정·부모',내면:'속마음',배우자:'나·배우자',미래자녀:'말년·자녀',실제자녀:'자녀·노년'};
const GUNG_EXPLAIN={
 사회상:'집 밖에서 남들에게 보이는 나의 모습이에요. 직업·명예·평판처럼 사회에서 내가 어떤 위치에 있고 어떻게 비치는지를 뜻해요.',
 뿌리:'내가 자라온 바탕이에요. 조상과 고향, 집안 분위기, 그리고 어린 시절에 겪은 환경을 뜻해요.',
 가치관:'내가 무엇을 옳다고 믿고 어떻게 배우며 사는지예요. 공부·원칙·직업관·이상 같은 마음의 기준을 뜻해요.',
 가정기반:'나의 생활 터전이에요. 부모와의 관계, 가정의 분위기, 그리고 일·직업의 바탕을 뜻해요.',
 내면:'겉으로는 잘 안 보이는 내 속마음이에요. 평소의 생각·감정·자아처럼 나만 아는 내면 세계를 뜻해요.',
 배우자:'현실의 나 자신, 그리고 배우자예요. 결혼·연애·가정생활처럼 가장 가까운 사람과의 인연을 뜻해요.',
 미래자녀:'앞으로의 삶과 자녀에 대한 마음이에요. 미래 계획·노년의 모습·자녀에 대한 생각을 뜻해요.',
 실제자녀:'실제 자녀와 노년의 환경이에요. 아랫사람이나 자녀, 그리고 인생 후반의 생활을 뜻해요.'
};
const GUNG_PLACE={사회상:'사회적 이미지·명예 자리',뿌리:'조상·뿌리 자리',가치관:'가치관·직업관 자리',가정기반:'가정·직업 기반 자리',내면:'내면(생각)의 자리',배우자:'현실의 나·배우자 자리',미래자녀:'미래·자녀 자리',실제자녀:'실제 자녀·말년 자리'};
const EVENT_BY_GUNG={
  배우자:{충:['결혼','이혼·별거','배우자 직장·건강 변화','이사·이동'],합:['결혼·새 인연','배우자와 협력'],형:['부부 갈등','배우자 수술수'],파:['관계 균열'],해:['소소한 불화']},
  내면:{충:['생각·가치관의 큰 변화','심리적 동요·결단','이직·이사 결심'],합:['새 관심사·인연','마음의 안정'],형:['내적 갈등·스트레스'],파:['의욕 저하·중단'],해:['잔걱정·번민']},
  가치관:{충:['진로·전공 변화','직업관의 전환','배움의 방향 변화'],합:['새 배움·자격·멘토'],형:['신념 충돌'],파:['계획 변경'],해:['방향 흔들림']},
  가정기반:{충:['이사·가정환경 변화','부모와 거리·갈등','직업 기반 변동'],합:['가정 안정·화목','직업 기반 강화'],형:['가족 마찰'],파:['기반 흔들림'],해:['집안 잔걱정']},
  사회상:{충:['사회적 평판·직위 변동','직장·명예의 변화','이미지 쇄신'],합:['평판 상승·인정','대외 인연'],형:['구설·시비'],파:['평판 손상'],해:['평판 잔걱정']},
  뿌리:{충:['고향·터전 변화','집안·조상 관련 일','이사'],합:['집안 경사·뿌리 회복'],형:['집안 시비'],파:['터전 이탈'],해:['뿌리 관련 잔일']},
  미래자녀:{충:['자녀 계획·진로 고민','말년 계획 변화'],합:['임신·자녀 경사 기대'],형:['자녀 걱정'],파:['계획 변경'],해:['잔걱정']},
  실제자녀:{충:['출산','자녀 진학·독립','말년 환경 변화'],합:['임신·자녀 경사'],형:['자녀와 갈등·수술수'],파:['자녀 문제'],해:['자녀 잔병']}
};
const PRED_REL={
  충:'두 기운이 정면으로 부딪히는 「충」이에요. 충은 가깝고 익숙한 것을 끊어내고 자리를 크게 뒤흔드는 힘이라, 일 년 중 변화의 폭이 가장 클 수 있어요.',
  합:'두 기운이 하나로 묶이는 「합」이에요. 새로운 인연·결합이 생기거나, 반대로 기존의 것이 묶여 제 역할을 못 하고 흐려지기도 해요.',
  형:'서로 어긋나 부대끼는 「형」이에요. 갈등·시비·관재(법적 문제)나 수술 같은 마찰이 따라올 수 있어요.',
  파:'관계나 일이 깨지는 「파」예요. 진행되던 것이 중단되거나 틀어질 수 있어요.',
  해:'은근히 발목을 잡는 「해」예요. 눈에 잘 안 띄게 일이 더디고 거슬립니다.'
};
const PRED_GUNG={
  배우자:{충:'연인·배우자나 가장 가까운 사람과의 관계가 크게 흔들릴 수 있어요. 다툼·이별·배우자의 건강 문제로 이어지거나, 반대로 결혼·동거처럼 한 매듭을 짓는 변화가 올 수도 있어요. 정들었던 가까운 존재(가족·반려동물 포함)와의 이별·사별 같은 상실을 겪을 가능성도 조심스럽게 봅니다.',합:'새 인연·결혼·동거처럼 관계가 묶이는 일이 생길 수 있어요. 다만 너무 얽매여 답답해질 수도 있어요.',형:'부부·연인 사이 갈등이나 배우자의 수술·건강 문제가 생길 수 있어요.',파:'가까운 관계에 금이 가거나 정리될 수 있어요.',해:'사소한 서운함·불화가 쌓일 수 있어요.'},
  내면:{충:'마음 깊은 곳이 흔들려 가치관·진로가 바뀌거나, 정든 것(사람·반려동물·오래된 일)을 떠나보내는 상실감을 겪을 수 있어요. 우울·번민이 깊어질 수 있으니 마음을 돌보는 시기로 삼으세요.',합:'새로운 관심사·신념이 생기거나 마음이 한쪽으로 묶일 수 있어요.',형:'내적 갈등·스트레스가 커질 수 있어요.',파:'의욕이 꺾이거나 하던 마음을 접게 될 수 있어요.',해:'잔걱정·번민이 늘 수 있어요.'},
  가정기반:{충:'집·가정환경이 흔들려 이사·가족 갈등·부모님 건강 같은 일이 생길 수 있어요.',합:'가정이 안정되거나 새 식구·기반이 생길 수 있어요.',형:'가족과의 마찰·시비가 있을 수 있어요.',파:'가정 기반에 균열이 생길 수 있어요.',해:'집안에 잔걱정이 생길 수 있어요.'},
  사회상:{충:'직장·사회적 위치가 흔들려 이직·평판 변동·구설이 생길 수 있어요.',합:'평판이 오르거나 좋은 대외 인연이 생길 수 있어요.',형:'구설·시비·관재가 따를 수 있어요.',파:'평판·지위에 손상이 올 수 있어요.',해:'평판에 잔잡음이 생길 수 있어요.'},
  가치관:{충:'진로·전공·직업관이 크게 바뀔 수 있어요. 배우던 길을 바꾸거나 새 길을 찾게 될 수 있어요.',합:'새 배움·멘토·자격과 인연이 생길 수 있어요.',형:'신념 충돌이 생길 수 있어요.',파:'세웠던 계획이 틀어질 수 있어요.',해:'방향이 흔들릴 수 있어요.'},
  뿌리:{충:'고향·터전·집안 관련 변화(이사·조상 일)가 생길 수 있어요.',합:'집안 경사나 뿌리와의 인연이 깊어질 수 있어요.',형:'집안 시비가 생길 수 있어요.',파:'터전을 떠나게 될 수 있어요.',해:'뿌리 관련 잔일이 생길 수 있어요.'},
  미래자녀:{충:'자녀 계획·진로나 말년 설계가 크게 바뀔 수 있어요.',합:'임신·자녀 경사를 기대할 수 있어요.',형:'자녀 걱정이 생길 수 있어요.',파:'계획이 변경될 수 있어요.',해:'잔걱정이 생길 수 있어요.'},
  실제자녀:{충:'출산·자녀 진학·독립처럼 자녀와 관련된 큰 변화나, 말년 환경의 변화가 생길 수 있어요.',합:'임신·자녀 경사가 있을 수 있어요.',형:'자녀와의 갈등·수술수가 있을 수 있어요.',파:'자녀 문제가 생길 수 있어요.',해:'자녀 잔병치레가 있을 수 있어요.'}
};
const SS_PRED={정관:'직장·명예·법·책임',편관:'갑작스러운 압박·사고·질병·이별',정재:'돈·재물·이성',편재:'사업·큰돈·이성',정인:'문서·공부·계약·돌봄',편인:'기술·종교·예민함',식신:'표현·먹을복·자녀',상관:'재능·구설·자녀',비견:'경쟁·동료·지출',겁재:'경쟁·손재·동업'};
function predictSection(gi){
  const action=(gi.type.indexOf('합')>=0)?'합':gi.type;
  const relP=PRED_REL[action]||'';
  const gp=(PRED_GUNG[gi.gt]&&PRED_GUNG[gi.gt][action])||'';
  const events=(EVENT_BY_GUNG[gi.gt]&&EVENT_BY_GUNG[gi.gt][action])||[];
  const ssf=SS_PRED[gi.ss]?('들어온 기운이 <b>'+SS_PRED[gi.ss]+'</b> 쪽이라, 변화도 그 분야에서 나타나기 쉬워요.'):'';
  const shock=((gi.ss==='편관'||gi.origSs==='편관')&&action==='충')?'<br><br>특히 편관(칠살)의 충은 갑작스러운 사고·질병·이별처럼 강한 충격으로 올 수 있으니, 이 시기엔 건강과 안전을 한 번 더 챙기고 무리한 결정은 미루는 게 좋아요.':'';
  let body=relP+'<br><br>'+gp+(ssf?'<br><br>'+ssf:'')+shock;
  if(events.length)body+='<br><br><b>구체적으로는</b> — '+events.join(' · ');
  body+='<br><br><span style="color:var(--sub)">— 당연히 틀릴 수도 있어요. 어디까지나 「이런 일이 생길 가능성도 있겠다」 하고 미리 짚어, 좋은 건 키우고 나쁜 건 대비하려는 거예요.</span>';
  return L('🔮 이 시기, 조심스럽게 예상해보면',body);
}
function luckGlyphInfo(r){
  if(r.tri)return null;
  const lk=LUCKKEYS.includes(r.ki)?r.ki:(LUCKKEYS.includes(r.kj)?r.kj:null);if(!lk)return null;
  const ok=(lk===r.ki)?r.kj:r.ki;if(LUCKKEYS.includes(ok))return null;
  const dg=CUR.s.dGan,which=r.which;
  const luckChar=(which==='g')?CUR.P[lk][0]:HIDDEN[CUR.P[lk][1]][0];
  const origChar=(which==='g')?CUR.P[ok][0]:HIDDEN[CUR.P[ok][1]][0];
  return {lk,ok,which,luckChar,ss:sipsin(dg,luckChar),origChar,origSs:sipsin(dg,origChar),gt:gtype(ok,which),type:r.type};
}
function gungReport(gi){
  const subj=SUBJW[gi.gt]||gi.gt,dom=SIPSIN_DOM[gi.ss]||'';
  const action=(gi.type.indexOf('합')>=0)?'합':gi.type;
  const events=(EVENT_BY_GUNG[gi.gt]&&EVENT_BY_GUNG[gi.gt][action])||['변화·움직임'];
  const core=subj+(gi.ss?(' + '+dom.split('·')[0]+'('+gi.ss+')'):'');
  return {subj,action,t2:(gi.ss?gi.ss+' → '+dom:'-'),t3:events,core};
}
/* 쉬운 말 사전 (사주 용어를 몰라도 이해되게) */
const SIPSIN_PLAIN={
  정재:{label:'꾸준한 돈·안정',desc:'성실하게 모으는 돈과 안정된 재산을 뜻해요. 남자에게는 아내를 의미하기도 해요.'},
  편재:{label:'큰 돈·사업·인기',desc:'크게 들어왔다 나가는 돈, 사업·투자 기질이에요. 이성에게 인기가 많고 아버지를 뜻하기도 해요.'},
  정관:{label:'직장·명예·책임',desc:'직장과 명예, 규칙을 잘 지키는 반듯한 기운이에요. 여자에게는 남편을 의미하기도 해요.'},
  편관:{label:'압박·도전·경쟁',desc:'강한 압박과 도전, 권력욕이에요. 잘 다스리면 큰 힘이지만 스트레스·건강을 조심해야 해요.'},
  정인:{label:'공부·문서·돌봄',desc:'공부, 자격증, 계약 같은 문서운이에요. 어머니의 보살핌처럼 나를 도와주는 기운이에요.'},
  편인:{label:'아이디어·기술·눈치',desc:'특이한 재주와 기술, 종교적 관심이에요. 임기응변과 눈치가 빠른 기운이에요.'},
  식신:{label:'표현·먹을복·여유',desc:'맛있게 먹고 즐기는 여유와 표현력이에요. 여자에게는 자녀를 뜻하기도 해요.'},
  상관:{label:'재능·말솜씨·끼',desc:'톡톡 튀는 재능과 말솜씨, 끼가 있어요. 자유로워서 규칙은 답답해하고, 말로 인한 구설을 조심해요.'},
  비견:{label:'친구·독립·고집',desc:'나와 비슷한 친구·형제·경쟁자예요. 독립심이 강하고 고집이 있어요.'},
  겁재:{label:'경쟁·욕심·지출',desc:'강한 경쟁심과 욕심이에요. 돈이 새어나가기 쉬우니 지출을 조심해야 해요.'}
};
const RELATION_PLAIN={
  충:{label:'세게 흔듦',verb:'정면으로 부딪쳐서',desc:'두 기운이 정면충돌해서 그 영역에 큰 변화·이동·다툼·이별 같은 흔들림이 생겨요. 좋게 풀리면 새 출발, 나쁘게 풀리면 충돌이에요.'},
  합:{label:'끌어당겨 묶음',verb:'서로 끌어당겨 묶이면서',desc:'두 기운이 만나 하나로 묶여요. 인연·만남·협력이 생기지만, 너무 묶이면 제 역할을 못 해서 오히려 약해지기도 해요.'},
  형:{label:'어긋나 마찰',verb:'서로 어긋나 부대끼면서',desc:'서로 부대끼며 갈등·구설·법적 문제(관재)나 수술 같은 일이 생길 수 있어요.'},
  파:{label:'깨뜨림',verb:'관계가 깨지면서',desc:'진행되던 일이 깨지거나 중단되고, 관계가 틀어질 수 있어요.'},
  해:{label:'은근히 방해',verb:'은근히 방해를 받으면서',desc:'눈에 잘 띄진 않지만 일이 더디고 거슬리며 잔걱정이 생겨요.'}
};
function luckPeriodLabel(lk){if(lk==='se')return (SELSE?SELSE.Y+'년':'그 해')+' 운';if(lk==='dae')return '대운('+(SELDAE?Math.round(SELDAE.age)+'세 무렵':'')+')';if(lk==='wol')return (SELWOL?SELWOL.label:'그 달')+' 운';return '운';}
function buildPlain(gi,sc){
  const sp=SIPSIN_PLAIN[gi.ss]||{label:gi.ss||'기운',desc:''};
  const osp=SIPSIN_PLAIN[gi.origSs]||{label:gi.origSs||'',desc:''};
  const subj=GUNG_SHORT[gi.gt]||SUBJECT_PLAIN[gi.gt]||gi.gt, place=GUNG_PLACE[gi.gt]||(subj+' 자리');
  const action=(gi.type.indexOf('합')>=0)?'합':gi.type;
  const rel=RELATION_PLAIN[action]||{label:gi.type,verb:gi.type,desc:''};
  const fav=sc>0?'좋은 쪽으로 풀릴 가능성이 큰':(sc<0?'조금 조심해야 할':'크고 작은');
  const period=luckPeriodLabel(gi.lk);
  const same=!!(gi.origSs && gi.origSs===gi.ss);
  const para=period+'에 들어온 「'+gi.luckChar+'」('+sp.label+') 기운이, '+(same?'':'원래 「'+gi.origChar+'」('+(gi.origSs||'')+'·'+osp.label+')에 해당하는 ')+'당신의 <b>'+place+'</b>와 '+rel.verb+', 그 영역에 '+fav+' 변화가 생길 수 있어요.';
  let h='<h3 style="margin-bottom:4px">'+period+'이 「'+subj+'」을(를) '+rel.label+'</h3>'
    +'<div class="meta">들어온 글자 <b>'+gi.luckChar+'</b>('+(gi.ss||'')+') · 건드려진 글자 <b>'+gi.origChar+'</b>('+(gi.origSs||'')+') · 작용 <b>'+rel.label+'</b>('+gi.type+')</div>'
    +'<p style="margin:7px 0;line-height:1.75">'+para+'</p>'
    +L('① 어디에 영향이 올까요?','<b>'+subj+'</b> 자리예요.<br>'+(GUNG_EXPLAIN[gi.gt]||''));
  if(same)h+=L('② 어떤 기운이 작용하나요?','이 자리(「'+gi.origChar+'」)도, 들어온 기운(「'+gi.luckChar+'」)도 모두 <b>'+sp.label+'('+gi.ss+')</b>예요. 같은 기운이 겹쳐서 그 성질이 평소보다 훨씬 강하게 드러나요.<br>· '+sp.desc);
  else h+=L('② 그 자리의 원래 성격','「'+gi.origChar+'」('+(gi.origSs||'-')+') — '+osp.label+(osp.desc?': '+osp.desc:''))
        +L('③ 들어온 기운','「'+gi.luckChar+'」('+(gi.ss||'')+') — '+sp.label+': '+sp.desc);
  h+=L('④ 어떻게 작용하나요?',rel.label+' — '+rel.desc);
  h+=predictSection(gi);
  h+='<div class="line" style="color:var(--sub);font-size:11.5px;margin-top:8px">※ 사주는 정해진 운명이 아니라 기운의 흐름이에요. 위 예상은 미리 알고 대비하려는 참고용이며, 상황과 선택에 따라 얼마든지 달라집니다.</div>';
  return h;
}
/* 고전 근거 (saju_full.db에서 추출, 쉬운 톤으로 안내) */
const REFKEY={천을귀인:'천을귀인',양인:'양인',백호:'백호',괴강:'괴강',도화:'도화',화개:'화개',공망:'공망',문창귀인:'문창',건록:'건록',천덕귀인:'천덕',월덕귀인:'월덕',원진:'원진',현침살:'현침',겁살:'겁살',재살:'재살',망신살:'망신',장성살:'장성',반안살:'반안',육해살:'육해',편관칠살:'칠살',홍염살:'홍염',진역마:'역마',살역마:'역마',자유귀문:'귀문',축오귀문:'귀문',인미귀문:'귀문',묘신귀문:'귀문',진해귀문:'귀문',사술귀문:'귀문',정관:'정관',편관:'편관',정재:'정재',편재:'편재',정인:'정인',편인:'편인',식신:'식신',상관:'상관',비견:'비견',겁재:'겁재'};
const REF_PLAIN={귀문:'예민함·직감·집착을 다룬 대목이에요.',도화:'매력·이성운(끼)을 다룬 대목이에요.',역마:'이동·여행·변동을 다룬 대목이에요.',칠살:'강한 압박·도전(칠살)을 다룬 대목이에요.',양인:'지나치게 강한 칼날 기운을 다룬 대목이에요.',백호:'피·사고와 관련된 강한 기운을 다룬 대목이에요.',괴강:'극단적 카리스마를 다룬 대목이에요.',천을귀인:'최고의 귀인(도움)을 다룬 대목이에요.',화개:'예술·종교·고독의 별을 다룬 대목이에요.',정관:'직장·명예·책임을 다룬 대목이에요.',편관:'압박·도전(칠살)을 다룬 대목이에요.',정재:'안정적 재물을 다룬 대목이에요.',편재:'사업·큰 재물을 다룬 대목이에요.',정인:'공부·문서·돌봄을 다룬 대목이에요.',식신:'표현·먹을복을 다룬 대목이에요.',상관:'재능·끼·구설을 다룬 대목이에요.'};
function toggleRef(el){el.classList.toggle('open');}
function refsHtml(kw){const arr=REFS[kw];if(!arr||!arr.length)return '';
  let h='<div class="refsec"><div class="reftitle">📜 옛 명리책은 이렇게 말해요'+(REF_PLAIN[kw]?' <span style="font-weight:400;color:var(--sub)">— '+REF_PLAIN[kw]+'</span>':'')+'</div>';
  arr.forEach(r=>{h+='<div class="refitem" onclick="toggleRef(this)"><div class="refhead">〔'+r.book+'〕 '+r.title+' <span class="refmore">눌러서 펼치기 ▾</span></div><div class="refsnip">'+r.snippet+'…</div><div class="reffull">'+r.full+'</div></div>';});
  return h+'</div>';
}

/* ===== 캐릭터 클릭 상세 설명 (길고 쉽게) ===== */
function L(t,b){return '<div class="line" style="line-height:1.75;margin:5px 0"><b>'+t+'</b><br>'+b+'</div>';}
const ELEM_INFO={
  木:{n:'나무처럼 위로 뻗어 자라는 기운',mind:'인정이 많고 자존심·명예욕이 있어요. 한번 정하면 곧게 밀고 나가는 추진력이 생겨요.',life:'새 시작·성장·교육·기획 같은 일, 명예와 관련된 변화'},
  火:{n:'불처럼 밝고 뜨거운 기운',mind:'밝고 적극적이며 표현력이 좋아져요. 다만 조급함·감정 기복이 커질 수 있어요.',life:'발표·홍보·예술·인기와 관련된 일, 감정 변화로 인한 사건'},
  土:{n:'흙처럼 듬직하고 안정된 기운',mind:'믿음직하고 끈기·포용력이 커져요. 다만 고집스럽거나 정체될 수 있어요.',life:'부동산·중개·관리처럼 신뢰가 필요한 일, 터전·이사 관련 변화'},
  金:{n:'쇠처럼 단단하고 결단력 있는 기운',mind:'분명하고 결단력이 강해지며 의리·원칙을 중시해요. 날카로워 부딪힐 수도 있어요.',life:'금융·기계·의료(수술)·법·군경처럼 정밀·결단이 필요한 일, 돈·계약 변화'},
  水:{n:'물처럼 지혜롭고 흐르는 기운',mind:'머리가 잘 돌고 융통성·적응력이 좋아져요. 다만 생각이 많아 산만해질 수 있어요.',life:'연구·교육·유통·해외·정보와 관련된 일, 이동·변동'},
};
function relKind(e,d){if(e===d)return '비겁';if(SHENG[e]===d)return '인성';if(SHENG[d]===e)return '식상';if(KE[e]===d)return '관성';if(KE[d]===e)return '재성';return '';}
const REL_INFO={
  비겁:{label:'비겁(나와 같은 편·경쟁)',mind:'독립심·경쟁심·자기 주장이 강해져요.',good:'동업·협업·경쟁 환경에서 내 주관과 추진력을 살리면 좋아요. 형제·동료·동기의 힘을 빌려 함께 밀어붙이세요.',bad:'친구·동업·보증으로 돈이 새기 쉽고, 고집으로 충돌해요. 금전 거래와 보증을 피하고, 한 발 양보하는 연습을 하세요.'},
  인성:{label:'인성(나를 도와주는 기운)',mind:'배우려는 마음과 안정감이 커지고 받아들이는 태도가 생겨요.',good:'공부·자격증·문서·계약에 길해요. 지금 배우고 자격을 갖추면 그게 곧 기회가 됩니다. 윗사람·어머니의 도움을 적극 받으세요.',bad:'생각만 많고 실행이 느려질 수 있어요. 의존·게으름을 경계하고, 배운 것을 바로 실전에 옮기세요.'},
  식상:{label:'식상(내가 내보내는 표현)',mind:'표현하고 싶고 활동적·자유로워져요.',good:'창작·발표·강의·SNS·새 시도에 길해요. 머릿속 아이디어와 끼를 밖으로 꺼내 보여주세요. (여성은 자녀운과도 연결)',bad:'말이 많아 구설이 생기거나 일만 벌일 수 있어요. 말조심하고 시작한 일은 끝맺음에 신경 쓰세요.'},
  재성:{label:'재성(내가 다스리는 재물)',mind:'현실적·계산적이 되고 성취욕·소유욕이 커져요.',good:'재물·사업·실리에 길해요. 현실 감각을 살려 돈 되는 일에 집중하고 부지런히 움직이면 결실이 커요. (남성은 이성·결혼운과도 연결)',bad:'욕심·과로·이성 문제로 탈이 나기 쉬워요. 무리한 투자·확장·보증을 자제하고 건강과 관계를 함께 챙기세요.'},
  관성:{label:'관성(나를 누르는 책임)',mind:'책임감·긴장이 커지고 규칙을 의식하게 돼요.',good:'직장·승진·명예·시험·자격에 길해요. 책임 있는 자리를 맡고 규칙을 지키면 인정받아요. (여성은 남편운과도 연결)',bad:'압박·스트레스·관재(법적 문제)가 생길 수 있어요. 과로와 상사와의 충돌을 피하고 스트레스 관리를 하세요.'},
};
const GAN_PERSON={甲:'큰 나무처럼 곧고 리더십이 있으며 명예를 중시',乙:'풀·넝쿨처럼 유연하고 끈질기며 현실 적응이 빠른',丙:'태양처럼 밝고 적극적이며 표현이 분명한',丁:'촛불처럼 따뜻하고 섬세하며 헌신적인',戊:'큰 산처럼 믿음직하고 포용력이 큰',己:'기름진 논밭처럼 자상하고 실속 있는',庚:'무쇠처럼 강직하고 의리 있으며 결단력 있는',辛:'보석처럼 예민하고 깔끔하며 자존심이 강한',壬:'큰 물처럼 지혜롭고 포부가 크며 활동적인',癸:'이슬·비처럼 섬세하고 상상력이 풍부하며 부드러운'};
const ZHI_TRAIT={子:'영리하고 부지런하며 적응력이 좋',丑:'성실하고 끈기 있게 묵묵히 밀고 가',寅:'용맹하고 자존심이 강한 리더 기질의',卯:'온순하고 섬세하며 사교적인',辰:'포부가 크고 변화를 즐기며 카리스마 있는',巳:'지혜롭고 집중력이 강하며 신비로운',午:'활발하고 정열적이며 표현이 분명한',未:'온화하고 예술적이며 인정이 많은',申:'재주가 많고 임기응변에 능한',酉:'깔끔하고 분명하며 자기 관리가 철저한',戌:'의리 있고 충직하며 정의감이 강한',亥:'순수하고 베풀기 좋아하며 낙천적인'};
function subjOfTarget(t){if(LUCKKEYS.includes(t.k))return t.k==='dae'?'대운(그 시기)':t.k==='se'?'세운(그 해)':'월운(그 달)';return SUBJECT_PLAIN[gtype(t.k,t.which)]||'';}
function gungAffectLine(c){const subs=[...new Set((c.targets||[]).map(subjOfTarget))].filter(Boolean);if(!subs.length)return '';return L('📍 지금 어디에 작용하나요?','당신의 <b>'+subs.join('</b>, <b>')+'</b> 자리에 영향을 줍니다.');}
function roleLifeMind(c){const r=c.role;
  if(r==='길신'||r==='길')return {life:'귀인의 도움이나 기회가 생기고, 막혔던 일이 풀리는 계기가 될 수 있어요.',mind:'마음이 편안해지고 긍정적·적극적으로 바뀌어요.'};
  if(r==='흉신'||r==='흉')return {life:'그 영역에서 변동·다툼·건강·손실 같은 일을 조심해야 해요.',mind:'예민해지거나 욕심·고집·불안이 커질 수 있어요.'};
  return {life:'쓰기에 따라 기회도 위기도 되는 일이 생겨요.',mind:'끼·매력·개성이 강해지지만 스스로 조절이 필요해요.'};}
const SS_RICH={
 천을귀인:{good:'어려울 때 윗사람·선배·귀인의 도움으로 풀려요. 평소 사람에게 진심으로 잘하고, 결정적일 때 도움을 청하세요. 면접·청탁·협상·인맥이 필요한 일에 적극 나서면 길합니다.',bad:'귀인을 믿고 노력을 게을리하면 복이 새요. 또 내가 베푼 만큼 돌아오니, 받기만 하려 들면 도움이 끊깁니다. 인간관계를 소홀히 하지 마세요.',mind:'사람을 믿고 의지하며 도움을 주고받는 여유가 생겨요.'},
 천덕귀인:{good:'위기에서 한 박자 늦게라도 보호받아요. 선행·기부·봉사·종교 활동의 덕이 실제로 나를 지켜줍니다. 결정 앞에서 양심대로 고르면 길로 풀려요.',bad:'덕을 믿고 막행동하면 보호막이 약해져요. 화나도 모질게 굴지 말고 베풂을 멈추지 마세요.',mind:'너그럽고 차분해져 손해 봐도 크게 흔들리지 않아요.'},
 월덕귀인:{good:'온화한 인덕으로 어려움이 부드럽게 풀려요. 급할수록 사람과의 관계로 풀고, 베풂을 이어가세요.',bad:'기대어 안주하면 복이 줄어요. 인덕에만 의지 말고 스스로 실력을 갖추세요.',mind:'마음이 편안하고 둥글어져요.'},
 문창귀인:{good:'시험·자격증·발표처럼 머리 쓰는 일에서 결과가 잘 나와요. 공부·연구·글쓰기·기획에 시간을 투자하면 곧 성과·승진이 됩니다. 자기계발·시험 도전이 길한 시기예요.',bad:'머리만 믿고 실행을 미루면 기회를 놓쳐요. 아는 것을 글·자격·실적으로 증명해두세요.',mind:'배우고 정리하려는 의욕과 호기심이 커져요.'},
 학당귀인:{good:'학업·연구·교육·시험에 길해요. 한 분야를 깊이 공부하면 전문가로 인정받습니다.',bad:'이론에만 머물면 현실과 멀어져요. 배운 것을 실전·실적으로 연결하세요.',mind:'탐구심과 집중력이 커져요.'},
 문곡귀인:{good:'문장·예술·기획·아이디어로 빛나요. 글·콘텐츠·창작·전략 분야에 적극 도전하세요.',bad:'재능을 펼치지 않으면 공상으로 끝나요. 결과물로 남기세요.',mind:'감수성과 표현욕이 풍부해져요.'},
 관귀학관:{good:'공부가 곧 승진·관운으로 이어져요. 자격·시험·학위를 갖춰 그 분야의 자리에 오르세요.',bad:'준비 없이 자리만 욕심내면 탈이 나요. 실력부터 갖추세요.',mind:'성취욕과 학구열이 함께 커져요.'},
 건록:{good:'자기 힘으로 버는 안정된 자리·재록이 생겨요. 한 우물을 꾸준히 파고 성실하게 일하면 차곡차곡 쌓입니다. 무리한 투기보다 꾸준함이 답이에요.',bad:'안정에 안주해 도전을 미루면 정체돼요. 또 비겁 기운이라 동업·보증으로 돈이 샐 수 있으니 금전 관리를 챙기세요.',mind:'독립심과 책임감, 현실 감각이 커져요.'},
 재고귀인:{good:'재물을 모으고 지키는 복이에요. 저축·부동산·자산관리에 집중하면 곳간이 채워집니다.',bad:'욕심내 무리하게 굴리면 오히려 새요. 안전한 자산 위주로 지키세요.',mind:'저축·소유 욕구와 현실 감각이 커져요.'},
 천주귀인:{good:'먹을 복·생활의 안정이 따라요. 의식주·요식·복지·식품 분야와 인연이 좋아요.',bad:'편안함에 빠져 게을러질 수 있어요. 여유를 즐기되 본업을 놓지 마세요.',mind:'여유롭고 낙천적으로 바뀌어요.'},
 복성귀인:{good:'낙천적 태도가 복을 키워요. 긍정적으로 사람을 대하면 기회가 모입니다.',bad:'운만 믿고 대충 하면 복이 흩어져요. 성실함을 더하세요.',mind:'밝고 느긋한 마음이 생겨요.'},
 금여:{good:'좋은 배우자·안락한 가정·후반 영화의 복이에요. 가정과 배우자에게 정성을 들이면 그 덕을 크게 봅니다.',bad:'안락에 안주해 노력을 멈추면 복이 줄어요. 관계에 정성을 이어가세요.',mind:'가정·안정을 중시하는 마음이 커져요.'},
 암록:{good:'드러나지 않는 곳에서 도움이 와요. 평소 덕을 쌓아두면 위기에 숨은 귀인이 나타납니다.',bad:'복이 은밀해 못 알아챌 수 있어요. 주변의 작은 도움도 감사히 받으세요.',mind:'속 깊고 차분한 면이 생겨요.'},
 태극귀인:{good:'총명함과 집중력으로 한 분야를 깊이 파면 대성해요. 전문·연구·역학 분야에 길합니다.',bad:'한쪽으로 치우치면 외골수가 돼요. 균형을 의식하세요.',mind:'몰입력과 통찰이 깊어져요.'},
 협록:{good:'주변의 협력으로 재물이 안정돼요. 사람들과 힘을 합치면 든든한 기반이 생깁니다.',bad:'기대다 보면 의존이 될 수 있어요. 내 몫의 책임도 다하세요.',mind:'협력·신뢰를 중시하게 돼요.'},
 편관칠살:{good:'강한 압박을 동력으로 바꾸면 군경·운동·영업·사업·전문직처럼 강단이 필요한 분야에서 크게 성취해요. 목표·마감·경쟁이 있는 환경에서 더 잘하고, 운동·취미(식신)나 공부(인성)로 스트레스를 풀면 칠살이 권위로 바뀝니다.',bad:'다스리지 못하면 과로·번아웃·관재(법적 문제)·사고·질병으로 터져요. 무리한 일·과음·과격한 언행을 줄이고, 정기 건강검진과 스트레스 관리를 꼭 하세요. 권력자와의 정면충돌은 피하세요.',mind:'책임감·승부욕이 커지지만 긴장·예민함·조급함도 함께 올라와요.'},
 양인:{good:'칼 같은 결단력·집중력을 살려 수술·정밀기술·운동·군경·요리처럼 힘과 정밀함이 필요한 일에 쓰면 최고의 무기가 돼요. 위기에 빠르게 결단하는 자리에 강합니다.',bad:'과격함·욱하는 성질로 사고·다툼·금전 손실·이별이 생겨요. 특히 운에서 양인을 충할 때 사고수가 큽니다. 운전·날카로운 도구·격한 언쟁을 조심하고, 화날 때 잠시 자리를 피하는 습관을 들이세요.',mind:'결단력·승부욕이 강해지지만 인내심이 짧아져요.'},
 백호:{good:'피·칼을 다루는 의료·간호·군경·정육·미용·생명을 살리는 활인업에서 오히려 큰 능력으로 쓰여요. 위급한 상황에 강합니다.',bad:'사고·수술·외상·출혈을 조심해야 해요. 운에서 백호 글자를 충·형할 때 특히 그렇습니다. 운전·작업 안전수칙과 정기검진을 철저히 하고, 위험한 레저·과로를 피하세요.',mind:'위기에 강해지지만 불안·예민함이 커질 수 있어요.'},
 괴강:{good:'강한 카리스마·결단력으로 조직의 우두머리·전문가·1인자 자리에서 빛나요. 분명한 목표와 큰 무대를 주면 대성합니다.',bad:'한번 무너지면 크게 흔들리고, 독선·고집으로 사람을 잃기 쉬워요. 잘나갈 때 겸손과 사람 관리를 챙기고, 극단적 선택을 경계하세요. 운에서 충을 맞을 때 기복이 큽니다.',mind:'자신감·주도성이 강해지지만 타협이 어려워져요.'},
 도화:{good:'사람을 끄는 매력·끼를 연예·예술·서비스·영업·교육·SNS처럼 인기가 곧 돈이 되는 분야에 쓰면 크게 길해요. 호감을 무기로 관계를 넓히세요.',bad:'이성 문제(색난)·구설·삼각관계로 신용을 잃기 쉬워요. 도화가 운에서 합·충될 때 이성 인연이 강해집니다. 공사 구분, 가벼운 처신 자제, 말조심으로 예방하세요.',mind:'사교성·표현욕·이성에 대한 관심이 커져요.'},
 홍염살:{good:'은근한 매력을 예술·서비스·상담·뷰티·연예처럼 사람을 상대하는 일에 쓰면 인기와 호감이 자산이 돼요.',bad:'이성의 인기가 많아 색난·구설·바람기로 신용을 잃을 수 있어요. 공사 구분과 처신을 조심하세요.',mind:'끼·로맨틱한 감수성·이성에 대한 관심이 커져요.'},
 화개:{good:'예술·종교·학문·연구·상담처럼 혼자 깊이 파고드는 분야에서 독보적 재능을 내요. 고독을 창작·수행의 힘으로 바꾸면 길합니다.',bad:'고립·우울·현실도피로 빠지기 쉽고 재물·인간관계엔 약해요. 혼자만의 세계에 갇히지 말고 사람과의 연결·현실 활동을 의식적으로 챙기세요.',mind:'사색적·영적·예술적으로 깊어지지만 외로움을 타요.'},
 공망:{good:'욕심을 내려놓는 쪽으로 쓰면 종교·철학·연구·전문직처럼 정신적 가치를 추구하는 일에 길해요. 그 자리의 집착을 놓으면 마음이 편해집니다.',bad:'해당 자리(재물·배우자·직장 등)의 결실이 약해져요. 그 분야에 큰 기대를 걸면 실망이 큽니다. 대안을 분산해두고 빈 부분은 자기계발·정신적 만족으로 채우세요.',mind:'허무감·초연함이 생기고 물질보다 의미를 찾게 돼요.'},
 진역마:{good:'이동이 곧 발전이에요. 해외·무역·영업·여행·물류·출장처럼 움직이는 일에 적극 나서면 길합니다. 이직·이사·새 환경이 기회가 돼요.',bad:'너무 분주해 정착을 못 하고 산만해질 수 있어요. 중요한 일은 우선순위를 정해 마무리하고, 이동 중 안전·계약을 챙기세요.',mind:'활동적이고 새로운 것을 찾는 마음이 커져요.'},
 살역마:{good:'어쩔 수 없는 이동이라면 미리 계획된 이동(준비된 이직·이사)으로 바꾸면 손해를 줄여요.',bad:'원치 않는 발령·도망·사고로 인한 이동, 분주하지만 실속 없는 헛걸음이 생겨요. 무리한 이동·투자·변동을 자제하고 자리를 지키는 게 이득입니다. 교통·이동 안전을 특히 조심하세요.',mind:'불안정·조급함으로 자꾸 옮기고 싶어져요.'},
 지살:{good:'스스로 환경을 바꾸는 독립·창업·이사·유학에 길해요. 능동적으로 터전을 옮기면 발전합니다.',bad:'잦은 이사·환경 변화로 안정이 깨질 수 있어요. 옮기기 전에 충분히 알아보고 결정하세요.',mind:'독립심·변화 욕구가 커져요.'},
 천살:{good:'내 힘으로 안 되는 일은 겸손히 받아들이고 미리 대비(보험·분산·비상금)하는 지혜로 쓰면 피해를 줄여요.',bad:'천재지변·갑작스러운 변고처럼 통제 밖의 일이 생길 수 있어요. 무리한 확장·과신을 피하고 안전장치를 마련하세요.',mind:'겸손·경외심이 생기지만 무력감이 들 수 있어요.'},
 월살:{good:'메마름의 시기엔 무리한 확장 대신 내실·절약·실력 다지기에 집중하면 다음 기회를 잡아요.',bad:'일이 위축되고 자금·기운이 마릅니다. 큰 투자·확장을 미루고 건강·자금을 비축하세요.',mind:'의욕이 가라앉고 신중해져요.'},
 망신살:{good:'드러남을 좋은 노출(발표·홍보·공개 활동)로 바꾸면 오히려 인지도가 돼요.',bad:'구설·망신·체면 손상이 생기기 쉬워요. 언행·SNS·돈거래·이성 문제를 조심하고, 드러내기보다 신중하게 처신하세요.',mind:'드러내고 싶은 마음과 부끄러움이 함께 와요.'},
 장성살:{good:'권위·통솔의 별이라 팀장·간부·대표·공직처럼 사람을 이끌고 책임지는 자리에서 능력을 발휘해요. 책임 있는 프로젝트를 자청하고 주도권을 잡으세요.',bad:'독선·권위주의로 사람을 누르면 고립되고 적이 생겨요. 혼자 다 하려 말고 경청·위임하세요. 아랫사람·동료를 존중하면 따르는 사람이 늘어납니다.',mind:'주도하려는 욕구와 책임감, 카리스마가 커져요.'},
 반안살:{good:'올라타는 기운이라 승진·발탁·후원받는 시기예요. 윗사람에게 인정받을 기회를 잡고 좋은 자리에 올라타세요.',bad:'안주하거나 윗사람에 지나치게 기대면 실력을 못 키워요. 후원을 발판 삼되 자기 역량도 함께 쌓으세요.',mind:'안정·상승 욕구, 인정받고 싶은 마음이 커져요.'},
 탕화살:{good:'위험을 아는 만큼 안전·예방 전문가(소방·안전관리·요리 등)로 쓰면 강점이 돼요.',bad:'화상·화재·끓는 물·폭발·약물 사고를 조심해야 해요. 불·뜨거운 것·화학물질 취급에 각별히 주의하고, 충동적 음주·약물을 멀리하세요.',mind:'예민하고 욱하는 기질이 올라올 수 있어요.'},
 원진:{good:'까닭 모를 미움은 거리 두기로 다스리면 불필요한 감정 소모를 줄여요. 안 맞는 사람과는 적당히 거리를 두세요.',bad:'특정 사람과 이유 없이 틀어지고 애증·갈등이 생겨요. 감정적으로 엮이지 말고, 예민할 땐 혼자만의 시간으로 풀어내세요.',mind:'예민함·의심·애증의 감정이 커져요.'},
 천라지망:{good:'갇히는 기운을 의료·법무·수사·종교·역학처럼 사람을 묶고 푸는 활인·관리 분야에 쓰면 오히려 길해요.',bad:'관재·구속·답답한 상황에 묶일 수 있어요. 보증·법적 분쟁·위험한 일을 피하고, 답답할수록 규칙을 지켜 처신하세요.',mind:'갇힌 듯 답답하고 신중·내향적으로 변해요.'},
 현침살:{good:'바늘처럼 예리하고 정밀한 감각을 침·한의·외과·치과·미용·디자인·비평·글처럼 정밀함이 필요한 일에 쓰면 발군이에요.',bad:'말이 날카로워 구설·관계 마찰이 생기기 쉬워요. 직설적인 말투를 부드럽게 다듬고, 뾰족한 도구·사고를 조심하세요.',mind:'분석적·비판적으로 예리해져요.'},
 겁살:{good:'빼앗기는 기운을 미리 알고 지키는 데 집중하면 손실을 막아요.',bad:'사기·도난·강제 손실·갑작스러운 지출이 생기기 쉬워요. 보증·투기·과욕을 금하고 계약서·돈 관리를 꼼꼼히 하세요.',mind:'긴장·경계심이 커져요.'},
 재살:{good:'규칙·법을 다루는 일(법무·공직·관리)에 쓰면 오히려 길해요.',bad:'관재·구속·송사·시비에 휘말리기 쉬워요. 계약·법규를 철저히 지키고 다툼·보증·위험한 자리를 피하세요.',mind:'예민하고 방어적으로 변해요.'},
 육해살:{good:'더딘 기운은 느리지만 꾸준히 가는 인내로 쓰면 큰 탈 없이 넘겨요.',bad:'질병·방해·구설로 일이 막히고 더뎌요. 건강을 챙기고 사람과의 갈등·송사를 피하며 무리한 일정을 줄이세요.',mind:'예민해지고 의욕이 떨어질 수 있어요.'},
 문창:{good:'시험·문서·학문에 길해요.',bad:'실행을 미루지 말고 증명하세요.',mind:'배우려는 의욕이 커져요.'}
};
const GUIMUN_RICH={good:'예민함·직감을 연구·상담·예술·종교·의료·역학·기획처럼 촉과 몰입이 필요한 일에 쓰면 남다른 통찰로 빛나요. 떠오르는 직감을 기록·창작으로 남기세요.',bad:'신경과민·집착·불면·의심으로 스스로를 갉아먹을 수 있어요. 규칙적인 수면·운동·명상으로 신경을 다스리고, 한 가지에 과몰입할 땐 의식적으로 거리를 두며, 마음이 힘들면 전문 상담을 받으세요.'};
['자유귀문','축오귀문','인미귀문','묘신귀문','진해귀문','사술귀문'].forEach(k=>{SS_RICH[k]={good:GUIMUN_RICH.good,bad:GUIMUN_RICH.bad,mind:(SS_INFO[k]&&SS_INFO[k].d)||''};});

function shinsalDetail(c){const o=SS_INFO[c.key]||{},r=SS_RICH[c.key]||{},rm=roleLifeMind(c);
  let h='<h3 style="color:'+c.color+'">'+(c.luck?'〔운〕 ':'')+c.name+'</h3>';
  h+='<div class="meta">세기 '+(c.str?c.str.lv:'')+' · '+roleLabel(c.role)+(c.str?' ('+c.str.why+')':'')+'</div>';
  if(o.b)h+='<p style="margin:6px 0;line-height:1.75">'+o.b+'</p>'; else if(o.g)h+='<p style="margin:6px 0;line-height:1.75">'+o.g+'</p>';
  h+=gungAffectLine(c);
  if(o.d)h+=L('📖 자세히 풀면',o.d);
  const good=r.good||o.a||'', bad=r.bad||'', mind=r.mind||o.mind||rm.mind;
  if(good)h+=L('✅ 좋게 쓰려면 (이렇게 하면 길해져요)',good);
  if(bad)h+=L('⚠️ 조심할 일과 예방법',bad); else if(c.role==='흉신'||c.role==='흉')h+=L('⚠️ 조심할 일과 예방법',rm.life);
  if(mind)h+=L('🧠 성향·생각의 변화',mind);
  if(o.w)h+=L('⚡ 이럴 때 강해져요',o.w);
  return h;
}
function spiritDetail(c){const E=c.hanja,ei=ELEM_INFO[E]||{n:'',mind:'',life:''},dw=GAN_WX[CUR.s.dGan],kind=relKind(E,dw),ri=REL_INFO[kind]||{label:kind,mind:'',good:'',bad:''};
  let h='<h3 style="color:'+c.color+'">'+(c.luck?'〔운〕 ':'')+WX_KO[E]+'('+E+') 원소</h3>';
  h+='<div class="meta">'+(c.types?c.types.join('·'):'')+' · 글자 '+(c.branches?c.branches.join(''):'')+' · 세기 '+(c.str?c.str.lv:'')+'</div>';
  h+='<p style="margin:6px 0;line-height:1.75">'+(c.branches?c.branches.join(''):'')+'이(가) 만나 <b>'+WX_KO[E]+'('+E+') 기운</b>이 크게 만들어졌어요. '+ei.n+'이에요.</p>';
  h+=gungAffectLine(c);
  h+=L('↔ 나(일간 '+CUR.s.dGan+')와의 관계',WX_KO[E]+'은(는) 당신에게 <b>'+ri.label+'</b>이에요. '+ri.mind);
  if(ri.good)h+=L('✅ 좋게 쓰려면 (이렇게 하면 길해져요)',ri.good);
  if(ri.bad)h+=L('⚠️ 조심할 일과 예방법',ri.bad);
  h+=L('🧠 성향·생각의 변화',ei.mind+' '+ri.mind);
  h+=L('🌳 이 오행이 어울리는 분야',ei.life);
  return h;
}
function animalDetail(c){const dg=CUR.s.dGan,dw=GAN_WX[dg],dz=CUR.s.pillars.day[1];
  let h='<h3 style="color:'+c.color+'">'+c.name+'</h3>';
  h+='<div class="meta">일간 '+dg+'('+dw+') · 일지 '+dz+'('+ZHI_KO[dz]+')</div>';
  h+='<p style="margin:6px 0;line-height:1.75">사주에서 <b>당신 자신</b>을 상징하는 동물이에요. 색은 타고난 기질의 오행을 나타내요.</p>';
  h+=L('🧍 타고난 나의 성향','일간이 '+dg+'('+dw+')이라, '+(GAN_PERSON[dg]||'')+' 사람이에요.');
  h+=L('🐾 일지(배우자·가정 자리)의 기질',ZHI_KO[dz]+'('+dz+') 기운이라 '+(ZHI_TRAIT[dz]||'')+' 면이 있어요. 이 자리는 배우자·가정과의 인연을 보여줍니다.');
  if(c.note)h+=L('💡 한 줄로',c.note);
  return h;
}
function charDetail(c){return c.kind==='animal'?animalDetail(c):(c.kind==='spirit'?spiritDetail(c):shinsalDetail(c));}

/* ===== 이 시기 총평 (자동 종합) ===== */
const SS_EVENT={
  망신살:'숨긴 일이나 돈 문제가 드러나 망신·구설을 당할 수 있어요.',
  백호:'사고·수술·다침 같은 일을 특히 조심해야 하는 시기예요.',
  양인:'결단력이 칼처럼 날카로워져요. 정밀기술·운동·의료·전문일에 쓰면 무기가 돼요 → 단, 운전·날선 도구·격한 언쟁을 피하고 화날 땐 자리를 떠야 사고·다툼·손실을 막아요.',
  도화:'이성 인연·연애·인기가 강하게 동하는 시기예요.',
  홍염살:'이성에게 인기가 많아지고 연애·구설이 생길 수 있어요.',
  진역마:'이사·이동·출장·해외처럼 좋은 움직임이 많아져요.',
  살역마:'원치 않는 이사·이동·분주함과 교통 사고를 조심하세요.',
  지살:'이사·독립·터전 변화가 생길 수 있어요.',
  화개:'예술·종교·연구에 깊이 몰입하기 좋은 시기예요. 혼자 파고드는 일에서 빛나요 → 단, 고립·우울로 빠지지 않게 사람·바깥 활동을 일부러 챙기세요.',
  공망:'기대했던 일의 결실이 비거나 허무함을 느낄 수 있어요.',
  천을귀인:'귀인·윗사람의 도움으로 어려움이 풀릴 수 있어요.',
  천덕귀인:'위기에도 보호받아 흉이 줄어드는 시기예요.',
  월덕귀인:'온화한 인덕으로 일이 부드럽게 풀려요.',
  문창귀인:'시험·문서·학업운이 좋은 시기예요.',
  학당귀인:'공부·연구·시험에 좋은 시기예요.',
  건록:'자기 힘으로 버는 재물·안정이 들어와요.',
  재고귀인:'재물을 모으고 지키기 좋은 시기예요.',
  겁살:'도난·사기·갑작스러운 금전 손실을 조심하세요.',
  재살:'관재·송사·구속수를 조심하세요.',
  천살:'갑작스러운 변고·천재지변을 대비하세요.',
  육해살:'질병·방해로 일이 더디고 막힐 수 있어요.',
  괴강:'카리스마·결단이 강해지는 시기예요. 전문분야·리더 자리에 정면 도전하면 큰 성취로 이어져요 → 단, 잘될수록 겸손·경청·사람 관리로 독선을 누르고 큰 결정은 한 박자 늦추면 흔들림이 줄어요.',
  현침살:'정밀한 일엔 길하나, 날선 말·구설과 사고를 주의하세요.',
  원진:'특정 사람과 까닭 없는 갈등·애증이 생길 수 있어요.',
  천라지망:'관재·구속·답답한 상황에 묶일 수 있어요.',
  장성살:'승진·통솔의 기회예요. 책임 있는 프로젝트를 자청하면 능력을 인정받아요 → 단, 혼자 다 하려 말고 경청·위임으로 아랫사람을 챙겨야 적이 안 생겨요.',
  반안살:'승진·발탁·윗사람의 후원을 받는 시기예요.',
  탕화살:'화상·화재·사고를 조심하세요.',
  편관칠살:'압박·경쟁이 세지는 시기예요. 목표를 정해 몰아붙이고 운동·취미로 스트레스를 풀면 성취로 바뀌어요 → 단, 과로·과음·상사와의 정면충돌을 피하고 건강검진을 꼭 챙기세요.',
  자유귀문:'신경이 예민해지고 집착·불면이 생길 수 있어요.',축오귀문:'마음의 기복·울화가 올라올 수 있어요.',인미귀문:'한 가지에 과몰입(집착)하기 쉬워요.',묘신귀문:'신경질·변덕이 날 수 있어요.',진해귀문:'예민·우울·영적 감수성이 깊어질 수 있어요.',사술귀문:'의심·집착이 강해질 수 있어요.'
};
const SS_LUCK={
  정인:{t:'시험·자격증·문서·계약·공부에 좋고, 윗사람·어머니의 도움을 받기 쉬운 시기예요.',cat:'good',w:3},
  편인:{t:'자격·기술·종교에 관심이 커지는 시기. 임기응변·눈치가 늘지만 생각이 많아질 수 있어요.',cat:'mid',w:2},
  정관:{t:'직장·승진·명예·시험에 좋은 시기. 책임 있는 자리를 맡기 좋아요.',cat:'good',w:3},
  편관:{t:'압박·도전·경쟁이 센 시기. 잘 다스리면 승진·성취, 못 다스리면 스트레스·관재·건강 주의.',cat:'bad',w:2},
  정재:{t:'안정적 재물·근면의 시기. 저축·실속 챙기기 좋아요(남성은 결혼·이성운).',cat:'good',w:3},
  편재:{t:'사업·투자·큰돈·이성의 시기. 기회도 욕심도 커지니 과욕·과로 주의.',cat:'mid',w:2},
  식신:{t:'표현·먹을복·여유의 시기. 창작·강의·새 시도에 좋아요(여성은 자녀운).',cat:'good',w:2},
  상관:{t:'재능·말솜씨가 빛나는 시기. 시험·창작엔 길하나 구설·반항·관재는 주의.',cat:'mid',w:2},
  비견:{t:'동료·경쟁·독립의 시기. 동업·협력엔 좋으나 금전 지출 주의.',cat:'mid',w:2},
  겁재:{t:'경쟁·욕심·지출의 시기. 동업·보증·투기로 인한 손재를 조심하세요.',cat:'bad',w:2}
};
const BIG_EVENTS=['결혼','이혼','별거','이직','입사','퇴사','해고','이사','매매','부동산','연애','이성','금전','재물','빚','손재','손실','이별','사별','상실','스트레스','사고','수술','다침','출산','임신','승진','발탁','시험','자격증','합격','망신','구설','질병','건강','관재','송사','도난','사기'];
const BIG_RE=new RegExp('('+BIG_EVENTS.join('|')+')','g');
function hlBig(t){return t.replace(BIG_RE,'<span class="bigev">$1</span>');}
const SUMCOL={good:['#c9a227','#fff8e6','#7a5b00','길'],bad:['#d23b2a','#fdeceb','#8a1f17','주의'],mid:['#888780','#f1efe8','#444441','중립']};
const SIPSIN_EMB={정인:'문서운',편인:'재주운',정관:'직장운',편관:'압박운',정재:'재물운',편재:'사업운',식신:'표현운',상관:'끼·재능',비견:'경쟁운',겁재:'욕심운'};
const REL_EMB={합:'만남',충:'충돌',형:'마찰',파:'깨짐',해:'방해'};
function glyphEmblem(txt,color){
  txt=String(txt);const fs=txt.length<=1?44:(txt.length===2?30:(txt.length===3?23:19));
  return '<svg viewBox="0 0 96 96" width="96" height="96" xmlns="http://www.w3.org/2000/svg"><circle cx="48" cy="48" r="40" fill="#fbf7ee" stroke="'+color+'" stroke-width="3.5"/><text x="48" y="48" dominant-baseline="central" text-anchor="middle" font-size="'+fs+'" font-weight="700" fill="'+color+'">'+txt+'</text></svg>';}
function sumStars(st){let s='';for(let i=0;i<Math.max(1,Math.min(3,st||1));i++)s+='★';return s;}
function summaryItems(){
  const se=[],dae=[],wol=[],seen={},use=CUR.ua.use,avoid=CUR.ua.avoid;
  const star=st=>Math.max(1,Math.min(3,st||1));
  STAGE.filter(c=>c.luck&&c.kind==='shinsal').forEach(c=>{const ev=SS_EVENT[c.key];if(!ev||seen['s'+c.key])return;seen['s'+c.key]=1;
    const bucket=c.lucksrc==='dae'?dae:(c.lucksrc==='wol'?wol:se);const cat=(c.role==='길신'||c.role==='길')?'good':((c.role==='흉신'||c.role==='흉')?'bad':'mid');
    const refkw=REFKEY[c.key];
    bucket.push({name:c.name.replace(/\s*\(.*\)/,''),cat,st:star(c.str?c.str.w:2),emblem:SC.specialToken(c.key,96),short:ev,detail:charDetail(c)+(refkw?refsHtml(refkw):'')});});
  STAGE.filter(c=>c.luck&&c.kind==='spirit').forEach(c=>{const dw=GAN_WX[CUR.s.dGan],ri=REL_INFO[relKind(c.hanja,dw)];if(!ri||seen['e'+c.hanja])return;seen['e'+c.hanja]=1;
    const inWol=c.targets.some(t=>t.k==='wol'),inSe=c.targets.some(t=>t.k==='se');const bucket=inWol?wol:(inSe?se:dae);const cat=use.has(c.hanja)?'good':(avoid.has(c.hanja)?'bad':'mid');
    bucket.push({name:WX_KO[c.hanja]+' 기운',cat,st:star(c.str?c.str.w:2),emblem:SC.specialToken(c.key,96),short:ri.good.split('. ')[0]+'.',detail:spiritDetail(c)});});
  (CUR.rels||[]).forEach(r=>{const gi=luckGlyphInfo(r);if(!gi)return;const action=(r.type.indexOf('합')>=0)?'합':r.type;const key='r'+gi.gt+action;if(seen[key])return;seen[key]=1;
    const evs=(EVENT_BY_GUNG[gi.gt]&&EVENT_BY_GUNG[gi.gt][action])||[];const rel=RELATION_PLAIN[action]||{label:r.type};
    const cat=(action==='충'||action==='형'||action==='파')?'bad':((action==='합'&&r.el&&use.has(r.el))?'good':'mid');
    const st=(action==='충'?3:((action==='합'&&r.el&&use.has(r.el))?3:2)),sc=cat==='good'?1:(cat==='bad'?-1:0);
    const subj=GUNG_SHORT[gi.gt]||gi.gt,col=SUMCOL[cat][0],refkw=REFKEY[gi.ss];
    (gi.lk==='dae'?dae:(gi.lk==='wol'?wol:se)).push({name:subj+' 자리 '+rel.label.split('(')[0],cat,st:star(st),
      emblem:glyphEmblem(REL_EMB[action]||'변화',col),short:(SUBJECT_PLAIN[gi.gt]||gi.gt)+' 자리가 '+rel.label+' — '+evs.slice(0,3).join('·'),
      detail:buildPlain(gi,sc)+(refkw?refsHtml(refkw):'')});});
  [['se',SELSE&&SELSE.gz,'올해'],['wol',SELWOL&&SELWOL.gz,'이달'],['dae',SELDAE&&SELDAE.gz,'이 대운']].forEach(L=>{
    if(!L[1])return;const ssg=sipsin(CUR.s.dGan,L[1][0]),info=SS_LUCK[ssg];if(!info)return;const key='l'+ssg+L[0];if(seen[key])return;seen[key]=1;
    const sp=SIPSIN_PLAIN[ssg]||{},col=SUMCOL[info.cat][0],bucket=L[0]==='dae'?dae:(L[0]==='wol'?wol:se);
    bucket.push({name:L[2]+' '+ssg+'운',cat:info.cat,st:star(info.w),emblem:glyphEmblem(SIPSIN_EMB[ssg]||'운세',col),short:info.t,
      detail:'<div class="line" style="line-height:1.75">'+info.t+'</div>'+(sp.desc?'<div class="line" style="line-height:1.75;margin-top:6px;color:#555"><b>'+(sp.label||ssg)+'</b> — '+sp.desc+'</div>':'')+(REFKEY[ssg]?refsHtml(REFKEY[ssg]):'')});});
  const byStar=(a,b)=>b.st-a.st;dae.sort(byStar);se.sort(byStar);wol.sort(byStar);
  return {dae:dae.slice(0,8),se:se.slice(0,10),wol:wol.slice(0,10)};
}
function sumCardEl(c,cls,oi){
  const col=SUMCOL[c.cat]||SUMCOL.mid,main=cls==='main',w=main?150:104,embH=main?96:64;
  return '<div class="pcw" data-i="'+oi+'" data-cls="'+cls+'" style="width:'+w+'px;'+(main?'':'opacity:.62;')+'">'
    +'<div class="pcd" style="border:'+(main?'2px':'1px')+' solid '+col[0]+'">'
    +'<div class="pchd" style="background:'+col[1]+'"><span class="pcnm" style="font-size:'+(main?12.5:11)+'px;color:'+col[2]+'">'+c.name+'</span><span class="pcst">'+sumStars(c.st)+'</span></div>'
    +'<div class="pcemb" style="background:'+col[1]+';height:'+(main?104:74)+'px"><div style="width:'+embH+'px;height:'+embH+'px">'+c.emblem+'</div></div>'
    +'<div class="pcft"><div class="pctype" style="color:'+col[0]+'">'+col[3]+'</div>'+(main?'<div class="pcshort">'+hlBig(c.short)+'</div>':'')+'</div></div></div>';
}
function renderLane(which,dir){
  const arr=SUMCARDS[which]||[],stg=document.getElementById('sumstg-'+which),dots=document.getElementById('sumdots-'+which);if(!stg)return;
  if(!arr.length){stg.innerHTML='<div class="sumitem sum-mid" style="font-size:12.5px">두드러진 신호가 적어요. 비교적 무난한 편입니다.</div>';if(dots)dots.innerHTML='';return;}
  const n=arr.length,idx=((SUMIDX[which]%n)+n)%n,L=(idx-1+n)%n,R=(idx+1)%n;
  let html='';
  if(n>=2)html+=sumCardEl(arr[L],'side',L);
  html+=sumCardEl(arr[idx],'main',idx);
  if(n>=2&&R!==L)html+=sumCardEl(arr[R],'side',R);
  stg.innerHTML=html;
  if(dir){stg.style.animation='none';void stg.offsetWidth;stg.style.animation=(dir>0?'sumNext':'sumPrev')+' .26s ease';}
  if(dots){let d='';for(let i=0;i<n;i++)d+='<i style="background:'+(i===idx?'#6a4ad0':'#d8d2c4')+'"></i>';dots.innerHTML=d;}
  stg.querySelectorAll('.pcw').forEach(el=>{el.onclick=()=>{const i=+el.dataset.i;if(el.dataset.cls==='main'){openSumModal(which,i);}else{const cur=((SUMIDX[which]%n)+n)%n,dd=(i===((cur-1+n)%n))?-1:1;SUMIDX[which]=i;renderLane(which,dd);}};});
}
function sumNav(which,d){const n=(SUMCARDS[which]||[]).length;if(!n)return;SUMIDX[which]=((SUMIDX[which]+d)%n+n)%n;renderLane(which,d);}
function openSumModal(which,i){const c=(SUMCARDS[which]||[])[i];if(!c)return;SUMIDX[which]=i;const col=SUMCOL[c.cat]||SUMCOL.mid;
  document.getElementById('sumModalBox').innerHTML=
    '<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">'
    +'<div style="width:78px;height:78px;flex:0 0 auto;border:2px solid '+col[0]+';border-radius:12px;background:'+col[1]+';display:flex;align-items:center;justify-content:center;overflow:hidden"><div style="width:68px;height:68px">'+c.emblem+'</div></div>'
    +'<div><div class="modalttl" style="margin:0">'+c.name+'</div><div style="font-size:13px;color:'+col[0]+';font-weight:700;margin-top:2px">'+col[3]+' · 세기 <span style="letter-spacing:1px">'+sumStars(c.st)+'</span></div></div></div>'
    +'<div style="font-size:13.5px;line-height:1.75">'+c.detail+'</div>'
    +'<div class="modalbtns"><button class="ghost" onclick="closeSumModal()">닫기</button></div>';
  document.getElementById('sumModal').classList.remove('hidden');renderLane(which);
}
function closeSumModal(){document.getElementById('sumModal').classList.add('hidden');}
function laneHTML(which,label,gz,bg,tc,pc,period){
  return '<div class="sumlane"><div class="lanehd" style="background:'+bg+'">'
    +'<div><span class="lt" style="color:'+tc+'">'+label+'</span><span class="lg" style="color:'+tc+'">'+gz+'</span></div>'
    +'<div class="lp" style="color:'+pc+'">'+period+'</div></div>'
    +'<div class="carow"><button class="nav navbtn" data-w="'+which+'" data-d="-1" aria-label="이전">‹</button>'
    +'<div class="carstg" id="sumstg-'+which+'"></div>'
    +'<button class="nav navbtn" data-w="'+which+'" data-d="1" aria-label="다음">›</button></div>'
    +'<div class="cardots" id="sumdots-'+which+'"></div></div>';
}
function renderSummary(){
  const box=document.getElementById('summaryBox');if(!box)return;
  if(!(SELDAE||SELSE||SELWOL)){box.innerHTML='<div class="infohint" style="padding:6px">대운·세운·월운을 선택하면 그 시기의 총평이 자동으로 나옵니다.</div>';return;}
  SUMCARDS=summaryItems();SUMIDX={dae:0,se:0,wol:0};
  const when=[SELDAE?'대운 '+Math.round(SELDAE.age)+'세 무렵':'',SELSE?SELSE.Y+'년':'',SELWOL?SELWOL.label:''].filter(Boolean).join(' · ');
  let h='<div class="sumwhen">🗓️ '+when+'</div>';
  h+='<div class="sumleg">⭐ 별 개수 = 신호 세기(★★★강·★★중·★약) &nbsp;|&nbsp; 카드를 누르면 자세히 · 화살표(또는 옆 카드)로 넘기기 &nbsp;|&nbsp; <span class="bigev">빨간 글씨</span> = 큰 사건</div>';
  if(SELDAE){const startY=Math.round(CUR.s.sajuYear+SELDAE.age-1),endY=startY+9,a0=Math.round(SELDAE.age),a1=a0+9;
    h+=laneHTML('dae','대운',SELDAE.gz,'#EEEDFE','#3C3489','#534AB7',startY+'–'+endY+'년 · 약 '+a0+'~'+a1+'세 · 10년의 큰 배경');}
  if(SELSE)h+=laneHTML('se','세운',SELSE.gz,'#E6F1FB','#0C447C','#185FA5',SELSE.Y+'년 1년 · 올해의 흐름');
  if(SELWOL)h+=laneHTML('wol','월운',SELWOL.gz,'#FBEAF0','#72243E','#993556',(SELWOL.year?SELWOL.year+'년 ':'')+(SELWOL.label||'')+' 무렵 · 한 달의 흐름');
  h+='<div class="line" style="color:var(--sub);font-size:11.5px;margin-top:8px">※ 가능성을 미리 짚어주는 참고용이에요. 카드를 누르면 각 항목의 근거(십성·고전)를 자세히 볼 수 있어요.</div>';
  box.innerHTML=h;
  box.querySelectorAll('.navbtn').forEach(b=>b.onclick=()=>sumNav(b.dataset.w,+b.dataset.d));
  ['dae','se','wol'].forEach(w=>{if(document.getElementById('sumstg-'+w))renderLane(w);});
}
function applyLuckReactions(){
  clearGung();if(!CUR||!(SELDAE||SELSE||SELWOL))return;const ua=CUR.ua;
  (CUR.rels||[]).forEach(r=>{const gi=luckGlyphInfo(r);if(!gi)return;
    const sc=judgeLuck(CUR.P[gi.lk],ua.use,ua.avoid),expr=sc>0?'happy':(sc<0?'sad':'surprise');
    const sev=({충:3,형:2,파:2,해:1})[r.type]||2;
    setGung(gi.ok,gi.which,expr,sev);});
}
function roleClass(role){return role==='길신'||role==='길'?'r-gil':role==='흉신'||role==='흉'?'r-hyung':role==='양면'?'r-yang':role==='오행'?'r-oh':'r-il';}
function roleLabel(role){return role==='길신'||role==='길'?'길':role==='흉신'||role==='흉'?'흉':role==='양면'?'양면':role==='오행'?'오행':'일주';}
function roleLineColor(role){return (role==='길신'||role==='길')?'#e0b400':(role==='흉신'||role==='흉')?'#d23b2a':(role==='양면')?'#d98a2a':'#2aa198';}
function relColor(e,d){if(e===d)return '#3aa05a';if(SHENG[e]===d)return '#e0b400';if(SHENG[d]===e)return '#5a8ac0';if(KE[e]===d)return '#e0573a';if(KE[d]===e)return '#9a5cc0';return '#888';}
function relLabel(e,d){if(e===d)return '일간과 같은 오행(비겁) — 동질·경쟁';if(SHENG[e]===d)return '일간을 생함(인성) — 도움';if(SHENG[d]===e)return '일간이 생함(식상) — 기운 새어나감';if(KE[e]===d)return '일간을 극함(관살) — 압박·주의';if(KE[d]===e)return '일간이 극함(재성) — 다스려 재물로';return '';}
function hex2rgba(h,a){const n=parseInt(h.slice(1),16);return 'rgba('+((n>>16)&255)+','+((n>>8)&255)+','+(n&255)+','+a+')';}

/* ===== 폼/상태 ===== */
let CAL="solar",SEX="남",LST=true;const TZ=540,LST_MIN=30;
function setCal(c){CAL=c;document.querySelectorAll("#calSeg button").forEach(b=>b.classList.toggle("on",b.dataset.cal===c));document.getElementById("leapWrap").classList.toggle("hidden",c!=="lunar");}
function setSex(s){SEX=s;document.querySelectorAll("#sexSeg button").forEach(b=>b.classList.toggle("on",b.dataset.sex===s));}
function setLst(v){LST=v==="1";document.querySelectorAll("#lstSeg button").forEach(b=>b.classList.toggle("on",b.dataset.lst===v));}
/* ===== 내 인생 백테스팅 ===== */
const CAT_SIG={
 '결혼·연애':{shin:['도화','홍염살','금여'],ss:['정재','편재','정관','편관'],gung:['배우자']},
 '이직·직장':{shin:['편관칠살','살역마','진역마','역마','장성살','반안살'],ss:['정관','편관'],gung:['사회상','가치관']},
 '이사·이동':{shin:['진역마','살역마','역마','지살'],ss:[],gung:['가정기반','뿌리','내면']},
 '금전·재물':{shin:['건록','재고귀인','천주귀인','금여','암록','복성귀인','겁살'],ss:['정재','편재'],gung:[]},
 '이별·상실':{shin:['공망','백호','원진'],ss:['편관','겁재'],gung:['배우자','내면','실제자녀','미래자녀']},
 '시험·자격·공부':{shin:['문창귀인','학당귀인','관귀학관','문곡귀인','태극귀인'],ss:['정인','편인','정관'],gung:['가치관']},
 '건강·사고':{shin:['백호','양인','괴강','천살','육해살','현침살'],ss:['편관'],gung:[]},
 '대인·갈등·스트레스':{shin:['원진','자유귀문','축오귀문','인미귀문','묘신귀문','진해귀문','사술귀문','양인','천라지망'],ss:['편관','겁재'],gung:[]},
 '승진·성취':{shin:['장성살','반안살','건록','괴강','태극귀인'],ss:['정관','정인'],gung:['사회상']},
 '기타':{shin:[],ss:[],gung:[]}
};
function activeDaeFor(Y){const s=CUR.s;const age=Y-s.sajuYear+1;let di=0;s.dae.list.forEach((d,idx)=>{if(d.age<=age)di=idx;});const d=s.dae.list[di];return {gz:d.gz,age:d.age,_i:di};}
function seGzFor(Y){const idx=((Y-4)%60+60)%60;return GAN[idx%10]+ZHI[idx%12];}
function periodSignals(Y,M){
  const s=CUR.s;const P=Object.assign({},s.pillars);const base=['year','month','day','hour'].filter(k=>s.pillars[k]);
  const dae=activeDaeFor(Y);P.dae=dae.gz;const seGz=seGzFor(Y);P.se=seGz;
  let wolGz=null;const ord=base.concat(['dae','se']);
  if(M){try{const w=(computeWol(Y)||[]).find(x=>x.sol===M);if(w){P.wol=w.gz;wolGz=w.gz;ord.push('wol');}}catch(e){}}
  const luckK=['dae','se','wol'];
  const shin=shinsalSet(P,ord,s.dGan).filter(e=>e.pillars.some(k=>luckK.includes(k)));
  const shinKeys=[...new Set(shin.map(e=>e.key))];
  const ssKeys=[];[dae.gz,seGz,wolGz].forEach(gz=>{if(gz)ssKeys.push(sipsin(s.dGan,gz[0]));});
  const savedP=CUR.P,savedOrd=CUR.ord;CUR.P=P;CUR.ord=ord;
  const rels=computeRelations(P,ord).filter(r=>{const ks=r.tri?r.tri:[r.ki,r.kj];return ks.some(k=>luckK.includes(k));});
  const relInfo=[];rels.forEach(r=>{const gi=luckGlyphInfo(r);const tp=(r.type.indexOf('합')>=0)?'합':r.type;relInfo.push({type:tp,gt:gi?gi.gt:null});});
  CUR.P=savedP;CUR.ord=savedOrd;
  return {dae,seGz,wolGz,shinKeys,ssKeys,relInfo};
}
const CAT_DESC={
 '결혼·연애':'결혼·연애는 <b>배우자 자리(일지)의 합·충</b>, 매력의 별 <b>도화·홍염</b>, 그리고 배우자에 해당하는 십성(남자는 재성, 여자는 관성)운이 동할 때 잘 나타나요.',
 '이직·직장':'직장·자리의 변동은 직장을 뜻하는 <b>관성(정관·편관)운</b>, 이동의 별 <b>역마·살역마</b>, 사회적 자리(사회상·직업)의 <b>충</b>에서 드러나요.',
 '이사·이동':'이사·이동·해외는 이동의 별 <b>역마·지살</b>과 <b>가정·터전 자리의 충</b>에서 잘 나타나요.',
 '금전·재물':'돈·재물 변화는 재물을 뜻하는 <b>재성(정재·편재)운</b>과 재물의 별 <b>건록·재고·금여</b>, 또는 손재의 별 <b>겁살</b>에서 드러나요.',
 '이별·상실':'이별·상실은 <b>배우자·자녀·내면 자리의 충</b>, 비어있음의 <b>공망</b>, 그리고 <b>백호·원진</b>에서 나타나요.',
 '시험·자격·공부':'시험·자격·공부는 문서·공부를 뜻하는 <b>인성(정인)운</b>과 학문의 별 <b>문창·학당·관귀학관</b>에서 잘 드러나요.',
 '건강·사고':'건강·사고는 강한 칼날의 별 <b>양인·백호·괴강</b>, 압박의 <b>칠살(편관)운</b>, 천재지변의 <b>천살</b>에서 나타나요.',
 '대인·갈등·스트레스':'사람과의 갈등·스트레스는 까닭 모를 미움 <b>원진</b>, 예민함의 <b>귀문</b>, 칼날의 <b>양인</b>, 압박의 <b>칠살</b>에서 드러나요.',
 '승진·성취':'승진·성취는 권위의 별 <b>장성·반안</b>, 직장·명예의 <b>관성·인성운</b>, 카리스마의 <b>괴강</b>에서 나타나요.',
 '기타':'특정 분류에 묶지 않고, 그 시기에 활성화된 신호 전체를 함께 살펴봐요.'
};
function matchEvent(sig,cat){const c=CAT_SIG[cat]||CAT_SIG['기타'];const hits=[];const seen={};
  sig.shinKeys.forEach(k=>{if(c.shin.includes(k)&&!seen['s'+k]){seen['s'+k]=1;hits.push({kind:'shin',key:k});}});
  sig.ssKeys.forEach(k=>{if(c.ss.includes(k)&&!seen['t'+k]){seen['t'+k]=1;hits.push({kind:'ss',key:k});}});
  sig.relInfo.forEach(r=>{if(r.gt&&c.gung.includes(r.gt)){const id='r'+r.gt+r.type;if(!seen[id]){seen[id]=1;hits.push({kind:'rel',gt:r.gt,type:r.type});}}});
  const lv=hits.length>=2?'강':(hits.length===1?'부분':'약');return {lv,hits};
}
function btSigName(h){
  if(h.kind==='shin')return (SS_INFO[h.key]&&SS_INFO[h.key].name)||h.key;
  if(h.kind==='ss')return h.key+'운';
  if(h.kind==='rel')return (GUNG_SHORT[h.gt]||h.gt)+' 자리 '+h.type;
  return '';
}
function btSigWhy(h,cat){
  if(h.kind==='shin'){const o=SS_INFO[h.key]||{},r=SS_RICH[h.key]||{};
    const what=o.d||o.b||o.g||'';const adv=r.bad||r.good||o.a||'';
    return what+(adv?' <span style="color:#8a5a00">→ '+adv.split('. ')[0]+'.</span>':'');}
  if(h.kind==='ss'){const k=h.key,sp=SIPSIN_PLAIN[k]||{},ll=SS_LUCK[k];
    return (sp.label?'<b>'+sp.label+'</b> — ':'')+(sp.desc||'')+(ll?' 운으로 들어오면 '+ll.t:'');}
  if(h.kind==='rel'){const rp=RELATION_PLAIN[h.type]||{},subj=SUBJECT_PLAIN[h.gt]||h.gt;
    return '이 시기 운이 <b>'+subj+'</b> 자리와 '+(rp.label||h.type)+'(을)를 일으켜요. '+(GUNG_EXPLAIN[h.gt]?GUNG_EXPLAIN[h.gt]+' ':'')+(rp.desc||'');}
  return '';
}
let btN=0,BT_LAST=null;
function btRowHtml(i){return `<div class="btrow" id="btrow-${i}" style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin:7px 0">`
 +`<input type="number" placeholder="연도" id="bty-${i}" style="width:84px;padding:8px;border:1px solid var(--bd);border-radius:8px">`
 +`<input type="number" placeholder="월(선택)" id="btm-${i}" min="1" max="12" style="width:96px;padding:8px;border:1px solid var(--bd);border-radius:8px">`
 +`<select id="btc-${i}" style="padding:8px;border:1px solid var(--bd);border-radius:8px">${Object.keys(CAT_SIG).map(c=>`<option>${c}</option>`).join('')}</select>`
 +`<input placeholder="메모(예: 회사 그만둠)" id="btnote-${i}" style="flex:1;min-width:130px;padding:8px;border:1px solid var(--bd);border-radius:8px">`
 +`<button type="button" onclick="btDel(${i})" style="border:0;background:#f3eaea;color:#c0392b;border-radius:8px;padding:8px 11px;cursor:pointer">✕</button></div>`;}
function btAddRow(){document.getElementById('btRows').insertAdjacentHTML('beforeend',btRowHtml(btN++));}
function btDel(i){const el=document.getElementById('btrow-'+i);if(el)el.remove();}
function toggleBT(){const c=document.getElementById('btCard');c.classList.toggle('hidden');if(!c.classList.contains('hidden')){if(!document.querySelector('.btrow'))btAddRow();c.scrollIntoView({behavior:'smooth',block:'start'});}}
function btAnalyze(){
  if(!CUR){alert('먼저 「사주 소환」으로 사주를 분석해 주세요.');return;}
  const out=[];document.querySelectorAll('.btrow').forEach(row=>{const i=row.id.split('-')[1];
    const Y=+document.getElementById('bty-'+i).value;if(!Y)return;
    const M=+(document.getElementById('btm-'+i).value||0);const cat=document.getElementById('btc-'+i).value;
    const note=document.getElementById('btnote-'+i).value.trim();
    const sig=periodSignals(Y,M||0);const m=matchEvent(sig,cat);out.push({Y,M,cat,note,sig,m});});
  const box=document.getElementById('btResult');
  if(!out.length){box.innerHTML='<div class="infohint" style="padding:8px">연도와 사건을 입력해 주세요.</div>';return;}
  BT_LAST=out;
  const LV={'강':['#EAF3DE','#2e6b14','강한 일치'],'부분':['#FAEEDA','#7a4b08','부분 일치'],'약':['#EFEDE6','#555555','약한 신호']};
  const agree=out.filter(o=>o.m.lv!=='약').length;
  box.innerHTML=`<div class="sectitle" style="margin-top:14px">결과 — ${out.length}건 중 ${agree}건이 사주 신호와 맞아떨어졌어요</div>`
   +`<div class="predhint" style="margin-bottom:4px">‘일치도’는 그 시기에 켜진 신호가 이 사건 종류가 보통 쓰는 신호와 몇 개나 겹쳤는지로 매겨요 — 2개 이상=강, 1개=부분, 0개=약. 아래에 무엇이 왜 맞물렸는지와 옛 명리책 근거를 함께 보여드려요.</div>`
   +out.map(o=>{
    const lv=LV[o.m.lv];const wol=o.sig.wolGz?(' 월운 '+o.sig.wolGz):'';
    const period=`${o.Y}년${o.M?' '+o.M+'월':''} · 대운 ${o.sig.dae.gz} 세운 ${o.sig.seGz}${wol}`;
    const c=CAT_SIG[o.cat]||CAT_SIG['기타'];
    const expect=[...c.shin.slice(0,5),...c.ss.map(x=>x+'운').slice(0,2)].join(' · ')||'정해진 핵심 신호 없음';
    let hitHtml;
    if(o.m.hits.length){
      hitHtml=o.m.hits.map(h=>`<div style="margin:5px 0;padding:7px 9px;background:#faf8f3;border:1px solid #efe7d6;border-radius:8px"><b style="color:${lv[1]}">✔ ${btSigName(h)}</b><div style="color:#555;font-size:12.5px;line-height:1.65;margin-top:2px">${btSigWhy(h,o.cat)}</div></div>`).join('');
    }else{
      hitHtml=`<div style="color:var(--sub);font-size:12.5px;margin-top:4px;line-height:1.6">이 분류가 보통 쓰는 핵심 신호(${expect})가 그 시기엔 약하게 잡혔어요. 사건이 다른 영역의 신호와 연결됐거나, 입력한 분류가 사주적으로 다르게 잡힐 수 있어요. 아래 ‘그 시기 전체 신호’를 참고해 분류를 바꿔 다시 눌러보세요.</div>`;
    }
    const refKws=[...new Set(o.m.hits.filter(h=>h.kind!=='rel').map(h=>REFKEY[h.key]).filter(Boolean))].slice(0,2);
    const refHtml=refKws.map(k=>refsHtml(k)).join('');
    const otherShin=o.sig.shinKeys.filter(k=>!o.m.hits.some(h=>h.kind==='shin'&&h.key===k)).slice(0,8);
    const allss=o.sig.ssKeys.join(' / ');
    return `<div class="sumitem" style="border-left:4px solid ${lv[1]}">`
     +`<span style="display:inline-block;font-size:11px;font-weight:700;padding:2px 9px;border-radius:8px;background:${lv[0]};color:${lv[1]};margin-right:7px">${lv[2]}</span>`
     +`<b>${o.cat}</b>${o.note?' · '+o.note:''}`
     +`<div style="color:var(--sub);font-size:12px;margin-top:3px">${period}</div>`
     +`<div style="margin-top:8px;font-size:12.5px;color:#444;background:#f3f0fb;border-radius:8px;padding:7px 9px"><b>이 분류는 이렇게 봅니다</b><br><span style="line-height:1.65">${CAT_DESC[o.cat]||''}</span></div>`
     +`<div style="margin-top:8px"><b style="font-size:13px">🔗 그 시기에 실제로 맞물린 신호</b>${hitHtml}</div>`
     +refHtml
     +`<div style="color:var(--sub);font-size:11.5px;margin-top:8px;line-height:1.6"><b>그 시기 전체 신호</b><br>· 운의 십성: ${allss||'-'}${otherShin.length?'<br>· 함께 켜진 다른 신살: '+otherShin.join(', '):''}</div>`
     +`</div>`;}).join('');
}
function btKeyStr(){return ['year','month','day','hour'].filter(k=>CUR.s.pillars[k]).map(k=>CUR.s.pillars[k]).join(' ');}
function btSave(){if(!BT_LAST){alert('먼저 「분석하기」를 눌러주세요.');return;}
  try{const db=JSON.parse(localStorage.getItem('sajuBT')||'[]');
    db.push({ts:Date.now(),saju:btKeyStr(),dg:CUR.s.dGan,sex:SEX,
      cases:BT_LAST.map(o=>({Y:o.Y,M:o.M,cat:o.cat,note:o.note,lv:o.m.lv,hits:o.m.hits,ss:o.sig.ssKeys,shin:o.sig.shinKeys}))});
    localStorage.setItem('sajuBT',JSON.stringify(db));
    alert('저장했어요(이 브라우저). 지금까지 '+db.length+'명의 사례가 쌓였어요.');}
  catch(e){alert('저장 실패: '+e.message);}}
function btExport(){let db=[];try{db=JSON.parse(localStorage.getItem('sajuBT')||'[]');}catch(e){}
  const rows=[];
  if(BT_LAST)BT_LAST.forEach(o=>rows.push([btKeyStr(),CUR.s.dGan,SEX,o.Y,o.M||'',o.cat,(o.note||'').replace(/[,\n]/g,';'),o.m.lv,o.m.hits.join('|'),o.sig.ssKeys.join('|'),o.sig.shinKeys.join('|')]));
  db.forEach(r=>(r.cases||[]).forEach(o=>rows.push([r.saju,r.dg,r.sex,o.Y,o.M||'',o.cat,(o.note||'').replace(/[,\n]/g,';'),o.lv,(o.hits||[]).join('|'),(o.ss||[]).join('|'),(o.shin||[]).join('|')])));
  if(!rows.length){alert('내보낼 사례가 없어요.');return;}
  const head='saju,day_gan,sex,year,month,category,note,match,matched_signals,luck_sipsin,luck_shinsal';
  const csv=head+'\n'+rows.map(r=>r.join(',')).join('\n');
  const blob=new Blob(['﻿'+csv],{type:'text/csv;charset=utf-8'});const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);a.download='saju_backtest.csv';a.click();}
function btShowSaved(){let db=[];try{db=JSON.parse(localStorage.getItem('sajuBT')||'[]');}catch(e){}
  const box=document.getElementById('btResult');
  if(!db.length){box.innerHTML='<div class="infohint" style="padding:8px">아직 저장된 사례가 없어요.</div>';return;}
  let n=0,agree=0;db.forEach(r=>(r.cases||[]).forEach(o=>{n++;if(o.lv!=='약')agree++;}));
  box.innerHTML=`<div class="sectitle" style="margin-top:14px">저장된 사례 — ${db.length}명 · 사건 ${n}건 · 신호 일치 ${n?Math.round(agree/n*100):0}%</div>`
   +db.map((r,idx)=>`<div class="sumitem"><b>${idx+1}. ${r.saju}</b> <span style="color:var(--sub);font-size:12px">(${r.sex})</span><br>`
    +(r.cases||[]).map(o=>`<span style="color:var(--sub);font-size:12px">· ${o.Y}${o.M?'.'+o.M:''} ${o.cat} — ${o.lv}${o.note?' ('+o.note+')':''}</span>`).join('<br>')+`</div>`).join('')
   +`<div class="predhint" style="margin-top:6px">CSV로 내보내면 이 전체를 사주엔진 사례 DB 검증에 쓸 수 있어요.</div>`;}

function fillForm(){
  const y=document.getElementById('y');for(let v=2100;v>=1900;v--)y.add(new Option(v+'년',v));y.value=1990;
  const m=document.getElementById('m');for(let v=1;v<=12;v++)m.add(new Option(v+'월',v));
  const d=document.getElementById('d');for(let v=1;v<=31;v++)d.add(new Option(v+'일',v));
  const h=document.getElementById('h');h.add(new Option('모름',''));for(let v=0;v<24;v++)h.add(new Option(String(v).padStart(2,'0')+'시',v));
  const mi=document.getElementById('mi');for(let v=0;v<60;v+=5)mi.add(new Option(String(v).padStart(2,'0')+'분',v));
  window._EX=[];
}
function loadEx(i){const e=window._EX[i];setCal('solar');document.getElementById('y').value=e[1];document.getElementById('m').value=e[2];document.getElementById('d').value=e[3];document.getElementById('h').value=e[4];document.getElementById('mi').value=0;setSex(e[5]);run();}

function readForm(){
  const g=id=>document.getElementById(id).value;
  let Y=+g('y'),M=+g('m'),D=+g('d');const hv=g('h'),h=(hv==='')?null:+hv;const mi=+(g('mi')||0);
  if(CAL==='lunar'){const sol=lunarToSolar(Y,M,D,document.getElementById('leap').value==='1');if(sol){Y=sol[0];M=sol[1];D=sol[2];}}
  let cY=Y,cM=M,cD=D,cH=h,cMi=mi;
  if(h!=null&&LST){const dt=new Date(Date.UTC(Y,M-1,D,h,mi));dt.setUTCMinutes(dt.getUTCMinutes()-LST_MIN);cY=dt.getUTCFullYear();cM=dt.getUTCMonth()+1;cD=dt.getUTCDate();cH=dt.getUTCHours();cMi=dt.getUTCMinutes();}
  return computeSaju(cY,cM,cD,cH,cMi,SEX,TZ);
}

let CUR=null,SELDAE=null,SELSE=null,SELWOL=null,CURSEL=null,CURREL=null,STAGE=[],WOLCACHE=[],WOLYEAR=null,SEWIN={y0:0,y1:0},DEF_SEWIN={y0:0,y1:0};
let SUMCARDS={},SUMIDX={dae:0,se:0,wol:0};
const LUCKKEYS=['wol','se','dae'];
const GUNGX={year:['조상·부모궁','년주'],month:['부모·사회궁','월주'],day:['배우자궁','일주'],hour:['자녀궁','시주'],
  dae:['대운(10년 시기)','대운'],se:['세운(그 해)','세운'],wol:['월운(그 달)','월운']};
const POSKEY={year:{g:'년간',z:'년지'},month:{g:'월간',z:'월지'},day:{z:'일지'},hour:{g:'시간',z:'시지'}};
const GUNGKEY={year:'년주',month:'월주',day:'일주',hour:'시주'};
const EXPRCOL={happy:'#2f9e57',sad:'#d23b2a',surprise:'#d98a2a'},RWMAP={1:6,2:10,3:15};
function szOf(which){return which==='pillar'?50:48;}
function symFor(k,which,expr,col,ringCount,sz){sz=sz||szOf(which);const rw=4;
  if(k==='day'&&which==='g')return SC.animalToken(CUR.s.pillars.day[1],WX_KO[GAN_WX[CUR.s.dGan]],sz,'',expr,col,rw,ringCount);
  if(which==='pillar')return SC.symbolToken(GUNGKEY[k],sz,'',expr,col,rw,ringCount);
  return SC.symbolToken(POSKEY[k][which],sz,'',expr,col,rw,ringCount);
}
function setGung(k,which,expr,w){const el=document.getElementById('gsym-'+k+'-'+which);if(!el)return;el.innerHTML=symFor(k,which,expr,EXPRCOL[expr],w,szOf(which));}
function clearGung(){if(!CUR)return;['year','month','day','hour'].forEach(k=>{if(!CUR.s.pillars[k])return;['pillar','g','z'].forEach(wc=>{const el=document.getElementById('gsym-'+k+'-'+wc);if(el)el.innerHTML=symFor(k,wc,null,null,1,szOf(wc));});});}

function run(){
  const s=readForm();const a=analyzeFull(s);const ua=useAvoid(s,a);
  CUR={s,a,ua};SELDAE=null;SELSE=null;SELWOL=null;CURSEL=null;
  renderLuckSelectors();
  // 오늘 기준 대운·세운·월운 자동 선택
  try{
    const nowY=new Date().getFullYear(),nowM=new Date().getMonth()+1,age=nowY-s.sajuYear+1;
    let di=0;s.dae.list.forEach((d,idx)=>{if(d.age<=age)di=idx;});
    SELDAE={gz:s.dae.list[di].gz,_i:di,age:s.dae.list[di].age};
    const startY=Math.round(s.sajuYear+SELDAE.age-1);
    const seIdx=((nowY-4)%60+60)%60;SELSE={gz:GAN[seIdx%10]+ZHI[seIdx%12],Y:nowY};
    renderSeRow(startY-1,startY+10);setOn('daeRow','dae-'+di);
    const wol=computeWol(nowY),wi=wol.findIndex(w=>w.sol===nowM);
    if(wi>=0)SELWOL={gz:wol[wi].gz,_i:wi,label:wol[wi].lab2,year:nowY};
    renderWolRow(nowY);
  }catch(e){}
  rebuild();
  document.getElementById('result').classList.remove('hidden');
  document.getElementById('info').innerHTML='<div class="infohint">오늘 기준 대운·세운·월운이 자동 선택됐어요. 위 캐릭터나 아래 칩을 누르면 자세한 풀이를 볼 수 있어요. 운 칩을 바꿔 다른 시기도 볼 수 있어요.</div>';
  document.getElementById('result').scrollIntoView({behavior:'smooth',block:'start'});
}

/* ===== 운 셀렉터 ===== */
function computeWol(Y){const yidx=((Y-4)%60+60)%60,yinHead=((yidx%10)%5)*2+2,zord=[2,3,4,5,6,7,8,9,10,11,0,1],WS=[2,3,4,5,6,7,8,9,10,11,12,1];
  return zord.map((zi,i)=>{const tg=(yinHead+i)%10;return {gz:GAN[tg]+ZHI[zi],zi,lab2:ZHI[zi]+'월',sol:WS[i]};});}
function renderLuckSelectors(){
  const s=CUR.s,ua=CUR.ua,dg=s.dGan;
  document.getElementById('daeRow').innerHTML=s.dae.list.map((d,i)=>{
    const [m,c]=luckMark(judgeLuck(d.gz,ua.use,ua.avoid));
    return `<div class="chip" id="dae-${i}" onclick="selDae(${i})"><div>${d.age}세</div><div class="cgz">${d.gz}</div><div class="${c}">${m} ${sipsin(dg,d.gz[0])}</div></div>`;
  }).join('');
  const nowY=new Date().getFullYear();DEF_SEWIN={y0:nowY-5,y1:nowY+12};renderSeRow(DEF_SEWIN.y0,DEF_SEWIN.y1);renderWolRow(nowY);
}
function renderSeRow(y0,y1){
  SEWIN={y0,y1};const s=CUR.s,ua=CUR.ua,dg=s.dGan;let h='';
  let dr=null;if(SELDAE){const startY=Math.round(s.sajuYear+SELDAE.age-1);dr=[startY,startY+9];}
  for(let Y=y0;Y<=y1;Y++){const idx=((Y-4)%60+60)%60,gz=GAN[idx%10]+ZHI[idx%12];const [m,c]=luckMark(judgeLuck(gz,ua.use,ua.avoid));
    const indae=(dr&&Y>=dr[0]&&Y<=dr[1])?' indae':'';
    h+=`<div class="chip${(SELSE&&SELSE.Y===Y)?' on':''}${indae}" id="se-${Y}" onclick="selSe(${Y})"><div>${Y}</div><div class="cgz">${gz}</div><div class="${c}">${m} ${sipsin(dg,gz[0])}</div></div>`;}
  document.getElementById('seRow').innerHTML=h;
}
function renderWolRow(Y){
  const s=CUR.s,ua=CUR.ua,dg=s.dGan;WOLCACHE=computeWol(Y);WOLYEAR=Y;
  document.getElementById('seYearLab').textContent='· '+Y+'년 기준';
  document.getElementById('wolRow').innerHTML=WOLCACHE.map((w,i)=>{const [m,c]=luckMark(judgeLuck(w.gz,ua.use,ua.avoid));
    return `<div class="chip${(SELWOL&&SELWOL._i===i&&SELWOL.year===Y)?' on':''}" id="wol-${i}" onclick="selWol(${i})"><div>양${w.sol}월</div><div class="cgz">${w.gz}</div><div class="${c}">${m} ${sipsin(dg,w.gz[0])}</div></div>`;}).join('');
}
function setOn(row,id){document.querySelectorAll('#'+row+' .chip').forEach(e=>e.classList.remove('on'));if(id){const el=document.getElementById(id);if(el)el.classList.add('on');}}
function selDae(i){const d=CUR.s.dae.list[i];
  if(SELDAE&&SELDAE._i===i){SELDAE=null;setOn('daeRow',null);renderSeRow(DEF_SEWIN.y0,DEF_SEWIN.y1);}
  else{SELDAE={gz:d.gz,_i:i,age:d.age};setOn('daeRow','dae-'+i);
    const startY=Math.round(CUR.s.sajuYear+d.age-1);renderSeRow(startY-1,startY+10);
    const row=document.getElementById('seRow');if(row)row.scrollLeft=0;}
  rebuild();}
function selSe(Y){const idx=((Y-4)%60+60)%60,gz=GAN[idx%10]+ZHI[idx%12];
  if(SELSE&&SELSE.Y===Y){SELSE=null;setOn('seRow',null);}else{SELSE={gz,Y};setOn('seRow','se-'+Y);renderWolRow(Y);}rebuild();}
function selWol(i){const w=WOLCACHE[i];if(SELWOL&&SELWOL._i===i&&SELWOL.year===WOLYEAR){SELWOL=null;setOn('wolRow',null);}else{SELWOL={gz:w.gz,_i:i,label:w.lab2,year:WOLYEAR};setOn('wolRow','wol-'+i);}rebuild();}

/* ===== 통합(원국+운) ===== */
function combined(){
  const s=CUR.s;const P=Object.assign({},s.pillars);const base=['year','month','day','hour'].filter(k=>s.pillars[k]);
  if(SELDAE)P.dae=SELDAE.gz;if(SELSE)P.se=SELSE.gz;if(SELWOL)P.wol=SELWOL.gz;
  return {P,ord:base.concat(LUCKKEYS.filter(k=>P[k]))};
}
function rebuild(){
  const {P,ord}=combined();const s=CUR.s,a=CUR.a;
  const shin=shinsalSet(P,ord,s.dGan);shin.forEach(e=>{e.luck=e.pillars.some(k=>LUCKKEYS.includes(k));});
  CUR.P=P;CUR.ord=ord;
  renderPillars(P,ord);renderStage(s,a,shin,spiritSet(P,ord));
  const anyLuck=!!(SELDAE||SELSE||SELWOL);
  const rels=computeRelations(P,ord).filter(r=>{const ks=r.tri?r.tri:[r.ki,r.kj];return anyLuck?ks.some(k=>LUCKKEYS.includes(k)):false;});
  CUR.rels=rels;
  renderRelList(rels);clearRel();const f=document.getElementById('fxSel');if(f)f.innerHTML='';CURSEL=null;
  applyLuckReactions();renderSummary();renderDogam();
}
/* ===== 신살 도감 ===== */
function dogamDesc(c){
  if(c.kind==='animal')return '나를 상징하는 일주 동물이에요. '+(c.note||'');
  if(c.kind==='spirit'){const ei=ELEM_INFO[c.hanja]||{};return WX_KO[c.hanja]+' 기운('+c.hanja+')이 '+(c.types?c.types.join('·'):'합')+'으로 강해졌어요 — '+(ei.mind||'');}
  const o=SS_INFO[c.key]||{};return o.d||o.b||o.g||c.note||'';
}
function dogamTok(c){
  if(c.kind==='animal')return SC.animalToken(c.key,WX_KO[GAN_WX[CUR.s.dGan]],54);
  return SC.specialToken(c.key,54);
}
function rolePill(role){
  if(role==='길신'||role==='길')return ['#EAF3DE','#2e6b14','길'];
  if(role==='흉신'||role==='흉')return ['#F6E2E0','#a3301f','흉'];
  if(role==='양면')return ['#FAEEDA','#7a4b08','양면'];
  if(role==='오행')return ['#eaf3fb','#1d5a8a','오행'];
  return ['#eef0f2','#555','일주'];
}
function dogamCard(i,c){
  const rp=rolePill(c.role);
  const strLabel={1:'약',2:'중',3:'강'}[(c.str&&c.str.w)||2];
  const srcTag=c.luck?(c.lucksrc==='se'?'세운':c.lucksrc==='wol'?'월운':c.lucksrc==='dae'?'대운':'운'):'원국';
  return `<div class="dgcard" onclick="dogamToggle(${i})">`
   +`<div class="dgtok">${dogamTok(c)}</div>`
   +`<div><div class="dgnm">${c.name}</div>`
   +`<div class="dgbadges"><span class="dgb" style="background:${rp[0]};color:${rp[1]}">${rp[2]}</span>`
   +`<span class="dgb" style="background:#eef0f2;color:#555">${srcTag}</span>`
   +`<span class="dgb" style="background:#f3eefc;color:#6a4ad0">세기 ${strLabel}</span></div>`
   +`<div class="dgdesc">${dogamDesc(c)}</div></div>`
   +`<div class="dgfull" id="dgfull-${i}"></div></div>`;
}
function dogamToggle(i){const el=document.getElementById('dgfull-'+i);if(!el)return;
  if(el.style.display==='block'){el.style.display='none';el.innerHTML='';return;}
  const c=STAGE[i];const refkw=REFKEY[c.key];
  el.innerHTML=charDetail(c)+(refkw?refsHtml(refkw):'');el.style.display='block';
}
function renderDogam(){const box=document.getElementById('dogamBox');if(!box)return;
  if(!STAGE.length){box.innerHTML='<div class="infohint" style="padding:8px">사주를 소환하면 캐릭터가 도감으로 모입니다.</div>';return;}
  const groups=[['animal','일주 — 나'],['spirit','오행 기운'],['shinsal','신살·귀인']];
  let h=`<div class="predhint" style="margin-bottom:4px">지금 원국과 선택한 운에 뜬 캐릭터 ${STAGE.length}종이에요. 카드를 누르면 자세한 설명과 옛 명리책 근거가 열려요. (운을 바꾸면 도감도 함께 갱신돼요.)</div>`;
  groups.forEach(g=>{const items=STAGE.map((c,i)=>[c,i]).filter(p=>p[0].kind===g[0]);if(!items.length)return;
    h+=`<div class="dggrp">${g[1]} <span style="color:var(--sub);font-weight:400">· ${items.length}종</span></div>`
      +`<div class="dggrid">`+items.map(p=>dogamCard(p[1],p[0])).join('')+`</div>`;});
  box.innerHTML=h;
}

/* ===== 기둥 표 ===== */
function wxSpanBox(c,big,id){const w=wxOf(c);return `<div class="gz ${WXCLASS[w]}${big?'':' sm'}"${id?' id="'+id+'"':''}>${c}</div>`;}
const DISP=['wol','se','dae','hour','day','month','year'];
function renderPillars(P,ord){
  const dg=CUR.s.dGan,ua=CUR.ua;
  document.getElementById('pillars').innerHTML=DISP.filter(k=>ord.includes(k)).map(k=>{
    const g=P[k][0],z=P[k][1],luck=LUCKKEYS.includes(k);
    const ss=(k==='day')?'<b>일간</b>':sipsin(dg,g);
    const tw=twelveStage(dg,z);
    const hid=(JANGGAN[z]||HIDDEN[z]).map(h=>h+'<small style="color:#7c4dff">'+(sipsin(dg,h)||'')+'</small>').join(' ');
    if(luck){const [m,c]=luckMark(judgeLuck(g+z,ua.use,ua.avoid));
      const lab=k==='dae'?('대운 '+(SELDAE?SELDAE.age+'세':'')):k==='se'?('세운 '+(SELSE?SELSE.Y:'')):('월운 '+(SELWOL?SELWOL.label:''));
      return `<div class="pcol luck" id="pcol-${k}"><div class="gung" style="color:#6a4ad0">${lab}<small>${GUNGX[k][1]}</small></div><div class="ss">${ss}</div>${wxSpanBox(g,true,'gz-'+k+'-g')}${wxSpanBox(z,true,'gz-'+k+'-z')}<div class="lmk ${c}">${m}</div><div class="twf">${tw}</div><div class="hidn">${hid}</div></div>`;}
    const gd=SC.GUNG_SYM[GUNGKEY[k]];
    const gsym=(wc,sz)=>`<span class="gsym" id="gsym-${k}-${wc}">${symFor(k,wc,null,null,null,sz)}</span>`;
    const gName=(k==='day')?'의식속의 나':SC.GUNG_SYM[POSKEY[k].g].gung, zName=SC.GUNG_SYM[POSKEY[k].z].gung;
    return `<div class="pcol" id="pcol-${k}">
      <div class="gunghead">${gsym('pillar',40)}<div class="gung">${gd.gung}<small>${GUNGX[k][1]}</small></div></div>
      <div class="ss">${ss}</div>
      <div class="gzrow">${gsym('g',34)}${wxSpanBox(g,true,'gz-'+k+'-g')}</div><div class="poscap">${gName}</div>
      <div class="gzrow">${gsym('z',34)}${wxSpanBox(z,true,'gz-'+k+'-z')}</div><div class="poscap">${zName}</div>
      <div class="twf">${tw}</div><div class="hidn">${hid}</div>
    </div>`;
  }).join('');
}

/* ===== 캐릭터 무대 ===== */
// 영향력 세기(약1/중2/강3) — 엔진 자료(십이운성·통근·합종류·위치·중복)로 가늠
const LIFE_STRONG=new Set(['장생','관대','건록','제왕']),LIFE_MID=new Set(['목욕','양','태']);
function lvName(w){return w===3?'강':(w===2?'중':'약');}
function posW(k){return (k==='day'||k==='month')?2:1;}
function charStrength(c){
  const P=CUR.P,a=CUR.a;
  if(c.kind==='animal'){const v=a.cls.strength.verdict,w=v==='신강'?3:(v==='신약'?1:2);return {lv:lvName(w),w,why:'일간 '+v};}
  if(c.kind==='spirit'){let sc=0;const T={삼합:3,방합:2,반합:1,육합:0},prim=(c.types&&c.types[0])||c.combo;
    sc+=T[prim]||0;if(c.types&&c.types.length>1)sc+=1;sc+=Math.max(0,c.branches.length-2);
    const wang={'水':'子','木':'卯','火':'午','金':'酉'}[c.hanja],wj=wang&&c.branches.includes(wang);if(wj)sc+=1;
    const stems=Object.keys(P).map(k=>P[k][0]),tu=stems.some(g=>GAN_WX[g]===c.hanja);if(tu)sc+=1;
    const w=sc>=4?3:(sc>=2?2:1);const why=[(c.types||[c.combo]).join('·')];if(wj)why.push('왕지');if(tu)why.push('투출');
    return {lv:lvName(w),w,why:why.join('·')};}
  // 신살
  let sc=0;const reasons=[];
  const best=c.targets.reduce((m,t)=>Math.max(m,posW(t.k)),0);sc+=best;if(best>=2)reasons.push('월·일 자리');
  let lf=0;c.targets.forEach(t=>{const tw=twelveStage(P[t.k][0],P[t.k][1]);if(LIFE_STRONG.has(tw))lf=Math.max(lf,2);else if(LIFE_MID.has(tw))lf=Math.max(lf,1);});
  if(lf>=2){sc+=2;reasons.push('왕지 기력');}else if(lf===1)sc+=1;
  const extra=c.pillars.length-1;if(extra>0){sc+=extra;reasons.push('중복'+(extra+1));}
  const stems=Object.keys(P).map(k=>P[k][0]),branchEls=c.targets.map(t=>ZHI_WX[P[t.k][1]]);
  if(branchEls.some(e=>stems.some(g=>GAN_WX[g]===e))){sc+=1;reasons.push('통근');}
  const w=sc>=5?3:(sc>=3?2:1);return {lv:lvName(w),w,why:reasons.join('·')||'기본'};
}
function charCardHtml(idx,c){
  const w=c.str?c.str.w:2;
  return `<div class="charcard${c.kind==='animal'?' big':''}" data-idx="${idx}" onclick="selChar(${idx})">
    <span class="stag s${w}">${c.str?c.str.lv:'중'}</span>
    ${c.luck?'<span class="lk">운</span>':''}${c.svg}<div class="charname">${c.name}</div>
    <div class="charrole ${roleClass(c.role)}">${roleLabel(c.role)}</div></div>`;
}
function renderStage(s,a,shin,spirits){
  STAGE=[];const dz=s.pillars.day[1],dgw=GAN_WX[s.dGan];
  STAGE.push({kind:'animal',key:dz,name:ZHI_KO[dz]+' ('+s.pillars.day+'일주)',role:'일주',targets:[{k:'day',which:'z'}],pillars:['day'],color:'#2aa198',svg:SC.animalToken(dz,WX_KO[dgw],76),note:'일간 '+GAN_KO[s.dGan]+'('+dgw+') · 배우자궁'});
  spirits.forEach(sp=>{const o=SC.SPECIALS[sp.key];const luck=sp.targets.some(t=>LUCKKEYS.includes(t.k));
    STAGE.push({kind:'spirit',luck,key:sp.key,hanja:sp.hanja,combo:sp.combo,types:sp.types,branches:sp.branches,
      name:o.name+' · '+sp.types.join('·'),role:'오행',targets:sp.targets,pillars:[...new Set(sp.targets.map(t=>t.k))],
      color:WXLINE[sp.hanja]||relColor(sp.hanja,dgw),svg:SC.specialToken(sp.key,60),note:sp.branches.join('')+' '+sp.types.join('·')});});
  shin.forEach(e=>{const o=SC.SPECIALS[e.key];if(!o)return;
    const src=e.pillars.indexOf('se')>=0?'se':(e.pillars.indexOf('wol')>=0?'wol':(e.pillars.indexOf('dae')>=0?'dae':null));
    STAGE.push({kind:'shinsal',luck:!!e.luck,lucksrc:src,key:e.key,name:o.name,role:o.role,targets:e.targets,pillars:e.pillars,color:roleLineColor(o.role),svg:SC.specialToken(e.key,60),note:o.sub});});
  STAGE.forEach(c=>{c.str=charStrength(c);});
  const orig=[],luck=[];
  STAGE.forEach((c,i)=>{(c.luck?luck:orig).push(charCardHtml(i,c));});
  document.getElementById('cellsOrig').innerHTML=orig.join('');
  document.getElementById('cellsLuck').innerHTML=luck.length?luck.join(''):'<div class="luckhint">아래에서 대운·세운·월운을<br>선택해 보세요</div>';
}

/* ===== 좌표/그리기 ===== */
function glyphXY(cont,k,which){const el=document.getElementById('gz-'+k+'-'+which);if(!el)return null;const r=el.getBoundingClientRect();return {x:r.left-cont.left+r.width/2,y:r.top-cont.top+r.height/2};}
function fxSize(svg){const result=document.getElementById('result');const cont=result.getBoundingClientRect();svg.setAttribute('width',cont.width);svg.setAttribute('height',result.scrollHeight);svg.style.height=result.scrollHeight+'px';return cont;}
function clearSel(){document.querySelectorAll('.pcol').forEach(el=>{el.style.boxShadow='';el.style.borderColor='';});document.querySelectorAll('.charcard').forEach(el=>el.classList.remove('sel'));const f=document.getElementById('fxSel');if(f)f.innerHTML='';applyLuckReactions();CURSEL=null;}
function exprOf(c){const r=c.role;
  if(r==='길신'||r==='길')return 'happy';
  if(r==='흉신'||r==='흉')return 'sad';
  if(c.kind==='spirit'){const e=c.hanja,d=GAN_WX[CUR.s.dGan];if(KE[e]===d)return 'sad';if(SHENG[e]===d||e===d)return 'happy';return 'surprise';}
  if(r==='양면')return 'surprise';
  return 'happy';}
function selChar(i){
  const c=STAGE[i];clearSel();clearRel();CURSEL=i;
  const cardEl=document.querySelector('.charcard[data-idx="'+i+'"]');if(cardEl)cardEl.classList.add('sel');
  const w=(c.str?c.str.w:2);
  const W={1:2.5,2:6,3:11},R={1:15,2:24,3:33},RW={1:2,2:4,3:7},INS={1:2,2:4,3:6},BLUR={1:5,2:24,3:48},AL={1:.35,2:.6,3:.9};
  c.pillars.forEach(k=>{const el=document.getElementById('pcol-'+k);if(el){el.style.borderColor=c.color;el.style.boxShadow='inset 0 0 0 '+INS[w]+'px '+c.color+', 0 0 '+BLUR[w]+'px '+hex2rgba(c.color,AL[w]);}});
  const fx=document.getElementById('fxSel');const cont=fxSize(fx);
  const cr=cardEl.getBoundingClientRect();const x1=cr.left-cont.left+cr.width/2,y1=cr.bottom-cont.top-8;let svg='';
  const halo=(d)=>w>=2?('<path fill="none" d="'+d+'" stroke="'+c.color+'" stroke-width="'+(W[w]*2.5)+'" stroke-linecap="round" opacity="'+(w===3?.36:.2)+'"/>'):'';
  c.targets.forEach(t=>{const pt=glyphXY(cont,t.k,t.which);if(!pt)return;const my=(y1+pt.y)/2;
    const d='M'+x1+','+y1+' C'+x1+','+my+' '+pt.x+','+my+' '+pt.x+','+pt.y;
    svg+=halo(d)+'<path class="fxline" fill="none" stroke="'+c.color+'" stroke-width="'+W[w]+'" stroke-dasharray="9 7" d="'+d+'"/>';
    svg+='<circle class="fxdot" cx="'+pt.x+'" cy="'+pt.y+'" r="'+R[w]+'" fill="none" stroke="'+c.color+'" stroke-width="'+RW[w]+'"/>';});
  if(c.kind==='spirit'&&c.targets.length>=2){for(let k=0;k<c.targets.length;k++){const A=glyphXY(cont,c.targets[k].k,c.targets[k].which),B=glyphXY(cont,c.targets[(k+1)%c.targets.length].k,c.targets[(k+1)%c.targets.length].which);if(A&&B){const d='M'+A.x+','+A.y+' L'+B.x+','+B.y;svg+=halo(d)+'<path class="fxline" fill="none" stroke="'+c.color+'" stroke-width="'+W[w]+'" stroke-dasharray="8 7" d="'+d+'"/>';}}}
  fx.innerHTML=svg;
  clearGung();const _e=exprOf(c);
  c.targets.forEach(t=>{if(GUNGKEY[t.k])setGung(t.k,t.which,_e,w);});
  [...new Set(c.targets.map(t=>t.k))].forEach(k=>{if(GUNGKEY[k])setGung(k,'pillar',_e,w);});
  const refkw=REFKEY[c.key],refsB=refkw?refsHtml(refkw):'';
  document.getElementById('info').innerHTML=`<div class="infobox" style="border-color:${hex2rgba(c.color,.55)}">${charDetail(c)}${refsB}</div>`;
}

/* ===== 합·충 관계선 ===== */
function computeRelations(P,ord){
  const rel=[];const br=k=>P[k][1],st=k=>P[k][0];
  for(let i=0;i<ord.length;i++)for(let j=i+1;j<ord.length;j++){const ki=ord[i],kj=ord[j];
    const gk=pairKey(st(ki),st(kj),GAN);
    if(GAN_HE[gk])rel.push({ki,kj,which:'g',type:'천간합',el:GAN_HE[gk]});
    else if(GAN_CHONG.has(gk))rel.push({ki,kj,which:'g',type:'충'});
    const zk=pairKey(br(ki),br(kj),ZHI);
    if(ZHI_LIUHE.has(zk))rel.push({ki,kj,which:'z',type:'육합'});
    else if(ZHI_CHONG.has(zk))rel.push({ki,kj,which:'z',type:'충'});
    else if(ZHI_XING.has(zk))rel.push({ki,kj,which:'z',type:'형'});
    else if(ZHI_PA.has(zk))rel.push({ki,kj,which:'z',type:'파'});
    else if(ZHI_HAI.has(zk))rel.push({ki,kj,which:'z',type:'해'});
  }
  for(const combo in ZHI_SANHE){const cols=combo.split('').map(b=>ord.filter(k=>br(k)===b));
    if(cols.every(arr=>arr.length))rel.push({tri:cols.map(arr=>arr[0]),which:'z',type:'삼합',el:ZHI_SANHE[combo]});}
  return rel;
}
function relStyle(r){const use=CUR.ua.use;
  if(r.type==='천간합'||r.type==='삼합'){const strong=r.el&&use.has(r.el);return {col:strong?'#2f9e57':'#d98a2a',lab:(r.type==='삼합'?'삼합':'합')+(r.el?'·'+WX_KO[r.el]:'')+(strong?' ▲강화':' 묶임')};}
  if(r.type==='육합')return {col:'#d98a2a',lab:'육합 묶임'};
  if(r.type==='충')return {col:'#d23b2a',lab:'충 ✕흔들림'};
  if(r.type==='형')return {col:'#d98a2a',lab:'형 마찰'};
  if(r.type==='파')return {col:'#9a5cc0',lab:'파'};
  if(r.type==='해')return {col:'#5a8ac0',lab:'해'};
  return {col:'#888',lab:r.type};
}
function relChip(x,y,text,col){const w=text.length*7.5+14;return `<rect class="relchipbg" x="${x-w/2}" y="${y-10}" width="${w}" height="20" rx="7"/><text class="reltext" x="${x}" y="${y+4}" text-anchor="middle" fill="${col}">${text}</text>`;}
const COLLAB={year:'년주',month:'월주',day:'일주',hour:'시주',dae:'대운',se:'세운',wol:'월운'};
function colLabel(k){return COLLAB[k]||k;}
function relMeaning(r){
  if(r.type==='천간합'||r.type==='삼합'){const strong=r.el&&CUR.ua.use.has(r.el);
    return strong?('두 기운이 '+(WX_KO[r.el]||'')+'(으)로 합하여 용신 오행이 강해집니다 — 힘이 세짐.'):('두 글자가 합으로 묶여(합거) 서로의 작용이 약해집니다 — 묶임.');}
  if(r.type==='육합')return '두 지지가 합으로 묶여 안정되나 움직임이 둔해질 수 있습니다.';
  if(r.type==='충')return '두 기운이 정면충돌 — 해당 궁/글자가 흔들리고 변동·이동·갈등이 생깁니다.';
  if(r.type==='형')return '서로 마찰·갈등 — 시비·관재·수술수 등에 주의.';
  if(r.type==='파')return '깨짐 — 관계나 일이 틀어지거나 중단될 수 있습니다.';
  if(r.type==='해')return '은근한 손상·방해 — 더디고 거슬리는 일.';
  return '';
}
function renderRelList(rels){
  CUR.rels=rels;const box=document.getElementById('relList'),ttl=document.getElementById('relTitle');
  if(!rels.length){box.className='';if(ttl){ttl.className='sectitle';ttl.textContent='합·충·형·파·해 — 운을 선택하면 표시됩니다';}
    box.innerHTML='<div class="infohint" style="padding:8px">운(대운·세운·월운)을 선택하면 합·충 관계가 여기에 표시됩니다.</div>';return;}
  if(ttl){ttl.className='sectitle hot';ttl.textContent='⚡ 운과의 합·충·형·파·해 '+rels.length+'개 — 칩을 눌러 상세 보기';}
  box.className='hot';
  box.innerHTML=rels.map((r,i)=>{const st=relStyle(r);const cols=(r.tri?r.tri:[r.ki,r.kj]).map(colLabel).join('·');
    return `<span class="relpill" id="relpill-${i}" onclick="showRel(${i})" style="border-color:${st.col};color:${st.col}">● ${cols} · ${st.lab}</span>`;}).join('');
}
function clearRel(){document.querySelectorAll('.gz').forEach(el=>{el.style.outline='';el.style.outlineOffset='';});
  document.querySelectorAll('.pcol').forEach(el=>{if(CURSEL==null){el.style.boxShadow='';el.style.borderColor='';}});
  const f=document.getElementById('fxRel');if(f)f.innerHTML='';
  document.querySelectorAll('#relList .relpill').forEach(e=>e.classList.remove('on'));CURREL=null;}
function infohintHTML(){return '<div class="infohint">위 캐릭터(또는 합·충 칩)를 누르면 상세 설명이 여기에 나타납니다.</div>';}
function showRel(i){
  const r=CUR.rels[i];if(!r)return;
  if(CURREL===i){clearRel();document.getElementById('info').innerHTML=infohintHTML();return;}
  clearSel();clearRel();CURREL=i;
  const st=relStyle(r);const cols=r.tri?r.tri:[r.ki,r.kj];
  const chip=document.getElementById('relpill-'+i);if(chip)chip.classList.add('on');
  cols.forEach(k=>{const el=document.getElementById('pcol-'+k);if(el){el.style.borderColor=st.col;el.style.boxShadow='0 0 16px '+hex2rgba(st.col,.5);}});
  const fx=document.getElementById('fxSel');const cont=fxSize(fx);let svg='';
  const pts=(r.tri?r.tri.map(k=>({k,w:'z'})):[{k:r.ki,w:r.which},{k:r.kj,w:r.which}]).map(o=>{const p=glyphXY(cont,o.k,o.w);return p?Object.assign({},p,o):null;}).filter(Boolean);
  const ring=p=>`<circle class="fxdot" cx="${p.x}" cy="${p.y}" r="24" fill="none" stroke="${st.col}" stroke-width="4"/>`;
  if(pts.length>=3){for(let k=0;k<3;k++){const p=pts[k],q=pts[(k+1)%3];svg+=`<line class="fxline" x1="${p.x}" y1="${p.y}" x2="${q.x}" y2="${q.y}" stroke="${st.col}" stroke-width="5" stroke-dasharray="10 8"/>`;}pts.forEach(p=>svg+=ring(p));const cx=pts.reduce((a,p)=>a+p.x,0)/3,cy=pts.reduce((a,p)=>a+p.y,0)/3;svg+=relChip(cx,cy,st.lab,st.col);}
  else if(pts.length===2){const p=pts[0],q=pts[1],up=(r.which==='g'),mx=(p.x+q.x)/2,my=(p.y+q.y)/2+(up?-34:34);
    svg+=`<path class="fxline" fill="none" d="M${p.x},${p.y} Q${mx},${my} ${q.x},${q.y}" stroke="${st.col}" stroke-width="5" stroke-dasharray="${r.type==='충'?'9 7':'12 0'}"/>`;svg+=ring(p)+ring(q);svg+=relChip(mx,my,st.lab,st.col);}
  fx.innerHTML=svg;
  pts.forEach(o=>{const el=document.getElementById('gz-'+o.k+'-'+o.w);if(el){el.style.outline='3px solid '+st.col;el.style.outlineOffset='2px';}});
  const gi=luckGlyphInfo(r);let inner;
  if(gi){const sc=judgeLuck(CUR.P[gi.lk],CUR.ua.use,CUR.ua.avoid);inner=buildPlain(gi,sc);}
  else{inner=`<h3 style="color:${st.col}">${st.lab}</h3><div class="meta">${cols.map(colLabel).join(' ↔ ')}</div><div class="line">${relMeaning(r)}</div>`;}
  const refsB=gi?refsHtml(REFKEY[gi.ss]):'';
  document.getElementById('info').innerHTML=`<div class="infobox" style="border-color:${hex2rgba(st.col,.55)}">${inner}${refsB}</div>`;
}
window.addEventListener('resize',()=>{if(!CUR)return;if(CURREL!=null){const i=CURREL;CURREL=null;showRel(i);}else if(CURSEL!=null)selChar(CURSEL);});

/* ===== 태어난 시간 추정 ===== */
const SIJI=[['子',0,'한밤 23~01시'],['丑',2,'한밤 01~03시'],['寅',4,'새벽 03~05시'],['卯',6,'새벽 05~07시'],['辰',8,'아침 07~09시'],['巳',10,'아침 09~11시'],['午',12,'한낮 11~13시'],['未',14,'한낮 13~15시'],['申',16,'오후 15~17시'],['酉',18,'오후 17~19시'],['戌',20,'저녁 19~21시'],['亥',22,'밤 21~23시']];
function openPred(){document.getElementById('predModal').classList.remove('hidden');}
function closePred(){document.getElementById('predModal').classList.add('hidden');}
function qv(name){const el=document.querySelector('input[name="'+name+'"]:checked');return el?el.value:'';}
const PRED_BAND={새벽:['寅','卯'],아침:['辰','巳'],한낮:['午','未'],오후:['申','酉'],저녁:['戌','亥'],한밤:['子','丑']};
const PRED_RH={아침형:['寅','卯','辰','巳'],중간:['午','未','申','酉'],저녁형:['戌','亥','子','丑']};
const PRED_SL={바로:['子','午','卯','酉'],옆으로:['寅','申','巳','亥'],엎드려:['辰','戌','丑','未']};
function sajuForHour(h){
  const g=id=>document.getElementById(id).value;
  let Y=+g('y'),M=+g('m'),D=+g('d');
  if(CAL==='lunar'){const sol=lunarToSolar(Y,M,D,document.getElementById('leap').value==='1');if(sol){Y=sol[0];M=sol[1];D=sol[2];}}
  let cY=Y,cM=M,cD=D,cH=h,cMi=0;
  if(LST){const dt=new Date(Date.UTC(Y,M-1,D,h,0));dt.setUTCMinutes(dt.getUTCMinutes()-LST_MIN);cY=dt.getUTCFullYear();cM=dt.getUTCMonth()+1;cD=dt.getUTCDate();cH=dt.getUTCHours();cMi=dt.getUTCMinutes();}
  return computeSaju(cY,cM,cD,cH,cMi,SEX,TZ);
}
function folkScore(z){let s=0;const r=qv('pq2'),sl=qv('pq3');if(PRED_RH[r]&&PRED_RH[r].indexOf(z)>=0)s+=2;if(PRED_SL[sl]&&PRED_SL[sl].indexOf(z)>=0)s+=1;return s;}
function chartScore(sa,reasons){
  const dg=sa.dGan,hz=sa.pillars.hour;if(!hz)return 0;const sg=hz[0],sz=hz[1];
  const ss=[sipsin(dg,sg),sipsin(dg,HIDDEN[sz][0])],sh=shensha(dg,sa.pillars.year[1],[sz]),wx=ZHI_WX[sz];
  const has=k=>ss.indexOf(k)>=0;let s=0;
  const q6=qv('pq6');
  if(q6==='리더'&&(sh['양인']||['寅','午','戌'].indexOf(sz)>=0||has('편관'))){s+=3;reasons.push('주도적 성격↔시주 기운');}
  if(q6==='예술'&&(sh['화개']||['卯','未','亥'].indexOf(sz)>=0)){s+=3;reasons.push('예술 감성↔화개/시지');}
  if(q6==='분석'&&(['金','水'].indexOf(wx)>=0||['酉','子'].indexOf(sz)>=0)){s+=3;reasons.push('분석·예민↔금수 시지');}
  if(q6==='사교'&&(sh['도화']||['午','巳'].indexOf(sz)>=0)){s+=3;reasons.push('사교·인기↔도화/시지');}
  if(q6==='성실'&&(wx==='土'||['丑','辰','未','戌'].indexOf(sz)>=0)){s+=3;reasons.push('성실·안정↔토 시지');}
  const q5=qv('pq5');
  if(q5==='재물'&&(has('정재')||has('편재'))){s+=3;reasons.push('말년 재물↔시주 재성');}
  if(q5==='공부'&&(has('정인')||has('편인')||sh['화개'])){s+=3;reasons.push('말년 공부·종교↔시주 인성/화개');}
  if(q5==='활동'&&(has('식신')||has('상관')||sh['역마'])){s+=3;reasons.push('말년 활동·이동↔시주 식상/역마');}
  if(q5==='명예'&&(has('정관')||has('편관'))){s+=3;reasons.push('말년 명예↔시주 관성');}
  const q4=qv('pq4'),childSS=(SEX==='남')?['정관','편관']:['식신','상관'];
  if(q4==='가깝다'&&childSS.some(has)){s+=2;reasons.push('자녀와 가까움↔시주 자녀성');}
  if(q4==='반듯'&&has('정관')){s+=2;reasons.push('반듯한 자녀↔시주 정관');}
  if(q4==='독립'&&(has('편관')||sh['양인'])){s+=2;reasons.push('독립적 자녀↔시주 칠살/양인');}
  return s;
}
function applyPred(){
  const band=qv('pq1');const cands=[];
  SIJI.forEach(si=>{let sa;try{sa=sajuForHour(si[1]);}catch(e){return;}
    const sz=(sa.pillars.hour?sa.pillars.hour[1]:si[0]);const reasons=[];
    let sc=folkScore(sz)+chartScore(sa,reasons);
    if(band&&PRED_BAND[band]){if(PRED_BAND[band].indexOf(sz)>=0)sc+=5;else sc-=100;}
    cands.push({z:si[0],hour:si[1],label:si[2],score:sc,sa,reasons});});
  cands.sort((a,b)=>b.score-a.score);
  const best=cands[0];if(!best||best.score<=0){alert('항목을 한 개 이상 선택해주세요.');return;}
  document.getElementById('h').value=best.hour;closePred();
  const hz=best.sa.pillars.hour||(best.z);
  let note='🕒 추정 시간: <b>'+best.z+'시 ('+best.label+')</b> → 시 칸에 '+String(best.hour).padStart(2,'0')+'시로 넣었어요. (시주 '+(best.sa.pillars.hour||'?')+')';
  if(best.reasons.length)note+='<br><span style="font-weight:400;color:var(--sub)">근거: '+[...new Set(best.reasons)].join(' · ')+'</span>';
  const near=cands.filter(c=>c.score>=best.score-1&&c.z!==best.z).slice(0,2);
  if(near.length)note+='<br><span style="font-weight:400;color:var(--sub)">비슷한 후보: '+near.map(c=>c.z+'시').join(', ')+'</span>';
  note+='<br>「사주 캐릭터 소환」을 눌러 확인하세요. (추정이라 실제와 다를 수 있어요)';
  document.getElementById('predNote').innerHTML=note;
}
fillForm();
</script>
</body>
</html>
"""

html = (TEMPLATE
        .replace("__CHARS__", CHARS)
        .replace("__JIEQI__", JIEQI)
        .replace("__LUNAR__", LUNAR)
        .replace("__GAMEREFS__", GAME_REFS)
        .replace("__ENGINE__", ENGINE))

out = os.path.join(HERE, "saju_game.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("wrote", out, len(html), "bytes")
