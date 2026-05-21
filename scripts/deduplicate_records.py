#!/usr/bin/env python3
"""Flag duplicate candidates in papers_master without deleting records."""
import csv
from pathlib import Path
PAPERS=Path('data/papers_master.csv')

def main()->int:
    if not PAPERS.exists():
        print('Missing required file: data/papers_master.csv'); return 1
    rows=list(csv.DictReader(PAPERS.open(encoding='utf-8',newline='')))
    doi_seen=set(); dup=0
    for r in rows:
        doi=(r.get('doi') or '').strip().lower()
        if doi and doi in doi_seen:
            if 'duplicate' not in (r.get('duplicate_flag') or ''):
                r['duplicate_flag']='duplicate_candidate'
            dup+=1
        elif doi:
            doi_seen.add(doi)
    fields=list(rows[0].keys()) if rows else []
    if rows:
        with PAPERS.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f'duplicate candidates flagged: {dup}')
    return 0
if __name__=='__main__':
    raise SystemExit(main())
