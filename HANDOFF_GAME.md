# 사주 캐릭터 게임 — 인수인계 문서 (HANDOFF_GAME)

> 새 세션에서 이 프로젝트를 이어서 작업할 때 **가장 먼저 읽는 문서**입니다.
> 작업자(사람)와 다음 AI 세션 모두를 위한 안내입니다.

---

## 1. 한 줄 요약
한국 사주명리(사주팔자·대운/세운/월운)를 입력하면 **신살·오행·일주 동물을 포켓몬 같은 캐릭터로 시각화**해 보여주는 **모바일 우선 단일 HTML 웹앱**. 검증된 만세력+고전 DB 엔진(saju_engine_v2) 위에 게임/도감 UI를 얹었다.

## 2. 폴더·파일 지도
- 작업 루트: `D:\kks\claude\sajugame\`
  - `index.html` — GitHub Pages 진입점. `saju_engine_v2/saju_game.html`로 자동 이동.
  - `saju_engine_v2\` — 실제 작업 공간
    - **`build_game.py`** ⭐ — 앱 빌더(이걸 수정하고 실행해 앱을 만든다)
    - **`saju_game.html`** ⭐ — 빌더가 만든 **완성 앱**(브라우저로 바로 열림, 자립형 단일 파일)
    - **`characters.js`** ⭐ — SVG 캐릭터 라이브러리(ANIMALS, SPECIALS, token 함수, 표정/테두리)
    - `game_refs.json` — 고전 근거 데이터(빌드 시 앱에 임베드). `build_game_refs.py`가 `saju_full.db`에서 생성.
    - `build_webapp.py` — **검증된 만세력/분석 JS 엔진의 원본**. build_game.py가 여기서 엔진을 문자열로 추출해 재사용(직접 수정하지 않음).
    - `HANDOFF.md` — 사주 **엔진/DB**(만세력·격국·고전) 쪽 상세 인수인계(별도, 깊은 내용).
    - 그 외 `translations_*.json`, `*.db`, `build_tr_*.py`, `mingli_*` 등은 **고전 텍스트/검증 데이터(정적 자산)** — 평소 안 건드림.
  - `bak001\` — **체크포인트 백업**(이 시점 작업본 복사). `CHECKPOINT.md` 참고. 복원 시 이 폴더 파일을 `saju_engine_v2\`에 덮어쓰기.

## 3. 빌드 방법 (가장 중요)
앱은 `saju_game.html`을 **직접 수정하지 않는다.** 항상 빌더를 고치고 재생성한다.
```
cd saju_engine_v2
python3 build_game.py        # → saju_game.html (자립형 단일 파일) 생성
```
- `build_game.py` 구조: `build_webapp.py`에서 엔진 블록을 `between()` 문자열 앵커로 추출 → 큰 `TEMPLATE`(원시 문자열 `r"""..."""`)의 placeholder에 주입.
- placeholder: `__CHARS__`(characters.js), `__JIEQI__`, `__LUNAR__`, `__GAMEREFS__`, `__ENGINE__`.
- 엔진 추출 앵커: `const GAN="甲乙..."` ~ `/* ============ UI ============ */`, `const GUNG={...}`, `useAvoid`~`...list,dl};}`. 이 문자열이 바뀌면 앵커도 맞춰 수정.

## 4. 경로 매핑 (샌드박스 ↔ Windows)
- Windows `D:\kks\claude\sajugame\` = 샌드박스 `/sessions/<id>/mnt/sajugame/`
- 파일 편집은 Windows 경로의 Read/Write/Edit 도구로, 빌드·테스트는 샌드박스 bash로.
- ⚠️ **샌드박스에서 git·sqlite 쓰기는 마운트에서 막힘**(Operation not permitted). git 커밋/태그/락 삭제는 **사용자가 GitHub Desktop/Windows에서** 해야 함. 단순 파일 cp/python 쓰기는 가능.

## 5. 앱 화면 구조 (사용자 흐름)
1. 입력 카드: 생년월일시·성별·양/음력·진태양시 보정 → **「사주 소환」**. (시 모름 시 「시간 예측하기」 팝업, 「내 인생 백테스팅」 버튼)
2. 결과(`#result`) — 각 영역 우측 상단 **접기/펼치기(▾)** 있음:
   - **운(運) 선택** — 대운/세운/월운 칩. 소환 시 오늘 기준 자동 선택.
   - **이 시기 총평** — **대운/세운/월운 3개 레인**, 각 레인은 신호들이 **포켓몬 카드 캐러셀**(별등급 ★1~3, 캐릭터 엠블럼, 화살표/옆카드로 회전, 카드 클릭 시 번개 이펙트→팝업 상세).
   - **✦ 캐릭터 스테이지 ✦** — 원국/운 캐릭터 토큰. 클릭 시 궁(宮)에 테두리·표정 반응 + 상세.
   - **사주 원국 + 궁(宮) 표** — 기둥별 간지·십성·지장간·궁성 + 합충 관계.
   - **📖 신살 도감** — 내게 뜬 캐릭터(원국+운)를 카드로 모아 설명.

## 6. 핵심 JS 함수 (build_game.py 내부, saju_game.html에 인라인)
- 흐름: `run()` → `CUR` 세팅·오늘 운 자동선택 → `rebuild()`.
- `rebuild()` → `combined()`(원국+운 P/ord) → `shinsalSet` / `spiritSet` / `computeRelations` → `renderPillars`, `renderStage`, `renderRelList`, `applyLuckReactions`, **`renderSummary`**, **`renderDogam`**.
- 총평 카드: **`summaryItems()`**(대운/세운/월운별 카드 객체 배열 반환: name·cat(good/bad/mid)·st(별 1~3)·emblem(SVG)·short·detail) → **`renderSummary()`**(3레인 `laneHTML`) → **`renderLane(which,dir)`**(중앙/좌우 카드 + 슬라이드 애니) → `sumNav` / `sumZap`(번개) / `openSumModal`/`closeSumModal`.
- 도감: **`renderDogam()`** + `dogamCard`/`dogamToggle`(STAGE 기반).
- 백테스팅: `periodSignals(Y,M)` → `matchEvent(sig,cat)` → `btAnalyze()`(결과+근거). 분류→기대신호 표 `CAT_SIG`, 설명 `CAT_DESC`.
- 상세 본문: `charDetail`→`shinsalDetail`/`spiritDetail`/`animalDetail`, 관계는 `buildPlain(gi,sc)`, 고전 `refsHtml(REFKEY[key])`.
- 접기: `secToggle(id,btn)` (영역 body id: `sb-luck`/`sb-sum`/`sb-stage`/`sb-gung`).

## 7. 핵심 데이터 사전 (수정 시 자주 건드림)
- `SUMCOL`(카드 길흉 색), `SIPSIN_EMB`/`REL_EMB`(엠블럼 한글 라벨), `glyphEmblem()`.
- `GUNG_SHORT`(궁성 짧은 이름·카드용), `GUNG_EXPLAIN`(궁성 긴 풀이·팝업용), `SUBJECT_PLAIN`, `GUNG_PLACE`.
- `SS_INFO`(신살 기본 g/b/a/d/w), `SS_RICH`(good/bad/mind), `SS_EVENT`(운에서 사건), `SS_LUCK`(십성운 총평).
- `CAT_SIG`/`CAT_DESC`(백테스팅 분류↔신호), `REFKEY`/`REF_PLAIN`/`REFS`(고전 근거), `EVENT_BY_GUNG`, `RELATION_PLAIN`, `REL_INFO`, `ELEM_INFO`, `SIPSIN_PLAIN`.
- 신살 판정: `shinsalSet()`(12신살·귀인·백호/괴강/현침·귀문6·원진·천라지망·역마 진/살 등), 오행 합 `spiritSet()`/`elemCombos()`.

## 8. 지금까지 구현된 기능 (체크포인트 bak001 기준)
- 만세력 입력(양/음력·윤달·분(分) 반영·진태양시 보정 TZ540/-30분), 오늘 기준 운 자동선택.
- 캐릭터 31+종(일주동물 12·오행정령·길흉신·역마 진/살·귀문 6·다수 귀인/흉신), SVG·표정·테두리·움직임.
- 운(대운/세운/월운) 연동, 합/충/형/파/해 관계선, 강약 테두리(약1/중2/강3줄).
- 총평 3분할 + 포켓몬 카드 캐러셀(별등급·한글 엠블럼·팝업·번개·부드러운 슬라이드).
- 신살 도감, 인생 백테스팅(사건↔신호 매칭+근거·고전), 각 영역 접기/펼치기.
- 쉬운 말(중학생 눈높이) 설명 + 고전 근거 + 실생활 처방 + 시기별 사건 가능성(틀릴 수 있음 고지).

## 9. 테스트 방법 (Node 스모크 테스트)
브라우저 없이 함수 검증: saju_game.html의 `<script>` 블록을 모두 합쳐 eval.
- ⚠️ **블록을 'src=' 로 필터링하지 말 것**(실제 코드 블록에 `src=` 문자열이 있어 통째로 누락됨 → 함수 미정의 버그).
- ⚠️ `global.window = global` 로 둬야 characters.js가 전역에 SAJU_CHARS를 심음. `global.Option` 등 로드시 호출되는 DOM API는 mock.
- 회귀 테스트 표준 사주: **1992-01-17 음력 13:35 여** → 壬申 壬寅 丙寅 乙未(일간 丙火), 현재 대운 己亥. (2022 회사소멸=편관·살역마, 2024 상사스트레스=원진·진해귀문, 2025 시험=정인운 등 실제 사건과 매칭 확인됨)

## 10. 함정·주의 (실수 방지)
- `TEMPLATE`은 파이썬 **원시 문자열 `r"""..."""`**. JS 작은따옴표 문자열 안 아포스트로피를 `\'`로 쓰면 깨짐 → **「」 같은 기호 사용**하거나 따옴표 회피.
- 같은 const 중복 선언 금지(빌드/실행 에러).
- 음력 입력은 `lunarToSolar()`가 **배열 `[y,m,d]`** 반환(.y/.m/.d 아님).
- 분(分) 반영 필수(13:35 → 未시). UTC 계산 시 `Date.UTC(Y,M-1,D,h,mi)`.
- 신살 키 이름과 `characters.js` SPECIALS 키, `REFKEY` 매핑을 일치시킬 것.

## 11. 배포 상태 & 사용자가 할 일 (미완)
- GitHub: 계정 `kks-sajuproject`, 레포 `sajugame`, 브랜치 `main`. Pages: main /(root). 공개 URL **https://kks-sajuproject.github.io/sajugame/**.
- 현재 **아직 Push 안 됨** → URL 접속 시 404. `index.html`과 최신 `saju_game.html`을 **GitHub Desktop에서 Commit→Push** 하면 1~2분 뒤 열림.
- ⚠️ 커밋이 "lock file already exists"로 막히면: Windows에서 `D:\kks\claude\sajugame\.git\index.lock` 삭제(빈 파일이라 안전) 후 재커밋. (`Win+R`→`cmd`→`del "D:\kks\claude\sajugame\.git\index.lock"`)
- 체크포인트 bak001도 같은 커밋에 포함해 Push하면 git에도 보관됨(원하면 History에서 그 커밋에 `bak001` 태그 생성).

## 12. 다음에 할 만한 것(아이디어, 미확정)
- 모바일 최적화 마무리(폭/터치 영역), 카드 디자인·레이아웃 추가 개선.
- 공용 사례 DB(백테스팅 데이터 수집·검증 파이프라인) — 서버 필요.
- 배포 완료 후 실제 모바일에서 점검.

---
*이 문서는 bak001 체크포인트 시점 기준. 큰 변경 후 갱신 권장.*
