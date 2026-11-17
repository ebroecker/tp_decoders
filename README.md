# tp_decoders

Kleine Python-Tools zum Dekodieren von CAN-Logfiles (.asc via [python-can](https://python-can.readthedocs.io/)):

- **ISO-TP (ISO 15765-2)**: Reassemblierung von Single- / First- / Consecutive-Frames zu vollständigen Diagnose-Telegrammen (`tp_decode.py`)
- **UDS (ISO 14229)**: Übersetzung eines zusammengesetzten Telegramms in SID / Positive / Negative Response mit NRC-Text (`uds_decode.py`)

Ergebnis ist ein einfaches Printing der REQ/RES-Telegramme direkt aus dem Log.

## Benutzung

IDs anpassen (req_id / res_id) und Logfile angeben:

```bash
python3 decode_tp_tool.py log.asc    # ISO-TP-Reassemblierung, hex output
python3 decode_uds_tool.py log.asc   # zusätzlich UDS-SID / NRC decoding
```

## Voraussetzungen

```
pip install python-can
```

## Ähnliche Open-Source-Projekte

Falls diese Minimallösung nicht reicht, gibt es etablierte Alternativen:

| Projekt | Beschreibung |
|---|---|
| [python-can-isotp](https://github.com/pylessard/python-can-isotp) | De-facto-Referenz in Python: komplette ISO-TP-State-Machine inkl. Flow Control, Block Sizes, Padding, CAN-FD |
| [python-udsoncan](https://github.com/pylessard/python-udsoncan) | UDS nach ISO 14229 in Python: sämtliche SIDs inkl. Subfunktionen und Parameter-Codierung |
| [cantools](https://github.com/cantools/cantools) | CAN-Datenbank Tools (DBC/ARXML), `cantools decode` für DBC-basierte Signale — passt gut als Zusatz für die Nutzdaten |
| [Wireshark](https://www.wireshark.org/) | UDS- und ISO-TP-Dissectoren ([UDS Filterreferenz](https://www.wireshark.org/docs/dfref/u/uds.html)); Logfiles vorher nach PCAP konvertieren |
| [SavvyCAN](https://www.savvycan.com/) | GUI-Analyse-Tool mit UDS/ISO-TP-Unterstützung |
| [uds-c (OpenXC)](https://github.com/openxc/uds-c) | UDS + OBD-II als C-Bibliothek, eher für Embedded-Ziele |
| [wireshark_doip](https://github.com/tobras/wireshark_doip) | Wireshark-Dissector für DoIP + UDS (Socket/DoIP-Logs statt raw CAN) |
