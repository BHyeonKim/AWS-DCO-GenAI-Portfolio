# Shift Handover Memo

작성자: 김보현
교대 시점: 2026-07-10 07:55

> 교육용 샘플 데이터입니다. `sample_shift_handover_log.txt`와 `ticket_priority_matrix.csv`를
> 근거로 작성했으며, 실제 AWS 내부 장비/절차가 아닙니다.

## 가장 먼저 확인할 Ticket

- `EDU-TKT-2026-0201` (Gi0/24 Link Flap 재발) — Link Down이 실제로 발생해 서버 2대가 일시적으로 끊겼고, Link Up 이후에도 Link Flap이 한 번 더 기록되어 재발 위험이 남아 있습니다.

## 우선순위별 Ticket 상태와 판단 근거

| 순위 | Ticket | Ticket 상태 | 판단 근거 |
|---|---|---|---|
| 1 | EDU-TKT-2026-0201 | Open | Link Down 발생 이력 + Link Up 이후 Link Flap 재발(반복) + 원인 미확인 |
| 2 | EDU-TKT-2026-0202 | Open·Escalated | 서비스 중단은 없으나 Feed A 경고가 지속되고, 이중 전원 미복구, 연관 서버 6대로 영향 범위가 가장 넓음 |
| 3 | EDU-TKT-2026-0203 | Monitoring | 스토리지 미러가 활성 상태라 즉시 영향은 낮지만 교체 일정 미기록으로 지속 관찰 필요 |
| 4 | EDU-TKT-2026-0204 | Resolved | 온도 정상 범위 유지, Fan RPM 정상 복구, 추가 조치 불필요 |

## 현재 Open 상태 Ticket

- EDU-TKT-2026-0201 — Gi0/24 Link Flap 재발, 현재 서비스는 사용 가능하나 반복 원인 미확인
- EDU-TKT-2026-0202 — Rack PDU Feed A 입력 전압 경고 지속, Escalated 상태, 이중 전원 미복구

## Monitoring 상태 Ticket

- EDU-TKT-2026-0203 — SSD Slot 2 예측 장애 경고, 스토리지 미러 활성, 교체 일정 미기록

## Resolved 상태 Ticket

- EDU-TKT-2026-0204 — Fan RPM 경고 후 정상 범위로 복구, 추가 조치 불필요

## 현재까지 확인된 사실

- SAMPLE_TOR_SW_03 Gi0/24에서 06:38 Link Flap 감지 → 06:42 Link Down(서버 2대 일시 단절) → 06:48 Link Up → 07:05 Link Flap 추가 기록
- SAMPLE_RACK_PDU_05A Feed A에서 06:50 입력 전압 경고 발생, 07:25까지 경고 지속, Feed B는 계속 정상(사용 가능)
- EDU_SRV_R02_N08 SSD Slot 2에서 07:02 예측 장애 경고 발생, 저장장치 미러는 활성 상태 유지
- DEMO_CORE_SW_04 Fan 모듈 1이 07:10 RPM 저하 경고 후 07:22 정상 범위로 복귀, 07:28 Ticket Resolved 처리

## 아직 확인되지 않은 내용

- EDU-TKT-2026-0201: Link Flap이 반복되는 근본 원인
- EDU-TKT-2026-0202: 정상 이중 전원 상태가 언제 복구될지, Feed A 경고의 원인
- EDU-TKT-2026-0203: SSD 교체 일정

## 다음 담당자가 확인할 내용

1. EDU-TKT-2026-0201 — Gi0/24에서 Link Flap이 추가로 발생하는지, 원인 조사 결과가 나왔는지 확인
2. EDU-TKT-2026-0202 — Feed A 전압이 정상 범위로 돌아왔는지, 이중 전원 상태가 복구되었는지 확인
3. EDU-TKT-2026-0203 — SSD Slot 2 교체 일정이 확정되었는지 확인

## 3줄 인수인계 요약

1. 가장 먼저 EDU-TKT-2026-0201(Link Flap 재발)을 확인하세요. Link Down 이력이 있고 원인이 아직 밝혀지지 않았습니다.
2. EDU-TKT-2026-0202(PDU 전압 경고)는 서비스 중단은 없지만 Escalated 상태이며 이중 전원이 아직 복구되지 않았으니 계속 지켜봐야 합니다.
3. EDU-TKT-2026-0203(SSD 경고)은 Monitoring 상태로 당장 위험하지 않고, EDU-TKT-2026-0204(Fan 경고)는 이미 Resolved되어 추가 조치가 필요 없습니다.

## AI(Claude Code) 결과와 내 판단 비교

- AI가 잘 정리한 내용: 로그에 기록된 시간순 사실(Link Flap/Down/Up, PDU 경고 지속, SSD 예측 장애, Fan 복구)을 Ticket별로 빠짐없이 구분해 정리했습니다.
- AI 결과에서 빠졌거나 부족했던 내용: 우선순위 판단 근거를 처음에는 Severity 위주로만 서술하기 쉬워서, 영향 범위(연관 서버 수)와 반복 여부를 근거 문장에 명시적으로 추가했습니다.
- 내가 정한 우선순위: 1) 0201 2) 0202 3) 0203 4) 0204
- 그렇게 판단한 이유: 0201은 실제 Link Down(서비스 단절 이력)과 반복 재발이 함께 있어 가장 시급하다고 판단했습니다. 0202는 현재 서비스 중단은 없지만 경고가 지속되고 영향 범위(6대)가 가장 넓어 2순위로 두었습니다. 0203은 미러 보호로 즉시 위험은 낮아 3순위, 0204는 이미 Resolved되어 마지막으로 두었습니다.

## 내가 직접 수정한 내용

1. Ticket 우선순위 근거 문장에 "영향 가능 범위(연관 서버 수)"를 명시적으로 추가해 Severity만으로 판단하지 않았음을 분명히 했습니다.
2. 원인이 아직 밝혀지지 않은 항목(Link Flap 반복 원인, PDU 전압 원인)을 "확정된 사실"이 아니라 "아직 확인되지 않은 내용"으로 분리했습니다.
