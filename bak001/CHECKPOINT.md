# bak001 — 체크포인트 백업

생성 시점의 사주 게임 앱 스냅샷입니다. 이후 디자인/레이아웃/기능 작업 전 복원 지점으로 사용하세요.

## 포함 파일
- index.html (루트 진입점: saju_engine_v2/saju_game.html 로 자동 이동)
- saju_engine_v2/saju_game.html  ← 완성된 단일 파일 앱 (브라우저로 바로 열림)
- saju_engine_v2/build_game.py   ← 앱 빌더(소스). 수정 후 `python build_game.py` 로 saju_game.html 재생성
- saju_engine_v2/characters.js   ← SVG 캐릭터 라이브러리
- saju_engine_v2/game_refs.json  ← 고전 근거 데이터(빌드 시 임베드)
- saju_engine_v2/build_game_refs.py ← game_refs.json 생성기
- saju_engine_v2/character_gallery.html ← 캐릭터 갤러리

## 이 시점까지 반영된 주요 기능
- 운(대운/세운/월운) 연동, 신살 도감
- 인생 백테스팅(사건↔사주 신호 매칭 + 근거·고전)
- 총평 3분할(대운/세운/월운) + 포켓몬 카드 캐러셀(별등급·캐릭터 엠블럼·팝업·번개 이펙트)
- 각 영역 접기/펼치기, 한글 엠블럼, 쉬운 궁성 풀이

## 복원 방법
이 폴더의 파일을 saju_engine_v2/ 로 덮어쓰면 됩니다.
