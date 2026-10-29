#!/usr/bin/env python3
"""Reproduce packet-level counts from the archived dual-benchmark tcpdump text.

This tool deliberately reports TCP endpoints, packet records, and parser-accepted
flows. It does not infer TLS versions, cipher groups, board identities, crypto
success, watchdog state, or a handshake success rate from port numbers.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


LINE_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+)"
    r"\s+IP\s+(?P<src>\S+)\s+>\s+(?P<dst>\S+):"
    r"\s+Flags\s+\[(?P<flags>[^\]]+)\].*?\blength\s+(?P<length>\d+)"
)


def endpoint_parts(endpoint: str) -> tuple[str, str]:
    host, port = endpoint.rstrip(":").rsplit(".", 1)
    return host, port


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def audit(path: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    windows: list[dict[str, object]] = []
    flows: dict[tuple[int, str, str], dict[str, object]] = {}
    accepted: list[dict[str, object]] = []
    tuple_syns: set[tuple[str, str]] = set()
    syn_events = 0
    tcp_lines = 0
    previous_time: datetime | None = None
    window_id = 0

    with path.open("r", encoding="utf-8", errors="replace") as stream:
        for line in stream:
            match = LINE_RE.match(line)
            if not match:
                continue
            tcp_lines += 1
            timestamp = datetime.strptime(match.group("timestamp"), "%Y-%m-%d %H:%M:%S.%f")
            src, dst = match.group("src"), match.group("dst")
            flags, payload_len = match.group("flags"), int(match.group("length"))
            try:
                src_host, src_port = endpoint_parts(src)
                dst_host, dst_port = endpoint_parts(dst)
            except ValueError:
                continue

            if previous_time is None or (timestamp - previous_time).total_seconds() > 120:
                window_id += 1
                windows.append({"window_id": window_id, "first_packet": timestamp, "last_packet": timestamp})
            previous_time = timestamp
            windows[-1]["last_packet"] = timestamp

            if dst_port in {"8443", "4443"}:
                endpoint_port, client_host, client_port = dst_port, src_host, src_port
                client_endpoint = src
                server_endpoint = dst
                is_client_packet = True
            elif src_port in {"8443", "4443"}:
                endpoint_port, client_host, client_port = src_port, dst_host, dst_port
                client_endpoint = dst
                server_endpoint = src
                is_client_packet = False
            else:
                continue

            key = (window_id, endpoint_port, client_endpoint)
            if "S" in flags and "." not in flags and is_client_packet:
                syn_events += 1
                tuple_syns.add((client_endpoint, server_endpoint))
                flows[key] = {
                    "window_id": window_id,
                    "endpoint_port": endpoint_port,
                    "client_ip": client_host,
                    "client_port": client_port,
                    "first_packet": timestamp,
                    "last_packet": timestamp,
                    "first_client_payload_bytes": 0,
                    "first_server_payload_bytes": 0,
                    "client_payload_bytes": 0,
                    "server_payload_bytes": 0,
                    "response_rule_met": False,
                    "fin_seen": False,
                }

            flow = flows.get(key)
            if flow is None:
                continue
            flow["last_packet"] = timestamp
            if is_client_packet:
                flow["client_payload_bytes"] = int(flow["client_payload_bytes"]) + payload_len
                if payload_len > 0 and int(flow["first_client_payload_bytes"]) == 0:
                    flow["first_client_payload_bytes"] = payload_len
            else:
                flow["server_payload_bytes"] = int(flow["server_payload_bytes"]) + payload_len
                if payload_len > 0 and int(flow["first_server_payload_bytes"]) == 0:
                    flow["first_server_payload_bytes"] = payload_len
                if endpoint_port == "8443" and payload_len >= 1100:
                    flow["response_rule_met"] = True
                if endpoint_port == "4443" and int(flow["server_payload_bytes"]) > 500 and "F" in flags:
                    flow["response_rule_met"] = True

            if "F" in flags:
                flow["fin_seen"] = True
                if endpoint_port == "4443" and int(flow["server_payload_bytes"]) > 500:
                    flow["response_rule_met"] = True
                if flow["response_rule_met"]:
                    accepted.append(dict(flow))
                    del flows[key]

    # Match the historical parser's end-of-capture rule for port 8443 only:
    # a qualifying server payload can be retained even without a captured FIN.
    for flow in flows.values():
        if flow["endpoint_port"] == "8443" and flow["response_rule_met"]:
            accepted.append(dict(flow))

    counts_by_window = Counter((int(row["window_id"]), str(row["endpoint_port"])) for row in accepted)
    for window in windows:
        window["span_seconds"] = (window["last_packet"] - window["first_packet"]).total_seconds()
        window["port_8443_parser_accepted"] = counts_by_window[(int(window["window_id"]), "8443")]
        window["port_4443_parser_accepted"] = counts_by_window[(int(window["window_id"]), "4443")]

    metadata = {
        "input_sha256": sha256_file(path),
        "input_bytes": path.stat().st_size,
        "tcp_lines": tcp_lines,
        "client_syn_events": syn_events,
        "distinct_client_server_socket_tuples": len(tuple_syns),
        "accepted_flow_records": len(accepted),
        "port_8443_parser_accepted": sum(row["endpoint_port"] == "8443" for row in accepted),
        "port_4443_parser_accepted": sum(row["endpoint_port"] == "4443" for row in accepted),
        "windows": len(windows),
    }
    return windows, accepted, metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", nargs="?", type=Path,
                        default=Path(__file__).resolve().parents[1] / "data/raw_logs/dual_bench_8h.log")
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "docs/evidence/endurance_packet_audit")
    args = parser.parse_args()
    if not args.capture.is_file():
        parser.error(f"capture not found: {args.capture}")

    windows, accepted, metadata = audit(args.capture)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "parser_accepted_tcp_flows.csv"
    fields = ["flow_id", "window_id", "endpoint_port", "client_ip", "client_port",
              "first_packet", "last_packet", "first_client_payload_bytes",
              "first_server_payload_bytes", "client_payload_bytes", "server_payload_bytes",
              "fin_seen", "parser_rule"]
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for flow_id, row in enumerate(accepted, 1):
            endpoint = str(row["endpoint_port"])
            writer.writerow({
                "flow_id": flow_id,
                "window_id": row["window_id"],
                "endpoint_port": endpoint,
                "client_ip": row["client_ip"],
                "client_port": row["client_port"],
                "first_packet": row["first_packet"].isoformat(),
                "last_packet": row["last_packet"].isoformat(),
                "first_client_payload_bytes": row["first_client_payload_bytes"],
                "first_server_payload_bytes": row["first_server_payload_bytes"],
                "client_payload_bytes": row["client_payload_bytes"],
                "server_payload_bytes": row["server_payload_bytes"],
                "fin_seen": row["fin_seen"],
                "parser_rule": "port 8443: server TCP payload >= 1100 B; port 4443: server payload > 500 B and FIN",
            })

    report_path = args.output_dir / "audit_report.md"
    span_total = sum(float(window["span_seconds"]) for window in windows)
    with report_path.open("w", encoding="utf-8") as stream:
        stream.write("# Packet-capture audit\n\n")
        stream.write("This analysis reports packet-level observations from the supplied tcpdump text. It does not establish a cryptographic handshake, a TLS version/group, physical device identity, or an all-attempt success rate.\n\n")
        stream.write("## Provenance and reproduced counts\n\n")
        stream.write(f"- Input: `{args.capture.name}` ({metadata['input_bytes']:,} bytes), SHA-256 `{metadata['input_sha256']}`.\n")
        stream.write(f"- Parsed TCP packet lines: {metadata['tcp_lines']:,}.\n")
        stream.write(f"- Client-origin SYN events to the two service ports: {metadata['client_syn_events']:,}; distinct source/destination socket tuples among those events: {metadata['distinct_client_server_socket_tuples']:,}. Repeated SYN events are not deduplicated into attempts.\n")
        stream.write(f"- Parser-accepted flow records: {metadata['accepted_flow_records']:,}: {metadata['port_8443_parser_accepted']:,} associated with TCP port 8443 and {metadata['port_4443_parser_accepted']:,} associated with TCP port 4443.\n")
        stream.write(f"- The parser groups traffic into {metadata['windows']} windows using a gap greater than 120 seconds; the summed first-to-last packet spans are {span_total / 3600:.2f} hours. These spans are not proof of uninterrupted board uptime.\n\n")
        stream.write("## Window counts\n\n| Window | First packet | Last packet | Span (h) | Port 8443 accepted records | Port 4443 accepted records |\n|---:|---|---|---:|---:|---:|\n")
        for window in windows:
            stream.write(f"| {window['window_id']} | {window['first_packet']} | {window['last_packet']} | {float(window['span_seconds']) / 3600:.2f} | {window['port_8443_parser_accepted']} | {window['port_4443_parser_accepted']} |\n")
        stream.write("\n## Interpretation limits\n\n")
        stream.write("The historical analysis script labels port 8443 as the custom hybrid endpoint and port 4443 as Classical TLS. A later manuscript labels port 4443 as wolfSSL hybrid TLS 1.3. The packet text and this parser identify ports and payload heuristics only; they do not resolve that disagreement. Separate USB serial excerpts show small classical and hybrid TLS acquisitions, but they do not map the port-4443 endurance traffic to a negotiated TLS group or to a specific build.\n\n")
        stream.write("A parser-accepted record is not a cryptographic-success assertion. The difference between SYN events, distinct socket tuples, and parser-accepted records must not be converted into a failure rate: SYN retransmissions, parser criteria, capture gaps, and endpoint attribution are not fully resolved. Turnaround values from the historical CSV are not complete TLS handshake latency. This capture does not establish a board model/clock, watchdog behavior, heap stability, or a matched performance comparison.\n\n")
        stream.write("The generated CSV preserves accepted records with neutral port-based labels. The original supplied CSV and raw capture remain unchanged.\n")

    print(f"Raw SHA-256: {metadata['input_sha256']}")
    print(f"TCP lines: {metadata['tcp_lines']}; client SYN events: {metadata['client_syn_events']}; unique socket tuples: {metadata['distinct_client_server_socket_tuples']}")
    print(f"Parser-accepted records: {metadata['accepted_flow_records']} (8443={metadata['port_8443_parser_accepted']}, 4443={metadata['port_4443_parser_accepted']})")
    print(f"Wrote {csv_path} and {report_path}")


if __name__ == "__main__":
    main()
