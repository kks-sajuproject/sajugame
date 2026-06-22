# 사주 분석 엔진 (Saju Analysis Engine)

고전 명리 9책의 한국어 번역 DB를 토대로 **만세력·격국·용신·신살·대운/세운/월운**을 계산하고,
성격·재능·직업·재물·연애·결혼·자녀·건강 등 **15영역 심층 해석**과 궁(宮) 기반 시기 사건을 제공하는 사주 분석 엔진입니다.
Python 코어 + 자립형 단일 HTML 웹앱(서버 불필요)으로 구성됩니다.

---

## 빠른 시작

```bash
# 1) 의존성 설치
pip install -r requirements.txt        # sxtwl, opencc-python-reimplemented

# 2) (선택) 통합 DB 빌드 — 원문+번역
python3 build_full_db.py               # → saju_full.db

# 3) 웹앱 빌드
python3 build_refs.py                  # 고전 근거 추출 → refs_table.json
python3 build_webapp.py                # → saju_web.html  (브라우저로 열기)

# 4) 검증
node test_webapp.js                    # JS 엔진 ↔ Python/sxtwl 대조
```

`saju_web.html`을 브라우저에서 더블클릭하면 바로 실행됩니다(인터넷·서버 불필요).

---

## 디렉터리 구조 (역할별)

**엔진 코어 (Python)**
- `saju_engine.py` — 만세력. 생년월일시 → 팔자·지장간·십신·신살·십이운성·합충·강약·대운. (의존: sxtwl)
- `geukguk.py` — 격국·용신·사령·종격/화기격 판정.
- `saju_report.py` — 원국 종합 분석 + 고전 근거 검색(RAG) 통합.

**웹앱 (JS 엔진 내장)**
- `build_webapp.py` — 위 로직을 JS로 이식한 단일 HTML 빌더. 절기·음력 테이블, 고전 근거를 임베드.
- `saju_web.html` — 빌드 산출물(자립형 웹앱). *gitignore*
- `test_webapp.js` — Node로 JS 엔진을 Python/sxtwl과 대조 검증.

**데이터 자산**
- `saju_classics.db` — 원문(간체) + FTS5 전문검색. **원본 소스.**
- `translations_*.json` — 9책 한국어 번역(3239절).
- `refs_table.json` — 영역별 고전 근거 구절(웹앱 임베드용).
- `jieqi_table.json` / `lunar_table.json` — 절기·음력 변환 테이블(만세력 JS용).
- `mingli_dataset.json` — 고전 命例(인물 사주) 1,848개. 검증용.
- `mingli_verify_clean.json` — 생몰 검증 인물 서브셋(엔진 대조 verified 9명).

**빌드·전처리 스크립트**
- `build_full_db.py` · `build_refs.py` · `build_webapp.py` · `build_viewer.py`
- `extract_mingli.py` · `refine_mingli.py` — 命例 추출·정제.
- `build_tr_*.py` — 책별 번역 머지 스크립트.

**문서**
- `HANDOFF.md` — 상세 작업 이력·설계 결정(새 세션 인수인계용).
- `README.md` — 이 문서.

---

## Python 엔진 사용 예

```python
from saju_engine import compute, fmt
r = compute(1982, 5, 4, hour=6, gender="남")   # 양력 생년월일시
print(fmt(r))                                   # 팔자·십신·신살·강약·대운

from geukguk import analyze                      # 팔자(간지) 직접 입력
a = analyze("壬戌","甲辰","丁亥","癸卯", days=28) # days=절입후 경과일(사령용)
print(a["classify"]["geuk"], a["yongsin"])

from saju_report import report, render           # 고전 근거 포함 종합 리포트
print(render(report(1982,5,4,hour=6,gender="남")))
```

---

## 데이터베이스 (saju_classics.db)

세 테이블 관계형: `books`(책) → `sources`(판본) → `passages`(본문 청크) + `passages_fts`(FTS5).
번체/간체 어느 쪽으로 검색해도 결과가 나오도록 정규화 색인. 수록: 9책·12판본·3,239청크.
통합 DB(`saju_full.db`)는 여기에 `translations`(한국어)·`translations_fts`를 더한 것.
상세 스키마·검색법은 `HANDOFF.md` 참조.

---

## 모바일/웹 서비스 배포

`saju_web.html`은 자립형이라 **정적 호스팅**(GitHub Pages·Netlify·Vercel)에 그대로 올리면 웹 서비스가 됩니다.
`manifest.webmanifest`가 포함돼 있어 모바일에서 **홈 화면에 추가(PWA)**하면 앱처럼 설치·실행됩니다.

```bash
# 예: 로컬 미리보기
python3 -m http.server 8000   # http://localhost:8000/saju_web.html
```

오프라인 캐싱(Service Worker)·푸시 알림(매일 운세) 등은 호스팅 후 확장 가능합니다.

---

## 다음 개발 (모바일/웹 서비스)

- [ ] 정적 호스팅 + PWA(오프라인·설치) 완성
- [ ] 결과 저장/공유(URL 해시 기반 — 이미 일부 구현)
- [ ] 백엔드 API(Flask/FastAPI)로 분리해 다중 클라이언트 지원
- [ ] 매일 운세 알림(세운·월운·일운) 구독 기능
- [ ] 번역 DB RAG + LLM 상담 챗봇

상세 이력과 설계 결정은 `HANDOFF.md`에 누적되어 있습니다.
