#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path
from typing import Dict, Optional, List


OUTPUT_NAME = "scan_metrics_minimal.csv"


def parse_summary_metadata(csv_path: Path) -> Optional[Dict[str, float]]:
    text = csv_path.read_text(encoding="utf-8", errors="ignore")
    result: Dict[str, float] = {}

    m = re.search(r"Time of simulation\s*:\s*([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE)
    if m:
        result["duration_seconds"] = float(m.group(1))

    m = re.search(r"Amount of Points scanned\s*:\s*([0-9]+)", text, re.IGNORECASE)
    if m:
        result["total_scanned_points"] = int(m.group(1))

    m = re.search(r"Amount of Sectors\s*:\s*([0-9]+)", text, re.IGNORECASE)
    if m:
        result["sector_count"] = int(m.group(1))

    return result if result else None


def is_summary_csv(csv_path: Path) -> bool:
    try:
        head = csv_path.read_text(encoding="utf-8", errors="ignore")[:400]
    except Exception:
        return False
    return "Time of simulation" in head or "Amount of Points scanned" in head or "Amount of Sectors" in head


def parse_timeseries(csv_path: Path) -> Optional[Dict[str, float]]:
    duration = None
    sectors = None

    with csv_path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return None

        time_key = None
        sector_key = None
        for name in reader.fieldnames:
            n = name.strip().lower()
            if n == "time":
                time_key = name
            if "sektor" in n or "sector" in n:
                sector_key = name

        if time_key is None or sector_key is None:
            return None

        for row in reader:
            try:
                duration = float(str(row[time_key]).strip())
                sectors = int(float(str(row[sector_key]).strip()))
            except Exception:
                continue

    if duration is None or sectors is None:
        return None

    return {
        "duration_seconds": duration,
        "final_explored_sectors": sectors,
    }


def parse_sector_density_map(csv_path: Path) -> Dict[str, int]:
    count = 0
    with csv_path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row and any(cell.strip() for cell in row):
                count += 1
    return {"sector_count": count}


def count_points_from_pts(pts_path: Path) -> Dict[str, int]:
    with pts_path.open("r", encoding="utf-8", errors="ignore") as f:
        first = f.readline().strip()
        if re.fullmatch(r"[0-9]+", first):
            return {"total_scanned_points": int(first)}

    count = 0
    with pts_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip():
                count += 1
    return {"total_scanned_points": count}


def count_points_from_xyz(xyz_path: Path) -> Dict[str, int]:
    count = 0
    with xyz_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip():
                count += 1
    return {"total_scanned_points": count}


def merge_dicts(base: Dict, incoming: Optional[Dict]) -> Dict:
    if not incoming:
        return base
    for k, v in incoming.items():
        if k not in base or base[k] in (None, "", 0):
            base[k] = v
    return base


def find_files(input_dir: Path) -> Dict[str, Optional[Path]]:
    summary_csvs = []
    for p in input_dir.glob("*.csv"):
        if p.name == OUTPUT_NAME:
            continue
        if is_summary_csv(p):
            summary_csvs.append(p)

    timeseries_csv = input_dir / "ExploredSectorsOverTime.csv"
    if not timeseries_csv.exists():
        timeseries_csv = None

    sector_density_csv = input_dir / "SectorDensityMap.csv"
    if not sector_density_csv.exists():
        sector_density_csv = None

    pts = next((p for p in input_dir.glob("*.pts")), None)
    xyz = next((p for p in input_dir.glob("*.xyz")), None)

    return {
        "summary_csvs": summary_csvs,
        "timeseries_csv": timeseries_csv,
        "sector_density_csv": sector_density_csv,
        "pts": pts,
        "xyz": xyz,
    }


def compute_metrics(input_dir: Path) -> Optional[Dict]:
    data = {
        "run_name": input_dir.name,
        "sector_count": None,
        "explored_sectors_per_second": None,
        "total_scanned_points": None,
        "points_per_second": None,
        "duration_seconds": None,
    }

    files = find_files(input_dir)

    for p in files["summary_csvs"]:
        data = merge_dicts(data, parse_summary_metadata(p))

    if files["timeseries_csv"] is not None:
        ts = parse_timeseries(files["timeseries_csv"])
        if ts:
            data = merge_dicts(data, ts)

    if files["sector_density_csv"] is not None:
        data = merge_dicts(data, parse_sector_density_map(files["sector_density_csv"]))

    if not data.get("total_scanned_points"):
        if files["pts"] is not None:
            data = merge_dicts(data, count_points_from_pts(files["pts"]))
        elif files["xyz"] is not None:
            data = merge_dicts(data, count_points_from_xyz(files["xyz"]))

    duration = data.get("duration_seconds")
    sector_count = data.get("sector_count")
    points = data.get("total_scanned_points")

    if duration and sector_count is not None:
        data["explored_sectors_per_second"] = sector_count / duration

    if duration and points is not None:
        data["points_per_second"] = points / duration

    # Only accept directories where all final metrics can be built.
    required = [
        data.get("sector_count"),
        data.get("explored_sectors_per_second"),
        data.get("total_scanned_points"),
        data.get("points_per_second"),
    ]
    if any(v is None for v in required):
        return None

    return {
        "run_name": data["run_name"],
        "sector_count": data["sector_count"],
        "explored_sectors_per_second": data["explored_sectors_per_second"],
        "total_scanned_points": data["total_scanned_points"],
        "points_per_second": data["points_per_second"],
    }


def write_metrics_csv(target_dir: Path, metrics: Dict) -> Path:
    out_csv = target_dir / OUTPUT_NAME
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "run_name",
                "sector_count",
                "explored_sectors_per_second",
                "total_scanned_points",
                "points_per_second",
            ],
        )
        writer.writeheader()
        writer.writerow(metrics)
    return out_csv


def process_recursive(root: Path) -> List[Path]:
    written: List[Path] = []
    for current_dir in [root] + [p for p in root.rglob("*") if p.is_dir()]:
        metrics = compute_metrics(current_dir)
        if metrics is not None:
            written.append(write_metrics_csv(current_dir, metrics))
    return written


def main():
    parser = argparse.ArgumentParser(
        description="Recursively create scan_metrics_minimal.csv in every scan folder where all required files are available."
    )
    parser.add_argument("--input", required=True, help="Root directory to search recursively")
    args = parser.parse_args()

    root = Path(args.input)
    written = process_recursive(root)

    if not written:
        print("No valid scan folders found.")
        return

    print(f"Created {len(written)} CSV file(s):")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
