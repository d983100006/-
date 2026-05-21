#!/usr/bin/env python3
from __future__ import annotations
import csv, json, re
from pathlib import Path
from datetime import datetime, timezone

SEED=Path('data/seeds/seed_inp_papers_21.csv')
MASTER=Path('data/papers_master.csv')
NORM=Path('data/seed_records_normalized.csv')
REPORT=Path('reports/seed_import_report.md')

SIM_THRESHOLD=0.9

def norm(s:str)->str:
    return re.sub(r'\s+',' ', re.sub(r'[^a-z0-9]+',' ',(s or '').lower())).strip()

def title_sim(a,b):
    sa=set(norm(a).split()); sb=set(norm(b).split())
    if not sa or not sb: return 0.0
    return len(sa&sb)/len(sa|sb)

def main():
    rows=list(csv.DictReader(SEED.open(encoding='utf-8-sig',newline='')))
    master_rows=list(csv.DictReader(MASTER.open(encoding='utf-8',newline='')))
    fields=list(master_rows[0].keys()) if master_rows else list(csv.DictReader(MASTER.open(encoding='utf-8')).fieldnames)
    add_cols=['user_index','source_database','discovered_from','discovered_round','relevance_level','fulltext_needed','has_pdf','duplicate_flag','pdf_filename','growth_method_seed','heating_method_seed','thermal_field_material_seed','category_seed','team_seed','extra_seed_metadata']
    for c in add_cols:
        if c not in fields: fields.append(c)

    doi_seen={ (r.get('doi') or '').strip().lower() for r in master_rows if (r.get('doi') or '').strip() }
    titles=[r.get('title','') for r in master_rows]
    now=datetime.now(timezone.utc).isoformat()

    normalized=[]; imported=0; dup=0; missing_doi=0; missing_url=0; has_pdf_n=0; need_dl=0; bad=0
    for i,r in enumerate(rows, start=1):
        try:
            doi=(r.get('doi') or '').strip(); url=(r.get('url') or '').strip(); acc=(r.get('access_status') or '').strip()
            if not doi: missing_doi+=1
            if not url: missing_url+=1
            fulltext='no' if acc=='has_pdf' else 'yes' if acc=='need_download' else 'unknown'
            has_pdf='yes' if acc=='has_pdf' else 'no' if acc=='need_download' else 'unknown'
            if has_pdf=='yes': has_pdf_n+=1
            if fulltext=='yes': need_dl+=1
            dup_flag=''
            if doi and doi.lower() in doi_seen:
                dup_flag='duplicate_candidate'; dup+=1
            else:
                for t in titles:
                    if title_sim(r.get('title',''), t) >= SIM_THRESHOLD:
                        dup_flag='potential_duplicate'; dup+=1; break
            extra={k:v for k,v in r.items() if k not in {'user_index','title','authors','year','publication_type','journal_or_conference','volume','issue','pages','doi','url','pdf_filename','ris_filename','access_status','source_pdf_status','growth_method_seed','heating_method_seed','thermal_field_material_seed','category_seed','team_seed','publisher','keywords','abstract','notes'}}
            rec={k:'' for k in fields}
            rec.update({
                'record_id':f"seed_inp_{r.get('user_index',str(i)).zfill(3)}",
                'source_db':'user_seed',
                'source_database':'user_seed',
                'source_record_id':r.get('ris_filename') or r.get('user_index',''),
                'title':r.get('title',''),'authors':r.get('authors',''),'year':r.get('year',''),
                'journal_or_venue':r.get('journal_or_conference',''),'doi':doi,'url':url,
                'abstract':r.get('abstract',''),'keywords':r.get('keywords',''),'doc_type':r.get('publication_type',''),
                'candidate_topic_fit':'uncertain','inclusion_status':'pending','raw_evidence':'seed_import_csv',
                'candidate_judgement':'seed_unreviewed','confidence':'uncertain',
                'full_text_available':has_pdf,'full_text_path':r.get('pdf_filename',''),'seed_flag':'yes',
                'notes':(r.get('notes','') or ''), 'created_at':now,'updated_at':now,
                'user_index':r.get('user_index',''),'discovered_from':'user_seed','discovered_round':'0','relevance_level':'seed_unreviewed',
                'fulltext_needed':fulltext,'has_pdf':has_pdf,'duplicate_flag':dup_flag,
                'pdf_filename':r.get('pdf_filename',''),'growth_method_seed':r.get('growth_method_seed',''),'heating_method_seed':r.get('heating_method_seed',''),'thermal_field_material_seed':r.get('thermal_field_material_seed',''),'category_seed':r.get('category_seed',''),'team_seed':r.get('team_seed',''),'extra_seed_metadata':json.dumps(extra,ensure_ascii=False)
            })
            master_rows.append(rec); normalized.append(rec); imported+=1
            if doi: doi_seen.add(doi.lower())
            titles.append(r.get('title',''))
        except Exception:
            bad+=1

    with MASTER.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(master_rows)
    with NORM.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(normalized)

    REPORT.write_text(f"""# Seed Import Report

- 匯入總數: {len(rows)}
- 成功匯入數: {imported}
- 疑似重複數: {dup}
- 缺 DOI 數: {missing_doi}
- 缺 URL 數: {missing_url}
- 有 PDF 數: {has_pdf_n}
- 需要全文下載數: {need_dl}
- 無法解析的紀錄: {bad}
- 是否有修正錯誤路徑: 是（`data/data/seeds/seed_inp_papers_21.csv` → `data/seeds/seed_inp_papers_21.csv`）

## 欄位對應
- 直接對應到 `papers_master.csv`：`title, authors, year, doi, url, abstract, keywords, publication_type -> doc_type, journal_or_conference -> journal_or_venue`。
- 來源追蹤欄位：`source_database=user_seed, discovered_from=user_seed, discovered_round=0, relevance_level=seed_unreviewed`。
- `access_status` 衍生：`fulltext_needed`, `has_pdf`。
- seed metadata 保留欄位：`growth_method_seed, heating_method_seed, thermal_field_material_seed, category_seed, team_seed, pdf_filename`。
- 無法直接對應的額外欄位：序列化至 `extra_seed_metadata`（JSON 字串）。

## 清理提醒
- `data/data/` 目錄目前保留，避免誤刪其他潛在檔案。
""",encoding='utf-8')

if __name__=='__main__':
    main()
