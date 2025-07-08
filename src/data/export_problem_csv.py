# 문제 추출 후 csv 파일로 저장

import re, csv, argparse
from pathlib import Path
from collections import defaultdict

def split_outside_quotes(s: str) -> list[str]:
    parts, buf = [], []
    in_quote = esc = False
    for ch in s:
        if ch == "\\" and in_quote and not esc:
            esc = True
            buf.append(ch)
            continue
        if ch == "'" and not esc:
            in_quote = not in_quote
        esc = False
        if ch == "," and not in_quote:
            parts.append("".join(buf))
            buf.clear()
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return parts

def unquote(val: str) -> str:
    if val == "NULL":
        return ""
    if val.startswith("'") and val.endswith("'"):
        val = val[1:-1]
    return (
        val.replace(r"\\", "\\")
           .replace(r"\'", "'")
           .replace(r'\"', '"')
           .replace(r"\n", "\n")
    )

def tuple_generator(values_clause: str):
    depth, start = 0, None
    in_quote = esc = False
    for i, ch in enumerate(values_clause):
        if ch == "\\" and in_quote and not esc:
            esc = True
            continue
        if ch == "'" and not esc:
            in_quote = not in_quote
        esc = False
        if in_quote:
            continue
        if ch == "(":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0 and start is not None:
                yield values_clause[start:i]

def load_category_map(sql: Path) -> dict[int, str]:
    m = re.compile(r"INSERT INTO `category`\s+VALUES\s+(.+);")
    mp = {}
    for line in sql.open(encoding="utf-8", errors="ignore"):
        mm = m.match(line.strip())
        if not mm:
            continue
        for tup in tuple_generator(mm.group(1)):
            cid, cname, *_ = split_outside_quotes(tup)
            mp[int(cid)] = unquote(cname)
    return mp

def load_problem_tags(sql: Path, cat_map: dict[int, str]) -> dict[int, list[str]]:
    m = re.compile(r"INSERT INTO `problem_category`\s+VALUES\s+(.+);")
    tags = defaultdict(list)
    for line in sql.open(encoding="utf-8", errors="ignore"):
        mm = m.match(line.strip())
        if not mm:
            continue
        for tup in tuple_generator(mm.group(1)):
            parts = split_outside_quotes(tup)
            # (problem_id, category_id) or (pk, problem_id, category_id)
            if len(parts) == 2:
                pid, cid = map(int, parts)
            else:
                pid, cid = int(parts[1]), int(parts[2])
            name = cat_map.get(cid)
            if name:
                tags[pid].append(name)
    return tags

def get_problem_columns(sql: Path) -> list[str]:
    cols, cap = [], False
    for line in sql.open(encoding="utf-8", errors="ignore"):
        if line.startswith("CREATE TABLE `problem`"):
            cap = True
            continue
        if cap:
            if line.startswith(")"):
                break
            m = re.match(r"\s*`([^`]+)`", line)
            if m:
                cols.append(m.group(1))
    return cols

def export(sql: Path, out_csv: Path):
    cat_map = load_category_map(sql)
    tag_map = load_problem_tags(sql, cat_map)
    p_cols  = get_problem_columns(sql)

    idx_id   = p_cols.index("id")
    idx_ttl  = p_cols.index("title")
    idx_desc = p_cols.index("description")
    idx_tier = p_cols.index("tier")

    m = re.compile(r"INSERT INTO `problem`\s+VALUES\s+(.+);")

    with sql.open(encoding="utf-8", errors="ignore") as fin, \
         out_csv.open("w", newline="", encoding="utf-8") as fout:

        wr = csv.writer(fout)
        wr.writerow(["id", "title", "description", "tier", "tags"])

        for line in fin:
            mm = m.match(line.strip())
            if not mm:
                continue
            for tup in tuple_generator(mm.group(1)):
                cols = split_outside_quotes(tup)
                pid = int(cols[idx_id])
                wr.writerow([
                    pid,
                    unquote(cols[idx_ttl]),
                    unquote(cols[idx_desc]),
                    unquote(cols[idx_tier]),
                    ",".join(sorted(tag_map.get(pid, [])))
                ])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sql", type=Path, help="MySQL dump (e.g. boj.sql)")
    ap.add_argument("-o", "--out", type=Path, default=Path("problem.csv"))
    args = ap.parse_args()

    export(args.sql, args.out)
    print(f"{args.out} 생성 완료")