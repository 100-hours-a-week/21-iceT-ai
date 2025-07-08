# 문제 카테고리 병합 후 csv 파일로 저장

import csv, argparse, sys
from pathlib import Path
from collections import defaultdict

def read_category(path: Path) -> dict[int, str]:
    mp = {}
    with path.open(encoding="utf-8") as f:
        rdr = csv.reader(f)
        next(rdr, None)
        for cid, cname, *rest in rdr:
            try:
                mp[int(cid)] = cname
            except ValueError:
                continue
    return mp

def read_problem_category(path: Path) -> dict[int, list[int]]:
    rel = defaultdict(list)
    with path.open(encoding="utf-8") as f:
        rdr = csv.reader(f)
        next(rdr, None)
        for cat_id, prob_id, *rest in rdr:
            try:
                cid = int(cat_id)
                pid = int(prob_id)
                rel[pid].append(cid)
            except ValueError:
                continue
    return rel

def merge(cat_csv: Path, pc_csv: Path, prob_csv: Path, out_csv: Path):
    cat_map = read_category(cat_csv)
    rel_map = read_problem_category(pc_csv)

    with prob_csv.open(encoding="utf-8") as fin, \
         out_csv.open("w", newline="", encoding="utf-8") as fout:

        rdr = csv.DictReader(fin)
        fieldnames = rdr.fieldnames
        if "tags" not in fieldnames:
            fieldnames.append("tags")
        wr = csv.DictWriter(fout, fieldnames=fieldnames)
        wr.writeheader()

        for row in rdr:
            pid = int(row["id"])
            tag_names = [cat_map[cid] for cid in rel_map.get(pid, [])
                         if cid in cat_map]
            row["tags"] = ",".join(sorted(set(tag_names)))
            wr.writerow(row)

    print(f"{out_csv} 생성 완료")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", required=True, type=Path)
    ap.add_argument("--problem-category", required=True, type=Path)
    ap.add_argument("--problem", required=True, type=Path)
    ap.add_argument("--out", default=Path("problem_with_tags.csv"), type=Path)
    args = ap.parse_args()

    merge(args.category, args.problem_category, args.problem, args.out)