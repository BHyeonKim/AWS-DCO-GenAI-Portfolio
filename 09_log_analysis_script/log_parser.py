"""
DCO 교육용 샘플 로그 분석 스크립트

이 스크립트는 무엇을 하나요?
  1. sample_dco_log.txt 파일을 한 줄씩 읽습니다.
  2. 각 줄을 "|" 기호를 기준으로 나누어서
     날짜/시간, 장비명, 심각도(SEVERITY), 이벤트, 메시지로 분리합니다.
  3. 아래 항목들을 계산합니다.
     - 전체 로그 줄 수
     - 심각도별 개수 (INFO / WARNING / ERROR 등)
     - 이벤트별 개수
     - WARNING 또는 CRITICAL 로그 목록
     - CRC 에러, 링크 다운, 티켓 에스컬레이션 관련 주요 이벤트 요약
  4. 결과를 incident_summary.md 파일로 저장합니다.

주의:
  - 이 로그는 수업용으로 만든 "샘플" 로그이며 실제 AWS 내부 장비 정보가 아닙니다.
  - 외부 패키지 없이 Python 표준 라이브러리(collections 등)만 사용합니다.
"""

from collections import Counter
from pathlib import Path

# 이 스크립트 파일이 있는 폴더를 기준으로 입력/출력 파일 경로를 정합니다.
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sample_dco_log.txt"
OUTPUT_FILE = BASE_DIR / "incident_summary.md"

# 로그 한 줄에서 몇 개의 항목(필드)이 나와야 하는지 정해둡니다.
# 형식: 날짜시간 | 장비 | 심각도 | 이벤트 | 메시지  -> 총 5개
EXPECTED_FIELD_COUNT = 5


def parse_log_line(line):
    """
    로그 한 줄(문자열)을 받아서
    {timestamp, device, severity, event, message} 형태의 딕셔너리로 바꿔줍니다.

    형식이 맞지 않는 줄(빈 줄, 필드 개수가 다른 줄)은 None을 반환해서
    걸러낼 수 있게 합니다.
    """
    line = line.strip()
    if not line:
        return None

    parts = [p.strip() for p in line.split("|")]
    if len(parts) != EXPECTED_FIELD_COUNT:
        return None

    timestamp, device, severity, event, message = parts
    return {
        "timestamp": timestamp,
        "device": device,
        "severity": severity,
        "event": event,
        "message": message,
    }


def load_log_entries(file_path):
    """로그 파일을 읽어서 파싱된 로그 딕셔너리들의 리스트로 돌려줍니다."""
    entries = []
    with open(file_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            entry = parse_log_line(raw_line)
            if entry is not None:
                entries.append(entry)
    return entries


def summarize_key_events(entries):
    """
    CRC 에러, 링크 다운(Link Down), 티켓 에스컬레이션(Ticket escalated)과
    관련된 로그만 골라서 리스트로 돌려줍니다.

    실제 이벤트 문구는 한글/영어가 섞여 있을 수 있어서,
    이벤트/메시지 텍스트를 대문자로 바꾼 뒤 키워드가 포함되어 있는지로 판단합니다.
    """
    keyword_map = {
        "CRC_ERROR": "CRC",
        "LINK_DOWN": "LINK DOWN",
        "TICKET_ESCALATED": "ESCALATED",
    }

    key_events = []
    for entry in entries:
        # 이벤트 이름만 검사합니다. (메시지까지 검사하면 "정상 복구" 안내문에도
        # CRC/Link 같은 단어가 섞여 있어 오탐이 생길 수 있기 때문입니다.)
        event_text = entry["event"].upper()
        for label, keyword in keyword_map.items():
            if keyword in event_text:
                key_events.append({"label": label, **entry})
                break  # 한 로그가 여러 키워드에 중복으로 잡히지 않도록 함

    return key_events


def build_markdown_report(entries):
    """분석 결과를 Markdown 문자열로 만들어서 돌려줍니다."""
    total_count = len(entries)
    severity_counter = Counter(e["severity"] for e in entries)
    event_counter = Counter(e["event"] for e in entries)
    warning_or_critical = [
        e for e in entries if e["severity"] in ("WARNING", "CRITICAL")
    ]
    key_events = summarize_key_events(entries)

    lines = []
    lines.append("# DCO 교육용 샘플 로그 분석 결과")
    lines.append("")
    lines.append("> 이 보고서는 교육 목적으로 만든 샘플 로그(`sample_dco_log.txt`)를")
    lines.append("> Python 표준 라이브러리만으로 분석한 결과입니다. 실제 AWS 내부")
    lines.append("> 장비/네트워크 정보가 아니며, 실제 장비 점검이나 외부 조치를")
    lines.append("> 요구하는 내용이 아닙니다.")
    lines.append("")

    # 1. 전체 로그 줄 수
    lines.append("## 1. 전체 로그 줄 수")
    lines.append("")
    lines.append(f"- 총 {total_count}건의 로그가 확인되었습니다.")
    lines.append("")

    # 2. 심각도별 개수
    lines.append("## 2. 심각도(SEVERITY)별 개수")
    lines.append("")
    lines.append("| 심각도 | 개수 |")
    lines.append("|---|---|")
    for severity, count in severity_counter.most_common():
        lines.append(f"| {severity} | {count} |")
    lines.append("")

    # 3. 이벤트별 개수
    lines.append("## 3. 이벤트별 개수")
    lines.append("")
    lines.append("| 이벤트 | 개수 |")
    lines.append("|---|---|")
    for event, count in event_counter.most_common():
        lines.append(f"| {event} | {count} |")
    lines.append("")

    # 4. WARNING 또는 CRITICAL 로그 목록
    lines.append("## 4. WARNING / CRITICAL 로그 목록")
    lines.append("")
    if warning_or_critical:
        lines.append("| 시간 | 장비 | 심각도 | 이벤트 | 메시지 |")
        lines.append("|---|---|---|---|---|")
        for e in warning_or_critical:
            lines.append(
                f"| {e['timestamp']} | {e['device']} | {e['severity']} "
                f"| {e['event']} | {e['message']} |"
            )
    else:
        lines.append("WARNING 또는 CRITICAL 로그가 없습니다.")
    lines.append("")

    # 5. 주요 이벤트 요약 (CRC_ERROR / LINK_DOWN / TICKET_ESCALATED)
    lines.append("## 5. 주요 이벤트 요약 (CRC_ERROR / LINK_DOWN / TICKET_ESCALATED)")
    lines.append("")
    if key_events:
        lines.append("| 구분 | 시간 | 장비 | 이벤트 | 메시지 |")
        lines.append("|---|---|---|---|---|")
        for e in key_events:
            lines.append(
                f"| {e['label']} | {e['timestamp']} | {e['device']} "
                f"| {e['event']} | {e['message']} |"
            )
    else:
        lines.append("CRC 에러, 링크 다운, 티켓 에스컬레이션 관련 로그가 없습니다.")
    lines.append("")

    # AI 활용 기록 (수업 과제 요구사항 - 수강생이 직접 작성/보완하는 항목)
    lines.append("---")
    lines.append("")
    lines.append("## [ AI 활용 기록 ]")
    lines.append("")
    lines.append("### 1. 사용한 도구")
    lines.append("")
    lines.append("- Claude Code (Sonnet 5) — 로그 분석 Python 스크립트(`log_parser.py`) 초안 작성 및 결과 리포트 생성")
    lines.append("")
    lines.append("### 2. AI가 생성한 내용 중 발견한 오류 또는 부족한 점")
    lines.append("")
    lines.append(
        "- 초기 버전에서는 '주요 이벤트 요약'을 이벤트명과 메시지를 합쳐서 키워드로 검색했는데, "
        "그 결과 정상 복구를 알리는 하트비트 메시지(`0 CRC errors`)까지 CRC_ERROR로 잘못 분류되는 "
        "오탐(false positive)이 발생했습니다."
    )
    lines.append(
        "- 메시지 대신 이벤트명만 검사하도록 수정해서 오탐을 제거했습니다. "
        "AI가 만든 로직을 그대로 신뢰하지 않고 결과를 직접 확인하는 과정이 필요했습니다."
    )
    lines.append("")
    lines.append("### 3. AI 결과에서 원본 자료와 다르거나 설명이 부족했던 부분")
    lines.append("")
    lines.append(
        "- (직접 작성) 원본 로그와 대조했을 때 실제로 다르거나 설명이 부족했던 부분을 이곳에 적어주세요. "
        "예: 특정 심각도/이벤트 분류 기준, 표에 포함되지 않은 항목, 요약이 생략한 맥락 등."
    )
    lines.append("")

    return "\n".join(lines)


def main():
    entries = load_log_entries(INPUT_FILE)
    report = build_markdown_report(entries)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"분석이 완료되었습니다. 결과 파일: {OUTPUT_FILE}")
    print(f"총 {len(entries)}건의 로그를 분석했습니다.")


if __name__ == "__main__":
    main()
