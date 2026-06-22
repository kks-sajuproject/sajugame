# -*- coding: utf-8 -*-
"""④ 단일 HTML 사주 분석기 빌더. 절기·음력 테이블을 주입해 자립형 saju_web.html 생성.
   서버 불필요(더블클릭 실행). 만세력·십신·신살·합충·강약·격국·용신·대운을 JS로 산출.
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
jieqi = open(os.path.join(HERE,"jieqi_table.json")).read()
lunar = open(os.path.join(HERE,"lunar_table.json")).read()
refs  = open(os.path.join(HERE,"refs_table.json"), encoding="utf-8").read()

HTML = r"""<!DOCTYPE html>
<html lang="ko" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>사주 분석기 · 命理</title>
<meta name="theme-color" content="#3a5bd9">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="사주분석">
<link rel="manifest" href="manifest.webmanifest">
<style>
:root{
  --bg:#0f1115; --surface:#171a21; --surface2:#1e222c; --line:#2a2f3a;
  --txt:#e8eaed; --muted:#9aa0ac; --accent:#7c9cff; --accent2:#b388ff;
  --mok:#4caf72; --hwa:#e2574c; --to:#d4a23a; --geum:#cfd4dc; --su:#5b8def;
  --radius:14px; --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.25);
}
[data-theme="light"]{
  --bg:#f6f7f9; --surface:#ffffff; --surface2:#f0f2f5; --line:#e3e6ea;
  --txt:#1a1d23; --muted:#5d646f; --accent:#3a5bd9; --accent2:#7c4dff;
  --geum:#6b7280; --shadow:0 1px 2px rgba(0,0,0,.06),0 8px 24px rgba(0,0,0,.08);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
  line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:920px;margin:0 auto;padding:32px 20px 80px}
header{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px}
h1{font-size:21px;font-weight:600;margin:0;letter-spacing:-.02em}
h1 span{color:var(--muted);font-weight:400;font-size:15px;margin-left:8px}
.theme-btn{background:var(--surface2);border:1px solid var(--line);color:var(--muted);
  border-radius:10px;padding:7px 12px;cursor:pointer;font-size:13px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  box-shadow:var(--shadow);padding:22px;margin-bottom:18px}
.form-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:14px}
label{display:block;font-size:12px;color:var(--muted);margin-bottom:6px;font-weight:500}
select,input{width:100%;background:var(--surface2);border:1px solid var(--line);color:var(--txt);
  border-radius:10px;padding:10px 11px;font-size:14px;font-family:inherit;-webkit-appearance:none}
select:focus,input:focus{outline:none;border-color:var(--accent)}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:14px}
.seg{display:inline-flex;background:var(--surface2);border:1px solid var(--line);border-radius:10px;padding:3px}
.seg button{background:none;border:none;color:var(--muted);padding:7px 14px;border-radius:8px;cursor:pointer;font-size:13px;font-family:inherit}
.seg button.on{background:var(--accent);color:#fff}
.go{margin-top:18px;width:100%;background:linear-gradient(135deg,var(--accent),var(--accent2));
  color:#fff;border:none;border-radius:12px;padding:14px;font-size:15px;font-weight:600;cursor:pointer;letter-spacing:.02em}
.go:active{transform:translateY(1px)}
.hidden{display:none}
#result{animation:fade .4s ease}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.pillars{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:6px 0 4px}
.pillars.wide{display:flex;gap:7px;overflow-x:auto;padding-bottom:6px}
.pillars.wide .pcol{flex:0 0 auto;min-width:74px;padding:10px 5px}
.pillarrow{display:flex;gap:14px;align-items:stretch;flex-wrap:wrap}
.pillarrow .pillars.wide{flex:1 1 auto;min-width:0}
.animal-card{flex:0 0 158px;width:158px;border-radius:14px;padding:16px 14px;color:#fff;box-shadow:var(--shadow);text-align:center}
.ac-emoji{font-size:52px;line-height:1.1} .ac-title{font-size:14.5px;font-weight:700;margin-top:6px}
.ac-sub{font-size:12px;opacity:.9;margin-top:2px} .ac-trait{font-size:11.5px;line-height:1.65;margin-top:10px;text-align:left;opacity:.96}
.ac-trait b{color:#fff} @media(max-width:560px){.animal-card{flex:1 1 100%;width:auto}}
.char-info{flex:1 1 180px;min-width:160px;background:var(--surface2);border:1px solid var(--line);border-radius:12px;padding:14px}
.char-info .ci-title{font-size:13px;font-weight:700} .char-info .ci-ch{display:inline-block;background:var(--accent);color:#fff;border-radius:6px;padding:1px 8px;font-size:15px;margin-right:4px}
.char-info .luck-good{font-weight:700} .char-info .luck-bad{font-weight:700}
@media(max-width:560px){.char-info{flex:1 1 100%}}
.gbox{font-size:25px;font-weight:700;line-height:1;padding:7px 0;border-radius:7px;margin:3px 0;color:#fff;text-align:center;cursor:pointer;position:relative}
.gbox.rel-self{outline:3px solid #fff;outline-offset:1px}
.gbox.rel-he-box{outline:3px solid #36d576;outline-offset:1px}
.gbox.rel-chong-box{outline:3px dashed #ff5a5a;outline-offset:1px}
.wx-mokb{background:#3a8f5a} .wx-hwab{background:#c0392b} .wx-tob{background:#b8860b} .wx-geumb{background:#8a929e} .wx-sub{background:#2c3e50}
.hss{font-size:10px;color:var(--accent);margin-top:6px;line-height:1.4} .hgan{font-size:12px;color:var(--muted);letter-spacing:1px}
.tw{font-size:11px;color:var(--txt);margin-top:5px;font-weight:600} .ssal{font-size:10px;color:var(--muted);margin-top:5px;line-height:1.5}
.pcol-luck{outline:2px solid var(--accent);outline-offset:-1px} .pcol-day .pos{color:var(--accent);font-weight:700}
.rel-he{border-color:var(--mok)!important} .rel-chong{border-color:var(--hwa)!important} .rel-xing{border-color:var(--to)!important}
.rel-pa{border-color:var(--accent2)!important} .rel-hai{border-color:var(--su)!important} .rel-won{border-color:var(--muted)!important}
.pcol{background:var(--surface2);border:1px solid var(--line);border-radius:12px;padding:14px 8px;text-align:center}
.pcol .pos{font-size:11px;color:var(--muted);margin-bottom:8px}
.pcol .ss{font-size:11px;color:var(--accent);min-height:14px}
.pcol .gz{font-size:34px;font-weight:600;line-height:1.15;margin:2px 0}
.pcol .ko{font-size:11px;color:var(--muted)}
.pcol .sub{font-size:10px;color:var(--muted);margin-top:8px;border-top:1px solid var(--line);padding-top:7px;min-height:26px}
.wx-mok{color:var(--mok)} .wx-hwa{color:var(--hwa)} .wx-to{color:var(--to)} .wx-geum{color:var(--geum)} .wx-su{color:var(--su)}
.kv{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px}
.tag{background:var(--surface2);border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:12.5px;color:var(--txt)}
.tag b{color:var(--accent);font-weight:600}
.sec-title{font-size:13px;color:var(--muted);font-weight:600;margin:18px 0 8px;letter-spacing:.02em}
.bignum{font-size:15px;font-weight:600}
.dae{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px}
.dcell{flex:0 0 auto;min-width:62px;text-align:center;background:var(--surface2);border:1px solid var(--line);border-radius:10px;padding:9px 6px}
.dcell .age{font-size:10px;color:var(--muted)} .dcell .dgz{font-size:18px;font-weight:600;margin-top:3px}
.life-sec{margin:12px 0;padding:12px 14px;background:var(--surface2);border:1px solid var(--line);border-radius:11px}
.life-t{font-size:13px;font-weight:700;color:var(--accent);margin-bottom:5px}
.deep-p{font-size:13.5px;line-height:1.75;margin:10px 0 0}
.axis-box{margin:4px 0}
.axis-row{display:flex;justify-content:space-between;align-items:center;padding:8px 2px;border-bottom:1px solid var(--line)}
.axis-name{font-size:12.5px;color:var(--muted)} .axis-pick{font-size:13.5px;font-weight:600} .axis-pick.strong{color:var(--accent)}
.cred{font-size:10.5px;font-weight:600;color:var(--mok);background:rgba(54,213,118,.13);border-radius:6px;padding:2px 7px;margin-left:5px}
.cred.low{color:var(--muted);background:var(--surface2)}
.flow-box{margin:4px 0}
.flow-row{display:flex;align-items:center;gap:9px;padding:7px 2px;border-bottom:1px solid var(--line);font-size:12.5px;flex-wrap:wrap}
.flow-age{min-width:46px;color:var(--muted)} .flow-ph{font-weight:600} .flow-d{color:var(--muted)}
.turn-list{margin:6px 0;padding-left:18px;font-size:13px;line-height:1.7} .turn-list li{margin:4px 0}
.life-sec p{margin:5px 0;font-size:13px;line-height:1.7} .life-sec b{color:var(--txt);font-weight:700}
.rune-block{margin:8px 0;padding:11px 13px;background:var(--surface2);border:1px solid var(--line);border-radius:11px}
.rune-h{font-size:14px;font-weight:700;margin-bottom:5px} .rune-block p{margin:5px 0;font-size:12.5px;line-height:1.7}
.ev{padding:7px 10px;margin:5px 0;border-radius:8px;font-size:12.5px;line-height:1.65;border-left:3px solid var(--line);background:var(--surface)}
.ev-chong{border-left-color:var(--hwa)} .ev-he{border-left-color:var(--mok)} .ev-pa{border-left-color:var(--to)} .ev-none{border-left-color:var(--line);color:var(--muted)}
.hl-c{color:var(--hwa);font-weight:700} .hl-h{color:var(--mok);font-weight:700}
.ev-ss{border-left-color:var(--accent2)} .ev-advice{border-left-color:var(--accent);background:rgba(124,156,255,.08)}
.interp p{margin:7px 0;font-size:13.5px;line-height:1.75;color:var(--txt)}
.interp b{color:var(--accent);font-weight:600}
.luck-good{color:var(--mok);font-weight:600} .luck-bad{color:var(--hwa);font-weight:600} .luck-mid{color:var(--muted)}
.dcell.click{cursor:pointer;transition:border-color .15s,transform .1s} .dcell.click:hover{border-color:var(--accent);transform:translateY(-1px)}
.se-cell.now{outline:2px solid var(--accent2);outline-offset:-1px}
.se-cell.in-dae{border-color:var(--accent);background:rgba(124,156,255,.12);box-shadow:0 0 0 1px var(--accent) inset}
.dae-cell.dae-on{border-color:var(--accent);background:rgba(124,156,255,.16)}
.ref.click{cursor:pointer} .ref.click:hover{border-color:var(--accent)} .ref .full{margin-top:8px;font-size:12.5px;line-height:1.7;color:var(--txt);display:none} .ref.open .full{display:block} .ref .more{font-size:11px;color:var(--accent);margin-top:5px}
.refs{margin-top:6px}
.ref{background:var(--surface2);border:1px solid var(--line);border-radius:10px;padding:11px 13px;margin-top:8px}
.ref .rt{font-size:12px;color:var(--accent);font-weight:600}
.ref .rb{font-size:12.5px;color:var(--muted);margin-top:4px}
.note{font-size:12px;color:var(--muted);margin-top:8px;line-height:1.6}
.disc{font-size:11.5px;color:var(--muted);margin-top:24px;text-align:center;opacity:.8}
.ex-open-btn{background:var(--surface2);border:1px solid var(--line);color:var(--txt);border-radius:11px;padding:12px 16px;cursor:pointer;font-size:14px;font-family:inherit;width:100%;font-weight:500}
.ex-open-btn:hover{border-color:var(--accent)}
.modal{position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;z-index:100;padding:20px}
.modal.hidden{display:none}
.modal-box{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;max-width:520px;width:100%;max-height:80vh;overflow:auto;box-shadow:var(--shadow)}
.modal-head{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:14px;font-weight:600;font-size:14px}
.modal-x{background:var(--surface2);border:1px solid var(--line);border-radius:8px;padding:5px 11px;cursor:pointer;color:var(--muted);font-size:14px}
.ex-cat{font-size:12px;font-weight:700;color:var(--accent);margin:12px 0 5px}
.head-actions{display:flex;gap:6px}
.head-actions button{background:var(--surface2);border:1px solid var(--line);color:var(--muted);border-radius:9px;padding:7px 10px;cursor:pointer;font-size:12px}
@media(max-width:560px){
  .wrap{padding:16px 11px 56px}
  h1{font-size:17px} h1 span{display:none}
  .pillars{gap:6px} .pcol{padding:10px 3px} .pcol .gz{font-size:25px} .pcol .sub{font-size:9px}
  .pcol .pos,.pcol .ss,.pcol .ko{font-size:10px}
  .form-grid{grid-template-columns:repeat(3,1fr);gap:10px}
  .dcell{min-width:54px} .head-actions button{padding:6px 8px;font-size:11px}
}
@media print{
  .no-print{display:none!important}
  body{background:#fff;color:#000} .wrap{max-width:100%}
  .card{box-shadow:none;border:1px solid #bbb;break-inside:avoid;page-break-inside:avoid}
  .tag,.dcell,.pcol{border-color:#ccc}
}
</style>
</head>
<body>
<div class="wrap">
  <header class="no-print">
    <h1>사주 분석기 <span>命理 · 만세력</span></h1>
    <div class="head-actions">
      <button onclick="copyLink()" id="linkBtn">🔗 링크</button>
      <button onclick="window.print()">🖨 인쇄</button>
      <button onclick="toggleTheme()">◐ 테마</button>
    </div>
  </header>

  <div class="card no-print">
    <div class="seg" id="calSeg" style="margin-bottom:16px">
      <button class="on" data-cal="solar" onclick="setCal('solar')">양력</button>
      <button data-cal="lunar" onclick="setCal('lunar')">음력</button>
    </div>
    <div class="form-grid">
      <div><label>연도</label><select id="y"></select></div>
      <div><label>월</label><select id="m"></select></div>
      <div><label>일</label><select id="d"></select></div>
      <div id="leapWrap" class="hidden"><label>윤달</label>
        <select id="leap"><option value="0">평달</option><option value="1">윤달</option></select></div>
      <div><label>시</label><select id="h"></select></div>
      <div><label>분</label><select id="mi"></select></div>
    </div>
    <div class="row">
      <div class="seg" id="sexSeg">
        <button class="on" data-sex="남" onclick="setSex('남')">남자</button>
        <button data-sex="여" onclick="setSex('여')">여자</button>
      </div>
      <div class="seg" id="lstSeg">
        <button class="on" data-lst="1" onclick="setLst('1')">진태양시 보정</button>
        <button data-lst="0" onclick="setLst('0')">표준시 그대로</button>
      </div>
    </div>
    <button class="go" onclick="analyze()">사주 분석</button>
    <div class="note" id="hint">한국 표준시(KST) 기준입니다. 시(時)를 모르면 "모름"을 선택하면 3주만 분석합니다. <b>진태양시 보정</b>은 한국 경도차(약 30분)를 반영해 시주를 더 정확히 잡습니다(대다수 한국 만세력 기본값).</div>
  </div>

  <div class="card no-print">
    <div class="seg" id="modeSeg" style="margin-bottom:14px">
      <button class="on" data-mode="single" onclick="setMode('single')">1인 분석</button>
      <button data-mode="pair" onclick="setMode('pair')">궁합 보기</button>
    </div>
    <div id="pairBox" class="hidden">
      <div class="note" style="margin:0 0 10px">상대방 정보 — 위에서 첫 번째 사람, 여기서 두 번째 사람을 입력하고 "궁합 분석"을 누르세요.</div>
      <div class="form-grid">
        <div><label>연도</label><select id="y2"></select></div>
        <div><label>월</label><select id="m2"></select></div>
        <div><label>일</label><select id="d2"></select></div>
        <div><label>시</label><select id="h2"></select></div>
        <div><label>성별</label><select id="sex2"><option value="남">남자</option><option value="여">여자</option></select></div>
      </div>
      <button class="go" onclick="analyzePair()" style="margin-top:14px">궁합 분석</button>
    </div>
    <div id="exWrap"><button class="ex-open-btn" onclick="openExModal()">📋 예시 사주로 보기</button></div>
  </div>

  <div id="exModal" class="modal hidden" onclick="if(event.target===this)closeExModal()">
    <div class="modal-box">
      <div class="modal-head"><span>예시 사주 — 한 명을 누르면 분석됩니다</span><button class="modal-x" onclick="closeExModal()">✕</button></div>
      <div class="note" style="margin:0 0 12px">공개된 생년월일 기준이며, 출생시(時)는 대부분 비공개라 <b>시 미상(3주)</b>으로 분석됩니다. 음/양력 차이가 있을 수 있는 참고·재미용 자료입니다.</div>
      <div id="exModalList"></div>
    </div>
  </div>

  <div id="result" class="hidden"></div>
  <div class="disc">고전 9책(삼명통회·자평진전·적천수·궁통보감·격국론명 등) 한국어 번역 DB 기반 · 격국·용신은 월령 기반 1차 판정이며 참고용입니다.</div>
</div>

<script>
const JIEQI = __JIEQI__;
const LUNAR = __LUNAR__;
const REFS = __REFS__;
/* ============ 기초 상수 ============ */
const GAN="甲乙丙丁戊己庚辛壬癸", ZHI="子丑寅卯辰巳午未申酉戌亥";
const GAN_KO={甲:"갑",乙:"을",丙:"병",丁:"정",戊:"무",己:"기",庚:"경",辛:"신",壬:"임",癸:"계"};
const ZHI_KO={子:"자",丑:"축",寅:"인",卯:"묘",辰:"진",巳:"사",午:"오",未:"미",申:"신",酉:"유",戌:"술",亥:"해"};
const GAN_WX={甲:"木",乙:"木",丙:"火",丁:"火",戊:"土",己:"土",庚:"金",辛:"金",壬:"水",癸:"水"};
const ZHI_WX={子:"水",丑:"土",寅:"木",卯:"木",辰:"土",巳:"火",午:"火",未:"土",申:"金",酉:"金",戌:"土",亥:"水"};
const WX_CLASS={木:"wx-mok",火:"wx-hwa",土:"wx-to",金:"wx-geum",水:"wx-su"};
const YIN=new Set(["乙","丁","己","辛","癸"]);
const SHENG={木:"火",火:"土",土:"金",金:"水",水:"木"};
const KE={木:"土",土:"水",水:"火",火:"金",金:"木"};
const HIDDEN={子:["癸"],丑:["己","癸","辛"],寅:["甲","丙","戊"],卯:["乙"],辰:["戊","乙","癸"],
  巳:["丙","庚","戊"],午:["丁","己"],未:["己","丁","乙"],申:["庚","壬","戊"],酉:["辛"],戌:["戊","辛","丁"],亥:["壬","甲"]};
function wxOf(c){return GAN_WX[c]||ZHI_WX[c];}
/* 십신 */
function sipsin(dg,o){if(!GAN_WX[o])return null;const dw=GAN_WX[dg],ow=GAN_WX[o];
  const same=YIN.has(dg)===YIN.has(o);
  if(ow===dw)return same?"비견":"겁재";
  if(SHENG[dw]===ow)return same?"식신":"상관";
  if(KE[dw]===ow)return same?"편재":"정재";
  if(KE[ow]===dw)return same?"편관":"정관";
  if(SHENG[ow]===dw)return same?"편인":"정인";return null;}
/* 십이운성 */
const TWELVE=["장생","목욕","관대","건록","제왕","쇠","병","사","묘","절","태","양"];
const CHANGSHENG={甲:"亥",丙:"寅",戊:"寅",庚:"巳",壬:"申",乙:"午",丁:"酉",己:"酉",辛:"子",癸:"卯"};
function twelveStage(g,z){let s=ZHI.indexOf(CHANGSHENG[g]),i=ZHI.indexOf(z);
  let pos=(YIN.has(g))?((s-i)%12+12)%12:((i-s)%12+12)%12;return TWELVE[pos];}
/* 신살 */
const TIANYI={甲:"丑未",戊:"丑未",庚:"丑未",乙:"子申",己:"子申",丙:"亥酉",丁:"亥酉",辛:"寅午",壬:"巳卯",癸:"巳卯"};
const MAYI={申:"寅",子:"寅",辰:"寅",寅:"申",午:"申",戌:"申",巳:"亥",酉:"亥",丑:"亥",亥:"巳",卯:"巳",未:"巳"};
const TAOHUA={申:"酉",子:"酉",辰:"酉",寅:"卯",午:"卯",戌:"卯",巳:"午",酉:"午",丑:"午",亥:"子",卯:"子",未:"子"};
const HUAGAI={申:"辰",子:"辰",辰:"辰",寅:"戌",午:"戌",戌:"戌",巳:"丑",酉:"丑",丑:"丑",亥:"未",卯:"未",未:"未"};
const YANGIN={甲:"卯",丙:"午",戊:"午",庚:"酉",壬:"子"};
const WENCHANG={甲:"巳",乙:"午",丙:"申",戊:"申",丁:"酉",己:"酉",庚:"亥",辛:"子",壬:"寅",癸:"卯"};
const LU={甲:"寅",乙:"卯",丙:"巳",戊:"巳",丁:"午",己:"午",庚:"申",辛:"酉",壬:"亥",癸:"子"};
function shensha(dg,yz,branches){const ty=new Set(TIANYI[dg].split("")),r={};
  const f=(arr)=>branches.filter(z=>arr.includes(z));
  r["천을귀인"]=branches.filter(z=>ty.has(z));
  r["역마"]=branches.filter(z=>z===MAYI[yz]); r["도화"]=branches.filter(z=>z===TAOHUA[yz]);
  r["화개"]=branches.filter(z=>z===HUAGAI[yz]);
  if(YANGIN[dg])r["양인"]=branches.filter(z=>z===YANGIN[dg]);
  r["문창귀인"]=branches.filter(z=>z===WENCHANG[dg]); r["건록"]=branches.filter(z=>z===LU[dg]);
  const o={};for(const k in r)if(r[k].length)o[k]=r[k];return o;}
/* 합충 */
const GAN_HE={"甲己":"土","乙庚":"金","丙辛":"水","丁壬":"木","戊癸":"火"};
const GAN_CHONG=new Set(["甲庚","乙辛","丙壬","丁癸"]);
const ZHI_LIUHE=new Set(["子丑","寅亥","卯戌","辰酉","巳申","午未"]);
const ZHI_CHONG=new Set(["子午","丑未","寅申","卯酉","辰戌","巳亥"]);
const ZHI_HAI=new Set(["子未","丑午","寅巳","卯辰","申亥","酉戌"]);
const ZHI_XING=new Set(["寅巳","巳申","寅申","丑戌","未戌","丑未","子卯","辰辰","午午","酉酉","亥亥"]);
const ZHI_PA=new Set(["子酉","卯午","巳申","寅亥","丑辰","未戌"]);
const ZHI_SANHE={"申子辰":"水","寅午戌":"火","巳酉丑":"金","亥卯未":"木"};
function pairKey(a,b,order){const i=order.indexOf(a),j=order.indexOf(b);return i<j?a+b:b+a;}
function interactions(gans,branches){const out={"천간합":[],"천간충":[],"지지육합":[],"지지삼합":[],"지지충":[],"지지해":[]};
  const ug=[...new Set(gans)],ub=[...new Set(branches)];
  for(let i=0;i<ug.length;i++)for(let j=i+1;j<ug.length;j++){const k=pairKey(ug[i],ug[j],GAN);
    if(GAN_HE[k])out["천간합"].push(k+"합("+GAN_HE[k]+")"); if(GAN_CHONG.has(k))out["천간충"].push(k+"충");}
  for(let i=0;i<ub.length;i++)for(let j=i+1;j<ub.length;j++){const k=pairKey(ub[i],ub[j],ZHI);
    if(ZHI_LIUHE.has(k))out["지지육합"].push(k+"합"); if(ZHI_CHONG.has(k))out["지지충"].push(k+"충"); if(ZHI_HAI.has(k))out["지지해"].push(k+"해");}
  const sb=new Set(branches);
  for(const combo in ZHI_SANHE){if([...combo].every(c=>sb.has(c)))out["지지삼합"].push(combo+"삼합("+ZHI_SANHE[combo]+")");}
  const o={};for(const k in out)if(out[k].length)o[k]=out[k];return o;}
/* 강약 */
function strength(dg,pillars,mz){const dw=GAN_WX[dg];
  let yin=null;for(const k in SHENG)if(SHENG[k]===dw)yin=k;
  const helps=new Set([dw,yin]);let score=0;
  const mwx=ZHI_WX[mz];
  if(helps.has(mwx))score+=3; else if(SHENG[dw]===mwx)score-=1.5; else score-=1.2;
  for(const pos in pillars){if(pos==="day")continue;score+=helps.has(GAN_WX[pillars[pos][0]])?1:-0.7;}
  for(const pos in pillars){const zwx=ZHI_WX[pillars[pos][1]],w=(pos==="month"||pos==="day")?1.5:1.0;
    score+=helps.has(zwx)?w:-w*0.6;}
  score=Math.round(score*10)/10;
  const verdict=score>=2?"신강":(score<=-2?"신약":"중화");return {score,verdict};}
/* 격국 */
const WANG=new Set(["子","午","卯","酉"]),GO=new Set(["辰","戌","丑","未"]);
const GEUK_MAP={정관:"정관격",편관:"칠살격",정인:"정인격",편인:"편인격",식신:"식신격",상관:"상관격",정재:"정재격",편재:"편재격",비견:"건록격",겁재:"양인격"};
function geukguk(pillars,days){const dg=pillars.day[0],mz=pillars.month[1],hid=HIDDEN[mz];
  const others=[];for(const k in pillars)if(k!=="day")others.push(pillars[k][0]);
  const tou=hid.filter(h=>others.includes(h));let gg;
  if(WANG.has(mz))gg=hid[0];
  else if(days!=null)gg=saryeong(mz,days);
  else if(GO.has(mz))gg=tou.length?tou[0]:hid[0];
  else gg=(others.includes(hid[0])||!tou.length)?hid[0]:tou[0];
  const ss=sipsin(dg,gg);
  return {geuk:GEUK_MAP[ss]||null,ss,gg,type:WANG.has(mz)?"왕지":(GO.has(mz)?"고지":"생지"),
    투출겸:tou.filter(h=>h!==gg).map(h=>[h,sipsin(dg,h)])};}
function yongsin(dg,st){const dw=GAN_WX[dg];let yin=null;for(const k in SHENG)if(SHENG[k]===dw)yin=k;
  const food=SHENG[dw],wealth=KE[dw];let off=null;for(const k in KE)if(KE[k]===dw)off=k;
  if(st.verdict==="신강")return {list:[["관살",off],["재성",wealth],["식상",food]],note:"신강 → 극·설하는 관살/재성/식상이 용신"};
  if(st.verdict==="신약"){let n="신약 → 생·부하는 인성/비겁이 용신";if(st.score<=-6)n="극신약 → 종격(從) 가능성";
    return {list:[["인성",yin],["비겁",dw]],note:n};}
  return {list:[["통관·조후",null]],note:"중화 → 통관/조후 위주 정밀판단 필요"};}
/* 세력·통근·화기·종격 */
function powerProfile(p){const dg=p.day[0],dw=GAN_WX[dg];let yin=null;for(const k in SHENG)if(SHENG[k]===dw)yin=k;
  const food=SHENG[dw],wealth=KE[dw];let off=null;for(const k in KE)if(KE[k]===dw)off=k;
  const cnt={비겁:0,인성:0,식상:0,재성:0,관살:0};const items=[];
  for(const k in p){items.push(p[k][0]);items.push(HIDDEN[p[k][1]][0]);}
  items.splice(items.indexOf(dg),1);
  for(const c of items){const w=GAN_WX[c];
    if(w===dw)cnt.비겁++;else if(w===yin)cnt.인성++;else if(w===food)cnt.식상++;else if(w===wealth)cnt.재성++;else if(w===off)cnt.관살++;}
  return cnt;}
function rooted(p){const dg=p.day[0],dw=GAN_WX[dg];let yin=null;for(const k in SHENG)if(SHENG[k]===dw)yin=k;
  for(const k in p)for(const h of HIDDEN[p[k][1]])if(GAN_WX[h]===dw||GAN_WX[h]===yin)return true;return false;}
function checkHua(p){const dg=p.day[0];const nb=[p.month[0]];if(p.hour)nb.push(p.hour[0]);
  for(const n of nb){const key=pairKey(dg,n,GAN);if(GAN_HE[key]&&ZHI_WX[p.month[1]]===GAN_HE[key])return GAN_HE[key];}return null;}
function ganRooted(p,gan){const w=GAN_WX[gan];for(const k in p)for(const h of HIDDEN[p[k][1]])if(GAN_WX[h]===w)return true;return false;}
function altGeuk(p){const dg=p.day[0],others=[];for(const k in p)if(k!=="day")others.push(p[k][0]);
  const pri={편관:5,정관:5,정재:4,편재:4,정인:3,편인:3,식신:2,상관:2};let best=null;
  for(const g of others){const ss=sipsin(dg,g);if(pri[ss]&&ganRooted(p,g)&&(!best||pri[ss]>pri[best[1]]))best=[GEUK_MAP[ss],ss];}return best;}
const SILYEONG={子:[["壬",10],["癸",20]],丑:[["癸",9],["辛",3],["己",18]],寅:[["戊",7],["丙",7],["甲",16]],
  卯:[["甲",10],["乙",20]],辰:[["乙",9],["癸",3],["戊",18]],巳:[["戊",7],["庚",7],["丙",16]],
  午:[["丙",10],["己",9],["丁",11]],未:[["丁",9],["乙",3],["己",18]],申:[["戊",7],["壬",7],["庚",16]],
  酉:[["庚",10],["辛",20]],戌:[["辛",9],["丁",3],["戊",18]],亥:[["戊",7],["甲",5],["壬",18]]};
function saryeong(zhi,days){let acc=0;for(const[g,d]of SILYEONG[zhi]){acc+=d;if(days<acc)return g;}return SILYEONG[zhi].slice(-1)[0][0];}
function geukCandidates(p,days){const dg=p.day[0],mz=p.month[1],hid=HIDDEN[mz];
  const others=[];for(const k in p)if(k!=="day")others.push(p[k][0]);
  const tou=hid.filter(h=>others.includes(h));const cands=[];
  const add=(gan,basis)=>{const ss=sipsin(dg,gan),gk=GEUK_MAP[ss];
    if(gk&&!cands.some(c=>c.geuk===gk))cands.push({geuk:gk,ss,gan,basis});};
  if(WANG.has(mz))add(hid[0],"본기(왕지 고정)");
  else{if(days!=null)add(saryeong(mz,days),"사령(司令)");add(hid[0],"월령 본기");tou.forEach(t=>{if(t!==hid[0])add(t,"투출(透出)");});}
  return cands;}
function classify(p,days){const dg=p.day[0];const st=strength(dg,p,p.month[1]);const prof=powerProfile(p);
  const support=prof.비겁+prof.인성,drain=prof.식상+prof.재성+prof.관살;
  const hua=checkHua(p);
  if(hua&&support<=2)return {type:"화기격",geuk:hua+"화격",strength:st,profile:prof,note:"일간이 인접 천간과 합하여 "+hua+"로 化"};
  if(st.score<=-4.5&&support<=1&&!rooted(p)){
    const cand=[["종재격",prof.재성],["종살격",prof.관살],["종아격",prof.식상]];cand.sort((a,b)=>b[1]-a[1]);
    return {type:"종격",geuk:cand[0][0],strength:st,profile:prof,note:"일간이 무근·고립 → 왕한 세력에 종속"};}
  if(st.score>=6&&drain<=1)return {type:"종격",geuk:prof.비겁>=prof.인성?"종왕격":"종강격",strength:st,profile:prof,note:"인비가 극왕 → 왕신을 따름"};
  const g=geukguk(p,days);let note=null,geuk=g.geuk,ss=g.ss;
  if(geuk==="건록격"||geuk==="양인격"){const alt=altGeuk(p);if(alt){geuk=alt[0];ss=alt[1];note="월령이 비겁 → 타주에서 격 취함";}}
  return {type:"정격",geuk,ss,gg:g,strength:st,profile:prof,note,candidates:geukCandidates(p,days)};}
const JOHU={亥:["火","해월 수왕·한랭 → 火로 조후·해동"],子:["火","자월 한기 극성 → 火 조후 긴요"],
  丑:["火","축월 동토 → 火로 해동, 木 보조"],寅:["火","인월 초봄 여한 → 火로 발영"],
  卯:["火","묘월 목왕 → 火로 수기를 설하여 빛냄"],辰:["木","진월 토왕 → 木으로 소토"],
  巳:["水","사월 화기 시작 → 水로 조후"],午:["水","오월 염열 → 水 조후 필수"],
  未:["水","미월 조토·염열 → 水·木으로 윤택"],申:["火","신월 금왕 → 火로 단련"],
  酉:["火","유월 금왕 → 火로 단련"],戌:["火","술월 조토 → 火·水로 한난 조절"]};
function johu(p){return JOHU[p.month[1]]||[null,"환절기 → 억부·격국 위주"];}
/* ============ 만세력 ============ */
function jdn(Y,M,D){const a=Math.floor((14-M)/12),y=Y+4800-a,m=M+12*a-3;
  return D+Math.floor((153*m+2)/5)+365*y+Math.floor(y/4)-Math.floor(y/100)+Math.floor(y/400)-32045;}
function jdnToGreg(j){let a=j+32044,b=Math.floor((4*a+3)/146097),c=a-Math.floor(146097*b/4);
  let d=Math.floor((4*c+3)/1461),e=c-Math.floor(1461*d/4),m=Math.floor((5*e+2)/153);
  const D=e-Math.floor((153*m+2)/5)+1,M=m+3-12*Math.floor(m/10),Y=100*b+d-4800+Math.floor(m/10);return [Y,M,D];}
const EPOCH_MIN=Date.UTC(2000,0,1,0,0)/60000;
function inputMinute(Y,M,D,h,mi,tz){return Math.round((Date.UTC(Y,M-1,D,h,mi)-tz*60000)/60000)-EPOCH_MIN;}
function monthBranchAndYearMin(min){ // 직전 절입 찾기 (이진탐색)
  let lo=0,hi=JIEQI.length/2-1,ans=0;
  while(lo<=hi){const mid=(lo+hi)>>1;if(JIEQI[mid*2]<=min){ans=mid;lo=mid+1;}else hi=mid-1;}
  return {branch:JIEQI[ans*2+1], eventMin:JIEQI[ans*2], idx:ans};}
function lunarToSolar(y,m,d,isLeap){const Y=LUNAR.years[String(y)];if(!Y)return null;
  const base=LUNAR.base0+Y[0],leap=Y[1],bits=Y[2];const seq=[];
  for(let mm=1;mm<=12;mm++){seq.push([mm,false]);if(leap===mm)seq.push([mm,true]);}
  let idx=-1;for(let i=0;i<seq.length;i++)if(seq[i][0]===m&&seq[i][1]===!!isLeap){idx=i;break;}
  if(idx<0)return null;let acc=0;for(let i=0;i<idx;i++)acc+=((bits>>i)&1)?30:29;
  return jdnToGreg(base+acc+(d-1));}
function computeSaju(Y,M,D,h,mi,gender,tz){
  // 일주
  const didx=(((jdn(Y,M,D)-2451545)%60)+54+60)%60, dGan=GAN[didx%10], dZhi=ZHI[didx%12];
  // 월주 (절입; 시 모름이면 정오 가정)
  const useH=(h==null)?12:h, useMi=(h==null)?0:mi;
  const min=inputMinute(Y,M,D,useH,useMi,tz);
  const mb=monthBranchAndYearMin(min);
  const monthZhi=ZHI[mb.branch];
  const daysIntoMonth=(min-mb.eventMin)/1440;   // 절입 후 경과일(사령용)
  // 년주: 직전 입춘(branch 2) 이벤트의 양력년
  let liIdx=mb.idx; while(liIdx>=0 && JIEQI[liIdx*2+1]!==2) liIdx--;
  const liMin=JIEQI[liIdx*2]; const liDate=new Date((liMin+EPOCH_MIN)*60000);
  const sajuYear=liDate.getUTCFullYear();
  const yidx=((sajuYear-4)%60+60)%60, yGan=GAN[yidx%10], yZhi=ZHI[yidx%12];
  // 월간 (오호둔)
  const yinHead=((yidx%10)%5)*2+2; const monthOrder=((mb.branch-2)%12+12)%12;
  const mGan=GAN[(yinHead+monthOrder)%10];
  const pillars={year:yGan+yZhi, month:mGan+monthZhi, day:dGan+dZhi};
  // 시주 (23시=야자시: 子시 천간은 다음날 일간 기준; 일주는 자정경계 유지)
  if(h!=null){const zi=Math.floor((h+1)/2)%12;
    const ganBase=(h===23)?(didx+1)%10:didx%10;   // 야자시 보정
    const hGan=GAN[(ganBase*2+zi)%10];
    pillars.hour=hGan+ZHI[zi];}
  // 대운
  const dae=daewoon(min,mb,yidx,mGan,monthZhi,gender,mb.branch);
  return {pillars,dGan,sajuYear,dae,days:daysIntoMonth};
}
function daewoon(min,mb,yidx,mGan,mZhi,gender,mBranch){
  const yangYear=(yidx%10)%2===0; const forward=(yangYear&&gender==="남")||(!yangYear&&gender==="여");
  // 다음/이전 절입까지 분
  let i=mb.idx; let targetMin;
  if(forward){const ni=i+1; targetMin=JIEQI[ni*2];} else {targetMin=JIEQI[i*2];}
  const diffDays=Math.abs(targetMin-min)/1440; const startAge=Math.round(diffDays/3*10)/10;
  let tg=GAN.indexOf(mGan), dz=mBranch; const list=[];
  for(let k=1;k<=8;k++){if(forward){tg=(tg+1)%10;dz=(dz+1)%12;}else{tg=(tg+9)%10;dz=(dz+11)%12;}
    list.push({age:Math.round((startAge+(k-1)*10)*10)/10, gz:GAN[tg]+ZHI[dz]});}
  return {forward,startAge,list};
}
/* ============ 종합 분석 ============ */
function analyzeFull(s){const p=s.pillars,dg=s.dGan;
  const order=["year","month","day","hour"].filter(k=>p[k]);
  const ss={};order.forEach(k=>ss[k]=(k==="day")?"일간":sipsin(dg,p[k][0]));
  const tw={};order.forEach(k=>tw[k]=twelveStage(dg,p[k][1]));
  const hid={};order.forEach(k=>hid[k]=HIDDEN[p[k][1]]);
  const branches=order.map(k=>p[k][1]), gans=order.map(k=>p[k][0]);
  const sh=shensha(dg,p.year[1],branches);
  const inter=interactions(gans,branches);
  const cls=classify(p,s.days); const st=cls.strength; const yo=yongsin(dg,st); const jh=johu(p);
  const wx={木:0,火:0,土:0,金:0,水:0};order.forEach(k=>{wx[GAN_WX[p[k][0]]]++;wx[ZHI_WX[p[k][1]]]++;});
  return {ss,tw,hid,sh,inter,st,cls,yo,jh,wx,order};
}
/* ============ UI ============ */
let CAL="solar",SEX="남",LST=true;const TZ=540,LST_MIN=30;
function setCal(c){CAL=c;document.querySelectorAll("#calSeg button").forEach(b=>b.classList.toggle("on",b.dataset.cal===c));
  document.getElementById("leapWrap").classList.toggle("hidden",c!=="lunar");}
function setSex(s){SEX=s;document.querySelectorAll("#sexSeg button").forEach(b=>b.classList.toggle("on",b.dataset.sex===s));}
function setLst(v){LST=v==="1";document.querySelectorAll("#lstSeg button").forEach(b=>b.classList.toggle("on",b.dataset.lst===v));}
let MODE="single";
function setMode(m){MODE=m;document.querySelectorAll("#modeSeg button").forEach(b=>b.classList.toggle("on",b.dataset.mode===m));
  document.getElementById("pairBox").classList.toggle("hidden",m!=="pair");
  document.getElementById("exWrap").classList.toggle("hidden",m==="pair");}
/* 공유 링크 */
function params(){const g=id=>document.getElementById(id).value;const lp=document.getElementById("leap");
  return [CAL,g("y"),g("m"),g("d"),g("h"),g("mi"),SEX,LST?1:0,lp?lp.value:0].join("_");}
function copyLink(){location.hash=params();
  const done=()=>{const b=document.getElementById("linkBtn");b.textContent="✓ 복사됨";setTimeout(()=>b.textContent="🔗 링크",1500);};
  if(navigator.clipboard&&location.protocol!=="file:")navigator.clipboard.writeText(location.href).then(done,done);
  else{const t=document.createElement("textarea");t.value=location.href;document.body.appendChild(t);t.select();try{document.execCommand("copy");}catch(e){}t.remove();done();}}
function loadFromHash(){if(!location.hash)return;const p=decodeURIComponent(location.hash.slice(1)).split("_");
  if(p.length<8)return;setCal(p[0]);["y","m","d","h","mi"].forEach((id,i)=>{const el=document.getElementById(id);if(el)el.value=p[i+1];});
  setSex(p[6]);setLst(p[7]==="1"?"1":"0");const lp=document.getElementById("leap");if(lp&&p[8]!==undefined)lp.value=p[8];analyze();}
/* 궁합 */
function fillSelects2(){const y=document.getElementById("y2");for(let v=2100;v>=1850;v--)y.add(new Option(v+"년",v));y.value=1992;
  const m=document.getElementById("m2");for(let v=1;v<=12;v++)m.add(new Option(v+"월",v));
  const d=document.getElementById("d2");for(let v=1;v<=31;v++)d.add(new Option(v+"일",v));
  const h=document.getElementById("h2");h.add(new Option("모름",""));for(let v=0;v<24;v++)h.add(new Option(String(v).padStart(2,"0")+"시",v));}
function computeFromForm(suf){const g=id=>document.getElementById(id+suf).value;
  let Y=+g("y"),M=+g("m"),D=+g("d");const hv=g("h"),h=(hv==="")?null:+hv;
  let cY=Y,cM=M,cD=D,cH=h,cMi=0;
  if(h!=null&&LST){const dt=new Date(Date.UTC(Y,M-1,D,h,0));dt.setUTCMinutes(dt.getUTCMinutes()-LST_MIN);
    cY=dt.getUTCFullYear();cM=dt.getUTCMonth()+1;cD=dt.getUTCDate();cH=dt.getUTCHours();cMi=dt.getUTCMinutes();}
  const sex=suf?document.getElementById("sex"+suf).value:SEX;
  return computeSaju(cY,cM,cD,cH,cMi,sex,TZ);}
function compat(sA,aA,sB,aB){const dgA=sA.dGan,dgB=sB.dGan,wA=GAN_WX[dgA],wB=GAN_WX[dgB];
  let rel,relNote;
  if(wA===wB){rel="비화(比和)";relNote="두 일간이 같은 오행 — 동질감과 선의의 경쟁이 공존";}
  else if(SHENG[wA]===wB){rel="내가 생함";relNote="내 일간이 상대를 생하니 베풀고 돌보는 관계";}
  else if(SHENG[wB]===wA){rel="상대가 생함";relNote="상대가 나를 생하니 보살핌을 받는 관계";}
  else if(KE[wA]===wB){rel="내가 극함";relNote="내가 주도·통제하는 경향";}
  else{rel="상대가 극함";relNote="상대에게 이끌리며 긴장도 공존";}
  const bA=aA.order.map(k=>sA.pillars[k][1]),bB=aB.order.map(k=>sB.pillars[k][1]);
  const he=[],ch=[];
  bA.forEach(x=>bB.forEach(y=>{const k=pairKey(x,y,ZHI);
    if(ZHI_LIUHE.has(k)&&!he.includes(k))he.push(k);if(ZHI_CHONG.has(k)&&!ch.includes(k))ch.push(k);}));
  const useA=new Set(aA.yo.list.map(x=>x[1]).filter(Boolean));
  const bWxB=bB.map(z=>ZHI_WX[z]).concat(aB.order.map(k=>GAN_WX[sB.pillars[k][0]]));
  const help=bWxB.filter(w=>useA.has(w)).length;
  let score=50;if(rel.includes("생"))score+=15;if(rel.includes("비화"))score+=6;if(rel.includes("극"))score-=4;
  score+=he.length*8-ch.length*6+help*3;score=Math.max(15,Math.min(98,Math.round(score)));
  return {rel,relNote,he,ch,help,score};}
function gzStr(s){const p=s.pillars;return ["year","month","day","hour"].filter(k=>p[k]).map(k=>p[k]).join("·");}
function analyzePair(){const sA=computeFromForm(""),aA=analyzeFull(sA);
  const sB=computeFromForm("2"),aB=analyzeFull(sB);const c=compat(sA,aA,sB,aB);
  const bar='<div style="height:8px;border-radius:99px;background:var(--surface2);overflow:hidden;margin:8px 0"><div style="height:100%;width:'+c.score+'%;background:linear-gradient(90deg,var(--accent),var(--accent2))"></div></div>';
  const html='<div class="card"><div class="sec-title">궁합 분석</div>'+
    '<div class="kv"><span class="tag">나 <b>'+gzStr(sA)+'</b> ('+aA.cls.strength.verdict+')</span></div>'+
    '<div class="kv"><span class="tag">상대 <b>'+gzStr(sB)+'</b> ('+aB.cls.strength.verdict+')</span></div>'+
    '<div class="kv" style="margin-top:10px"><span class="tag">일간관계 <b>'+c.rel+'</b></span><span class="tag">궁합점수 <b>'+c.score+'</b>/100</span></div>'+bar+
    '<div class="note">'+c.relNote+'. '+
    (c.he.length?'지지 육합(<b>'+c.he.join("·")+'</b>)으로 서로 끌리는 인연이 있고, ':'')+
    (c.ch.length?'지지 육충(<b>'+c.ch.join("·")+'</b>)으로 부딪힘·변동 요소가 있습니다. ':'')+
    '상대가 내 용신(<b>'+[...new Set(aA.yo.list.map(x=>x[1]).filter(Boolean))].map(w=>({木:"목",火:"화",土:"토",金:"금",水:"수"}[w])).join("·")+'</b>) 기운을 <b>'+c.help+'개</b> 보완해 줍니다. (자평 명리 기준 참고용)</div></div>';
  const r=document.getElementById("result");r.innerHTML=html.replace(/<b>/g,'<b class="luck-good" style="color:var(--accent)">');r.classList.remove("hidden");
  r.scrollIntoView({behavior:"smooth",block:"start"});}
function toggleTheme(){const h=document.documentElement;h.dataset.theme=h.dataset.theme==="light"?"":"light";}
function fillSelects(){const y=document.getElementById("y");for(let v=2100;v>=1850;v--)y.add(new Option(v+"년",v));y.value=1990;
  const m=document.getElementById("m");for(let v=1;v<=12;v++)m.add(new Option(v+"월",v));
  const d=document.getElementById("d");for(let v=1;v<=31;v++)d.add(new Option(v+"일",v));
  const h=document.getElementById("h");h.add(new Option("모름",""));
  for(let v=0;v<24;v++)h.add(new Option(String(v).padStart(2,"0")+"시",v));
  const mi=document.getElementById("mi");for(let v=0;v<60;v+=5)mi.add(new Option(String(v).padStart(2,"0")+"분",v));}
function wxSpan(c){const w=wxOf(c);return '<span class="'+WX_CLASS[w]+'">'+c+'</span>';}
function analyze(){
  let Y=+document.getElementById("y").value,M=+document.getElementById("m").value,D=+document.getElementById("d").value;
  const hv=document.getElementById("h").value, h=(hv==="")?null:+hv, mi=+document.getElementById("mi").value||0;
  if(CAL==="lunar"){const leap=document.getElementById("leap").value==="1";const sol=lunarToSolar(Y,M,D,leap);
    if(!sol){alert("해당 음력 날짜를 변환할 수 없습니다.");return;}[Y,M,D]=sol;}
  // 진태양시 보정: 시각 전체를 -30분(날짜 넘어가면 함께 조정). 시 미상이면 미적용.
  let cY=Y,cM=M,cD=D,cH=h,cMi=mi;
  if(h!=null && LST){const dt=new Date(Date.UTC(Y,M-1,D,h,mi)); dt.setUTCMinutes(dt.getUTCMinutes()-LST_MIN);
    cY=dt.getUTCFullYear();cM=dt.getUTCMonth()+1;cD=dt.getUTCDate();cH=dt.getUTCHours();cMi=dt.getUTCMinutes();}
  const s=computeSaju(cY,cM,cD,cH,cMi,SEX,TZ); const a=analyzeFull(s);
  render(s,a,Y,M,D,h);
  try{location.hash=params();}catch(e){}
}
const EXAMPLES=[
  // 정치 (최근 대통령 — 양력 공개일 기준)
  {n:"문재인",y:1953,m:1,d:24,h:null,s:"남",cat:"정치"},
  {n:"윤석열",y:1960,m:12,d:18,h:null,s:"남",cat:"정치"},
  {n:"반기문",y:1944,m:6,d:13,h:null,s:"남",cat:"정치"},
  // 스포츠
  {n:"손흥민",y:1992,m:7,d:8,h:null,s:"남",cat:"스포츠"},
  {n:"박지성",y:1981,m:2,d:25,h:null,s:"남",cat:"스포츠"},
  {n:"차범근",y:1953,m:5,d:22,h:null,s:"남",cat:"스포츠"},
  {n:"김민재",y:1996,m:11,d:15,h:null,s:"남",cat:"스포츠"},
  {n:"이강인",y:2001,m:2,d:19,h:null,s:"남",cat:"스포츠"},
  {n:"김연아",y:1990,m:9,d:5,h:null,s:"여",cat:"스포츠"},
  {n:"박찬호",y:1973,m:6,d:29,h:null,s:"남",cat:"스포츠"},
  {n:"류현진",y:1987,m:3,d:25,h:null,s:"남",cat:"스포츠"},
  {n:"박세리",y:1977,m:9,d:28,h:null,s:"여",cat:"스포츠"},
  {n:"추신수",y:1982,m:7,d:13,h:null,s:"남",cat:"스포츠"},
  // 배우
  {n:"송강호",y:1967,m:1,d:17,h:null,s:"남",cat:"배우"},
  {n:"이병헌",y:1970,m:7,d:12,h:null,s:"남",cat:"배우"},
  {n:"최민식",y:1962,m:4,d:27,h:null,s:"남",cat:"배우"},
  {n:"마동석",y:1971,m:3,d:1,h:null,s:"남",cat:"배우"},
  {n:"공유",y:1979,m:7,d:10,h:null,s:"남",cat:"배우"},
  {n:"현빈",y:1982,m:9,d:25,h:null,s:"남",cat:"배우"},
  {n:"이정재",y:1972,m:12,d:15,h:null,s:"남",cat:"배우"},
  {n:"정우성",y:1973,m:3,d:20,h:null,s:"남",cat:"배우"},
  {n:"전지현",y:1981,m:10,d:30,h:null,s:"여",cat:"배우"},
  {n:"김혜수",y:1970,m:9,d:5,h:null,s:"여",cat:"배우"},
  {n:"손예진",y:1982,m:1,d:11,h:null,s:"여",cat:"배우"},
  // 가수
  {n:"아이유",y:1993,m:5,d:16,h:null,s:"여",cat:"가수"},
  {n:"싸이",y:1977,m:12,d:31,h:null,s:"남",cat:"가수"},
  {n:"비(정지훈)",y:1982,m:6,d:25,h:null,s:"남",cat:"가수"},
  {n:"BTS RM",y:1994,m:9,d:12,h:null,s:"남",cat:"가수"},
  {n:"BTS 정국",y:1997,m:9,d:1,h:null,s:"남",cat:"가수"},
  {n:"지드래곤",y:1988,m:8,d:18,h:null,s:"남",cat:"가수"},
  {n:"태연",y:1989,m:3,d:9,h:null,s:"여",cat:"가수"},
  // 기업
  {n:"이건희",y:1942,m:1,d:9,h:null,s:"남",cat:"기업"},
  {n:"이재용",y:1968,m:6,d:23,h:null,s:"남",cat:"기업"},
  {n:"정주영",y:1915,m:11,d:25,h:null,s:"남",cat:"기업"},
  {n:"김범수",y:1966,m:3,d:8,h:null,s:"남",cat:"기업"},
  // 해외·역사 (생년월일 검증됨)
  {n:"증국번",y:1811,m:11,d:26,h:4,s:"남",cat:"해외·역사"},
  {n:"장제스",y:1887,m:10,d:31,h:null,s:"남",cat:"해외·역사"},
  {n:"마오쩌둥",y:1893,m:12,d:26,h:null,s:"남",cat:"해외·역사"},
  // 해외 유명인 (출생지 현지 시각·시간대 반영, 진태양시 보정 미적용)
  {n:"버락 오바마",y:1961,m:8,d:4,h:19,mi:24,s:"남",tz:-600,lst:false,cat:"해외 유명인"},
  {n:"오프라 윈프리",y:1954,m:1,d:29,h:4,mi:30,s:"여",tz:-360,lst:false,cat:"해외 유명인"},
  {n:"레이디 가가",y:1986,m:3,d:28,h:9,mi:53,s:"여",tz:-300,lst:false,cat:"해외 유명인"},
  {n:"엘비스 프레슬리",y:1935,m:1,d:8,h:4,mi:35,s:"남",tz:-360,lst:false,cat:"해외 유명인"},
  {n:"도널드 트럼프",y:1946,m:6,d:14,h:10,mi:54,s:"남",tz:-240,lst:false,cat:"해외 유명인"},
  {n:"마릴린 먼로",y:1926,m:6,d:1,h:9,mi:30,s:"여",tz:-480,lst:false,cat:"해외 유명인"},
  {n:"월트 디즈니",y:1901,m:12,d:5,h:0,mi:35,s:"남",tz:-360,lst:false,cat:"해외 유명인"},
  {n:"스티브 잡스",y:1955,m:2,d:24,h:19,mi:15,s:"남",tz:-480,lst:false,cat:"해외 유명인"},
  {n:"다이애나 왕비",y:1961,m:7,d:1,h:19,mi:45,s:"여",tz:60,lst:false,cat:"해외 유명인"},
  {n:"일론 머스크",y:1971,m:6,d:28,h:7,mi:30,s:"남",tz:120,lst:false,cat:"해외 유명인"},
  // 예시 템플릿
  {n:"현대 남성 예",y:1990,m:5,d:15,h:10,s:"남",cat:"예시 템플릿"},
  {n:"현대 여성 예",y:1988,m:3,d:22,h:18,s:"여",cat:"예시 템플릿"},
  {n:"야자시 예(23시)",y:1995,m:7,d:7,h:23,s:"남",cat:"예시 템플릿"},
];
function renderExamples(){const box=document.getElementById("exModalList");
  const cats={};EXAMPLES.forEach((e,i)=>{(cats[e.cat]=cats[e.cat]||[]).push([e,i]);});
  let h='';for(const c in cats){h+='<div class="ex-cat">'+c+'</div><div class="kv" style="margin-bottom:10px">'+
    cats[c].map(([e,i])=>'<span class="tag" style="cursor:pointer;padding:8px 13px" onclick="loadExample('+i+')">'+e.n+' <span style="color:var(--muted)">'+e.y+'</span></span>').join("")+'</div>';}
  box.innerHTML=h;}
function openExModal(){document.getElementById("exModal").classList.remove("hidden");}
function closeExModal(){document.getElementById("exModal").classList.add("hidden");}
function loadExample(i){const e=EXAMPLES[i];setCal("solar");
  document.getElementById("y").value=e.y;document.getElementById("m").value=e.m;document.getElementById("d").value=e.d;
  document.getElementById("h").value=(e.h==null?"":e.h);document.getElementById("mi").value=(e.mi||0);setSex(e.s);
  closeExModal();
  if(e.tz!==undefined){  // 해외: 출생지 시간대로 직접 계산
    let Y=e.y,M=e.m,D=e.d,h=(e.h==null?null:e.h),mi=e.mi||0,lst=(e.lst!==false);
    let cY=Y,cM=M,cD=D,cH=h,cMi=mi;
    if(h!=null&&lst){const dt=new Date(Date.UTC(Y,M-1,D,h,mi));dt.setUTCMinutes(dt.getUTCMinutes()-LST_MIN);
      cY=dt.getUTCFullYear();cM=dt.getUTCMonth()+1;cD=dt.getUTCDate();cH=dt.getUTCHours();cMi=dt.getUTCMinutes();}
    const s=computeSaju(cY,cM,cD,cH,cMi,e.s,e.tz),a=analyzeFull(s);
    render(s,a,Y,M,D,h);return;
  }
  analyze();}
/* ===== 통합 기둥 뷰 (원국 + 대운/세운) + 관계 도식 ===== */
const BAEKHO=new Set(["甲辰","乙未","丙戌","丁丑","戊辰","壬戌","癸丑"]);
const CHEONDEOK={寅:"丁",卯:"申",辰:"壬",巳:"辛",午:"亥",未:"甲",申:"癸",酉:"寅",戌:"丙",亥:"乙",子:"巳",丑:"庚"};
const WOLDEOK={寅:"丙",午:"丙",戌:"丙",申:"壬",子:"壬",辰:"壬",亥:"甲",卯:"甲",未:"甲",巳:"庚",酉:"庚",丑:"庚"};
const WONJIN={子:"未",未:"子",丑:"午",午:"丑",寅:"酉",酉:"寅",卯:"申",申:"卯",辰:"亥",亥:"辰",巳:"戌",戌:"巳"};
const POSF={year:"연주",month:"월주",day:"일주",hour:"시주"};
/* 일주 상징동물 카드 */
const ELEM_COLOR={木:"푸른",火:"붉은",土:"황금빛",金:"하얀",水:"검은"};
const ZHI_ANIMAL={子:["쥐","🐀"],丑:["소","🐂"],寅:["호랑이","🐅"],卯:["토끼","🐇"],辰:["용","🐉"],巳:["뱀","🐍"],午:["말","🐎"],未:["양","🐑"],申:["원숭이","🐒"],酉:["닭","🐓"],戌:["개","🐕"],亥:["돼지","🐖"]};
const GAN_TRAIT={甲:"큰 나무처럼 곧고 진취적이며 리더십이 있는",乙:"화초처럼 유연하고 적응력이 뛰어나며 끈기 있는",丙:"태양처럼 밝고 정열적이며 표현력이 좋은",丁:"촛불처럼 따뜻하고 섬세하며 헌신적인",戊:"큰 산처럼 듬직하고 포용력 있으며 신의 있는",己:"기름진 밭처럼 실속 있고 섬세하며 너그러운",庚:"단단한 쇠처럼 강직하고 결단력 있으며 의리 있는",辛:"보석처럼 예리하고 세련되며 자존심 강한",壬:"바다처럼 넓고 지혜로우며 포용력 큰",癸:"이슬비처럼 맑고 총명하며 섬세한"};
const ZHI_TRAIT={子:"영리하고 재치 있으며 적응이 빠른",丑:"성실하고 인내심 강하며 우직한",寅:"용맹하고 진취적이며 통솔력 있는",卯:"온화하고 예민하며 섬세한",辰:"포부가 크고 변화를 즐기는",巳:"지혜롭고 직관이 뛰어난",午:"활동적이고 정열적이며 명랑한",未:"온순하고 예술적이며 정 많은",申:"재주 많고 임기응변에 능한",酉:"예리하고 정확하며 미적 감각 있는",戌:"충직하고 정의로우며 책임감 강한",亥:"순수하고 낙천적이며 베푸는"};
function animalCard(s){const dg=s.dGan,dz=s.pillars.day[1];
  const col=ELEM_COLOR[GAN_WX[dg]],an=ZHI_ANIMAL[dz],tw=twelveStage(dg,dz),wxb=WX_CLASS[GAN_WX[dg]]+"b";
  return '<div class="animal-card '+wxb+'"><div class="ac-emoji">'+an[1]+'</div>'+
    '<div class="ac-title">'+GAN_KO[dg]+ZHI_KO[dz]+'('+dg+dz+') 일주</div>'+
    '<div class="ac-sub">'+col+' '+an[0]+'</div>'+
    '<div class="ac-trait">'+GAN_TRAIT[dg]+' 성정에, 일지 '+an[0]+'(이)가 '+ZHI_TRAIT[dz]+' 기질을 더합니다. 자좌(自坐) 십이운성은 <b>'+tw+'</b>.</div></div>';}
/* ===== 차별화 운세 해석: 신체·십신 영역 + 원국/운 조합 ===== */
const GAN_BODY={甲:"머리·담(쓸개)",乙:"목·어깨·간",丙:"어깨·소장",丁:"가슴·심장",戊:"옆구리·위",己:"복부·비장",庚:"대장·뼈",辛:"폐·치아",壬:"방광·정강이",癸:"신장·발·생식기"};
const ZHI_BODY={子:"방광·생식기·귀",丑:"비장·복부",寅:"담·팔·모발",卯:"간·손·눈",辰:"위·피부·어깨",巳:"심장·얼굴·인후",午:"심장·눈·정신",未:"위·척추",申:"폐·대장",酉:"폐·코·뼈",戌:"위·다리",亥:"신장·머리·혈액"};
const WX_ORGAN={木:"간·담·근육·눈·신경",火:"심장·소장·혈액·정신",土:"비위·소화기·피부",金:"폐·대장·호흡기·뼈·코",水:"신장·방광·비뇨생식·귀"};
const WX_CARE={木:"과로·음주·스트레스를 줄이고 휴식·스트레칭으로 간을 보호",火:"과흥분을 피하고 혈압·심혈관 관리와 규칙적 수면",土:"과식·불규칙한 식사를 피하고 위장을 따뜻하게 관리",金:"호흡기·환절기 감기에 유의하고 금연·보습",水:"한기·과로를 피하고 신장·허리·생식기 관리와 수분 섭취"};
const SIPSIN_LIFE={
 비견:{dom:"대인",d:"형제·친구·동료와의 인연, 독립심과 경쟁심"},
 겁재:{dom:"재물·대인",d:"동업·경쟁 관계, 지출 증가와 재물 분탈 주의"},
 식신:{dom:"건강·표현",d:"의식주의 여유와 표현력·재능(여성은 자녀)"},
 상관:{dom:"사회·표현",d:"재능이 빛나나 구설·직장과의 마찰 소지"},
 정재:{dom:"재물",d:"꾸준한 수입과 안정적 재물(남성은 배우자)"},
 편재:{dom:"재물",d:"사업·투자·유동 자금의 기회(부친 인연)"},
 정관:{dom:"사회·명예",d:"직장·지위·명예와 책임(여성은 배우자)"},
 편관:{dom:"사회·도전",d:"권력·도전·압박과 결단의 시기(남성은 자녀)"},
 정인:{dom:"학업·귀인",d:"학문·문서·안정과 귀인의 도움(모친 인연)"},
 편인:{dom:"학업·기술",d:"기술·종교·심리 등 전문성"}};
const GUNG={year:["조상·부모궁","조상·부모·초년 기반"],month:["부모·사회궁","부모·형제·직장(사회)"],day:["배우자궁","배우자·가정"],hour:["자녀궁","자녀·아랫사람·말년"]};
const CHONG_EV={year:"부모·조상·초년 기반에 변동이 옵니다 — <b>부모님 건강</b>, 이사, 고향·근거지 변화에 유의하세요.",
 month:"직장·사회·형제 영역이 흔들립니다 — <b>이직·부서이동·이사</b>, 부모님 건강에 신경 쓰세요.",
 day:"배우자·가정에 변동수입니다 — <b>부부 갈등이나 이별·이동, 이사</b>가 생기기 쉬우니 대화와 신중함이 필요합니다.",
 hour:"자녀·아랫사람·말년에 변동이 옵니다 — <b>자녀 문제</b>, 거처 변화, 부하·후배 관계에 유의하세요."};
const HE_EV={year:"윗사람·가문과 좋은 인연이 맺어집니다(귀인·후원).",month:"직장·인맥의 결합 — <b>협력·이직·승진</b>의 기회입니다.",
 day:"배우자·이성과의 인연 — <b>연애·결혼·화합</b>의 기운입니다.",hour:"자녀·아랫사람과의 인연이 깊어집니다."};
const SS_CHONG={정인:"문서·계약·시험·이사 변동과 모친 건강",편인:"문서·자격·종교와 모친 관련",정재:"재물 손실·금전 변동(남: 아내 갈등)",편재:"사업·투자 변동과 부친·이성 문제",정관:"직장·명예 변동·관재(여: 남편 갈등)",편관:"직장 압박·송사·사고(남: 자녀)",식신:"건강·표현 변동(여: 자녀)",상관:"구설·직장 마찰(여: 자녀)",비견:"형제·동료 갈등·경쟁",겁재:"재물 분탈·동업 분쟁"};
const SS_HE={정인:"문서·자격·계약 성사와 귀인·학업",편인:"기술·자격·후원",정재:"재물·결혼(남: 연애)",편재:"사업 기회·투자·이성 인연",정관:"승진·취업·명예(여: 결혼)",편관:"발탁·중책·결단",식신:"창작·식복(여: 출산)",상관:"재능 발휘·창업",비견:"협력·동료의 도움",겁재:"동업·인맥(금전 주의)"};
const SHINSAL_SHORT={천을귀인:"귀인의 도움·재액 해소",역마:"이동·여행·해외·이사",도화:"이성·인기·연애·예술",화개:"예술·종교·고독·수행",양인:"과감·추진하나 다툼·사고 주의",문창:"학문·시험·문서에 길",건록:"자립·건강·실력",공망:"헛됨·정신적·종교적 전환",천덕:"음덕·재액 해소",월덕:"자비·평안·흉 완화",백호:"혈광·사고·수술 주의(활인업은 길)"};
function lifeReport(s,a){const dg=s.dGan,p=s.pillars,L=[];
  const branches=a.order.map(k=>p[k][1]),gans=a.order.map(k=>p[k][0]);
  const cntJ=ss=>gans.filter(g=>ss.includes(sipsin(dg,g))).length+branches.filter(z=>ss.includes(sipsin(dg,HIDDEN[z][0]))).length;
  // 건강
  const weak=Object.entries(a.wx).filter(([w,c])=>c===0).map(([w])=>w);
  const strong=Object.entries(a.wx).filter(([w,c])=>c>=4).map(([w])=>w);
  let hp=[];
  if(weak.length)hp.push("오행 중 <b>"+weak.map(w=>WXN[w]).join("·")+"</b>이 없어 <b>"+weak.map(w=>WX_ORGAN[w]).join(" / ")+"</b> 계통이 선천적으로 약할 수 있습니다. "+weak.map(w=>WX_CARE[w]).join("; ")+"하는 것이 좋습니다.");
  if(strong.length)hp.push("<b>"+strong.map(w=>WXN[w]).join("·")+"</b>이 과다하여 "+strong.map(w=>WX_ORGAN[w]).join(" / ")+"에 부담이 가고, 이 기운이 극하는 장부도 약해지기 쉽습니다.");
  const chong=[];for(let i=0;i<branches.length;i++)for(let j=i+1;j<branches.length;j++){const k=pairKey(branches[i],branches[j],ZHI);if(ZHI_CHONG.has(k))chong.push([branches[i],branches[j]]);}
  if(chong.length)hp.push("원국 지지 "+chong.map(c=>c[0]+c[1]+"충").join(", ")+"이 있어 <b>"+chong.map(c=>ZHI_BODY[c[0]]+"·"+ZHI_BODY[c[1]]).join(" / ")+"</b> 부위에 충돌·기복이 나기 쉬우니 정기 검진을 권합니다.");
  if(!hp.length)hp.push("오행이 비교적 고르게 갖춰져 건강 균형이 양호합니다. 다만 일간 "+wxWord(dg)+"의 "+WX_ORGAN[GAN_WX[dg]]+" 계통은 기본적으로 살펴두세요.");
  L.push(["건강운","🩺",hp,["질병","수명"]]);
  // 재물
  const jae=cntJ(["정재","편재"]);let wp=[];
  if(jae===0)wp.push("재성(財星)이 드러나지 않아 큰 재물보다 명예·전문성으로 안정을 꾀하는 편이 유리합니다. 재성운(財運)에 기회를 잡으세요.");
  else if(a.st.verdict==="신강")wp.push("신강한데 재성이 있어 재물을 능히 감당합니다(身旺財旺). 적극적 재테크·사업이 유리하며 재성운에 발복합니다.");
  else if(a.st.verdict==="신약")wp.push("신약한데 재성이 "+(jae>=3?"많아 '재다신약(財多身弱)'으로 재물에 비해 몸이 따르지 못하니, 욕심을 줄이고 비겁·인성운의 도움으로 ":"있어 ")+"무리한 투자보다 안정적 관리가 유리합니다. 비겁·인성운에 재물운이 트입니다.");
  else wp.push("재성이 적절해 분수에 맞는 재물을 꾸립니다. 재성운·식상운에 재물 기회가 늘어납니다.");
  L.push(["재물운","💰",wp,["부귀","재성"]]);
  // 사회·관
  const gwan=cntJ(["정관","편관"]);let cp=[];
  if(gwan===0)cp.push("관성(官星)이 약해 조직보다 자유로운 전문직·자영업이 맞습니다. 관운(官運)에 직위·명예가 따릅니다.");
  else if(gwan>=3)cp.push("관성이 강해 책임·압박이 큰 자리에 오르기 쉬우나 과중한 부담·관재(官災)에 유의해야 합니다. 인성으로 관을 化하면 명예가 빛납니다.");
  else cp.push("관성이 적절해 조직 내 신망과 지위를 얻기 좋습니다. 관운·인성운에 승진·명예가 따릅니다.");
  L.push(["사회·관운","🏛️",cp,["관성","부귀"]]);
  // 대인
  const big=cntJ(["비견","겁재"]);let pp=[];
  if(big>=3)pp.push("비겁(比劫)이 많아 형제·동료·경쟁자와의 인연이 강합니다. 협력하면 큰 힘이 되나 동업·금전 거래의 분쟁·손재에 주의하세요.");
  else if(big===0)pp.push("비겁이 약해 독립적으로 움직이며 스스로의 노력으로 이룹니다. 귀인(인성)·동료운을 의식적으로 넓히면 좋습니다.");
  else pp.push("대인 관계가 무난하며 협력과 독립의 균형이 좋습니다. 비겁·관성운에 인맥·조직 인연이 활발해집니다.");
  L.push(["대인·사회운","🤝",pp,["육친"]]);
  return '<div class="card"><div class="sec-title">사주 8자 종합 풀이 — 건강·재물·사회·대인</div>'+
    L.map(([t,e,arr,rk])=>'<div class="life-sec"><div class="life-t">'+e+' '+t+'</div>'+arr.map(x=>'<p>'+x+'</p>').join("")+refBlock(rk)+'</div>').join("")+
    '<div class="note">사주 여덟 글자의 오행·십신·충극을 고전 명리(적천수·삼명통회 등)의 신체·육친 배속으로 풀이한 것으로, 의학 진단이 아닌 예방·참고용입니다.</div></div>';}
function runeReport(s,a,sel){if(!sel||(!sel.dae&&!sel.se&&!sel.wol))return "";
  const dg=s.dGan,p=s.pillars,{use,avoid}=useAvoid(s,a);
  const items=[];
  if(sel.dae)items.push(["대운",sel.dae.gz,sel.dae.age+"세 전후 약 10년"]);
  if(sel.se)items.push(["세운",sel.se.gz,sel.se.Y+"년 한 해"]);
  if(sel.wol)items.push(["월운",sel.wol.gz,sel.wol.label]);
  const gm=gongmangOf(gzIndex(p.day));
  const blocks=items.map(([label,gz,period])=>{const g=gz[0],z=gz[1],evs=[];
    const sc=judgeLuck(gz,use,avoid),ts=sipsin(dg,g),zs=sipsin(dg,HIDDEN[z][0]),tw=twelveStage(dg,z),ti=SIPSIN_LIFE[ts];
    const vigor=["장생","관대","건록","제왕"].includes(tw)?"기력이 <b>왕성</b>한":["쇠","병","사","묘","절"].includes(tw)?"기력이 <b>가라앉는</b>":"기력이 평이한";
    const lead=period+"에는 천간 <b>"+g+"("+ts+")</b>로 <b>"+(ti?ti.dom:"여러")+"</b> 영역이 부각되고, 지지 <b>"+z+"("+zs+")</b>의 십이운성이 <b>"+tw+"</b>라 "+vigor+" 시기입니다.";
    a.order.forEach(k=>{const bz=p[k][1],zk=pairKey(z,bz,ZHI),gng=GUNG[k],bzSS=sipsin(dg,HIDDEN[bz][0]),tWx=ZHI_WX[bz];
      const grade=use.has(tWx)?" <b class='hl-c'>[용신 손상 — 영향이 큼]</b>":avoid.has(tWx)?" <b class='hl-h'>[기신 충거 — 흉이 길로 바뀔 수 있음]</b>":"";
      const rel=a.order.filter(o=>o!==k).map(o=>p[o][1]).find(oz=>ZHI_LIUHE.has(pairKey(bz,oz,ZHI)));
      const relTxt=rel?" 다만 <b>"+bz+"</b>가 원국 <b>"+rel+"</b>와 합을 이뤄 충격이 일부 풀립니다(충중봉합).":"";
      if(ZHI_CHONG.has(zk))evs.push(["chong","운 <b class='hl-c'>"+z+"</b> ↔ "+gng[0]+" <b>"+bz+"("+bzSS+")</b> <b>충(沖)</b> — "+CHONG_EV[k]+" 육친으로는 <b>"+SS_CHONG[bzSS]+"</b> 관련 일이 생기기 쉽고, "+ZHI_BODY[bz]+" 건강을 살피세요."+grade+relTxt]);
      else if(ZHI_LIUHE.has(zk))evs.push(["he","운 <b class='hl-h'>"+z+"</b> ↔ "+gng[0]+" <b>"+bz+"("+bzSS+")</b> <b>합(合)</b> — "+HE_EV[k]+" <b>"+SS_HE[bzSS]+"</b>의 기운이 더해집니다."]);
      if(ZHI_XING.has(zk))evs.push(["chong","운 <b class='hl-c'>"+z+"</b> ↔ "+gng[0]+" "+bz+" <b>형(刑)</b> — 수술·관재·구설·다툼의 소지이니 계약·언행을 신중히 하고 무리한 일은 피하세요."]);
      if(ZHI_PA.has(zk))evs.push(["pa","운 "+z+" ↔ "+gng[0]+" "+bz+" <b>파(破)</b> — 계획·문서·관계가 깨지기 쉬우니 마무리를 점검하세요."]);
      if(ZHI_HAI.has(zk))evs.push(["pa","운 "+z+" ↔ "+gng[0]+" "+bz+" <b>해(害)</b> — 가까운 사이의 방해·배신·질병에 유의하세요."]);});
    a.order.forEach(k=>{const bg=p[k][0],gk=pairKey(g,bg,GAN),gng=GUNG[k],bgSS=sipsin(dg,bg);
      if(GAN_CHONG.has(gk))evs.push(["chong","운 천간 <b class='hl-c'>"+g+"</b> ↔ "+gng[0]+" "+bg+"("+bgSS+") <b>충</b> — "+gng[1]+"의 명분·마음에 동요, <b>"+SS_CHONG[bgSS]+"</b> 관련."]);
      else if(GAN_HE[gk])evs.push(["he","운 천간 <b class='hl-h'>"+g+"</b> ↔ "+gng[0]+" "+bg+"("+bgSS+") <b>합("+GAN_HE[gk]+")</b> — "+gng[1]+"에 결합·계약·인연, <b>"+SS_HE[bgSS]+"</b>."]);});
    const rss=shenshaCol(dg,p.year[1],p.month[1],gz,gm);if(BAEKHO.has(gz))rss.push("백호");
    if(rss.length)evs.push(["ss","🔮 신살 동(動): <b>"+rss.join("·")+"</b> — "+rss.map(x=>SHINSAL_SHORT[x]||x).join("; ")+"."]);
    if(!evs.length)evs.push(["none","원국과 뚜렷한 충·합·형이 없어 평이하게 흐릅니다."+(ti?" "+ti.dom+" 영역에서 "+ti.d+"의 기운이 무난히 작동합니다.":"")]);
    const advice=sc>0?"용신을 돕는 시기이니 <b>적극적으로 도모</b>하기 좋습니다(이직·투자·결혼 등 큰일에 유리).":sc<0?"기신이 강한 시기이니 <b>확장보다 수성(守城)</b>하며 건강·계약·관재를 특히 살피세요.":"무리하지 않고 <b>흐름을 지키며 내실</b>을 다질 때입니다.";
    const tone=sc>0?"<span class='luck-good'>순조</span>":sc<0?"<span class='luck-bad'>주의</span>":"무난";
    return '<div class="rune-block"><div class="rune-h">'+wxSpan(g)+wxSpan(z)+' '+label+' · '+period+' <span style="font-size:11px;font-weight:400;color:var(--muted)">('+tone+')</span></div>'+
      '<p style="margin:3px 0 7px;font-size:12.5px;line-height:1.65">'+lead+'</p>'+
      evs.map(([cls,txt])=>'<div class="ev ev-'+cls+'">'+txt+'</div>').join("")+
      '<div class="ev ev-advice">💡 <b>이 시기 조언:</b> '+advice+'</div></div>';}).join("");
  const head=items.length>1?("원국 + "+items.map(x=>x[0]).join("+")+" 누적"):("원국 + "+items[0][0]);
  return '<div class="sec-title" style="margin-top:14px">📜 '+head+' — 글자 조합으로 본 이 시기의 일</div>'+
    '<div class="note" style="margin:0 0 6px">충·형=빨강, 합=초록, 파·해=주황. <b>[용신 손상]</b>은 영향이 크고, <b>[기신 충거]</b>는 흉이 길로 바뀔 수 있습니다. 충중봉합은 합으로 충이 풀림을 뜻합니다.</div>'+blocks;}
/* ===== 정밀 풀이: 직업적성·연애결혼·자녀·학업이동 ===== */
const SIPSIN_JOB={정관:"공직·행정·대기업 관리직·법조·금융 관리",편관:"군인·경찰·검찰·외과의·스포츠·보안·위기관리",
 정인:"교육·학자·연구·행정·출판·공공기관",편인:"의약·종교·예술·기술·심리상담·역학·전문기술",
 식신:"요식·교육·서비스·예술·생산·콘텐츠 기획",상관:"방송·연예·강사·디자인·마케팅·언론·비평",
 정재:"회계·금융·은행·세무·경영관리·실물 비즈니스",편재:"사업·무역·유통·투자·영업·부동산·프랜차이즈",
 비견:"전문직·자영업·동업·프리랜서·1인 기업",겁재:"영업·경쟁 업종·스포츠·투자·승부 분야"};
const WX_FIELD={木:"교육·출판·기획·의류·디자인·환경·바이오",火:"IT·전기전자·방송·미디어·요식·미용·엔터테인먼트",
 土:"부동산·건축·중개·농업·요식·종교·컨설팅",金:"금융·기계·의료·법률·군경·금속·반도체",水:"유통·무역·수산·물류·관광·연구"};
const HONGYEOM={甲:"午",乙:"午",丙:"寅",丁:"未",戊:"辰",己:"辰",庚:"戌",辛:"酉",壬:"子",癸:"申"};
const GROUP_REP={비겁:"비견",인성:"정인",식상:"상관",재성:"편재",관살:"정관"};
function careerAptitude(s,a){const dg=s.dGan,dw=GAN_WX[dg],prof=a.cls.profile||{};
  const top=Object.entries(prof).sort((x,y)=>y[1]-x[1])[0];
  const geukSs=a.cls.ss, mainSs=(geukSs&&SIPSIN_JOB[geukSs])?geukSs:(top?GROUP_REP[top[0]]:"비견");
  const food=SHENG[dw],wealth=KE[dw];
  return "격국("+(a.cls.geuk||"-")+")과 가장 강한 <b>"+mainSs+"</b> 기운으로 보아 <b>"+SIPSIN_JOB[mainSs]+"</b> 방면이 잘 맞습니다. "+
    "일간 "+wxWord(dg)+"의 기질은 <b>"+WX_FIELD[dw]+"</b> 업종과, 활동·표현을 뜻하는 식상("+WXN[food]+")·재물을 뜻하는 재성("+WXN[wealth]+") 분야("+WX_FIELD[food]+" / "+WX_FIELD[wealth]+")에서 강점을 보입니다.";}
function timings(s,a,targetSS,love){const dg=s.dGan,p=s.pillars,dayZ=p.day[1],yz=p.year[1],dohwa=TAOHUA[yz],hy=HONGYEOM[dg];
  const nowY=new Date().getFullYear(),res=[];
  for(let Y=nowY;Y<=nowY+25;Y++){const idx=((Y-4)%60+60)%60,gz=GAN[idx%10]+ZHI[idx%12];let sc=0;
    if(targetSS.includes(sipsin(dg,gz[0])))sc+=2;
    if(targetSS.includes(sipsin(dg,HIDDEN[gz[1]][0])))sc+=2;
    if(love&&(gz[1]===dohwa||gz[1]===hy))sc+=1;
    const zk=pairKey(gz[1],dayZ,ZHI);if(ZHI_LIUHE.has(zk))sc+=2;else if(ZHI_CHONG.has(zk))sc+=1;
    if(sc>=3)res.push({Y,sc});}
  res.sort((x,y)=>y.sc-x.sc);const yrs=[...new Set(res.slice(0,5).map(x=>x.Y))].sort();
  return yrs;}
function lifeReport2(s,a){const dg=s.dGan,male=(SEX==="남"),L=[];
  // 직업
  L.push(["직업 적성","🧭",[careerAptitude(s,a)],["성정"]]);
  // 연애·결혼
  const spouseSS=male?["정재","편재"]:["정관","편관"];
  const spouseName=male?"재성(財星)":"관성(官星)";
  const dayZ=s.pillars.day[1],dohwa=TAOHUA[s.pillars.year[1]];
  const hasDohwa=a.order.some(k=>s.pillars[k][1]===dohwa);
  let lm=[];
  lm.push("배우자성은 <b>"+spouseName+"</b>이며, 배우자궁인 <b>일지 "+dayZ+"("+ZHI_BODY[dayZ]+" 자리)</b>의 상태가 인연의 바탕입니다. "+
    (hasDohwa?"사주에 도화가 있어 이성에게 매력이 닿기 쉽고 인연이 활발한 편입니다. ":"")+
    "연애 성향은 "+(male?"재성":"관성")+"이 "+(spouseSS.some(ss=>a.order.some(k=>sipsin(dg,s.pillars[k][0])===ss))?"드러나 적극적·현실적":"감춰져 신중·내향적")+"입니다.");
  const myr=timings(s,a,spouseSS,true);
  lm.push(myr.length?("인연·혼인이 무르익기 쉬운 시기는 <b>"+myr.map(y=>y+"년").join(", ")+"</b>경입니다(배우자성·도화·배우자궁 합이 드는 해). 이때 적극적으로 만남을 넓히면 좋습니다."):"향후 25년 중 뚜렷한 배우자성 시기는 약하니, 운에서 배우자성이 드는 해에 인연이 열립니다.");
  L.push(["연애·결혼운","💞",lm,["처","육친"]]);
  // 자녀
  const childSS=male?["정관","편관"]:["식신","상관"];
  const cyr=timings(s,a,childSS,false);
  L.push(["자녀운","🍼",["자녀성은 <b>"+(male?"관성(官星)":"식상(食傷)")+"</b>이며 시주(時柱)가 자녀 자리입니다. "+
    (cyr.length?"자녀·출산과 인연이 깊어지는 시기는 <b>"+cyr.map(y=>y+"년").join(", ")+"</b>경입니다.":"자녀성운이 드는 해에 자녀 인연이 깊어집니다.")+
    (s.pillars.hour?"":" (출생시 미상이라 시주 기반 분석은 제한됩니다.)")],["자식"]]);
  // 학업·이동
  const inseong=a.order.some(k=>["정인","편인"].includes(sipsin(dg,s.pillars[k][0])));
  const yeokma=new Set(["寅","申","巳","亥"]);const hasYeokma=a.order.some(k=>yeokma.has(s.pillars[k][1]));
  L.push(["학업·이동·기타","🎓",[
    (inseong?"인성(印星)이 있어 학문·문서·자격과 인연이 좋고 꾸준한 공부가 힘이 됩니다. ":"인성이 약해 실전·경험으로 배우는 편이 유리합니다. ")+
    (hasYeokma?"역마(寅申巳亥)가 있어 이동·여행·해외·변동과 인연이 많고, 활동 반경을 넓힐수록 기회가 옵니다.":"역마가 약해 한 자리에서 깊이를 더하는 안정형입니다.")],["인성","역마"]]);
  return '<div class="card"><div class="sec-title">정밀 풀이 — 직업·연애·결혼·자녀·학업</div>'+
    L.map(([t,e,arr,rk])=>'<div class="life-sec"><div class="life-t">'+e+' '+t+'</div>'+arr.map(x=>'<p>'+x+'</p>').join("")+refBlock(rk)+'</div>').join("")+
    '<div class="note">시기는 향후 25년 세운에서 배우자성·자녀성·도화·배우자궁 합충이 드는 해를 짚은 것으로, 절대적 예언이 아닌 가능성이 높은 흐름입니다.</div></div>';}
/* ===== 근거 인용 + 신살 상세 + 개운법 ===== */
function refBlock(keys){if(!keys)return "";for(const k of keys){if(REFS[k]&&REFS[k][0]){const r=REFS[k][0];
  return '<div class="ref click" onclick="this.classList.toggle(\'open\')" style="margin-top:8px"><div class="rt">📖 ['+k+'] 〔'+r.book+'〕 '+r.title+'</div><div class="rb">'+r.snippet+'…</div><div class="full">'+(r.full||r.snippet)+'…</div><div class="more">▾ 명리 원전 근거 펼쳐보기</div></div>';}}return "";}
const SHINSAL_INFO={
 "천을귀인":["길","하늘이 돕는 으뜸 길신. 총명·인덕이 있고 위기에 귀인의 도움을 받으며, 흉한 일도 길로 化합니다. 대인관계와 위기 대처에서 특히 빛납니다.",["천을귀인"]],
 "괴강":["양면","庚辰·庚戌·壬辰·戊戌 일주의 강렬한 살. 카리스마·결단·총명으로 권력·전문직·학문에서 크게 발하나, 충·형되면 길흉이 극단으로 갈리니 처세를 신중히 해야 합니다.",["괴강"]],
 "백호":["주의","피·사고·수술과 연관된 강한 살. 기질이 강하고 추진력이 있으나 혈광지사(血光之事)·건강을 조심해야 하며, 현대엔 외과·군경·정육·활인업(사람 살리는 일)으로 化하면 오히려 길합니다.",["백호"]],
 "양인":["양면","칼날처럼 강한 기운(羊刃). 과감·추진력·전문기술의 힘이나 과하면 부상·관재·다툼을 부르니, 칠살(七殺)과 어울리면 살인상정(殺刃相停)으로 큰 위세가 됩니다.",["양인"]],
 "도화":["양면","이성·매력·예술의 끼(桃花). 인기·연예·미적 감각에 유리하나 지나치면 색정·구설을 부르니 절제가 필요합니다.",["도화"]],
 "역마":["양면","이동·변동·해외의 기운(驛馬). 무역·여행·영업·유학에 길하나 분주함·이별·교통사고를 주의합니다.",["역마"]],
 "화개":["양면","예술·종교·철학·고독의 별(華蓋). 학예·수행에 깊이가 있으나 세속과 거리를 두는 고독함이 따릅니다. 인성과 만나면 학자·예술가의 격을 이룹니다.",["화개"]],
 "문창":["길","학문·시험·총명의 길신(文昌). 공부·자격·문서·창작 일에 유리합니다.",["문창"]],
 "건록":["길","일간이 뿌리내린 자립의 자리(建祿). 건강·자수성가·실력의 바탕이며 의지가 굳습니다.",["건록"]],
 "공망":["주의","비어 헛된 자리(空亡). 해당 기둥의 육친·재관이 결실을 맺기 어렵고 정신·종교성이 강해지나, 충·합으로 풀리거나 흉신이 공망되면 오히려 길이 되기도 합니다.",["공망"]],
 "천덕":["길","하늘의 덕(天德). 재앙을 막고 음덕과 평안을 주는 해신(解神)입니다.",["천덕"]],
 "월덕":["길","달의 덕(月德). 어려움에 도움과 자비·평안이 따르며 흉을 덜어줍니다.",["월덕"]]};
const GWE_GANG=new Set(["庚辰","庚戌","壬辰","戊戌"]);
function shinsalReport(s,a){const dg=s.dGan,yz=s.pillars.year[1],mz=s.pillars.month[1],gm=gongmangOf(gzIndex(s.pillars.day));
  const found=new Set();a.order.forEach(k=>{shenshaCol(dg,yz,mz,s.pillars[k],gm).forEach(x=>found.add(x));});
  if(GWE_GANG.has(s.pillars.day))found.add("괴강");
  const items=[...found].filter(x=>SHINSAL_INFO[x]);if(!items.length)return "";
  const ic={길:"🟢",양면:"🟡",주의:"🔴"};
  return '<div class="card"><div class="sec-title">신살(神煞) 상세 풀이</div>'+
    items.map(nm=>{const[gh,desc,rk]=SHINSAL_INFO[nm];
      return '<div class="life-sec"><div class="life-t">'+(ic[gh]||"")+' '+nm+' <span style="font-weight:400;color:var(--muted)">('+gh+')</span></div><p>'+desc+'</p>'+refBlock(rk)+'</div>';}).join("")+
    '<div class="note">신살은 사주의 색채를 더하는 요소입니다. 길신은 살리고 흉살은 직업·생활로 化하면 약이 되며, 근본은 격국·용신입니다.</div></div>';}
const GAEWOON={
 木:{방위:"동쪽",색:"초록·청록",숫자:"3·8",음식:"신맛·푸른 채소·간에 이로운 음식",직업:"교육·출판·기획·의류·환경"},
 火:{방위:"남쪽",색:"빨강·자주",숫자:"2·7",음식:"쓴맛·붉은 음식·심장에 이로운 음식",직업:"IT·방송·미디어·요식·미용"},
 土:{방위:"중앙",색:"노랑·황토",숫자:"5·0",음식:"단맛·황색 음식·위장에 이로운 음식",직업:"부동산·중개·건축·컨설팅"},
 金:{방위:"서쪽",색:"흰색·은색",숫자:"4·9",음식:"매운맛·흰 음식·폐에 이로운 음식",직업:"금융·기계·의료·법·금속"},
 水:{방위:"북쪽",색:"검정·남색",숫자:"1·6",음식:"짠맛·검은 음식·신장에 이로운 음식",직업:"무역·유통·수산·연구·관광"}};
function gaewoonReport(s,a){const yong=[...new Set(a.yo.list.map(x=>x[1]).filter(Boolean))];
  const lack=Object.entries(a.wx).filter(([w,c])=>c===0).map(([w])=>w);
  const need=[...new Set([...yong,...lack])].filter(w=>GAEWOON[w]);if(!need.length)return "";
  const L=need.map(w=>{const g=GAEWOON[w];return '<div class="life-sec"><div class="life-t">'+WXN[w]+'('+w+') 기운 보강</div>'+
    '<p>방위 <b>'+g.방위+'</b> · 행운색 <b>'+g.색+'</b> · 숫자 '+g.숫자+'<br>음식 '+g.음식+'<br>어울리는 분야 '+g.직업+'</p></div>';}).join("");
  return '<div class="card"><div class="sec-title">개운법(開運法) — 용신·부족 오행 보강</div>'+
    '<div class="note" style="margin:0 0 8px">용신/부족한 오행(<b>'+need.map(w=>WXN[w]).join("·")+'</b>)의 기운을 방위·색·생활·직업으로 북돋우면 운의 균형이 좋아집니다.</div>'+
    L+refBlock(["용신","조후"])+
    '<div class="note">색·방위·숫자 등은 상징적 보조이며, 근본 개운은 용신에 맞는 직업·환경·마음가짐의 선택에 있습니다.</div></div>';}
/* ===== 15영역 심층 분석 ===== */
function countSS(s,a){const dg=s.dGan,c={};
  a.order.forEach(k=>{if(k!=="day"){const t=sipsin(dg,s.pillars[k][0]);if(t&&t!=="일간")c[t]=(c[t]||0)+1;}
    const t2=sipsin(dg,HIDDEN[s.pillars[k][1]][0]);if(t2)c[t2]=(c[t2]||0)+1;});return c;}
const TALENT={식신:"표현·교육·요리·콘텐츠 창작",상관:"언변·예술·기획·비평·퍼포먼스",정재:"재무·회계·실무 관리",편재:"사업 수완·영업·투자 감각",정관:"조직 관리·통솔·공정한 리더십",편관:"위기관리·결단·강한 추진력",정인:"학습·연구·기획·전략 수립",편인:"전문기술·직관·심리·예술 감각",비견:"독립심·자기 주도·추진력",겁재:"승부 근성·경쟁력·실행력"};
function personalityReport(s,a){const dg=s.dGan,c=countSS(s,a),wx=a.wx,g=k=>c[k]||0;
  const sik=g("식신")+g("상관"),ins=g("정인")+g("편인"),jae=g("정재")+g("편재"),gwan=g("정관")+g("편관"),big=g("비견")+g("겁재");
  const jeong=g("정관")+g("정재")+g("정인"),pyeon=g("편관")+g("편재")+g("상관");
  const ax=(name,L,R,lv,rv)=>({name,pick:lv>rv?L:(lv<rv?R:"양쪽 균형"),strong:Math.abs(lv-rv)>=2});
  const A=[ax("사고 방식","직관·창의형","분석·신중형",sik+wx.火,ins+wx.金+wx.水),
    ax("삶의 태도","모험·도전형","안정·계획형",pyeon+big,jeong),
    ax("관심의 축","사람·관계 중심","결과·성취 중심",ins+big,jae+gwan),
    ax("판단 기준","감정·공감형","논리·체계형",sik+wx.火,gwan+ins+wx.金),
    ax("일하는 방식","즉흥·순발력형","장기·전략형",g("상관")+g("편재")+wx.火,g("정관")+g("정인")+wx.土+wx.金)];
  const axHtml=A.map(x=>'<div class="axis-row"><span class="axis-name">'+x.name+'</span><span class="axis-pick'+(x.strong?" strong":"")+'">'+x.pick+'</span></div>').join("");
  const desc="일간 "+wxWord(dg)+"을 중심으로, "+(ins>=sik?"받아들이고 분석하는 힘이 강해 신중하고 깊이 있게 사고":"표현하고 발산하는 힘이 강해 직관적이고 창의적으로 사고")+"하며, "+(jeong>=pyeon?"원칙과 안정 속에서 차근차근 쌓아가는":"변화와 도전 속에서 기회를 잡는")+" 성향입니다.";
  const tals=Object.entries(c).filter(([k])=>TALENT[k]).sort((x,y)=>y[1]-x[1]).slice(0,3);
  const talHtml=tals.length?("가장 도드라진 재능은 <b>"+tals.map(([k])=>k).join("·")+"</b>로, "+tals.map(([k])=>TALENT[k]).join("; ")+" 방면에서 강점을 보입니다."):"십신이 고르게 분포해 다방면에 두루 능한 편입니다.";
  return '<div class="card"><div class="sec-title">① 성격·사고방식 <span class="cred">정확도 높음 ★</span></div>'+
    '<div class="axis-box">'+axHtml+'</div><p class="deep-p">'+desc+'</p>'+refBlock(["성정"])+
    '<div class="sec-title" style="margin-top:16px">② 재능·강점</div><p class="deep-p">'+talHtml+'</p></div>';}
function extraReport(s,a){const dg=s.dGan,c=countSS(s,a),g=k=>c[k]||0,st=a.cls.strength.verdict,strong=(st==="신강");
  const jJ=g("정재"),pJ=g("편재"),jae=jJ+pJ,sik=g("식신")+g("상관"),big=g("비견")+g("겁재"),ins=g("정인")+g("편인");
  let money;
  if(jae===0)money="재성이 약해 <b>전문직·월급형</b>(기술·자격·조직 내 보상)이 안정적입니다. 재성운이 올 때 부수입·투자 기회가 열립니다.";
  else if(pJ>jJ&&sik>0)money="편재+식상 구조의 <b>사업·투자형</b>입니다. 재능과 기회를 결합해 유동적으로 버는 데 강점이 있습니다.";
  else if(pJ>jJ)money="편재가 강한 <b>사업·유동수입형</b>입니다. 큰 흐름을 보고 움직이되 관리가 따라야 합니다.";
  else if(big>=2&&jae>0)money="비겁+재 구조의 <b>동업·네트워크형</b>입니다. 사람을 통해 벌되 금전 관계는 명확히 하세요.";
  else money="정재 중심의 <b>안정 수입형</b>입니다. 꾸준한 직장·실물 비즈니스로 착실히 쌓는 데 유리합니다.";
  let inv=(pJ>0&&sik>0&&strong)?"편재·식상이 살아있고 신강하여 <b>공격적 투자</b>를 감당할 그릇이 있으나, 수익 실현(매도) 타이밍을 정해두는 규율이 관건입니다.":(jJ>0&&!strong)?"정재 중심·신약이라 <b>보수적·분산 투자</b>가 맞습니다. 무리한 레버리지는 피하세요.":"투자 성향이 뚜렷하지 않아, 용신운에 집중하고 기신운엔 보수적으로 운용하는 편이 안전합니다.";
  let biz=(pJ>0&&sik>0&&strong)?"편재·식상·신강의 조합으로 <b>사업 적성이 있는</b> 편입니다. 다만 성패는 업종·시기·동업 구도가 더 크게 좌우합니다.":(!strong&&jae>=3)?"재다신약이라 사업보다 <b>전문성·조직 기반</b>이 안전하며, 큰 확장은 신왕운에 도모하세요.":"사업은 작게 시작해 검증 후 키우는 방식이 맞습니다.";
  const jaego=a.order.some(k=>["辰","戌","丑","未"].includes(s.pillars[k][1]));
  let scale="사주는 '얼마'보다 '버는 방식'을 봅니다. "+(strong&&jae>0?"신왕재왕이라 노력에 비례해 재물을 모으는 그릇이 좋고, ":"")+(jaego?"재고(財庫)가 있어 모으고 쌓는 힘이 있습니다.":"꾸준한 흐름으로 관리하는 것이 핵심입니다.")+" (부의 절대 규모는 시대·선택·노력에 더 좌우됩니다.)";
  const cheonul=a.order.some(k=>TIANYI[dg].includes(s.pillars[k][1]));
  let help=(ins>0||cheonul||g("정관")>0)?"인성·"+(cheonul?"천을귀인·":"")+"정관의 도움 구조가 있어 <b>귀인의 조력을 잘 받는</b> 편입니다. 어른·스승·상사와의 인연을 소중히 하세요.":"스스로 개척하는 자수성가형입니다. 의식적으로 멘토·네트워크를 만들면 운이 트입니다.";
  const yeokma=a.order.some(k=>["寅","申","巳","亥"].includes(s.pillars[k][1]));
  let abroad=(yeokma||pJ>0)?"역마·편재의 기운으로 <b>해외·타지와 인연</b>이 있습니다. 유학·무역·해외 근무가 기회가 될 수 있습니다.":"해외 인연은 강하지 않으나, 역마운(寅申巳亥)이 드는 시기에 이동·해외 기회가 열립니다.";
  const sec=(t,cr,body,rk)=>'<div class="life-sec"><div class="life-t">'+t+' <span class="cred'+(cr==="참고"?" low":"")+'">'+cr+'</span></div><p>'+body+'</p>'+refBlock(rk)+'</div>';
  return '<div class="card"><div class="sec-title">③ 돈 버는 방식 · 투자 · 사업 · 부 · 귀인 · 해외</div>'+
    sec("💵 돈 버는 방식","정확도 높음",money,["재성","부귀"])+
    sec("📈 투자운","참고",inv)+sec("🏢 사업 가능성","참고",biz)+sec("💎 부의 규모","참고",scale)+
    sec("🤲 귀인운","",help,["천을귀인"])+sec("✈️ 해외운","",abroad,["역마"])+'</div>';}
function lifeFlowReport(s,a){const dg=s.dGan,{use,avoid}=useAvoid(s,a),dayZ=s.pillars.day[1];
  const phases=s.dae.list.map(d=>{const sc=judgeLuck(d.gz,use,avoid),ss=sipsin(dg,d.gz[0]);let p;
    if(sc>=1)p=["확장기","🟢",(ss.includes("재"))?"재물·실리가 늘어나는":(ss.includes("관"))?"지위·명예가 오르는":"기운이 트이고 뻗어가는"];
    else if(sc<=-1)p=["정체·수렴기","🔴","무리한 확장보다 내실을 다질"];
    else p=["변화·조정기","🟡","흐름이 바뀌고 재정비할"];
    return {age:d.age,gz:d.gz,p};});
  const flowHtml=phases.map(x=>'<div class="flow-row"><span class="flow-age">'+x.age+'세~</span><span style="font-size:15px;font-weight:700">'+wxSpan(x.gz[0])+wxSpan(x.gz[1])+'</span><span class="flow-ph">'+x.p[1]+' '+x.p[0]+'</span><span class="flow-d">— '+x.p[2]+' 시기</span></div>').join("");
  const turns=[];s.dae.list.forEach(d=>{const z=d.gz[1],r=[];
    if(ZHI_CHONG.has(pairKey(z,dayZ,ZHI)))r.push("일지 충(이사·이직·독립·관계 변화)");
    if(["寅","申","巳","亥"].includes(z)&&!a.order.some(o=>s.pillars[o][1]===z))r.push("역마운(이동·해외)");
    const ss=sipsin(dg,d.gz[0]);if(["정재","편재","정관","편관"].includes(ss))r.push((ss.includes("재")?"재성":"관성")+"운(결혼·취업·승진의 계기)");
    if(r.length)turns.push(d.age+"세 전후 — "+r.join(", "));});
  return '<div class="card"><div class="sec-title">⑨ 인생의 흐름 (대운) <span class="cred">정확도 높음 ★</span></div>'+
    '<div class="flow-box">'+flowHtml+'</div>'+
    '<div class="sec-title" style="margin-top:14px">⑩ 큰 전환점</div>'+
    (turns.length?'<ul class="turn-list">'+turns.map(t=>'<li>'+t+'</li>').join("")+'</ul>':'<p class="note">뚜렷한 대운 전환점은 약하며, 세운에서 충·역마가 드는 해에 변동이 옵니다.</p>')+
    '<div class="note">시기는 용신 부합·충·역마로 가늠한 흐름으로, 절대적 예언이 아닌 큰 추세입니다.</div></div>';}
function gzIndex(gz){for(let i=0;i<60;i++)if(GAN[i%10]===gz[0]&&ZHI[i%12]===gz[1])return i;return 0;}
function gongmangOf(didx){const s=(didx-(didx%10))%12;return [ZHI[(s+10)%12],ZHI[(s+11)%12]];}
function shenshaCol(dg,yz,mz,gz,gm){const z=gz[1],g=gz[0],r=[];
  if(TIANYI[dg].includes(z))r.push("천을귀인");
  if(z===MAYI[yz])r.push("역마"); if(z===TAOHUA[yz])r.push("도화"); if(z===HUAGAI[yz])r.push("화개");
  if(YANGIN[dg]===z)r.push("양인"); if(WENCHANG[dg]===z)r.push("문창"); if(LU[dg]===z)r.push("건록");
  if(BAEKHO.has(gz))r.push("백호"); if(gm&&gm.includes(z))r.push("공망");
  if(CHEONDEOK[mz]===g||CHEONDEOK[mz]===z)r.push("천덕"); if(WOLDEOK[mz]===g)r.push("월덕");
  return r;}
function colHtml(label,gz,ss,dg,yz,mz,gm,kind){const g=gz[0],z=gz[1];
  const hid=HIDDEN[z],hidss=hid.map(h=>sipsin(dg,h)),tw=twelveStage(dg,z),sh=shenshaCol(dg,yz,mz,gz,gm);
  const cls='pcol'+(kind==='day'?' pcol-day':'')+(kind==='luck'?' pcol-luck':'');
  return '<div class="'+cls+'"><div class="pos">'+label+'</div>'+
    '<div class="ss">'+(ss==="일간"?"일간":ss)+'</div>'+
    '<div class="gbox '+WX_CLASS[wxOf(g)]+'b" data-char="'+g+'" data-type="gan" onclick="charClick(this)">'+g+'</div>'+
    '<div class="gbox '+WX_CLASS[wxOf(z)]+'b" data-char="'+z+'" data-type="zhi" onclick="charClick(this)">'+z+'</div>'+
    '<div class="hss">'+hidss.join("·")+'</div>'+
    '<div class="hgan">'+hid.join("")+'</div>'+
    '<div class="tw">'+tw+'</div>'+
    '<div class="ssal">'+(sh.length?sh.join("<br>"):"·")+'</div></div>';}
function charRelations(ch,ty){const he=new Set(),chong=new Set();
  if(ty==="gan"){
    Object.keys(GAN_HE).forEach(k=>{if(k.includes(ch))[...k].forEach(x=>{if(x!==ch)he.add(x);});});
    GAN_CHONG.forEach(k=>{if(k.includes(ch))[...k].forEach(x=>{if(x!==ch)chong.add(x);});});
  }else{
    ZHI_LIUHE.forEach(k=>{if(k.includes(ch))[...k].forEach(x=>{if(x!==ch)he.add(x);});});
    Object.keys(ZHI_SANHE).forEach(k=>{if(k.includes(ch))[...k].forEach(x=>{if(x!==ch)he.add(x);});});
    ZHI_CHONG.forEach(k=>{if(k.includes(ch))[...k].forEach(x=>{if(x!==ch)chong.add(x);});});
  }
  return {he,chong};}
function relationDesc(ch,ty){const he=[],chong=[];
  if(ty==="gan"){
    Object.entries(GAN_HE).forEach(([k,v])=>{if(k.includes(ch))he.push([...k].filter(x=>x!==ch).join("")+"과 천간합("+v+")");});
    GAN_CHONG.forEach(k=>{if(k.includes(ch))chong.push([...k].filter(x=>x!==ch).join("")+"과 천간충");});
  }else{
    ZHI_LIUHE.forEach(k=>{if(k.includes(ch))he.push([...k].filter(x=>x!==ch).join("")+" 육합");});
    Object.entries(ZHI_SANHE).forEach(([k,v])=>{if(k.includes(ch))he.push([...k].filter(x=>x!==ch).join("·")+" 삼합("+v+")");});
    ZHI_CHONG.forEach(k=>{if(k.includes(ch))chong.push([...k].filter(x=>x!==ch).join("")+" 충");});
  }
  return {he,chong};}
const CHAR_INFO_DEFAULT='<div class="ci-title">글자 관계</div><div class="note" style="margin:0">천간·지지 글자를 누르면 <span class="luck-good">합(초록 실선)</span>·<span class="luck-bad">충(빨강 점선)</span> 관계 글자가 테두리로 표시되고, 여기에 설명이 나옵니다.</div>';
function autoHighlightRune(){const wrap=document.getElementById("pillarsWrap");if(!wrap||!window.CUR)return;
  const sel=window.CUR.sel||{},runeC=[];
  ["wol","se","dae"].forEach(k=>{if(sel[k]){runeC.push(["gan",sel[k].gz[0]]);runeC.push(["zhi",sel[k].gz[1]]);}});
  wrap.querySelectorAll(".gbox").forEach(b=>{b.classList.remove("rel-self","rel-he-box","rel-chong-box");});
  if(!runeC.length)return;
  wrap.querySelectorAll(".gbox").forEach(b=>{const ch=b.dataset.char,ty=b.dataset.type,isLuck=!!b.closest(".pcol-luck");
    if(isLuck){b.classList.add("rel-self");return;}
    let he=false,chong=false;
    runeC.forEach(([rty,rc])=>{if(rty!==ty)return;const R=charRelations(rc,ty);
      if(R.chong.has(ch))chong=true;else if(R.he.has(ch))he=true;});
    if(chong)b.classList.add("rel-chong-box");else if(he)b.classList.add("rel-he-box");});}
function charClick(el){const wrap=document.getElementById("pillarsWrap");if(!wrap)return;
  const info=document.getElementById("charInfo");
  const already=el.classList.contains("rel-self");
  wrap.querySelectorAll(".gbox").forEach(b=>b.classList.remove("rel-self","rel-he-box","rel-chong-box"));
  if(already){if(info)info.innerHTML=CHAR_INFO_DEFAULT;return;}
  el.classList.add("rel-self");
  const ch=el.dataset.char,ty=el.dataset.type,{he,chong}=charRelations(ch,ty);
  wrap.querySelectorAll(".gbox").forEach(b=>{if(b===el||b.dataset.type!==ty)return;
    if(he.has(b.dataset.char))b.classList.add("rel-he-box");
    else if(chong.has(b.dataset.char))b.classList.add("rel-chong-box");});
  if(info){const d=relationDesc(ch,ty);
    info.innerHTML='<div class="ci-title"><span class="ci-ch">'+ch+'</span> ('+(ty==="gan"?"천간":"지지")+') 관계</div>'+
      '<div style="font-size:12.5px;margin-top:6px"><span class="luck-good">━</span> 합: <b>'+(d.he.length?d.he.join(", "):"없음")+'</b></div>'+
      '<div style="font-size:12.5px;margin-top:4px"><span class="luck-bad">┅</span> 충: <b>'+(d.chong.length?d.chong.join(", "):"없음")+'</b></div>';}}
function relationsDiagram(s,sel,dg){const cols=[];
  if(sel&&sel.wol)cols.push(["월운",sel.wol.gz]); if(sel&&sel.se)cols.push(["세운",sel.se.gz]); if(sel&&sel.dae)cols.push(["대운",sel.dae.gz]);
  ["hour","day","month","year"].forEach(k=>{if(s.pillars[k])cols.push([POSF[k],s.pillars[k]]);});
  const rels=[];
  for(let i=0;i<cols.length;i++)for(let j=i+1;j<cols.length;j++){const[la,ga]=cols[i],[lb,gb]=cols[j];
    const gk=pairKey(ga[0],gb[0],GAN);
    if(GAN_HE[gk])rels.push([la+"·"+lb,ga[0]+gb[0]+"합("+GAN_HE[gk]+")","he"]);
    if(GAN_CHONG.has(gk))rels.push([la+"·"+lb,ga[0]+gb[0]+"충","chong"]);
    const zk=pairKey(ga[1],gb[1],ZHI);
    if(ZHI_LIUHE.has(zk))rels.push([la+"·"+lb,ga[1]+gb[1]+"육합","he"]);
    if(ZHI_CHONG.has(zk))rels.push([la+"·"+lb,ga[1]+gb[1]+"충","chong"]);
    if(ZHI_XING.has(zk))rels.push([la+"·"+lb,ga[1]+gb[1]+(ga[1]===gb[1]?"자형":"형"),"xing"]);
    if(ZHI_PA.has(zk))rels.push([la+"·"+lb,ga[1]+gb[1]+"파","pa"]);
    if(ZHI_HAI.has(zk))rels.push([la+"·"+lb,ga[1]+gb[1]+"해","hai"]);
    if(WONJIN[ga[1]]===gb[1])rels.push([la+"·"+lb,ga[1]+gb[1]+"원진","won"]);}
  const allz=cols.map(c=>c[1][1]);
  for(const combo in ZHI_SANHE){if([...combo].every(c=>allz.includes(c)))rels.push(["전국",combo+"삼합("+ZHI_SANHE[combo]+")","he"]);}
  if(!rels.length)return '<div class="note" style="margin-top:10px">기둥 간 뚜렷한 합·충·형·파·해·원진 없음.</div>';
  return '<div class="sec-title" style="margin-top:14px;font-size:12px">기둥 관계 (합·충·형·파·해·원진·삼합)</div>'+
    '<div class="kv">'+rels.map(r=>'<span class="tag rel-'+r[2]+'"><b>'+r[0]+'</b> '+r[1]+'</span>').join("")+'</div>';}
function pillarsCard(s,a,sel){const dg=s.dGan,yz=s.pillars.year[1],mz=s.pillars.month[1];
  const gm=gongmangOf(gzIndex(s.pillars.day));const cols=[];
  if(sel&&sel.wol)cols.push(colHtml("월운 "+sel.wol.label,sel.wol.gz,sipsin(dg,sel.wol.gz[0]),dg,yz,mz,gm,'luck'));
  if(sel&&sel.se)cols.push(colHtml("세운"+(sel.se.Y?" "+sel.se.Y:""),sel.se.gz,sipsin(dg,sel.se.gz[0]),dg,yz,mz,gm,'luck'));
  if(sel&&sel.dae)cols.push(colHtml("대운"+(sel.dae.age?" "+sel.dae.age+"세":""),sel.dae.gz,sipsin(dg,sel.dae.gz[0]),dg,yz,mz,gm,'luck'));
  ["hour","day","month","year"].forEach(k=>{if(s.pillars[k]){const ss=k==="day"?"일간":sipsin(dg,s.pillars[k][0]);
    cols.push(colHtml(POSF[k],s.pillars[k],ss,dg,yz,mz,gm,k==="day"?'day':''));}});
  const sub=(sel&&(sel.se||sel.dae))?' + 운 (다시 누르면 해제)':'';
  return '<div class="card" id="pillarsWrap"><div class="sec-title">사주 원국'+sub+'</div>'+
    '<div class="pillarrow"><div class="pillars wide">'+cols.join("")+'</div>'+animalCard(s)+
      '<div class="char-info" id="charInfo">'+CHAR_INFO_DEFAULT+'</div></div>'+
    '<div class="note" style="margin-top:6px">아래 대운·세운을 누르면 이 자리에 함께 표시됩니다.</div>'+
    relationsDiagram(s,sel,dg)+runeReport(s,a,sel)+'</div>';}
function pickLuck(kind,gz,extra){if(!window.CUR)return;window.CUR.sel=window.CUR.sel||{};
  const key=(kind==="세운")?"se":(kind==="대운")?"dae":"wol",sel=window.CUR.sel;
  if(sel[key]&&sel[key].gz===gz)sel[key]=null;
  else sel[key]=(kind==="세운")?{gz:gz,Y:extra}:(kind==="대운")?{gz:gz,age:extra}:{gz:gz,label:extra};
  const el=document.getElementById("pillarsWrap");if(el)el.outerHTML=pillarsCard(window.CUR.s,window.CUR.a,sel);
  if(kind==="대운"){highlightDae(sel.dae?sel.dae.age:null);}
  if(kind==="세운"){refreshWol(sel.se?sel.se.Y:new Date().getFullYear());}
  autoHighlightRune();
  const nw=document.getElementById("pillarsWrap");if(nw)nw.scrollIntoView({behavior:"smooth",block:"start"});}
function highlightDae(age){
  document.querySelectorAll(".se-cell").forEach(c=>{const a=+c.dataset.age;
    c.classList.toggle("in-dae", age!=null && a>=Math.round(age) && a<Math.round(age)+10);});
  document.querySelectorAll(".dae-cell").forEach(c=>c.classList.toggle("dae-on", age!=null && +c.dataset.daeage===age));
  const sf=document.getElementById("seFlow");const fst=sf&&sf.querySelector(".se-cell.in-dae");
  if(sf&&fst)sf.scrollLeft=fst.offsetLeft-sf.offsetLeft-20;}
function render(s,a,Y,M,D,h){
  const p=s.pillars,POS={year:"년주",month:"월주",day:"일주",hour:"시주"};
  let pc="";a.order.forEach(k=>{const g=p[k][0],z=p[k][1];
    pc+='<div class="pcol"><div class="pos">'+POS[k]+'</div>'+
      '<div class="ss">'+(a.ss[k]==="일간"?"일간(아신)":a.ss[k])+'</div>'+
      '<div class="gz">'+wxSpan(g)+wxSpan(z)+'</div>'+
      '<div class="ko">'+GAN_KO[g]+ZHI_KO[z]+'</div>'+
      '<div class="sub">'+a.hid[k].map(x=>x+"("+sipsin(s.dGan,x)+")").join("<br>")+
      '<br>'+a.tw[k]+'</div></div>';});
  const wxStr=Object.entries(a.wx).map(([w,c])=>'<span class="'+WX_CLASS[w]+'">'+w+c+'</span>').join("  ");
  const shStr=Object.entries(a.sh).map(([k,v])=>'<span class="tag"><b>'+k+'</b> '+v.join("")+'</span>').join("");
  const itStr=Object.entries(a.inter).map(([k,v])=>'<span class="tag"><b>'+k+'</b> '+v.join("·")+'</span>').join("");
  const yoStr=a.yo.list.map(([l,w])=>l+(w?"("+w+")":"")).join(", ");
  let dae=s.dae.list.map(x=>'<div class="dcell"><div class="age">'+x.age+'세</div><div class="dgz">'+wxSpan(x.gz[0])+wxSpan(x.gz[1])+'</div></div>').join("");
  const hourNote=(h==null)?'<div class="note">시(時) 미상 → 시주 제외 3주 분석. 신살·대운은 정오 가정값입니다.</div>':'';
  const html=
    pillarsCard(s,a,null)+
    '<div class="card"><div class="kv"><span class="tag">'+Y+'.'+M+'.'+D+(h!=null?' '+String(h).padStart(2,"0")+'시':'')+' '+SEX+'</span>'+
      '<span class="tag">일간 <b>'+wxWord(s.dGan)+'</b></span>'+
      '<span class="tag">오행 '+wxStr+'</span>'+
      '<span class="tag">강약 <b>'+a.st.verdict+'</b> ('+a.st.score+')</span></div>'+hourNote+'</div>'+
    fortuneCard(s,a)+
    personalityReport(s,a)+
    lifeReport2(s,a)+
    extraReport(s,a)+
    lifeReport(s,a)+
    lifeFlowReport(s,a)+
    shinsalReport(s,a)+
    gaewoonReport(s,a)+
    interpretCard(s,a)+
    '<div class="card"><div class="sec-title">격국 · 용신 · 조후</div>'+
      '<div class="kv"><span class="tag">격국 <b>'+(a.cls.geuk||"미정")+'</b> <span style="color:var(--muted)">'+a.cls.type+'</span></span>'+
        '<span class="tag">월지 '+p.month[1]+'</span>'+
        ((a.cls.gg&&a.cls.gg.투출겸&&a.cls.gg.투출겸.length)?'<span class="tag">투출 '+a.cls.gg.투출겸.map(x=>x[0]+'·'+x[1]).join(", ")+'</span>':'')+
        (a.cls.note?'<span class="tag">'+a.cls.note+'</span>':'')+'</div>'+
      '<div class="kv"><span class="tag">용신(부억) <b>'+yoStr+'</b></span>'+
        (a.jh[0]?'<span class="tag">조후 <b>'+a.jh[0]+'</b></span>':'')+'</div>'+
      '<div class="note">'+a.yo.note+(a.jh[0]?' · '+a.jh[1]:'')+'</div>'+
      twoViewsHtml(a)+'</div>'+
    ((shStr||itStr)?'<div class="card"><div class="sec-title">신살 · 합충</div><div class="kv">'+shStr+itStr+'</div></div>':'')+
    refsCard(a);
  window.CUR={s,a,sel:null};
  const r=document.getElementById("result");r.innerHTML=html;r.classList.remove("hidden");
  const sf=document.getElementById("seFlow");const nowc=sf&&sf.querySelector(".se-cell.now");
  if(sf&&nowc)sf.scrollLeft=nowc.offsetLeft-sf.offsetLeft-100;
  r.scrollIntoView({behavior:"smooth",block:"start"});
}
function wxWord(g){const w=GAN_WX[g];const names={木:"목",火:"화",土:"토",金:"금",水:"수"};
  return GAN_KO[g]+g+"("+names[w]+")";}
const WXN={木:"목",火:"화",土:"토",金:"금",水:"수"};
function interpret(s,a){const dg=s.dGan,dw=GAN_WX[dg],cls=a.cls,L=[];
  L.push("일간이 <b>"+GAN_KO[dg]+dg+"("+WXN[dw]+")</b>이며, 사주 전체로 보아 <b>"+cls.strength.verdict+"</b>(점수 "+cls.strength.score+")합니다. "+
    (cls.strength.verdict==="신강"?"기운이 강하니 이를 덜어 쓰는 길을 기뻐합니다.":
     cls.strength.verdict==="신약"?"기운이 약하니 도와주는 운을 기뻐합니다.":"기운이 비교적 균형을 이룹니다."));
  if(cls.geuk){let d=cls.type==="종격"?"일간이 무근·고립하여 왕한 세력을 따르는 ":(cls.type==="화기격"?"일간이 인접 천간과 합하여 기운이 化한 ":"월령을 중심으로 정해지는 ");
    L.push("격국은 "+d+"<b>"+cls.geuk+"</b>입니다"+(cls.note?" — "+cls.note:"")+".");}
  L.push("부조·억부로 본 용신은 <b>"+a.yo.list.map(x=>x[0]+(x[1]?"("+WXN[x[1]]+")":"")).join("·")+"</b> 계열입니다. "+a.yo.note+".");
  if(a.jh[0])L.push("계절(조후)로는 "+a.jh[1]+".");
  const shk=Object.keys(a.sh);if(shk.length)L.push("주요 신살로는 <b>"+shk.join("·")+"</b>이(가) 있습니다.");
  const lack=Object.entries(a.wx).filter(x=>x[1]===0).map(x=>WXN[x[0]]);
  const many=Object.entries(a.wx).filter(x=>x[1]>=4).map(x=>WXN[x[0]]);
  if(lack.length||many.length){let m="오행으로는 ";if(many.length)m+="<b>"+many.join("·")+"</b>이 왕성";if(many.length&&lack.length)m+="하고 ";
    if(lack.length)m+="<b>"+lack.join("·")+"</b>이 없어 그 기운이 부족";m+="합니다.";L.push(m);}
  return L;}
function twoViewsHtml(a){let cs=(a.cls.candidates||[]).slice();
  if(cs.length<2)return "";
  cs.sort((x,y)=>(y.geuk===a.cls.geuk?1:0)-(x.geuk===a.cls.geuk?1:0));  // 주격 우선
  let h='<div class="sec-title" style="margin-top:16px;font-size:12px">⚖ 격이 갈리는 사주 — 두 견해</div>'+
    '<div class="note" style="margin:0 0 6px">잡기·투출 등으로 관점에 따라 격이 다르게 잡힙니다. 각 견해의 고전 근거를 펼쳐 비교해 보세요.</div>';
  cs.forEach((c,i)=>{const r=(REFS[c.geuk]||[])[0];
    h+='<div class="ref click" onclick="this.classList.toggle(\'open\')">'+
      '<div class="rt">'+(i===0?'주격 ':'또 다른 견해 ')+'<b>'+c.geuk+'</b> — '+c.basis+' 기준 ('+wxSpan(c.gan)+' '+c.ss+')</div>'+
      (r?'<div class="rb">'+r.snippet+'…</div><div class="full">'+(r.full||r.snippet)+'…</div><div class="more">▾ 고전 근거 자세히</div>':'')+
      '</div>';});
  return h;}
function interpretCard(s,a){return '<div class="card"><div class="sec-title">종합 해석</div><div class="interp">'+
  interpret(s,a).map(x=>'<p>'+x+'</p>').join("")+'</div><div class="note">고전 명리 규칙에 따른 자동 해석으로, 참고용입니다.</div></div>';}
function refsCard(a){const keys=[];
  if(a.cls.geuk&&REFS[a.cls.geuk])keys.push(a.cls.geuk);
  if(REFS[a.cls.strength.verdict])keys.push(a.cls.strength.verdict);
  Object.keys(a.sh).forEach(k=>{if(REFS[k])keys.push(k);});
  if(REFS["용신"])keys.push("용신");
  const uniq=[...new Set(keys)].filter(k=>REFS[k]).slice(0,5);
  if(!uniq.length)return "";
  let h='<div class="card"><div class="sec-title">고전 근거</div>';
  uniq.forEach(k=>{const r=REFS[k][0];const full=(r.full||r.snippet);
    h+='<div class="ref click" onclick="this.classList.toggle(\'open\')"><div class="rt">['+k+'] 〔'+r.book+'〕 '+r.title+'</div>'+
       '<div class="rb">'+r.snippet+'…</div>'+
       '<div class="full">'+full+'…</div><div class="more">▾ 자세히 보기</div></div>';});
  h+='<div class="note">고전 9책 한국어 번역 DB에서 발췌. 구절을 누르면 펼쳐집니다.</div></div>';return h;}
/* ===== 운세: 세운·대운 길흉 (용신 부합도) ===== */
const FIELD={정관:"명예·직장·승진",편관:"도전·권력·압박·관재",정인:"학업·문서·귀인·안정",편인:"학문·자격·심리",
  식신:"표현·재능·여유·식복",상관:"활동·변화·구설",정재:"재물·안정·결실",편재:"사업·투자·기회",
  비견:"협력·독립·경쟁",겁재:"경쟁·지출·동료"};
function luckWx(a){const dg=a.order&&a.cls?a.cls:null;return null;}
function useAvoid(s,a){const dg=s.dGan,dw=GAN_WX[dg];let yin=null;for(const k in SHENG)if(SHENG[k]===dw)yin=k;
  const food=SHENG[dw],wealth=KE[dw];let off=null;for(const k in KE)if(KE[k]===dw)off=k;
  const v=a.cls.strength.verdict;let use,avoid;
  if(v==="신강"){use=new Set([off,wealth,food]);avoid=new Set([dw,yin]);}
  else if(v==="신약"){use=new Set([dw,yin]);avoid=new Set([food,wealth,off]);}
  else{use=new Set([a.jh[0]].filter(Boolean));avoid=new Set();}
  return {use,avoid};}
function judgeLuck(gz,use,avoid){let sc=0;[GAN_WX[gz[0]],ZHI_WX[gz[1]]].forEach(w=>{
  if(use.has(w))sc++;if(avoid.has(w))sc--;});return sc;}
function luckMark(sc){return sc>0?['○','luck-good']:(sc<0?['●','luck-bad']:['△','luck-mid']);}
function fortune(s,a){const dg=s.dGan;const {use,avoid}=useAvoid(s,a);
  const nowY=new Date().getFullYear();const sajuY=s.sajuYear;const list=[];
  for(let Y=sajuY;Y<=sajuY+89;Y++){const idx=((Y-4)%60+60)%60;const gz=GAN[idx%10]+ZHI[idx%12];
    const sc=judgeLuck(gz,use,avoid);const tg=sipsin(dg,gz[0]);
    list.push({Y,age:Y-sajuY+1,gz,sc,sipsin:tg,now:Y===nowY});}
  // 대운 길흉
  const dl=s.dae.list.map(d=>({...d,sc:judgeLuck(d.gz,use,avoid),sipsin:sipsin(dg,d.gz[0])}));
  return {use:[...use],avoid:[...avoid],list,dl};}
const WOL_JQ=["입춘","경칩","청명","입하","망종","소서","입추","백로","한로","입동","대설","소한"];
const WOL_SOLAR=[2,3,4,5,6,7,8,9,10,11,12,1];  // 寅월~丑월의 양력 시작월(절입 기준)
function wolCells(s,a,Y){const yidx=((Y-4)%60+60)%60,yinHead=((yidx%10)%5)*2+2;
  const {use,avoid}=useAvoid(s,a),dg=s.dGan,order=[2,3,4,5,6,7,8,9,10,11,0,1];
  return order.map((zi,i)=>{const tg=(yinHead+i)%10,gz=GAN[tg]+ZHI[zi];
    const sc=judgeLuck(gz,use,avoid),[m,c]=luckMark(sc),ss=sipsin(dg,gz[0]),lab=ZHI[zi]+"월";
    return '<div class="dcell click" onclick="pickLuck(\'월운\',\''+gz+'\',\''+lab+'\')"><div class="age">양 '+WOL_SOLAR[i]+'월<br>'+lab+'·'+WOL_JQ[i]+'</div><div class="dgz">'+wxSpan(gz[0])+wxSpan(gz[1])+'</div><div class="'+c+'" style="font-size:13px">'+m+' '+ss+'</div></div>';}).join("");}
function refreshWol(Y){const box=document.getElementById("wolFlowBox");if(!box||!window.CUR)return;
  box.innerHTML=wolCells(window.CUR.s,window.CUR.a,Y);box.dataset.year=Y;
  const t=document.getElementById("wolTitle");if(t)t.innerHTML="월운 흐름 ("+Y+"년)";}
/* 운(대운·세운) ↔ 원국 관계 */
const POSKO={year:"년주",month:"월주",day:"일주",hour:"시주"};
function luckRelations(gz,s,a){const lg=gz[0],lz=gz[1],p=s.pillars,dg=s.dGan,rel=[];
  a.order.forEach(k=>{const g=p[k][0],z=p[k][1];
    const gk=pairKey(lg,g,GAN);
    if(GAN_HE[gk])rel.push(POSKO[k]+" 천간 "+lg+g+"합("+GAN_HE[gk]+")");
    if(GAN_CHONG.has(gk))rel.push(POSKO[k]+" 천간 "+lg+g+"충");
    const zk=pairKey(lz,z,ZHI);
    if(ZHI_LIUHE.has(zk))rel.push(POSKO[k]+" 지지 "+lz+z+"육합");
    if(ZHI_CHONG.has(zk))rel.push(POSKO[k]+" 지지 "+lz+z+"충");
    if(ZHI_XING.has(zk))rel.push(POSKO[k]+" 지지 "+lz+z+(lz===z?"자형":"형"));
    if(ZHI_PA.has(zk))rel.push(POSKO[k]+" 지지 "+lz+z+"파");
    if(ZHI_HAI.has(zk))rel.push(POSKO[k]+" 지지 "+lz+z+"해");});
  // 삼합: 운 지지 + 원국 지지들
  const br=a.order.map(k=>p[k][1]);
  for(const combo in ZHI_SANHE){if(combo.includes(lz)){const need=[...combo].filter(c=>c!==lz);
    if(need.every(c=>br.includes(c)))rel.push("원국과 "+combo+" 삼합("+ZHI_SANHE[combo]+")");}}
  return rel;}
function showLuck(gz,label){const s=window.CUR&&window.CUR.s,a=window.CUR&&window.CUR.a;if(!s)return;
  const dg=s.dGan,lg=gz[0],lz=gz[1];
  const rels=luckRelations(gz,s,a);
  const tgss=sipsin(dg,lg),dzss=sipsin(dg,HIDDEN[lz][0]),tw=twelveStage(dg,lz);
  const sh=shensha(dg,s.pillars.year[1],[lz]);
  const shStr=Object.keys(sh).length?Object.keys(sh).join("·"):"없음";
  const {use,avoid}=useAvoid(s,a);const sc=judgeLuck(gz,use,avoid);const[mk,mc]=luckMark(sc);
  const h='<div class="sec-title" style="margin-top:4px">'+label+' 상세 — '+wxSpan(lg)+wxSpan(lz)+' <span class="'+mc+'">'+mk+'</span></div>'+
    '<div class="kv"><span class="tag">천간 <b>'+tgss+'</b></span><span class="tag">지지본기 <b>'+dzss+'</b></span>'+
      '<span class="tag">십이운성 <b>'+tw+'</b></span><span class="tag">신살 '+shStr+'</span></div>'+
    '<div class="note" style="margin-top:8px"><b>원국과의 관계:</b> '+(rels.length?rels.join(", "):"뚜렷한 합충형파해 없음")+
      '. '+(FIELD[tgss]?"이 시기는 "+FIELD[tgss]+" 관련 기운이 작동합니다.":"")+'</div>';
  const el=document.getElementById("luckPanel");if(el){el.innerHTML=h;el.classList.remove("hidden");el.scrollIntoView({behavior:"smooth",block:"center"});}}
function fortuneCard(s,a){const f=fortune(s,a);const WXN={木:"목",火:"화",土:"토",金:"금",水:"수"};const nowY=new Date().getFullYear();
  const cells=f.list.map(x=>{const[m,c]=luckMark(x.sc);
    return '<div class="dcell click se-cell'+(x.now?' now':'')+'" data-age="'+x.age+'" onclick="pickLuck(\'세운\',\''+x.gz+'\','+x.Y+')"><div class="age">'+x.Y+'·'+x.age+'세</div><div class="dgz">'+wxSpan(x.gz[0])+wxSpan(x.gz[1])+'</div><div class="'+c+'" style="font-size:13px">'+m+' '+(x.sipsin||'')+'</div></div>';}).join("");
  const dcells=f.dl.map(x=>{const[m,c]=luckMark(x.sc);
    return '<div class="dcell click dae-cell" data-daeage="'+x.age+'" onclick="pickLuck(\'대운\',\''+x.gz+'\','+x.age+')"><div class="age">'+x.age+'세~</div><div class="dgz">'+wxSpan(x.gz[0])+wxSpan(x.gz[1])+'</div><div class="'+c+'" style="font-size:13px">'+m+'</div></div>';}).join("");
  const nowAge=(f.list.find(x=>x.now)||{age:1}).age;
  const fut=f.list.filter(x=>x.sc>0&&x.age>=nowAge);
  const fields=[...new Set(fut.map(x=>FIELD[x.sipsin]).filter(Boolean))];
  const fieldNote=fut.length?('앞으로의 길운('+fut.map(x=>x.Y+"년").slice(0,4).join("·")+(fut.length>4?" 등":"")+')에는 '+fields.slice(0,3).join(", ")+' 방면이 순조롭습니다.'):'';
  return '<div class="card"><div class="sec-title">대운 ('+(s.dae.forward?"순행":"역행")+'·기운 '+s.dae.startAge+'세) 길흉 <span style="font-weight:400;color:var(--muted)">— 칸을 누르면 위 사주에 합쳐집니다</span></div>'+
    '<div class="note" style="margin:0 0 8px">간지 밑 표시: <span class="luck-good">○ 길</span>(용신 도움) · <span class="luck-bad">● 주의</span>(기신) · <span class="luck-mid">△ 평</span>(중립). 대운을 누르면 그 10년에 속한 세운이 테두리로 묶입니다.</div>'+
    '<div class="dae">'+dcells+'</div>'+
    '<div class="sec-title" style="margin-top:16px">세운 흐름 (출생~만년 · <span class="luck-mid">올해 강조</span>)</div><div class="dae" id="seFlow">'+cells+'</div>'+
    '<div class="sec-title" id="wolTitle" style="margin-top:16px">월운 흐름 ('+nowY+'년)</div>'+
    '<div class="note" style="margin:0 0 6px">세운(연)을 누르면 그 해의 월운으로 바뀝니다. 월운을 누르면 위 사주에 합쳐집니다.</div>'+
    '<div class="dae" id="wolFlowBox" data-year="'+nowY+'">'+wolCells(s,a,nowY)+'</div>'+
    '<div class="note">용신 <b>'+f.use.map(w=>WXN[w]).join("·")+'</b> 기준. '+fieldNote+' (억부용신 기준 참고용)</div></div>';}
fillSelects();
renderExamples();
fillSelects2();
loadFromHash();
</script>
</body>
</html>"""

out = HTML.replace("__JIEQI__", jieqi).replace("__LUNAR__", lunar).replace("__REFS__", refs)
open(os.path.join(HERE,"saju_web.html"),"w",encoding="utf-8").write(out)
print("saju_web.html 생성:", round(len(out)/1024,1),"KB")
