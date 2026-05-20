# Stage 1.5 Internal Schema Audit

> Scope: internal repository audit only. No external search, no technical conclusions.

## 1) `data/papers_master.csv` 欄位清單

Header:
`record_id,source_db,source_record_id,title,authors,year,journal_or_venue,doi,url,abstract,keywords,doc_type,candidate_topic_fit,inclusion_status,exclusion_reason,raw_evidence,candidate_judgement,confidence,full_text_available,full_text_path,seed_flag,notes,created_at,updated_at`

欄位用途：
- `record_id`: 本 repo 內唯一主鍵。
- `source_db`: 來源資料庫名稱（匯入來源）。
- `source_record_id`: 來源資料庫原始 ID。
- `title`: 題名。
- `authors`: 作者字串。
- `year`: 年份。
- `journal_or_venue`: 期刊/會議/出版場域。
- `doi`: DOI。
- `url`: 紀錄 URL。
- `abstract`: 摘要文字（若有）。
- `keywords`: 關鍵字。
- `doc_type`: 文件類型。
- `candidate_topic_fit`: 候選相關性描述（Stage 1 候選層級）。
- `inclusion_status`: 收錄狀態。
- `exclusion_reason`: 排除原因（若排除）。
- `raw_evidence`: 原始證據片段/指標。
- `candidate_judgement`: 候選判斷。
- `confidence`: 判斷信心。
- `full_text_available`: 是否有全文可用。
- `full_text_path`: 全文檔案路徑（若有）。
- `seed_flag`: 是否 seed 紀錄。
- `notes`: 備註。
- `created_at`: 建立時間。
- `updated_at`: 更新時間。

## 2) `data/patents_master.csv` 欄位清單

Header:
`record_id,source_db,source_record_id,patent_number,application_number,title,assignee,inventors,priority_date,publication_date,jurisdiction,url,abstract,claims_excerpt,keywords,candidate_topic_fit,inclusion_status,exclusion_reason,raw_evidence,candidate_judgement,confidence,full_text_available,full_text_path,seed_flag,notes,created_at,updated_at`

欄位用途：
- `record_id`: 本 repo 內唯一主鍵。
- `source_db`: 來源資料庫名稱。
- `source_record_id`: 來源庫原始 ID。
- `patent_number`: 專利公報號。
- `application_number`: 申請號。
- `title`: 專利標題。
- `assignee`: 權利人。
- `inventors`: 發明人。
- `priority_date`: 優先權日。
- `publication_date`: 公開日。
- `jurisdiction`: 法域。
- `url`: 紀錄 URL。
- `abstract`: 摘要。
- `claims_excerpt`: 權利項摘錄。
- `keywords`: 關鍵字。
- `candidate_topic_fit`: 候選相關性描述。
- `inclusion_status`: 收錄狀態。
- `exclusion_reason`: 排除原因。
- `raw_evidence`: 原始證據片段。
- `candidate_judgement`: 候選判斷。
- `confidence`: 信心標記。
- `full_text_available`: 是否可得全文。
- `full_text_path`: 全文路徑。
- `seed_flag`: 是否 seed。
- `notes`: 備註。
- `created_at`: 建立時間。
- `updated_at`: 更新時間。

## 3) `data/references_edges.csv` 欄位清單

Header:
`edge_id,from_record_id,to_record_id,to_raw_citation_text,relation_type,source_stage,confidence,notes,created_at`

欄位用途：
- `edge_id`: 關係邊唯一 ID。
- `from_record_id`: 引用來源紀錄 ID。
- `to_record_id`: 被引用目標紀錄 ID（可先空待對應）。
- `to_raw_citation_text`: 原始引用文字。
- `relation_type`: 關係型態（例如 cites/refers）。
- `source_stage`: 關係建立階段。
- `confidence`: 連結信心。
- `notes`: 備註。
- `created_at`: 建立時間。

## 4) `data/excluded_records.csv` 欄位清單

Header:
`exclusion_id,record_type,record_id,title,source_db,exclusion_stage,exclusion_reason,raw_evidence,candidate_judgement,confidence,reviewer,created_at`

欄位用途：
- `exclusion_id`: 排除事件 ID。
- `record_type`: 紀錄類型（paper/patent 等）。
- `record_id`: 被排除紀錄 ID。
- `title`: 被排除題名。
- `source_db`: 來源資料庫。
- `exclusion_stage`: 執行排除的階段。
- `exclusion_reason`: 排除原因。
- `raw_evidence`: 排除依據之原始證據。
- `candidate_judgement`: 排除判斷描述。
- `confidence`: 判斷信心。
- `reviewer`: 執行者。
- `created_at`: 建立時間。

## 5) `AGENTS.md` 規則摘要

- Stage 1 目標以 **recall > precision** 為優先。
- 不可太早排除候選。
- 不可宣稱已讀全文，除非確實取得並閱讀全文。
- 不可用常識替代證據。
- 每個判斷都要保留：`raw evidence`、`candidate judgement`、`confidence`。
- `heating_method` 僅允許：`induction` / `resistance` / `mixed` / `unclear` / `not_applicable`。
- 證據不足時一律標記 `uncertain`。
- 目前任務限制：僅 Stage 1 repository setup；不得外部搜尋；不得做技術結論。

## 6) `docs/search_queries.md` 摘要

- 目標：最大化召回 InP bulk single crystal growth 與 polycrystalline InP synthesis 候選紀錄。
- 原則：先廣後窄、納入同義詞、分 papers/patents query 版本、追蹤 query 版本與來源 DB。
- concept buckets：材料詞、單晶詞、多晶詞、製程控制詞。
- query logging template 欄位：query_id、target database、query string、date、filters、results count、notes。
- citation expansion 流程：seed 匯出 references → 正規化 → 映射既有紀錄 → 缺漏則新增候選。

## 7) `scripts/` 目前哪些是 TODO

- `scripts/import_bibtex.py`: **TODO/骨架**。僅檢查輸入檔存在與可寫入 CSV，尚未實作 BibTeX 解析與匯入。
- `scripts/import_ris.py`: **TODO/骨架**。僅檢查輸入檔存在與可寫入 CSV，尚未實作 RIS 解析與匯入。
- `scripts/deduplicate_records.py`: **TODO/骨架**。明確標註待做 normalize、exact/fuzzy dedup、canonical 選擇、寫入 excluded_records。
- `scripts/build_reports.py`: **可實際使用（基礎）**。可讀取 papers/patents 並輸出 `reports/stage_summary.md` 計數摘要；屬 Stage 1 skeleton 報表功能。
