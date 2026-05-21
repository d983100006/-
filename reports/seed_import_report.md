# Seed Import Report

- 匯入總數: 21
- 成功匯入數: 21
- 疑似重複數: 0
- 缺 DOI 數: 4
- 缺 URL 數: 3
- 有 PDF 數: 20
- 需要全文下載數: 1
- 無法解析的紀錄: 0
- 是否有修正錯誤路徑: 是（`data/data/seeds/seed_inp_papers_21.csv` → `data/seeds/seed_inp_papers_21.csv`）

## 欄位對應
- 直接對應到 `papers_master.csv`：`title, authors, year, doi, url, abstract, keywords, publication_type -> doc_type, journal_or_conference -> journal_or_venue`。
- 來源追蹤欄位：`source_database=user_seed, discovered_from=user_seed, discovered_round=0, relevance_level=seed_unreviewed`。
- `access_status` 衍生：`fulltext_needed`, `has_pdf`。
- seed metadata 保留欄位：`growth_method_seed, heating_method_seed, thermal_field_material_seed, category_seed, team_seed, pdf_filename`。
- 無法直接對應的額外欄位：序列化至 `extra_seed_metadata`（JSON 字串）。

## 清理提醒
- `data/data/` 目錄目前保留，避免誤刪其他潛在檔案。
