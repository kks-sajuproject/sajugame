// JS 만세력 엔진 ↔ Python(sxtwl) 정답 대조 검증
const fs = require('fs');
let html = fs.readFileSync(__dirname + '/saju_web.html', 'utf8');
let js = html.match(/<script>([\s\S]*)<\/script>/)[1];
js = js.replace(/fillSelects\(\);\s*renderExamples\(\);\s*fillSelects2\(\);\s*loadFromHash\(\);\s*$/, '');  // DOM 호출 제거
// DOM/alert 더미
global.document = { getElementById:()=>({value:'',add(){},classList:{toggle(){}}}),
                    documentElement:{}, querySelectorAll:()=>[],
                    createElement:()=>({select(){},remove(){},style:{}}), body:{appendChild(){}} };
global.location = { hash:'', protocol:'file:' }; global.navigator = {}; global.alert = ()=>{};
// 함수들을 현재 스코프로 노출
js += "\nglobal.computeSaju=computeSaju; global.lunarToSolar=lunarToSolar; global.analyzeFull=analyzeFull; global.interpret=interpret; global.refsCard=refsCard;";
eval(js);

const tc = JSON.parse(fs.readFileSync('/tmp/testcases.json','utf8'));
let ok=0, bad=0, miss=[];
for (const c of tc.solar) {
  // Python sxtwl은 베이징시 기준 → tz=480, 정오(h=12)로 맞춤
  const s = global.computeSaju(c.Y, c.M, c.D, 12, 0, '남', 480);
  const m3 = (s.pillars.year===c.year)+(s.pillars.month===c.month)+(s.pillars.day===c.day);
  if (m3===3) ok++; else { bad++; if(miss.length<8) miss.push(
    `${c.Y}-${c.M}-${c.D}  JS:${s.pillars.year}·${s.pillars.month}·${s.pillars.day}  PY:${c.year}·${c.month}·${c.day}`); }
}
let lok=0, lbad=0, lmiss=[];
for (const c of tc.lunar) {
  const sol = global.lunarToSolar(c.y, c.m, c.d, false);
  if (sol && sol[0]===c.sY && sol[1]===c.sM && sol[2]===c.sD) lok++;
  else { lbad++; if(lmiss.length<5) lmiss.push(`음${c.y}-${c.m}-${c.d} JS:${sol} PY:${c.sY}-${c.sM}-${c.sD}`); }
}
console.log(`양력 사주(년월일) 일치: ${ok}/${ok+bad}`);
miss.forEach(x=>console.log('  ✗ '+x));
console.log(`음력→양력 변환 일치: ${lok}/${lok+lbad}`);
lmiss.forEach(x=>console.log('  ✗ '+x));
// 분석 로직 스폿체크 (손중산·증국번)
for (const [nm,Y,M,D,h] of [['손중산',1866,11,12,4],['증국번',1811,11,26,4]]) {
  const s=global.computeSaju(Y,M,D,h,0,'남',480), a=global.analyzeFull(s);
  console.log(`[${nm}] JS 팔자 ${s.pillars.year}·${s.pillars.month}·${s.pillars.day}·${s.pillars.hour} | ${a.cls.type} ${a.cls.geuk} | 강약 ${a.st.verdict}(${a.st.score}) | 조후 ${a.jh[0]}`);
}
// 야자시(23시) 시주 검증 — sxtwl 정답 대조
console.log("야자시(23시) 시주:");
for (const [Y,M,D,exp] of [[2000,1,1,'甲子'],[1990,5,15,'戊子'],[1985,8,8,'丙子']]) {
  const s=global.computeSaju(Y,M,D,23,0,'남',480);
  console.log(`  ${Y}-${M}-${D} 23시 → ${s.pillars.hour} (sxtwl ${exp}) ${s.pillars.hour===exp?'OK':'✗'}`);
}
// 해석문 출력 (손중산)
const s2=global.computeSaju(1866,11,12,4,0,'남',540),a2=global.analyzeFull(s2);
console.log("\n[손중산 자동 해석문]");
global.interpret(s2,a2).forEach(x=>console.log("  · "+x.replace(/<[^>]+>/g,'')));
const rc=global.refsCard(a2).replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').slice(0,160);
console.log("[근거 카드 발췌] "+rc);
