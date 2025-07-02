# 카테고리 추출 후 csv 파일로 저장

import re, csv, argparse
from pathlib import Path

def split_outside_quotes(s):
    buf, parts, in_q, esc = [], [], False, False
    for ch in s:
        if ch == "\\" and in_q and not esc:  esc = True; buf.append(ch); continue
        if ch == "'"  and not esc:           in_q = not in_q
        esc = False
        if ch == "," and not in_q:           parts.append("".join(buf)); buf.clear()
        else:                                buf.append(ch)
    parts.append("".join(buf))
    return parts

def tuple_gen(values):
    depth, start, in_q, esc = 0, None, False, False
    for i,ch in enumerate(values):
        if ch == "\\" and in_q and not esc:  esc = True; continue
        if ch == "'"  and not esc:           in_q = not in_q
        esc = False
        if in_q:   continue
        if ch == "(":
            if depth == 0: start = i+1
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0: yield values[start:i]

def unq(v):
    return "" if v=="NULL" else v.strip("'").replace(r"\'","'").replace(r"\n","\n")

def export(sql: Path):
    out = Path("category.csv").open("w", newline="", encoding="utf-8")
    wr  = csv.writer(out); wr.writerow(["id","name"])
    pat = re.compile(r"INSERT INTO `category`\s+VALUES\s+(.+);")
    with sql.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = pat.match(line.strip()); 0
            if not m: continue
            for tup in tuple_gen(m.group(1)):
                cols = split_outside_quotes(tup)
                if len(cols) == 2:
                    cid, cname = cols
                else:
                    cid, cname = cols[2], cols[1]
                wr.writerow([int(cid), unq(cname)])
    out.close();  print("category.csv 생성 완료")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sql", type=Path)
    export(ap.parse_args().sql)