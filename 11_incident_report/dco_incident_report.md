# 교육용 DCO Incident Report

- 차시: 11차시
- 작성자: 김보현
- 학번: 2602370223
- 작성일: 2026-07-20
- 사용 자료: 교육용 샘플 데이터 (실제 AWS 내부 자료 아님)

## 1. 작성 목적

- 이 문서는 실제 DCO 장애 보고서가 아니며, 공개 직무 맥락과 교육용 샘플 로그를 이용해
  Incident Report의 기본 구조(사건 개요 → 시간순 이벤트 → 사실/원인 구분 → 전달 메모)를
  연습하기 위해 작성되었습니다.

## 2. 교육용 사건 개요

- 2026-07-03 03:05~03:30 사이, 샘플 장비 `SAMPLE_TOR_SW_01`의 `Gi0/1` 인터페이스에서
  CRC Error가 짧은 시간에 급증한 뒤 Link Down이 발생했습니다.
- Ticket이 생성되어 담당팀에 전달되었고, 패치 코드 교체와 커넥터 정리 조치 후
  Link Up과 CRC Error 0 상태로 복구된 것이 로그에 기록되어 있습니다.

## 3. 관련 대상

- 샘플 장비명: `SAMPLE_TOR_SW_01`
- 샘플 Ticket ID: `EDU-TKT-2026-0003`
- 주요 이벤트: CRC error 증가, Link Down, Ticket opened, Ticket escalated, Maintenance completed, Link Up, Normal heartbeat

## 4. 시간순 이벤트

| 시간 | 대상 | 이벤트 | 내용 |
|---|---|---|---|
| 03:05 | SAMPLE_TOR_SW_01 (Gi0/1) | CRC error 증가 | CRC Error 카운터가 5분 동안 154까지 증가 |
| 03:06 | SAMPLE_TOR_SW_01 (Gi0/1) | Link Down | 인터페이스 상태가 DOWN으로 변경, 서버 연결 끊김 |
| 03:07 | SAMPLE_TOR_SW_01 | Ticket opened | `EDU-TKT-2026-0003` 생성 (Gi0/1 포트 오프라인 관련) |
| 03:12 | SAMPLE_TOR_SW_01 | Ticket escalated | Onsite Cabling Team으로 전달 |
| 03:25 | SAMPLE_TOR_SW_01 | Maintenance completed | 패치 코드 교체, 포트 커넥터 정리 |
| 03:26 | SAMPLE_TOR_SW_01 (Gi0/1) | Link Up | 인터페이스 상태가 UP으로 변경 |
| 03:30 | SAMPLE_TOR_SW_01 (Gi0/1) | Normal heartbeat | 정상 상태 복귀, CRC Error 0건 기록 |

## 5. 확인된 사실

- Gi0/1의 CRC Error가 5분 동안 154까지 증가했습니다.
- CRC Error 증가 1분 뒤 Gi0/1이 Link Down 상태로 바뀌었습니다.
- Ticket EDU-TKT-2026-0003이 생성되어 Onsite Cabling Team에 에스컬레이션되었습니다.
- 패치 코드 교체와 포트 커넥터 정리 후 Link Up과 CRC Error 0이 기록되었습니다.

## 6. 가능한 원인

- 패치 코드(케이블) 자체의 물리적 손상 또는 노후화 (조치 목록에 케이블 교체가 포함되어 있어 가능성 있음)
- 커넥터/포트 접속 불량, 예를 들어 먼지나 헐거운 결합 (조치 목록에 커넥터 정리가 포함되어 있어 가능성 있음)
- 인터페이스(포트) 하드웨어 자체의 일시적 이상 (로그만으로는 배제할 수 없음)

> 위 세 가지는 모두 가능성 수준의 추정이며, 로그만으로 어느 것이 실제 원인인지 확정할 수 없습니다.

## 7. 현재 확인되지 않은 내용

- 세 가지 가능한 원인 중 정확히 무엇이 최초 원인이었는지
- CRC Error가 이번 사건 이전에도 반복적으로 발생했는지
- 패치 코드 교체와 커넥터 정리 중 어느 조치가 실제로 문제를 해결했는지

## 8. 추가로 필요한 정보

- Gi0/1의 사건 이전 CRC Error 이력
- 연결 대상 장비(반대편 포트)의 같은 시간대 로그
- 교체된 패치 코드의 사용 기간 및 손상 여부
- 사건 이후 CRC Error 재발 여부
- Ticket EDU-TKT-2026-0003에 남아있는 추가 기록

## 9. Escalation 전달 메모

- 대상: SAMPLE_TOR_SW_01 / Gi0/1, Ticket EDU-TKT-2026-0003
- 증상: 03:05 CRC Error 급증 → 03:06 Link Down
- 수행된 조치: 패치 코드 교체, 포트 커넥터 정리 (03:25 완료)
- 조치 후 상태: 03:26 Link Up, 03:30 CRC Error 0건으로 정상 확인
- 참고: 최초 원인은 로그만으로 확정되지 않았으므로, 다음 담당자는 케이블/커넥터/포트 하드웨어 세 가지 가능성을 모두 열어두고 확인하는 것을 권장합니다.

## 10. 최종 요약

- 교육용 샘플 로그에서 CRC Error 증가 이후 Link Down이 관찰되었고, Ticket 생성과 Escalation이 이어졌으나, 현재 제공된 정보만으로 정확한 원인을 확정할 수 없습니다.

## 11. 사용한 agy 프롬프트

- agy는 사용하지 않았습니다. 대신 Claude Code에게 아래 세 파일을 함께 참고해 교육용 Incident Report 초안을 작성해달라고 요청했습니다.
  1. `09_log_analysis_script/sample_dco_log.txt`
  2. `09_log_analysis_script/incident_summary.md`
  3. `10_incident_analysis/crc_linkdown_analysis.md`
- 요청 조건: 실제 AWS 내부 보고서처럼 표현하지 않을 것, 교육용 샘플 데이터임을 명시할 것, 확인된 사실과 가능한 원인을 분리할 것, 원인을 하나로 확정하지 않을 것, 입력 파일에 없는 내용을 사실처럼 쓰지 않을 것, 실제 장비 조작 절차를 쓰지 않을 것, 비전공자도 이해할 수 있는 짧은 문장으로 쓸 것.

## 12. 내가 직접 수정한 내용

1. 사건 시간(03:05~03:30), 장비명(`SAMPLE_TOR_SW_01`), Ticket ID(`EDU-TKT-2026-0003`)를 원본 `sample_dco_log.txt`와 한 줄씩 대조해 오탈자가 없는지 확인했습니다.
2. "가능한 원인" 항목에 확정적인 표현("~가 원인이었다")이 들어가지 않도록 문장을 "~가능성이 있음"으로 통일하고, 원인과 사실이 섞이지 않게 표(5번)와 목록(6번)을 분리했습니다.
