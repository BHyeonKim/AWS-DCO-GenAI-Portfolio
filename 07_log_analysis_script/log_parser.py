"""
교육용 샘플 DCO 로그 분석 스크립트

- 이 스크립트는 실제 AWS 내부 로그가 아니라 교육용 샘플 로그(sample_dco_log.txt)만 사용합니다.
- 실제 장비 점검이나 외부 대상 점검을 하지 않으며, 이미 저장된 텍스트 파일만 읽습니다.
- Python 표준 라이브러리만 사용합니다 (별도 설치가 필요한 외부 패키지 없음).

로그 한 줄의 형식:
YYYY-MM-DD HH:MM:SS | DEVICE | SEVERITY | EVENT | MESSAGE
"""

from collections import Counter
from pathlib import Path

# 이 스크립트와 같은 폴더에 있는 파일을 기준으로 경로를 정합니다.
# (다른 컴퓨터에서 실행해도 경로가 깨지지 않도록, 절대경로 대신 상대경로를 사용합니다.)
SCRIPT_DIR = Path(__file__).resolve().parent
LOG_FILE_PATH = SCRIPT_DIR / "sample_dco_log.txt"
OUTPUT_FILE_PATH = SCRIPT_DIR / "incident_summary.md"

# 확인항목 4번에서 "경고성 로그"로 취급할 심각도 목록입니다.
WARNING_LEVEL_SEVERITIES = {"WARNING", "CRITICAL"}

# 확인항목 5번에서 찾아볼 핵심 키워드입니다.
# 실제 로그의 EVENT 표현(예: "CRC error 증가", "Link Down", "Ticket escalated")과
# 비교하기 쉽도록 소문자 + 띄어쓰기 형태로 정리해 두었습니다.
KEY_EVENT_KEYWORDS = {
    "CRC_ERROR": "crc error",
    "LINK_DOWN": "link down",
    "TICKET_ESCALATED": "ticket escalated",
}


def parse_log_line(line):
    """
    로그 한 줄을 "|" 기준으로 나누어 딕셔너리로 반환합니다.
    형식이 맞지 않는 줄(빈 줄 등)은 None을 반환해서 건너뛸 수 있게 합니다.
    """
    line = line.strip()
    if not line:
        return None

    parts = [part.strip() for part in line.split("|")]
    if len(parts) < 5:
        # 필요한 항목(시간/장비/심각도/이벤트/메시지)이 다 없으면 분석 대상에서 제외합니다.
        return None

    timestamp, device, severity, event, message = parts[0], parts[1], parts[2], parts[3], "|".join(parts[4:])
    return {
        "timestamp": timestamp,
        "device": device,
        "severity": severity,
        "event": event,
        "message": message,
        "raw": line,
    }


def load_log_entries(log_path):
    """로그 파일을 읽어서 파싱된 로그 목록을 반환합니다."""
    entries = []
    with open(log_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            entry = parse_log_line(raw_line)
            if entry is not None:
                entries.append(entry)
    return entries


def analyze_entries(entries):
    """
    분석 요청 1~5번에 해당하는 결과를 계산합니다.
    원인을 하나로 단정하지 않고, 로그에 나타난 내용만 그대로 집계합니다.
    """
    total_count = len(entries)

    # 2. 심각도별 개수
    severity_counter = Counter(entry["severity"] for entry in entries)

    # 3. 이벤트별 개수
    event_counter = Counter(entry["event"] for entry in entries)

    # 4. WARNING 또는 CRITICAL 로그 목록
    warning_entries = [
        entry for entry in entries
        if entry["severity"].upper() in WARNING_LEVEL_SEVERITIES
    ]

    # 5. CRC_ERROR / LINK_DOWN / TICKET_ESCALATED 키워드가 포함된 주요 이벤트 요약
    key_event_matches = {label: [] for label in KEY_EVENT_KEYWORDS}
    for entry in entries:
        event_lower = entry["event"].lower()
        for label, keyword in KEY_EVENT_KEYWORDS.items():
            if keyword in event_lower:
                key_event_matches[label].append(entry)

    return {
        "total_count": total_count,
        "severity_counter": severity_counter,
        "event_counter": event_counter,
        "warning_entries": warning_entries,
        "key_event_matches": key_event_matches,
    }


def format_entry_line(entry):
    """로그 한 건을 보고서에 넣기 좋은 한 줄 문자열로 만듭니다."""
    return f"- `{entry['timestamp']}` | {entry['device']} | {entry['severity']} | {entry['event']} | {entry['message']}"


def build_markdown_report(stats):
    """분석 결과를 Markdown 문자열로 만듭니다."""
    lines = []
    lines.append("# 교육용 샘플 DCO 로그 분석 결과")
    lines.append("")
    lines.append("*이 문서는 실제 AWS 내부 로그가 아니라 교육용 샘플 로그(`sample_dco_log.txt`)를 "
                  "Python 표준 라이브러리로 분석한 결과입니다. 원인은 하나로 단정하지 않고, "
                  "로그에 나타난 내용만 정리했습니다.*")
    lines.append("")

    # 1. 전체 로그 줄 수
    lines.append("## 1. 전체 로그 줄 수")
    lines.append("")
    lines.append(f"총 {stats['total_count']}줄의 로그를 확인했습니다.")
    lines.append("")

    # 2. 심각도별 개수
    lines.append("## 2. 심각도별 개수")
    lines.append("")
    lines.append("| 심각도 | 개수 |")
    lines.append("| --- | --- |")
    for severity, count in stats["severity_counter"].most_common():
        lines.append(f"| {severity} | {count} |")
    lines.append("")

    # 3. 이벤트별 개수
    lines.append("## 3. 이벤트별 개수")
    lines.append("")
    lines.append("| 이벤트 | 개수 |")
    lines.append("| --- | --- |")
    for event, count in stats["event_counter"].most_common():
        lines.append(f"| {event} | {count} |")
    lines.append("")

    # 4. WARNING 또는 CRITICAL 로그 목록
    lines.append("## 4. WARNING 또는 CRITICAL 로그 목록")
    lines.append("")
    warning_entries = stats["warning_entries"]
    if warning_entries:
        for entry in warning_entries:
            lines.append(format_entry_line(entry))
    else:
        lines.append("WARNING 또는 CRITICAL 로그가 없습니다.")
    lines.append("")

    # 5. 주요 이벤트(CRC_ERROR / LINK_DOWN / TICKET_ESCALATED) 요약
    lines.append("## 5. 주요 이벤트 요약 (CRC_ERROR / LINK_DOWN / TICKET_ESCALATED)")
    lines.append("")
    for label, matched_entries in stats["key_event_matches"].items():
        lines.append(f"### {label}")
        lines.append("")
        if matched_entries:
            for entry in matched_entries:
                lines.append(format_entry_line(entry))
        else:
            lines.append(f"{label} 관련 로그가 없습니다.")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("> 이 요약은 교육용 시나리오 분석 연습 결과이며, 실제 장비 점검이나 "
                 "실제 네트워크 진단 결과가 아닙니다. 원인 판단이 필요한 부분은 "
                 "Escalation 필요 여부로 남기고, 사람이 다시 확인하는 것을 권장합니다.")

    return "\n".join(lines) + "\n"


def main():
    entries = load_log_entries(LOG_FILE_PATH)
    stats = analyze_entries(entries)
    report = build_markdown_report(stats)

    with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"분석 완료: 총 {stats['total_count']}줄")
    print(f"결과 파일 저장 위치: {OUTPUT_FILE_PATH}")


if __name__ == "__main__":
    main()
