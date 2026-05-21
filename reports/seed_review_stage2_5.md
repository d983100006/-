# Stage 2.5 Seed 文獻複核與初步分流

> 範圍限制：僅使用 `papers_master.csv` 的 `title`, `journal_or_venue`, `doc_type`, `keywords` 與 seed metadata（`team_seed`, `category_seed` 等）進行初步分流；不做最終技術結論。

## 分類結果（21 筆）

| user_index | title | year | team_seed | category_seed | proposed_seed_role | reason_based_on_title_or_seed_metadata | recommended_next_action |
|---|---|---:|---|---|---|---|---|
| 001 | Growth of 4-Inch InP Single-Crystal Wafer Using the VGF-VB Technique | 2025 | 雲南 | 長晶+模擬 | core_growth_experiment | 標題直接描述 4 吋 InP 晶體成長與 VGF-VB 製程，且 seed 類別含「長晶」。 | use_as_primary_reference_expansion_seed |
| 002 | The impact of cooling rate on the structure and properties of VGF-InP single crystals | 2025 | 雲南 | 長晶 | core_growth_experiment | 標題聚焦 VGF-InP 單晶之冷卻速率對結構/性質影響，屬成長實驗後的工藝變因研究。 | use_as_primary_reference_expansion_seed |
| 003 | Regulation of the Temperature Field and Evolution of the Melt Convection Field During InP Crystal Growth with the Vertical Gradient Freeze Method | 2023 | 中電科 46 所 | 模擬 | simulation_or_thermal_model | 標題與 keywords（heat transfer, numerical simulation）明確指出溫場/熔體對流的數值模擬方向。 | use_for_thermal_field_track |
| 004 | Design and optimization of complex single heater for vertical gradient freeze (VGF) grower | 2023 | 勤益科大 | 模擬 | simulation_or_thermal_model | 標題強調加熱器設計與優化，屬熱場/設備建模與優化取向。 | use_for_thermal_field_track |
| 005 | Melt-conditioned vertical gradient freeze (MCVGF) to increase growth speed and process efficiency: a modelling approach | 2023 | 勤益科大 | 模擬 | simulation_or_thermal_model | 標題明示「a modelling approach」，偏向流程與熱-流場模型分析。 | use_for_thermal_field_track |
| 006 | A study on solid–liquid interface shape optimization and dislocation suppression for 4.5-inch InP single crystal growth based on vertical gradient freezing technique | 2026 | 雲南 | 長晶+模擬 | core_growth_experiment | 標題同時涉及介面形貌優化與位錯抑制，與大尺寸成長工藝高度相關；seed 類別為長晶+模擬。 | use_as_primary_reference_expansion_seed |
| 007 | VGF–VB stage switched growth process for 4.5 inch InP single crystals with low dislocation density and high uniformity | 2026 | 雲南 | 長晶 | core_growth_experiment | 標題明確是階段切換成長流程與晶體品質（低位錯、高均勻）之工藝實作。 | use_as_primary_reference_expansion_seed |
| 008 | Crystal growth and wafer processing of 6-inch Indium Phosphide substrate | 2016 | Sumitomo |  | characterization_or_downstream_analysis | 標題同時含晶體成長與晶圓加工（wafer processing），偏向製程與後段處理串接。 | use_as_secondary_reference_expansion_seed |
| 009 | Growth and characterization of LEC, VCZ and VB InP single crystals | 2004 | Sumitomo |  | characterization_or_downstream_analysis | 標題含多種成長法比較與 characterization，較接近對照/表徵型彙整。 | use_as_secondary_reference_expansion_seed |
| 010 | 4-inch Fe-doped InP substrates manufactured using vertical boat technique | 2003 | Sumitomo |  | core_growth_experiment | 標題為特定摻雜基板之製造（manufactured）與 VB 工藝，偏成長製程實作。 | use_as_secondary_reference_expansion_seed |
| 011 | Vertical gradient freeze growth of large diameter, low defect density indium phosphide | 1987 | AT&T／Bell Labs |  | core_growth_experiment | 標題聚焦 VGF 大尺寸低缺陷密度成長，屬早期核心成長實驗脈絡。 | use_as_secondary_reference_expansion_seed |
| 012 | The dynamic gradient freeze growth of InP | 1989 | AT&T／Bell Labs |  | core_growth_experiment | 標題直接指向 dynamic gradient freeze 成長方法本身，屬工藝路徑關鍵節點。 | use_as_secondary_reference_expansion_seed |
| 013 | Growth of 2" InP and GaAs crystals by the vertical gradient freeze (VGF) technique and characterization | 1996 | Erlangen、Freiberger、G. Muller、U. Sahr |  | characterization_or_downstream_analysis | 標題同時含 growth 與 characterization，且跨 InP/GaAs；可作工藝與品質連結參考。 | use_as_secondary_reference_expansion_seed |
| 014 | Growth and characterization of 2 in InP crystals by the vertical gradient freeze technique | 1994 |  |  | uncertain | 雖屬 growth+characterization，但 metadata 顯示 `has_pdf=no`、`fulltext_needed=yes`，資訊完整度不足。 | hold_until_fulltext_review |
| 015 | Growth and characterization of 2" and 4" low EPD InP substrate crystals by the Vertical Gradient Freeze (VGF)-method | 2005 | Erlangen、Freiberger、G. Muller、U. Sahr |  | characterization_or_downstream_analysis | 標題關注低 EPD 基板之成長與表徵，偏品質驗證與結果分析。 | use_as_secondary_reference_expansion_seed |
| 016 | Photoluminescence topography of sulfur doped 2" InP grown by the vertical gradient freeze technique | 2002 | Erlangen、Freiberger、G. Muller、U. Sahr |  | characterization_or_downstream_analysis | 標題主軸為 photoluminescence topography，屬典型表徵/下游分析文獻。 | use_as_secondary_reference_expansion_seed |
| 017 | Growth of S-doped 2" InP-crystals by the vertical gradient freeze technique | 2001 | Erlangen、Freiberger、G. Muller、U. Sahr |  | core_growth_experiment | 標題核心為 S 摻雜 InP 的 VGF 成長，為具體成長工藝實作。 | use_as_secondary_reference_expansion_seed |
| 018 | Recent Technologies in InP Bulk Crystals | 2000 | 專書 | 專書 | review_or_book_chapter | `doc_type=CHAP` 且 seed metadata 註記專書，屬回顧/章節型資料。 | use_as_secondary_reference_expansion_seed |
| 019 | In-situ synthesis and growth of indium phosphide | 1983 | Varian Associates |  | polycrystal_or_in_situ_synthesis | 標題明確含 in-situ synthesis，優先歸入原位合成/多晶前驅相關軌。 | use_for_polycrystal_synthesis_track |
| 020 | Indium phosphide single crystal furnace cooling crystallization temperature control model research | 2024 | 雲南 |  | simulation_or_thermal_model | 標題包含 temperature control model research，偏熱場/控溫模型研究。 | use_for_thermal_field_track |
| 021 | Thermal field of 6-inch indium phosphide single crystal growth by semi-sealed Czochralski method | 2023 | 中電科 13所 |  | simulation_or_thermal_model | 標題直接聚焦 thermal field，雖成長法為 SSC/CZ，但仍屬熱場模型/分析方向。 | use_for_thermal_field_track |

## 備註
- 本分流僅為 Stage 2.5 seed-level triage，不涉及全文驗證與最終納入判定。
- `heating_method_seed` 僅保留作 seed metadata 參考，未用作最終 heating method 判斷。
