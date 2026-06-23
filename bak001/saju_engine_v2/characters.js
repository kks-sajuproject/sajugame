/* characters.js — 사주 캐릭터 SVG 라이브러리 (31종) + idle 애니메이션
   - 일주 동물 12 (오행 색으로 틴팅) · 오행 정령 5 · 길신 5 · 흉신/양면 9
   - 표준 좌표: 200x200, 메달 중심 (100,100) r92
   - 사용: SAJU_CHARS.style(한 번 주입) + SAJU_CHARS.token(spec) 또는 SAJU_CHARS.animalToken(지지, 오행)
*/
(function (root) {
  // 오행 색 (몸통 / 메달 테두리)
  const WX_BODY = { 목:'#2aa198', 화:'#e2574a', 토:'#d6a23c', 금:'#9aa6ae', 수:'#3f74b8' };
  const WX_RING = { 목:'#1f7a6f', 화:'#b3261e', 토:'#a87c1f', 금:'#5f6b73', 수:'#274d80' };

  // 활발한 idle 애니메이션 (한 번만 페이지에 주입)
  const STYLE = `<style id="saju-char-style">
.scAnim{transform-box:fill-box}
.scFloat{animation:scfl 2.0s ease-in-out infinite}
.scFloat2{animation:scfl 2.4s ease-in-out infinite}
.scPulse{transform-origin:center;animation:scpulse 1.1s ease-in-out infinite}
.scBreathe{transform-origin:center;animation:scbreathe 1.6s ease-in-out infinite}
.scF1{transform-origin:50% 100%;animation:scflick .7s ease-in-out infinite}
.scF2{transform-origin:50% 100%;animation:scflick .55s ease-in-out infinite}
.scF3{transform-origin:50% 100%;animation:scflick .42s ease-in-out infinite}
.scWL{transform-origin:bottom right;animation:scwig 1.3s ease-in-out infinite}
.scWR{transform-origin:bottom left;animation:scwigr 1.3s ease-in-out infinite .15s}
.scGlint{animation:scglint 1.4s ease-in-out infinite}
.scSway{transform-origin:left center;animation:scsway 1.4s ease-in-out infinite}
.scBob{transform-origin:center;animation:scbob 1.5s ease-in-out infinite}
.scSpin{transform-origin:center;animation:scspin 3.2s linear infinite}
.scTongue{transform-origin:top center;animation:sctongue .55s ease-in-out infinite}
.scFade{animation:scfade 2.2s ease-in-out infinite}
.scBlink{animation:scblink 3s steps(1) infinite}
@keyframes scfl{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes scpulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.5);opacity:.7}}
@keyframes scbreathe{0%,100%{transform:scale(1)}50%{transform:scale(1.07)}}
@keyframes scflick{0%,100%{transform:scaleY(1) translateX(0)}30%{transform:scaleY(1.16) translateX(-2.5px)}65%{transform:scaleY(.88) translateX(2.5px)}}
@keyframes scwig{0%,100%{transform:rotate(0)}50%{transform:rotate(-16deg)}}
@keyframes scwigr{0%,100%{transform:rotate(0)}50%{transform:rotate(16deg)}}
@keyframes scglint{0%,100%{opacity:0}50%{opacity:.95}}
@keyframes scsway{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(10deg)}}
@keyframes scbob{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(6deg)}}
@keyframes scspin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
@keyframes sctongue{0%,100%{transform:scaleY(.5)}50%{transform:scaleY(1.1)}}
@keyframes scfade{0%,100%{opacity:1}50%{opacity:.45}}
@keyframes scblink{0%,92%{transform:scaleY(1)}94%,98%{transform:scaleY(.1)}100%{transform:scaleY(1)}}
</style>`;

  const EYE = '#2a2020';

  /* ---------- 일주 동물 12종 (지지 → fig(몸통색)) ---------- */
  const ANIMALS = {
    子: { name:'쥐', fig:c=>`
<g class="scAnim scSway"><path d="M138,118 q42,4 30,42 q-5,13 -18,7" fill="none" stroke="${c}" stroke-width="6" stroke-linecap="round"/></g>
<g class="scAnim scWL"><circle cx="74" cy="60" r="18" fill="${c}"/><circle cx="74" cy="60" r="9" fill="#ffd9d0"/></g>
<g class="scAnim scWR"><circle cx="126" cy="60" r="18" fill="${c}"/><circle cx="126" cy="60" r="9" fill="#ffd9d0"/></g>
<g class="scAnim scBreathe"><circle cx="100" cy="98" r="40" fill="${c}"/>
<ellipse cx="100" cy="112" rx="15" ry="11" fill="#fff3ee"/><circle cx="100" cy="106" r="4" fill="${EYE}"/>
<g stroke="#00000033" stroke-width="1.4"><line x1="100" y1="111" x2="62" y2="106"/><line x1="100" y1="114" x2="64" y2="120"/><line x1="100" y1="111" x2="138" y2="106"/><line x1="100" y1="114" x2="136" y2="120"/></g>
<circle cx="86" cy="92" r="4.5" fill="${EYE}"/><circle cx="114" cy="92" r="4.5" fill="${EYE}"/></g>` },

    丑: { name:'소', fig:c=>`
<g class="scAnim scBob"><path d="M62,70 q-18,-22 -2,-34 q6,12 16,18" fill="${c}"/><path d="M138,70 q18,-22 2,-34 q-6,12 -16,18" fill="${c}"/></g>
<g class="scAnim scWL"><ellipse cx="66" cy="92" rx="12" ry="16" fill="${c}"/></g>
<g class="scAnim scWR"><ellipse cx="134" cy="92" rx="12" ry="16" fill="${c}"/></g>
<g class="scAnim scBreathe"><circle cx="100" cy="100" r="42" fill="${c}"/>
<ellipse cx="100" cy="116" rx="22" ry="15" fill="#f6e7df"/><circle cx="92" cy="116" r="3.5" fill="${EYE}"/><circle cx="108" cy="116" r="3.5" fill="${EYE}"/>
<circle cx="86" cy="94" r="5" fill="${EYE}"/><circle cx="114" cy="94" r="5" fill="${EYE}"/></g>` },

    寅: { name:'범', fig:c=>`
<g class="scAnim scWL"><path d="M70,64 l-10,-20 l24,8 Z" fill="${c}"/></g>
<g class="scAnim scWR"><path d="M130,64 l10,-20 l-24,8 Z" fill="${c}"/></g>
<g class="scAnim scBreathe"><circle cx="100" cy="100" r="44" fill="${c}"/>
<g stroke="#00000040" stroke-width="3" stroke-linecap="round"><line x1="100" y1="62" x2="100" y2="74"/><line x1="86" y1="66" x2="89" y2="76"/><line x1="114" y1="66" x2="111" y2="76"/></g>
<ellipse cx="100" cy="116" rx="20" ry="13" fill="#fff4ec"/><path d="M100,110 l-6,6 h12 Z" fill="${EYE}"/>
<g stroke="#00000033" stroke-width="2"><line x1="100" y1="118" x2="76" y2="116"/><line x1="100" y1="118" x2="124" y2="116"/></g>
<circle cx="85" cy="96" r="5.5" fill="${EYE}"/><circle cx="115" cy="96" r="5.5" fill="${EYE}"/></g>` },

    卯: { name:'토끼', fig:c=>`
<g class="scAnim scWL"><ellipse cx="80" cy="52" rx="11" ry="34" fill="${c}"/><ellipse cx="80" cy="52" rx="5" ry="24" fill="#ffd9e2"/></g>
<g class="scAnim scWR"><ellipse cx="120" cy="52" rx="11" ry="34" fill="${c}"/><ellipse cx="120" cy="52" rx="5" ry="24" fill="#ffd9e2"/></g>
<g class="scAnim scBreathe"><circle cx="100" cy="108" r="38" fill="${c}"/>
<circle cx="88" cy="104" r="5" fill="${EYE}"/><circle cx="112" cy="104" r="5" fill="${EYE}"/>
<path d="M100,116 v6" stroke="${EYE}" stroke-width="2"/><path d="M94,118 q6,6 12,0" fill="none" stroke="${EYE}" stroke-width="2"/>
<ellipse cx="100" cy="114" rx="4" ry="3" fill="#e8889a"/>
<circle cx="78" cy="116" r="6" fill="#ffffff44"/><circle cx="122" cy="116" r="6" fill="#ffffff44"/></g>` },

    辰: { name:'용', fig:c=>`
<g class="scAnim scBob"><path d="M76,62 q-6,-26 8,-30 q-2,16 6,24" fill="${c}"/><path d="M124,62 q6,-26 -8,-30 q2,16 -6,24" fill="${c}"/></g>
<g class="scAnim scSway"><path d="M134,118 q34,10 22,40" fill="none" stroke="${c}" stroke-width="7" stroke-linecap="round"/></g>
<g class="scAnim scBreathe"><circle cx="100" cy="100" r="42" fill="${c}"/>
<rect x="84" y="112" width="32" height="16" rx="7" fill="#f2e6c8"/>
<g stroke="#00000033" stroke-width="1.4"><line x1="84" y1="120" x2="60" y2="116"/><line x1="116" y1="120" x2="140" y2="116"/></g>
<circle cx="86" cy="94" r="6" fill="#fff"/><circle cx="86" cy="94" r="3" fill="${EYE}"/>
<circle cx="114" cy="94" r="6" fill="#fff"/><circle cx="114" cy="94" r="3" fill="${EYE}"/>
<path d="M100,72 q-8,-4 -2,-12 q6,6 2,12" fill="#ffe08a"/></g>` },

    巳: { name:'뱀', fig:c=>`
<g class="scAnim scBreathe"><path d="M100,138 q-44,-2 -38,-34 q4,-26 38,-22 q26,4 22,24 q-3,16 -20,14 q-12,-2 -10,-12" fill="none" stroke="${c}" stroke-width="13" stroke-linecap="round"/>
<circle cx="120" cy="78" r="13" fill="${c}"/>
<circle cx="116" cy="74" r="3" fill="${EYE}"/><circle cx="126" cy="74" r="3" fill="${EYE}"/></g>
<g class="scAnim scTongue"><path d="M132,84 l12,4 l-3,-5 l3,-4 l-12,1 Z" fill="#e23b5a"/></g>` },

    午: { name:'말', fig:c=>`
<g class="scAnim scWL"><path d="M78,60 l-4,-20 l14,12 Z" fill="${c}"/></g>
<g class="scAnim scWR"><path d="M122,60 l4,-20 l-14,12 Z" fill="${c}"/></g>
<g class="scAnim scSway"><path d="M70,66 q-16,8 -10,40 q8,-6 14,-18" fill="${c}"/></g>
<g class="scAnim scBreathe"><ellipse cx="102" cy="100" rx="38" ry="42" fill="${c}"/>
<ellipse cx="106" cy="126" rx="20" ry="16" fill="${c}"/>
<ellipse cx="100" cy="132" rx="14" ry="9" fill="#f3e3d6"/><circle cx="95" cy="132" r="2.6" fill="${EYE}"/><circle cx="107" cy="132" r="2.6" fill="${EYE}"/>
<circle cx="90" cy="92" r="5" fill="${EYE}"/><circle cx="116" cy="92" r="5" fill="${EYE}"/></g>` },

    未: { name:'양', fig:c=>`
<g class="scAnim scBob"><path d="M64,84 q-22,-4 -16,-22 q-12,14 4,28" fill="none" stroke="${c}" stroke-width="7"/><path d="M136,84 q22,-4 16,-22 q12,14 -4,28" fill="none" stroke="${c}" stroke-width="7"/></g>
<g class="scAnim scBreathe">
<circle cx="72" cy="80" r="14" fill="#f4efe8"/><circle cx="128" cy="80" r="14" fill="#f4efe8"/><circle cx="76" cy="118" r="14" fill="#f4efe8"/><circle cx="124" cy="118" r="14" fill="#f4efe8"/><circle cx="100" cy="68" r="14" fill="#f4efe8"/><circle cx="100" cy="124" r="14" fill="#f4efe8"/>
<circle cx="100" cy="100" r="34" fill="${c}"/>
<ellipse cx="100" cy="112" rx="13" ry="9" fill="#f3e3d6"/><circle cx="90" cy="98" r="4.5" fill="${EYE}"/><circle cx="110" cy="98" r="4.5" fill="${EYE}"/></g>` },

    申: { name:'원숭이', fig:c=>`
<g class="scAnim scWL"><circle cx="64" cy="96" r="14" fill="${c}"/><circle cx="64" cy="96" r="7" fill="#f3d9c2"/></g>
<g class="scAnim scWR"><circle cx="136" cy="96" r="14" fill="${c}"/><circle cx="136" cy="96" r="7" fill="#f3d9c2"/></g>
<g class="scAnim scBreathe"><circle cx="100" cy="100" r="40" fill="${c}"/>
<ellipse cx="100" cy="110" rx="26" ry="24" fill="#f6e2cd"/>
<circle cx="90" cy="100" r="5" fill="${EYE}"/><circle cx="110" cy="100" r="5" fill="${EYE}"/>
<circle cx="96" cy="112" r="2.5" fill="${EYE}"/><circle cx="104" cy="112" r="2.5" fill="${EYE}"/>
<path d="M90,120 q10,8 20,0" fill="none" stroke="${EYE}" stroke-width="2.4"/></g>` },

    酉: { name:'닭', fig:c=>`
<g class="scAnim scBob"><circle cx="88" cy="56" r="8" fill="#e2453a"/><circle cx="100" cy="50" r="9" fill="#e2453a"/><circle cx="112" cy="56" r="8" fill="#e2453a"/></g>
<g class="scAnim scBreathe"><circle cx="100" cy="100" r="40" fill="${c}"/>
<path d="M138,102 l22,-6 l-22,-6 Z" fill="#f0a93a"/>
<path d="M104,128 q8,14 -4,18 q-2,-10 4,-18" fill="#e2453a"/>
<circle cx="118" cy="92" r="6" fill="#fff"/><circle cx="118" cy="92" r="3" fill="${EYE}"/></g>` },

    戌: { name:'개', fig:c=>`
<g class="scAnim scWL"><path d="M66,72 q-18,6 -14,38 q14,-6 20,-26" fill="${c}"/></g>
<g class="scAnim scWR"><path d="M134,72 q18,6 14,38 q-14,-6 -20,-26" fill="${c}"/></g>
<g class="scAnim scBreathe"><circle cx="100" cy="98" r="40" fill="${c}"/>
<ellipse cx="100" cy="116" rx="18" ry="14" fill="#f3e6da"/><ellipse cx="100" cy="110" rx="6" ry="4.5" fill="${EYE}"/>
<path d="M100,116 v8" stroke="${EYE}" stroke-width="2"/>
<g class="scAnim scTongue" style="transform-origin:100px 124px"><path d="M94,124 q6,12 12,0 Z" fill="#e8889a"/></g>
<circle cx="86" cy="94" r="5" fill="${EYE}"/><circle cx="114" cy="94" r="5" fill="${EYE}"/></g>` },

    亥: { name:'돼지', fig:c=>`
<g class="scAnim scBreathe"><ellipse cx="100" cy="120" rx="40" ry="30" fill="${c}"/><circle cx="100" cy="96" r="38" fill="${c}"/>
<g class="scAnim scWL"><path d="M95,78 Q92,52 75,53 Q60,57 68,82 Q80,86 95,78 Z" fill="${c}"/><path d="M88,73 Q86,61 77,62 Q70,65 74,76 Q81,78 88,73 Z" fill="#ffffff30"/></g>
<g class="scAnim scWR"><path d="M105,78 Q108,52 125,53 Q140,57 132,82 Q120,86 105,78 Z" fill="${c}"/><path d="M112,73 Q114,61 123,62 Q130,65 126,76 Q119,78 112,73 Z" fill="#ffffff30"/></g>
<circle cx="84" cy="88" r="5" fill="${EYE}"/><circle cx="116" cy="88" r="5" fill="${EYE}"/>
<circle cx="82.5" cy="86.5" r="1.5" fill="#fff"/><circle cx="114.5" cy="86.5" r="1.5" fill="#fff"/>
<ellipse cx="100" cy="110" rx="21" ry="15" fill="#f6c9bf"/>
<ellipse cx="100" cy="110" rx="21" ry="15" fill="none" stroke="#0000001a" stroke-width="1.5"/>
<ellipse cx="91" cy="110" rx="3.4" ry="6.5" fill="#8a3f34"/><ellipse cx="109" cy="110" rx="3.4" ry="6.5" fill="#8a3f34"/></g>` },
  };

  /* ---------- 오행 정령 5 · 길신 5 · 흉신 9 ---------- */
  const SPECIALS = {
    // 오행 정령
    목: { cat:'오행', name:'목(木) 원소', sub:'강한 木이 정령으로', role:'오행', ring:WX_RING.목, badge:['#d7efe9','#2aa198','#1d6b5f'], fig:`
<g class="scAnim scSway"><path d="M100,150 V92" stroke="#7a5230" stroke-width="10" stroke-linecap="round"/>
<path d="M100,96 q-30,-6 -34,-34 q30,2 34,26" fill="#2aa198"/><path d="M100,86 q30,-10 36,-40 q-32,4 -36,30" fill="#3fc0b3"/>
<path d="M100,78 q-22,-14 -14,-40 q22,12 14,36" fill="#2aa198"/></g>
<circle cx="92" cy="60" r="3.4" fill="${EYE}"/><circle cx="108" cy="60" r="3.4" fill="${EYE}"/>` },
    화: { cat:'오행', name:'화(火) 원소', sub:'강한 火가 정령으로', role:'오행', ring:WX_RING.화, badge:['#ffe1cc','#ff7537','#b34a14'], fig:`
<path class="scAnim scF1" d="M100,46 C66,88 68,128 100,180 C132,128 134,88 100,46 Z" fill="#ff7537"/>
<path class="scAnim scF2" d="M100,76 C80,108 80,134 100,168 C120,134 120,108 100,76 Z" fill="#ffad46"/>
<path class="scAnim scF3" d="M100,106 C90,124 90,140 100,164 C110,140 110,124 100,106 Z" fill="#ffd166"/>
<circle cx="90" cy="120" r="6" fill="#fffaf0"/><circle cx="91" cy="121" r="3" fill="#3a2a1a"/>
<circle cx="110" cy="120" r="6" fill="#fffaf0"/><circle cx="111" cy="121" r="3" fill="#3a2a1a"/>` },
    토: { cat:'오행', name:'토(土) 원소', sub:'강한 土가 정령으로', role:'오행', ring:WX_RING.토, badge:['#f3e6c8','#d6a23c','#8f6c1a'], fig:`
<g class="scAnim scBreathe"><path d="M58,140 L100,70 L142,140 Z" fill="#d6a23c"/><path d="M80,140 L100,104 L120,140 Z" fill="#c08a2a"/>
<path d="M86,84 l6,-8 l6,8 l8,2 l-8,4 l-2,8 l-6,-6 l-8,2 Z" fill="#ffe9a8"/>
<circle cx="90" cy="124" r="4" fill="${EYE}"/><circle cx="110" cy="124" r="4" fill="${EYE}"/></g>` },
    금: { cat:'오행', name:'금(金) 원소', sub:'강한 金이 정령으로', role:'오행', ring:WX_RING.금, badge:['#e6eaee','#8e9aa3','#566069'], fig:`
<g class="scAnim scBreathe"><path d="M100,52 L138,86 L120,150 L80,150 L62,86 Z" fill="#aab4bc"/>
<path d="M100,52 L138,86 L100,96 Z" fill="#c7d0d6"/><path d="M100,52 L62,86 L100,96 Z" fill="#8e9aa3"/>
<circle cx="90" cy="116" r="4" fill="${EYE}"/><circle cx="110" cy="116" r="4" fill="${EYE}"/></g>
<line class="scAnim scGlint" x1="74" y1="70" x2="126" y2="132" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>` },
    수: { cat:'오행', name:'수(水) 원소', sub:'강한 水가 정령으로', role:'오행', ring:WX_RING.수, badge:['#dbe7f5','#3f74b8','#274d80'], fig:`
<g class="scAnim scBreathe"><path d="M100,54 C66,104 70,150 100,150 C130,150 134,104 100,54 Z" fill="#3f74b8"/>
<path d="M100,80 C84,108 86,134 100,140 C114,134 116,108 100,80 Z" fill="#6aa0db"/>
<circle cx="90" cy="118" r="6" fill="#eaf3ff"/><circle cx="91" cy="119" r="3" fill="#22405f"/>
<circle cx="110" cy="118" r="6" fill="#eaf3ff"/><circle cx="111" cy="119" r="3" fill="#22405f"/></g>` },

    // 길신
    천을귀인: { cat:'길신', name:'천을귀인', sub:'최고 길신 · 귀인의 도움', role:'길신', ring:'#c9a227', badge:['#fff3cf','#d9b24a','#9a7b1a'], fig:`
<g class="scAnim scFloat"><path d="M62,150 Q100,134 138,150 L150,188 Q100,200 50,188 Z" fill="#2a7d72"/>
<circle cx="100" cy="112" r="24" fill="#f0c9a0"/><path d="M88,126 Q100,158 112,126 Z" fill="#f3f0e6"/>
<rect x="72" y="96" width="56" height="9" rx="3" fill="#b8901f"/><polygon points="78,96 122,96 100,62" fill="#c9a227"/>
<circle cx="92" cy="112" r="2.6" fill="#4a3b2a"/><circle cx="108" cy="112" r="2.6" fill="#4a3b2a"/>
<line x1="146" y1="100" x2="146" y2="184" stroke="#8a5a2b" stroke-width="5" stroke-linecap="round"/>
<circle class="scAnim scPulse" cx="146" cy="92" r="9" fill="#e63946"/></g>` },
    천덕귀인: { cat:'길신', name:'천덕귀인', sub:'하늘이 베푸는 덕 · 보호', role:'길신', ring:'#c9a227', badge:['#fff3cf','#d9b24a','#9a7b1a'], fig:`
<circle class="scAnim scPulse" cx="100" cy="104" r="40" fill="#ffe9a8" opacity=".5"/>
<g class="scAnim scFloat"><path d="M64,154 Q100,140 136,154 L146,188 Q100,198 54,188 Z" fill="#3a6ea5"/>
<circle cx="100" cy="108" r="22" fill="#f0c9a0"/><circle cx="92" cy="108" r="2.6" fill="#4a3b2a"/><circle cx="108" cy="108" r="2.6" fill="#4a3b2a"/>
<path d="M92,118 q8,7 16,0" fill="none" stroke="#9a6b3a" stroke-width="2"/>
<path d="M70,86 h60 l-8,12 h-44 Z" fill="#ffd23f"/></g>` },
    월덕귀인: { cat:'길신', name:'월덕귀인', sub:'달의 덕 · 온화한 구원', role:'길신', ring:'#9fb3cc', badge:['#e7eef7','#9fb3cc','#4a5a72'], fig:`
<g class="scAnim scFloat2"><path d="M118,60 a44,44 0 1 0 4,76 a34,34 0 1 1 -4,-76 Z" fill="#e9eef6"/>
<circle cx="92" cy="92" r="5" fill="#c3d0e0"/><circle cx="110" cy="118" r="3.5" fill="#c3d0e0"/><circle cx="84" cy="120" r="3" fill="#c3d0e0"/>
<circle cx="88" cy="104" r="3" fill="#5a6b80"/><circle cx="104" cy="100" r="3" fill="#5a6b80"/>
<path d="M86,114 q8,6 16,1" fill="none" stroke="#5a6b80" stroke-width="2"/></g>
<g class="scAnim scPulse"><path d="M150,70 l3,7 l7,3 l-7,3 l-3,7 l-3,-7 l-7,-3 l7,-3 Z" fill="#ffe08a"/></g>` },
    문창귀인: { cat:'길신', name:'문창귀인', sub:'학문·시험·문서운', role:'길신', ring:'#2a9d8f', badge:['#d7efe9','#2aa198','#1d6b5f'], fig:`
<g class="scAnim scFloat"><rect x="62" y="96" width="76" height="52" rx="5" fill="#f3ece0"/><line x1="100" y1="98" x2="100" y2="146" stroke="#cbb89a" stroke-width="2"/>
<g stroke="#9a8a6a" stroke-width="2"><line x1="70" y1="110" x2="94" y2="110"/><line x1="70" y1="122" x2="94" y2="122"/><line x1="106" y1="110" x2="130" y2="110"/><line x1="106" y1="122" x2="130" y2="122"/></g>
<circle cx="100" cy="80" r="18" fill="#f0c9a0"/><circle cx="93" cy="80" r="2.4" fill="#4a3b2a"/><circle cx="107" cy="80" r="2.4" fill="#4a3b2a"/>
<rect x="74" y="60" width="52" height="8" rx="3" fill="#2a7d72"/></g>
<g class="scAnim scBob"><rect x="132" y="70" width="6" height="40" rx="3" fill="#8a5a2b"/><path d="M132,108 l6,0 l-3,12 Z" fill="#222"/></g>` },
    건록: { cat:'길신', name:'건록(祿)', sub:'재록·안정된 녹봉', role:'길신', ring:'#2a9d8f', badge:['#d7efe9','#2aa198','#1d6b5f'], fig:`
<g class="scAnim scFloat"><path d="M64,152 Q100,138 136,152 L146,188 Q100,198 54,188 Z" fill="#2a7d72"/>
<rect x="84" y="146" width="32" height="12" rx="3" fill="#c9a227"/>
<circle cx="100" cy="108" r="22" fill="#f0c9a0"/><circle cx="92" cy="108" r="2.6" fill="#4a3b2a"/><circle cx="108" cy="108" r="2.6" fill="#4a3b2a"/>
<path d="M92,118 q8,6 16,0" fill="none" stroke="#9a6b3a" stroke-width="2"/></g>
<g class="scAnim scPulse"><circle cx="142" cy="120" r="13" fill="#f0c64a"/><text x="142" y="125" text-anchor="middle" font-size="13" fill="#7a5a10">祿</text></g>` },

    // 흉신 / 양면
    편관칠살: { cat:'흉신', name:'편관(칠살)', sub:'제압하면 권력 · 흉신', role:'흉신', ring:'#8a1c0a', badge:['#fbdcd6','#c0392b','#8a1c0a'], fig:`
<g class="scAnim scFloat2"><path d="M62,154 Q100,142 138,154 L146,196 L54,196 Z" fill="#5c6b73"/>
<rect x="80" y="116" width="40" height="44" rx="4" fill="#8a9ba8"/>
<circle cx="100" cy="92" r="24" fill="#6b7780"/><rect x="88" y="88" width="24" height="18" rx="3" fill="#e0b48c"/>
<line x1="88" y1="96" x2="112" y2="96" stroke="#4a4a4a" stroke-width="2"/><polygon points="92,70 108,70 100,50" fill="#b3261e"/>
<circle cx="94" cy="97" r="2" fill="#3a2a2a"/><circle cx="106" cy="97" r="2" fill="#3a2a2a"/>
<polygon points="146,78 154,78 150,176 Z" fill="#c0c8d0"/><line class="scAnim scGlint" x1="149" y1="86" x2="151" y2="168" stroke="#fff" stroke-width="2.4"/>
<rect x="140" y="172" width="20" height="7" rx="2" fill="#8a5a2b"/></g>` },
    양인: { cat:'흉신', name:'양인(羊刃)', sub:'날카로운 칼 · 과강한 기운', role:'흉신', ring:'#8a1c0a', badge:['#fbdcd6','#c0392b','#8a1c0a'], fig:`
<g class="scAnim scFloat"><polygon points="100,44 112,150 88,150" fill="#cdd6dd"/><polygon points="100,44 112,150 100,150" fill="#9aa6ae"/>
<line class="scAnim scGlint" x1="100" y1="56" x2="100" y2="146" stroke="#fff" stroke-width="3"/>
<rect x="80" y="150" width="40" height="10" rx="3" fill="#8a5a2b"/><rect x="92" y="158" width="16" height="22" rx="3" fill="#6b4329"/></g>
<g class="scAnim scPulse"><circle cx="138" cy="74" r="6" fill="#e2574a"/></g>` },
    백호: { cat:'흉신', name:'백호(白虎)', sub:'사고·수술수 · 맹수의 기운', role:'흉신', ring:'#5f6b73', badge:['#e6eaee','#8e9aa3','#4a545c'], fig:`
<g class="scAnim scWL"><path d="M70,62 l-8,-18 l22,8 Z" fill="#eef2f4"/></g><g class="scAnim scWR"><path d="M130,62 l8,-18 l-22,8 Z" fill="#eef2f4"/></g>
<g class="scAnim scBreathe"><circle cx="100" cy="100" r="44" fill="#eef2f4"/>
<g stroke="#9aa6ae" stroke-width="3" stroke-linecap="round"><line x1="100" y1="60" x2="100" y2="74"/><line x1="84" y1="64" x2="88" y2="76"/><line x1="116" y1="64" x2="112" y2="76"/></g>
<ellipse cx="100" cy="118" rx="20" ry="13" fill="#fff"/><path d="M100,112 l-6,6 h12 Z" fill="#3a2a2a"/>
<path d="M88,124 q12,8 24,0" fill="none" stroke="#3a2a2a" stroke-width="2"/><path d="M92,124 l-2,8 M108,124 l2,8" stroke="#fff" stroke-width="3"/>
<circle cx="84" cy="96" r="6" fill="#e2a23c"/><circle cx="84" cy="96" r="3" fill="#2a2020"/><circle cx="116" cy="96" r="6" fill="#e2a23c"/><circle cx="116" cy="96" r="3" fill="#2a2020"/></g>` },
    괴강: { cat:'흉신', name:'괴강(魁罡)', sub:'극단·카리스마 · 폭발력', role:'흉신', ring:'#3a3550', badge:['#e0dcef','#5b5276','#3a3550'], fig:`
<g class="scAnim scFloat2"><circle cx="100" cy="98" r="40" fill="#4a4566"/>
<rect x="84" y="92" width="32" height="14" rx="3" fill="#1c1830"/>
<rect x="88" y="96" width="9" height="6" rx="2" fill="#ff5a3c"/><rect x="103" y="96" width="9" height="6" rx="2" fill="#ff5a3c"/>
<path d="M76,120 q24,12 48,0" fill="none" stroke="#1c1830" stroke-width="3"/></g>
<g class="scAnim scGlint"><polygon points="150,58 138,92 150,88 142,120 168,80 154,84 162,58" fill="#ffe14a"/></g>` },
    도화: { cat:'양면', name:'도화(桃花)', sub:'매력·인기 · 이성운', role:'양면', ring:'#d46a8c', badge:['#fbdce6','#d46a8c','#9c3a5a'], fig:`
<g class="scAnim scBob"><g fill="#f7a8c4">
<ellipse cx="100" cy="70" rx="13" ry="20"/><ellipse cx="128" cy="92" rx="13" ry="20" transform="rotate(72 128 92)"/><ellipse cx="118" cy="124" rx="13" ry="20" transform="rotate(144 118 124)"/><ellipse cx="82" cy="124" rx="13" ry="20" transform="rotate(216 82 124)"/><ellipse cx="72" cy="92" rx="13" ry="20" transform="rotate(288 72 92)"/></g>
<circle cx="100" cy="100" r="15" fill="#ffd23f"/>
<circle cx="94" cy="98" r="2.4" fill="#7a3a30"/><circle cx="106" cy="98" r="2.4" fill="#7a3a30"/><path d="M94,106 q6,5 12,0" fill="none" stroke="#7a3a30" stroke-width="2"/></g>` },
    진역마: { cat:'역마', name:'진역마(眞驛馬)', sub:'길성과 동행 · 발전하는 이동', role:'길', ring:'#c9a227', badge:['#fff3cf','#d9b24a','#9a7b1a'], fig:`
<circle class="scAnim scPulse" cx="150" cy="62" r="15" fill="#ffd23f" opacity=".55"/>
<g class="scAnim scBreathe"><ellipse cx="92" cy="98" rx="34" ry="25" fill="#c2913a"/><ellipse cx="118" cy="90" rx="17" ry="13" fill="#c2913a"/>
<path d="M130,84 l5,-16 l-13,9 Z" fill="#c2913a"/><path d="M108,80 q-13,6 -9,26 q8,-6 11,-16" fill="#8a5a20"/>
<ellipse cx="126" cy="96" rx="9" ry="6" fill="#f3e6d2"/><circle cx="118" cy="86" r="3.4" fill="${EYE}"/>
<g stroke="#8a5a20" stroke-width="6" stroke-linecap="round"><line x1="74" y1="120" x2="64" y2="144"/><line x1="102" y1="122" x2="114" y2="144"/></g></g>
<g class="scAnim scGlint"><path d="M40,104 h26 M44,116 h22" stroke="#ffd23f" stroke-width="4" stroke-linecap="round"/></g>
<polygon points="150,152 168,142 150,132" fill="#e2a23c"/>` },
    살역마: { cat:'역마', name:'살역마(殺驛馬)', sub:'흉살과 동행 · 강제·손해 이동', role:'흉', ring:'#8a1c0a', badge:['#fbdcd6','#c0392b','#8a1c0a'], fig:`
<g class="scAnim scBreathe"><ellipse cx="96" cy="96" rx="33" ry="25" fill="#6b5238"/><ellipse cx="120" cy="104" rx="16" ry="12" fill="#6b5238"/>
<path d="M72,72 l-5,-16 l13,10 Z" fill="#6b5238"/><ellipse cx="127" cy="110" rx="8" ry="6" fill="#cdbfae"/>
<path d="M80,86 l8,5 M80,92 l8,-3" stroke="${EYE}" stroke-width="1.8" stroke-linecap="round"/></g>
<g class="scAnim scBob"><circle cx="70" cy="150" r="16" fill="none" stroke="#3a2a1a" stroke-width="4"/><line x1="70" y1="134" x2="70" y2="166" stroke="#3a2a1a" stroke-width="3"/><line x1="54" y1="150" x2="86" y2="150" stroke="#3a2a1a" stroke-width="3"/><path d="M84,150 l12,8" stroke="#b3261e" stroke-width="3" stroke-linecap="round"/></g>
<g class="scAnim scPulse"><polygon points="148,56 134,82 162,82" fill="#e2574a"/><rect x="146" y="66" width="4" height="9" fill="#fff"/><circle cx="148" cy="79" r="2" fill="#fff"/></g>` },
    화개: { cat:'양면', name:'화개(華蓋)', sub:'예술·종교·고독한 재능', role:'양면', ring:'#6b4a8a', badge:['#e7dcf2','#7e5aa0','#4f3470'], fig:`
<g class="scAnim scFloat2"><path d="M100,50 L150,96 L50,96 Z" fill="#7e5aa0"/><path d="M100,62 L134,94 L66,94 Z" fill="#9a78bb"/>
<rect x="97" y="96" width="6" height="40" fill="#5a3f78"/>
<g fill="#e7dcf2"><circle cx="100" cy="120" r="12"/><circle cx="88" cy="128" r="9"/><circle cx="112" cy="128" r="9"/></g>
<circle cx="95" cy="120" r="2.4" fill="#4f3470"/><circle cx="105" cy="120" r="2.4" fill="#4f3470"/></g>` },
    공망: { cat:'흉신', name:'공망(空亡)', sub:'비어있음·허무 · 결실 약화', role:'흉신', ring:'#7a8590', badge:['#e6eaee','#8e9aa3','#566069'], fig:`
<g class="scAnim scFade"><path d="M70,80 q30,-26 60,0 q6,40 -6,70 q-6,-8 -12,0 q-6,8 -12,0 q-6,8 -12,0 q-6,8 -12,0 q-12,-30 -6,-70 Z" fill="#c3ccd3"/>
<ellipse cx="86" cy="96" rx="7" ry="9" fill="#fff"/><ellipse cx="114" cy="96" rx="7" ry="9" fill="#fff"/>
<circle cx="86" cy="98" r="3" fill="#566069"/><circle cx="114" cy="98" r="3" fill="#566069"/>
<ellipse cx="100" cy="118" rx="6" ry="9" fill="#7a8590"/></g>` },
    육해살: { cat:'흉신', name:'육해살(六害殺)', sub:'질병·구설·방해 · 가시밭', role:'흉신', ring:'#7a3a4a', badge:['#fbdce0','#a8475e','#6a2333'], fig:`
<g class="scAnim scBob"><g fill="#9c4a5c">
<polygon points="100,46 108,66 92,66"/><polygon points="150,72 138,88 154,94"/><polygon points="154,124 134,124 146,140"/><polygon points="100,154 92,134 108,134"/><polygon points="50,124 66,114 54,134"/><polygon points="50,72 62,90 46,94"/></g></g>
<g class="scAnim scBreathe"><circle cx="100" cy="100" r="32" fill="#7a3a4a"/>
<path d="M84,92 l10,5 M116,92 l-10,5" stroke="#2a1018" stroke-width="3" stroke-linecap="round"/>
<circle cx="91" cy="100" r="3" fill="#ffd9d0"/><circle cx="109" cy="100" r="3" fill="#ffd9d0"/>
<path d="M88,116 q12,-7 24,0" fill="none" stroke="#2a1018" stroke-width="2.6"/></g>` },
    지살: { cat:'양면', name:'지살(地殺)', sub:'이사·독립·터전의 변동', role:'양면', ring:'#a87c1f', badge:['#f3e6c8','#d6a23c','#8f6c1a'], fig:`
<g class="scAnim scFloat"><path d="M68,108 L100,78 L132,108 Z" fill="#c08a2a"/><rect x="78" y="106" width="44" height="38" fill="#d6a23c"/>
<rect x="94" y="120" width="14" height="24" fill="#7a5230"/><rect x="84" y="114" width="10" height="9" fill="#f2e6c8"/><rect x="106" y="114" width="10" height="9" fill="#f2e6c8"/></g>
<g class="scAnim scGlint"><path d="M134,152 h22 M148,142 l12,10 l-12,10" fill="none" stroke="#b0772f" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>` },
    천살: { cat:'흉신', name:'천살(天殺)', sub:'천재지변 · 거스를 수 없는 일', role:'흉신', ring:'#3a4250', badge:['#dde2e8','#5a6470','#333a44'], fig:`
<g class="scAnim scFloat2"><ellipse cx="100" cy="80" rx="42" ry="22" fill="#5a6470"/><ellipse cx="74" cy="86" rx="18" ry="14" fill="#5a6470"/><ellipse cx="126" cy="86" rx="18" ry="14" fill="#5a6470"/>
<ellipse cx="100" cy="76" rx="14" ry="8" fill="#eef2f4"/><circle cx="100" cy="76" r="4" fill="${EYE}"/></g>
<g class="scAnim scGlint"><polygon points="98,96 84,128 100,122 90,156 120,112 104,116 114,96" fill="#ffe14a"/></g>` },
    천의: { cat:'길신', name:'천의(天醫)', sub:'치유·의약 · 건강의 별', role:'길신', ring:'#2a9d8f', badge:['#d7efe9','#2aa198','#1d6b5f'], fig:`
<circle class="scAnim scPulse" cx="100" cy="104" r="40" fill="#bfe6cf" opacity=".45"/>
<g class="scAnim scFloat"><rect x="78" y="86" width="44" height="46" rx="9" fill="#2aa15c"/>
<rect x="95" y="94" width="10" height="30" fill="#fff"/><rect x="85" y="104" width="30" height="10" fill="#fff"/></g>
<g class="scAnim scSway" style="transform-origin:100px 86px"><path d="M100,86 q-12,-16 -2,-30 q9,10 2,22" fill="#3fc07a"/><path d="M100,80 q12,-12 24,-12 q-8,12 -22,16" fill="#52d68c"/></g>` },
    천문: { cat:'길신', name:'천문(天門)', sub:'영성·통찰 · 의약·역학의 문', role:'길신', ring:'#7e5aa0', badge:['#e7dcf2','#7e5aa0','#4f3470'], fig:`
<g class="scAnim scFloat2"><rect x="62" y="68" width="76" height="12" rx="3" fill="#7e5aa0"/><rect x="70" y="56" width="60" height="8" rx="3" fill="#9a78bb"/>
<rect x="72" y="80" width="13" height="62" fill="#7e5aa0"/><rect x="115" y="80" width="13" height="62" fill="#7e5aa0"/></g>
<g class="scAnim scFade"><rect x="88" y="84" width="24" height="58" fill="#efe6f8"/></g>
<g class="scAnim scPulse"><path d="M100,104 l3,7 l7,3 l-7,3 l-3,7 l-3,-7 l-7,-3 l7,-3 Z" fill="#ffe08a"/></g>` },
    원진: { cat:'흉신', name:'원진(怨嗔)', sub:'까닭 모를 미움 · 애증', role:'흉신', ring:'#8a4a6a', badge:['#f3dce8','#a8557a','#6a2f4a'], fig:`
<g class="scAnim scPulse"><path d="M100,52 q-7,9 0,16 q7,-7 0,-16" fill="#e2574a"/></g>
<g class="scAnim scBreathe"><circle cx="82" cy="104" r="27" fill="#a86a8a"/><circle cx="118" cy="104" r="27" fill="#6f6aa8"/>
<circle cx="72" cy="102" r="3.4" fill="${EYE}"/><path d="M66,114 q7,-5 11,-1" fill="none" stroke="${EYE}" stroke-width="2.2"/>
<circle cx="128" cy="102" r="3.4" fill="${EYE}"/><path d="M123,113 q7,-4 11,1" fill="none" stroke="${EYE}" stroke-width="2.2"/></g>` },
    천라지망: { cat:'양면', name:'천라지망(天羅地網)', sub:'속박·관재 · 활인·수사엔 길', role:'양면', ring:'#4a5a6a', badge:['#dde4ea','#5a6b7a','#37434f'], fig:`
<g stroke="#5a6b7a" stroke-width="2" fill="none"><path d="M62,80 H138 M58,102 H142 M62,126 H138"/><path d="M80,62 V142 M100,58 V146 M120,62 V142"/></g>
<g stroke="#6a7b8a" stroke-width="1.4" fill="none" opacity=".55"><path d="M68,68 L132,140 M132,68 L68,140"/></g>
<g class="scAnim scFade"><circle cx="100" cy="102" r="13" fill="#e2a23c"/><circle cx="95" cy="100" r="2.4" fill="${EYE}"/><circle cx="105" cy="100" r="2.4" fill="${EYE}"/><path d="M94,110 q6,4 12,0" fill="none" stroke="${EYE}" stroke-width="2"/></g>` },
  };

  // 귀문관살 6종 (지지 쌍별 · 색·기운 차별화)
  function guimunFig(main, glow, pair) { return `
<g class="scAnim scFloat2"><path d="M64,92 q0,-40 36,-40 q36,0 36,40 l0,40 l-9,-7 l-8,7 l-8,-7 l-7,7 l-8,-7 l-8,7 l-8,-7 l-5,5 Z" fill="${main}"/>
<path d="M78,82 l16,8 l-16,6 Z" fill="#f4ead8"/><path d="M122,82 l-16,8 l16,6 Z" fill="#f4ead8"/>
<circle class="scAnim scPulse" cx="86" cy="88" r="3.6" fill="${glow}"/><circle class="scAnim scPulse" cx="114" cy="88" r="3.6" fill="${glow}"/>
<path d="M88,112 q12,-7 24,0" fill="none" stroke="#160a1c" stroke-width="2.4"/>
<path d="M93,112 v7 M100,112 v8 M107,112 v7" stroke="#160a1c" stroke-width="1.8"/></g>
<rect x="76" y="150" width="48" height="22" rx="7" fill="#160a1c"/><text x="100" y="166" text-anchor="middle" font-size="15" fill="#fff" font-family="serif">${pair}</text>`; }
  [
    ['자유귀문','子酉','#3f5a7a','#7fd4ff'],
    ['축오귀문','丑午','#7a3a2a','#ff8a4c'],
    ['인미귀문','寅未','#4a6a3a','#bce86a'],
    ['묘신귀문','卯申','#357066','#7ff0e0'],
    ['진해귀문','辰亥','#3a3560','#a78aff'],
    ['사술귀문','巳戌','#6a2a3e','#ff6a96'],
  ].forEach(([key, pair, main, glow]) => {
    SPECIALS[key] = { cat:'귀문', name:key+'('+pair+')', sub:'예민·직감·집착 · '+pair+' 귀문', role:'양면',
      ring:main, badge:['#ecdcf2','#7e4a96','#4a1c5c'], fig:guimunFig(main, glow, pair) };
  });

  // 추가 귀인·신살 (신살론 확장)
  const GOLD_BADGE = ['#fff3cf','#d9b24a','#9a7b1a'];
  const RED_BADGE  = ['#fbdcd6','#c0392b','#8a1c0a'];
  const AMBER_BADGE= ['#f7e3c4','#c8842a','#8a571a'];
  const PINK_BADGE = ['#fbdce6','#d46a8c','#9c3a5a'];
  Object.assign(SPECIALS, {
    재고귀인: { cat:'길신', name:'재고귀인(財庫)', sub:'재물 창고 · 부의 저장', role:'길신', ring:'#c9a227', badge:GOLD_BADGE, fig:`
<g class="scAnim scFloat"><rect x="62" y="98" width="76" height="46" rx="6" fill="#9a6b2a"/><path d="M62,98 q38,-26 76,0 Z" fill="#b5832f"/>
<rect x="58" y="112" width="84" height="10" fill="#d9a441"/><rect x="93" y="116" width="14" height="14" rx="2" fill="#f0d24a"/></g>
<g class="scAnim scPulse"><circle cx="80" cy="74" r="10" fill="#ffd23f"/><text x="80" y="79" text-anchor="middle" font-size="12" fill="#7a5a10">財</text><circle cx="116" cy="80" r="8" fill="#ffd23f"/></g>` },
    천주귀인: { cat:'길신', name:'천주귀인(天廚)', sub:'식록 · 먹을 복', role:'길신', ring:'#c9a227', badge:GOLD_BADGE, fig:`
<g class="scAnim scFade"><path d="M84,62 q4,-10 0,-16 M100,58 q4,-10 0,-16 M116,62 q4,-10 0,-16" stroke="#cfc6b4" stroke-width="2.5" fill="none"/></g>
<g class="scAnim scFloat"><path d="M62,106 q38,42 76,0 Z" fill="#e8e2d6"/><rect x="56" y="102" width="88" height="9" rx="4" fill="#cfc6b4"/>
<path d="M74,104 q26,-20 52,0 Z" fill="#ffffff"/><line x1="98" y1="70" x2="98" y2="100" stroke="#9a8a6a" stroke-width="3"/><line x1="108" y1="70" x2="106" y2="100" stroke="#9a8a6a" stroke-width="3"/></g>` },
    복성귀인: { cat:'길신', name:'복성귀인(福星)', sub:'복록·행운의 별', role:'길신', ring:'#c9a227', badge:GOLD_BADGE, fig:`
<g class="scAnim scFloat"><line x1="100" y1="50" x2="100" y2="62" stroke="#8a5a2b" stroke-width="3"/>
<rect x="74" y="62" width="52" height="14" rx="4" fill="#b3261e"/><rect x="80" y="76" width="40" height="44" rx="14" fill="#e2453a"/><rect x="74" y="120" width="52" height="12" rx="4" fill="#b3261e"/>
<text x="100" y="106" text-anchor="middle" font-size="22" fill="#ffe08a">福</text></g>
<g class="scAnim scSway" style="transform-origin:100px 132px"><path d="M92,132 v14 M100,132 v18 M108,132 v14" stroke="#e2453a" stroke-width="3"/></g>` },
    금여: { cat:'길신', name:'금여(金輿)', sub:'금수레 · 안락·좋은 배우자', role:'길신', ring:'#c9a227', badge:GOLD_BADGE, fig:`
<g class="scAnim scFloat"><path d="M66,92 L100,66 L134,92 Z" fill="#c08a2a"/><rect x="70" y="90" width="60" height="40" rx="6" fill="#d9a441"/><rect x="86" y="100" width="28" height="30" rx="4" fill="#a8761f"/>
<line x1="56" y1="138" x2="144" y2="138" stroke="#7a5230" stroke-width="5" stroke-linecap="round"/></g>
<g class="scAnim scSpin"><circle cx="76" cy="146" r="10" fill="none" stroke="#7a5230" stroke-width="3"/><line x1="76" y1="140" x2="76" y2="152" stroke="#7a5230" stroke-width="2"/></g>
<g class="scAnim scSpin"><circle cx="124" cy="146" r="10" fill="none" stroke="#7a5230" stroke-width="3"/><line x1="124" y1="140" x2="124" y2="152" stroke="#7a5230" stroke-width="2"/></g>` },
    암록: { cat:'길신', name:'암록(暗祿)', sub:'숨은 복록·드러나지 않는 귀인', role:'길신', ring:'#5a7a4a', badge:['#dde9d2','#5a7a4a','#3a5530'], fig:`
<g class="scAnim scFade"><circle cx="132" cy="64" r="16" fill="#e9eef6"/><circle cx="126" cy="60" r="13" fill="#fbf8f3"/></g>
<g class="scAnim scFloat"><path d="M82,98 q18,-16 36,0 l8,40 q-26,12 -52,0 Z" fill="#6a7a4a"/><ellipse cx="100" cy="98" rx="18" ry="6" fill="#566a3a"/>
<text x="100" y="128" text-anchor="middle" font-size="16" fill="#ffe08a">祿</text></g>` },
    태극귀인: { cat:'길신', name:'태극귀인(太極)', sub:'총명·시작과 끝의 귀인', role:'길신', ring:'#c9a227', badge:GOLD_BADGE, fig:`
<g class="scAnim scSpin"><circle cx="100" cy="100" r="40" fill="#c0392b"/>
<path d="M100,60 a40,40 0 0 0 0,80 a20,20 0 0 0 0,-40 a20,20 0 0 1 0,-40 Z" fill="#2a5599"/>
<circle cx="100" cy="80" r="6" fill="#ffffff"/><circle cx="100" cy="120" r="6" fill="#ffffff"/></g>` },
    학당귀인: { cat:'길신', name:'학당귀인(學堂)', sub:'학문·총명·시험운', role:'길신', ring:'#2a9d8f', badge:['#d7efe9','#2aa198','#1d6b5f'], fig:`
<g class="scAnim scFloat"><polygon points="100,68 152,86 100,104 48,86" fill="#2a3550"/><rect x="86" y="98" width="28" height="20" fill="#2a3550"/>
<polygon points="86,98 86,116 76,112 76,96 Z" fill="#3a4868"/>
<line x1="152" y1="86" x2="152" y2="116" stroke="#ffd23f" stroke-width="2"/><circle cx="152" cy="118" r="4" fill="#ffd23f"/></g>
<g class="scAnim scBreathe"><rect x="84" y="124" width="32" height="6" rx="2" fill="#9a8a6a"/></g>` },
    겁살: { cat:'흉신', name:'겁살(劫殺)', sub:'빼앗김·강탈·갑작스런 손실', role:'흉신', ring:'#8a1c0a', badge:RED_BADGE, fig:`
<g class="scAnim scFloat2"><circle cx="96" cy="96" r="34" fill="#2a2a32"/><rect x="66" y="86" width="60" height="16" rx="6" fill="#4a4a55"/>
<rect x="74" y="90" width="13" height="7" rx="2" fill="#ffffff"/><rect x="106" y="90" width="13" height="7" rx="2" fill="#ffffff"/>
<circle cx="80" cy="93" r="2.4" fill="#2a2020"/><circle cx="112" cy="93" r="2.4" fill="#2a2020"/></g>
<g class="scAnim scGlint"><polygon points="138,114 152,150 145,151 131,116 Z" fill="#c0c8d0"/><rect x="126" y="110" width="16" height="6" rx="2" fill="#8a5a2b"/></g>` },
    재살: { cat:'흉신', name:'재살(囚獄殺)', sub:'관재·구속·송사', role:'흉신', ring:'#8a1c0a', badge:RED_BADGE, fig:`
<g class="scAnim scBreathe"><rect x="62" y="62" width="76" height="76" rx="6" fill="#3a4250"/><rect x="70" y="70" width="60" height="60" fill="#1c222c"/>
<g stroke="#5a6470" stroke-width="6"><line x1="84" y1="70" x2="84" y2="130"/><line x1="100" y1="70" x2="100" y2="130"/><line x1="116" y1="70" x2="116" y2="130"/></g>
<circle cx="92" cy="100" r="4" fill="#e2a23c"/><circle cx="108" cy="100" r="4" fill="#e2a23c"/></g>` },
    월살: { cat:'흉신', name:'월살(枯草殺)', sub:'메마름·위축·소모', role:'흉신', ring:'#7a7060', badge:['#e6e1d6','#7a7060','#4f4738'], fig:`
<g class="scAnim scFade"><path d="M120,56 a40,40 0 1 0 4,78 a30,30 0 1 1 -4,-78 Z" fill="#9aa0a8"/>
<circle cx="96" cy="92" r="4" fill="#c3c8cf"/><circle cx="110" cy="116" r="3" fill="#c3c8cf"/></g>
<g class="scAnim scSway" style="transform-origin:100px 142px"><path d="M100,142 q-6,-30 -18,-44 M100,142 q4,-26 16,-40 M100,142 V100" stroke="#8a7a5a" stroke-width="3" fill="none" stroke-linecap="round"/></g>` },
    망신살: { cat:'흉신', name:'망신살(亡神殺)', sub:'망신·구설·체면 손상', role:'흉신', ring:'#8a1c0a', badge:RED_BADGE, fig:`
<g class="scAnim scBreathe"><circle cx="100" cy="100" r="34" fill="#e8b48c"/>
<ellipse cx="82" cy="110" rx="9" ry="5" fill="#e2574a" opacity=".5"/><ellipse cx="118" cy="110" rx="9" ry="5" fill="#e2574a" opacity=".5"/>
<circle cx="88" cy="96" r="3.4" fill="#2a2020"/><circle cx="112" cy="96" r="3.4" fill="#2a2020"/>
<ellipse cx="100" cy="118" rx="8" ry="10" fill="#7a3a30"/></g>
<g class="scAnim scPulse"><text x="146" y="72" font-size="22" fill="#e2574a">!</text></g>` },
    탕화살: { cat:'흉신', name:'탕화살(湯火殺)', sub:'화상·끓는 물 · 화재수', role:'흉신', ring:'#8a1c0a', badge:RED_BADGE, fig:`
<path class="scAnim scF1" d="M86,88 C70,114 72,140 90,160 C104,142 104,116 86,88 Z" fill="#ff7537"/>
<path class="scAnim scF2" d="M88,112 C78,128 79,146 90,152 C101,146 102,128 88,112 Z" fill="#ffd166"/>
<g class="scAnim scBreathe"><path d="M122,104 C110,124 112,148 126,150 C140,148 142,124 122,104 Z" fill="#3f74b8"/></g>
<g class="scAnim scPulse"><polygon points="104,50 92,74 116,74" fill="#e2574a"/><rect x="102" y="58" width="4" height="9" fill="#fff"/><circle cx="104" cy="71" r="2" fill="#fff"/></g>` },
    장성살: { cat:'양면', name:'장성살(將星殺)', sub:'장수의 별 · 권위·통솔', role:'양면', ring:'#c8842a', badge:AMBER_BADGE, fig:`
<g class="scAnim scFloat"><rect x="88" y="58" width="4" height="84" fill="#7a5230"/>
<path d="M92,60 L144,70 L92,88 Z" fill="#b3261e"/><path d="M112,68 l2,6 l6,1 l-5,4 l1,6 l-4,-3 l-5,3 l1,-6 l-5,-4 l6,-1 Z" fill="#ffe08a"/></g>
<g class="scAnim scBreathe"><rect x="74" y="138" width="36" height="8" rx="3" fill="#8a5a2b"/></g>` },
    반안살: { cat:'양면', name:'반안살(攀鞍殺)', sub:'안장 · 승진·출세', role:'양면', ring:'#c8842a', badge:AMBER_BADGE, fig:`
<g class="scAnim scFloat"><path d="M62,112 q38,-32 76,0 q-6,20 -38,20 q-32,0 -38,-20 Z" fill="#8a5a2b"/>
<path d="M70,110 q30,-24 60,0" fill="none" stroke="#b5832f" stroke-width="4"/><rect x="96" y="90" width="8" height="16" rx="3" fill="#a8761f"/></g>
<g class="scAnim scPulse"><circle cx="148" cy="68" r="8" fill="#ffd23f"/></g>` },
    홍염살: { cat:'양면', name:'홍염살(紅艶殺)', sub:'매혹·끼 · 이성의 인기', role:'양면', ring:'#d46a8c', badge:PINK_BADGE, fig:`
<g class="scAnim scBob"><path d="M100,82 q-18,-6 -18,14 q0,18 18,18 q18,0 18,-18 q0,-20 -18,-14 Z" fill="#e25786"/>
<circle cx="100" cy="100" r="10" fill="#f48aab"/><circle cx="100" cy="100" r="4.5" fill="#c0395f"/></g>
<g class="scAnim scSway" style="transform-origin:100px 116px"><path d="M100,116 v28" stroke="#3fa05a" stroke-width="4"/><path d="M100,130 q16,-2 20,-13 q-16,0 -20,13 Z" fill="#3fa05a"/></g>` },
  });

  // 추가 귀인·신살 (2차 확장)
  Object.assign(SPECIALS, {
    협록: { cat:'길신', name:'협록(夾祿)', sub:'좌우서 록을 끼다 · 든든한 재록', role:'길신', ring:'#c9a227', badge:GOLD_BADGE, fig:`
<g class="scAnim scPulse"><path d="M60,70 a42,42 0 0 0 0,60" fill="none" stroke="#c08a2a" stroke-width="8" stroke-linecap="round"/>
<path d="M140,70 a42,42 0 0 1 0,60" fill="none" stroke="#c08a2a" stroke-width="8" stroke-linecap="round"/></g>
<g class="scAnim scFloat"><circle cx="100" cy="100" r="28" fill="#d9a441"/><circle cx="100" cy="100" r="20" fill="#f0d24a"/>
<text x="100" y="107" text-anchor="middle" font-size="18" fill="#7a5a10">祿</text></g>` },
    관귀학관: { cat:'길신', name:'관귀학관(官貴學館)', sub:'학문으로 얻는 관운·승진', role:'길신', ring:'#2a6a8a', badge:['#d3e6ef','#2a6a8a','#184a63'], fig:`
<g class="scAnim scFloat"><rect x="52" y="86" width="24" height="10" rx="4" fill="#2a2a38"/><rect x="124" y="86" width="24" height="10" rx="4" fill="#2a2a38"/>
<rect x="78" y="76" width="44" height="32" rx="6" fill="#2a2a38"/><rect x="84" y="64" width="32" height="16" rx="6" fill="#2a2a38"/><rect x="92" y="58" width="16" height="8" rx="3" fill="#c0392b"/></g>
<g class="scAnim scBreathe"><rect x="74" y="116" width="52" height="26" rx="4" fill="#f3ece0"/><circle cx="74" cy="129" r="6" fill="#cbb89a"/><circle cx="126" cy="129" r="6" fill="#cbb89a"/>
<line x1="86" y1="124" x2="114" y2="124" stroke="#9a8a6a" stroke-width="2"/><line x1="86" y1="132" x2="114" y2="132" stroke="#9a8a6a" stroke-width="2"/></g>` },
    문곡귀인: { cat:'길신', name:'문곡귀인(文曲)', sub:'문장·예술·지혜의 별', role:'길신', ring:'#3f74b8', badge:['#dbe7f5','#3f74b8','#274d80'], fig:`
<g class="scAnim scPulse"><path d="M62,74 l3,7 l7,2 l-7,3 l-3,7 l-3,-7 l-7,-3 l7,-2 Z" fill="#9ad0ff"/></g>
<g class="scAnim scFloat" style="transform-origin:100px 60px"><rect x="96" y="56" width="8" height="62" rx="3" fill="#8a5a2b"/><path d="M95,116 q5,20 10,0 Z" fill="#222"/><path d="M100,118 l-2,10" stroke="#222" stroke-width="2"/></g>
<g class="scAnim scBreathe"><ellipse cx="100" cy="142" rx="24" ry="10" fill="#2a3550"/><ellipse cx="100" cy="139" rx="16" ry="6" fill="#10131f"/></g>` },
    현침살: { cat:'양면', name:'현침살(懸針殺)', sub:'예리함 · 침·의술 길 / 구설 흉', role:'양면', ring:'#7a8590', badge:['#e2e6ea','#7a8590','#4a545c'], fig:`
<g class="scAnim scSway" style="transform-origin:100px 54px"><path d="M100,54 q-14,-10 -7,-22" fill="none" stroke="#b3261e" stroke-width="2.4"/></g>
<g class="scAnim scFloat"><circle cx="100" cy="62" r="11" fill="none" stroke="#9aa6ae" stroke-width="4"/>
<polygon points="95,72 105,72 100,154" fill="#c0c8d0"/><line class="scAnim scGlint" x1="100" y1="80" x2="100" y2="142" stroke="#ffffff" stroke-width="2"/></g>` },
  });

  /* ---------- 렌더 헬퍼 ---------- */
  // 일주 동물 표정 오버레이 (웃음/슬픔/놀람) — 얼굴 기준점
  const FACE = {
    子:{mx:100,my:118,ex:14,ey:92,by:80}, 丑:{mx:100,my:124,ex:14,ey:94,by:82},
    寅:{mx:100,my:126,ex:15,ey:96,by:84}, 卯:{mx:100,my:122,ex:12,ey:104,by:92},
    辰:{mx:100,my:126,ex:14,ey:94,by:82}, 巳:{mx:120,my:90,ex:6,ey:74,by:64},
    午:{mx:102,my:134,ex:13,ey:92,by:80}, 未:{mx:100,my:120,ex:10,ey:98,by:86},
    申:{mx:100,my:126,ex:10,ey:100,by:88}, 酉:{mx:108,my:108,ex:8,ey:92,by:80},
    戌:{mx:100,my:124,ex:14,ey:94,by:82}, 亥:{mx:100,my:128,ex:16,ey:88,by:74}
  };
  function exprOverlay(zhi, expr) {
    const f = FACE[zhi] || {mx:100,my:124,ex:14,ey:92,by:80}, D='#2a2020';
    if (expr==='happy') return `<g><path d="M${f.mx-13} ${f.my} Q${f.mx} ${f.my+13} ${f.mx+13} ${f.my}" fill="none" stroke="${D}" stroke-width="3" stroke-linecap="round"/><ellipse cx="${f.mx-f.ex-6}" cy="${f.my-6}" rx="6" ry="4" fill="#ff8a8a" opacity=".55"/><ellipse cx="${f.mx+f.ex+6}" cy="${f.my-6}" rx="6" ry="4" fill="#ff8a8a" opacity=".55"/><path d="M${f.mx-f.ex-6} ${f.by} q5,-5 10,-3 M${f.mx+f.ex-4} ${f.by-3} q5,-2 10,3" fill="none" stroke="${D}" stroke-width="2.4" stroke-linecap="round"/></g>`;
    if (expr==='sad') return `<g><path d="M${f.mx-12} ${f.my+5} Q${f.mx} ${f.my-7} ${f.mx+12} ${f.my+5}" fill="none" stroke="${D}" stroke-width="3" stroke-linecap="round"/><path d="M${f.mx-f.ex-7} ${f.by-3} q6,5 11,3 M${f.mx+f.ex-4} ${f.by} q5,-2 11,-3" fill="none" stroke="${D}" stroke-width="2.4" stroke-linecap="round"/><path d="M${f.mx+f.ex+4} ${f.ey+3} q-4,9 1,14 q5,-4 1,-14 Z" fill="#7fc4ff"/></g>`;
    if (expr==='surprise') return `<g><ellipse cx="${f.mx}" cy="${f.my+2}" rx="6.5" ry="9" fill="${D}"/><path d="M${f.mx-f.ex-7} ${f.by-4} q5,-3 11,-1 M${f.mx+f.ex-4} ${f.by-5} q6,-2 11,1" fill="none" stroke="${D}" stroke-width="2.4" stroke-linecap="round"/></g>`;
    return '';
  }
  function token(ring, figInner, size, extraAttr, ringW, ringCount) {
    size = size || 120; ringW = ringW || 6; ringCount = ringCount || 1;
    let rings = `<circle cx="100" cy="100" r="92" fill="#faf7f2" stroke="${ring}" stroke-width="${ringW}"/>`;
    for (let i = 1; i < ringCount; i++) rings += `<circle cx="100" cy="100" r="${92 - i*8}" fill="none" stroke="${ring}" stroke-width="${ringW}"/>`;
    return `<svg viewBox="0 0 200 200" width="${size}" height="${size}" ${extraAttr||''}>` + rings + figInner + `</svg>`;
  }
  function animalToken(zhi, wx, size, extraAttr, expr, ring, ringW, ringCount) {
    const a = ANIMALS[zhi]; if (!a) return '';
    let fig = a.fig(WX_BODY[wx] || '#bbb');
    if (expr) fig += exprOverlay(zhi, expr);
    return token(ring || WX_RING[wx] || '#999', fig, size, extraAttr, ringW, ringCount);
  }
  function specialToken(key, size, extraAttr) {
    const s = SPECIALS[key]; if (!s) return '';
    return token(s.ring, s.fig, size, extraAttr);
  }

  // ===== 궁성(宮) 상징 캐릭터 (8위치 + 4궁) — 표정/세기 테두리 지원 =====
  function gface(){return `<circle cx="100" cy="104" r="46" fill="#f1d0a6"/><circle cx="83" cy="98" r="5.4" fill="#2a2020"/><circle cx="117" cy="98" r="5.4" fill="#2a2020"/>`;}
  function symExpr(expr){const D='#2a2020',mx=100,my=124,ex=18,ey=98,by=80;
    if(expr==='happy')return `<g><path d="M${mx-19} ${my} Q${mx} ${my+19} ${mx+19} ${my}" fill="none" stroke="${D}" stroke-width="4.5" stroke-linecap="round"/><ellipse cx="${mx-ex-9}" cy="${my-7}" rx="8" ry="5" fill="#ff8a8a" opacity=".55"/><ellipse cx="${mx+ex+9}" cy="${my-7}" rx="8" ry="5" fill="#ff8a8a" opacity=".55"/><path d="M${mx-ex-10} ${by} q7,-7 15,-3 M${mx+ex-5} ${by-4} q8,-4 15,3" fill="none" stroke="${D}" stroke-width="3.2" stroke-linecap="round"/></g>`;
    if(expr==='sad')return `<g><path d="M${mx-18} ${my+7} Q${mx} ${my-10} ${mx+18} ${my+7}" fill="none" stroke="${D}" stroke-width="4.5" stroke-linecap="round"/><path d="M${mx-ex-11} ${by-4} q8,7 16,3 M${mx+ex-5} ${by} q8,-4 16,-3" fill="none" stroke="${D}" stroke-width="3.2" stroke-linecap="round"/><path d="M${mx+ex+8} ${ey+5} q-6,13 1,19 q7,-6 1,-19 Z" fill="#7fc4ff"/></g>`;
    if(expr==='surprise')return `<g><ellipse cx="${mx}" cy="${my+2}" rx="10" ry="14" fill="${D}"/><path d="M${mx-ex-11} ${by-6} q7,-5 16,-1 M${mx+ex-5} ${by-7} q9,-4 16,1" fill="none" stroke="${D}" stroke-width="3.2" stroke-linecap="round"/></g>`;
    return `<path d="M${mx-11} ${my-2} q11,6 22,0" fill="none" stroke="${D}" stroke-width="3" stroke-linecap="round"/>`;
  }
  // 단순 얼굴 캐릭터 — 표정만으로 길흉 표시, 세기는 테두리 줄 수로
  const NRING='#cbb89a';
  const GUNG_SYM = {
    년주:{gung:'조상/사회/초년',domain:'조상·가문',ring:NRING,fig:gface()},
    월주:{gung:'부모/직업/중년',domain:'부모·성장환경',ring:NRING,fig:gface()},
    일주:{gung:'나/중장년',domain:'나의 기둥',ring:NRING,fig:gface()},
    시주:{gung:'자녀/말년',domain:'자녀·미래',ring:NRING,fig:gface()},
    년간:{gung:'집안·사회 드러난 이미지',domain:'겉으로 보이는 집안·사회적 모습',ring:NRING,fig:gface()},
    년지:{gung:'조상·고향·어린 시절 분위기',domain:'뿌리·고향·유년의 기운',ring:NRING,fig:gface()},
    월간:{gung:'배움·원칙·직업관·이상',domain:'가치관·직업관·이상',ring:NRING,fig:gface()},
    월지:{gung:'가정·부모관계·직장 기반',domain:'가정환경·부모·직업 기반',ring:NRING,fig:gface()},
    일지:{gung:'현실속의 나·배우자',domain:'현실의 나·배우자·가정',ring:NRING,fig:gface()},
    시간:{gung:'미래의 자녀·말년 생각',domain:'미래·자녀·말년의 마음',ring:NRING,fig:gface()},
    시지:{gung:'실제 자녀·말년 환경',domain:'실제 자녀·노년의 환경',ring:NRING,fig:gface()},
  };
  function symbolToken(key, size, extraAttr, expr, ring, ringW, ringCount){
    const o=GUNG_SYM[key]; if(!o) return '';
    return token(ring||o.ring, o.fig + symExpr(expr), size, extraAttr, ringW, ringCount);
  }

  root.SAJU_CHARS = {
    style: STYLE, WX_BODY, WX_RING, ANIMALS, SPECIALS, GUNG_SYM,
    token, animalToken, specialToken, symbolToken,
  };
})(typeof window !== 'undefined' ? window : globalThis);
