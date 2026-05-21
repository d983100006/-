# Stage 3 Reference Expansion Seed Priority

## Priority Tier A（建議最優先）
> 以「可直接延展 VGF/VB 成長流程、熱場調控、近年大尺寸 InP」為優先。

1. **001** — Growth of 4-Inch InP Single-Crystal Wafer Using the VGF-VB Technique（core_growth_experiment）
2. **006** — interface shape optimization + dislocation suppression（core_growth_experiment）
3. **007** — VGF-VB stage switched growth（core_growth_experiment）
4. **003** — temperature field + melt convection（simulation_or_thermal_model）
5. **002** — cooling rate impact on VGF-InP（core_growth_experiment）
6. **020** — cooling crystallization temperature control model（simulation_or_thermal_model）
7. **004** — heater design optimization for VGF grower（simulation_or_thermal_model）
8. **005** — MCVGF modelling approach（simulation_or_thermal_model）

## Priority Tier B（次優先，補歷史與品質鏈結）
1. **011** — large diameter low-defect VGF（core_growth_experiment）
2. **012** — dynamic gradient freeze growth（core_growth_experiment）
3. **017** — S-doped InP by VGF（core_growth_experiment）
4. **015** — low EPD substrate growth + characterization（characterization_or_downstream_analysis）
5. **016** — photoluminescence topography（characterization_or_downstream_analysis）
6. **013** — VGF growth and characterization of InP/GaAs（characterization_or_downstream_analysis）
7. **009** — LEC/VCZ/VB growth and characterization（characterization_or_downstream_analysis）
8. **010** — Fe-doped substrate by VB（core_growth_experiment）
9. **008** — 6-inch substrate growth and wafer processing（characterization_or_downstream_analysis）

## Priority Tier C（專軌或待補件）
1. **021** — thermal field with SSC/CZ（simulation_or_thermal_model；method differs from VGF mainline）
2. **019** — in-situ synthesis track（polycrystal_or_in_situ_synthesis）
3. **018** — book chapter/review context（review_or_book_chapter）
4. **014** — hold for fulltext review（uncertain；缺 PDF）

## 使用建議（對應 Stage 2.5 action）
- Tier A：優先作為 `use_as_primary_reference_expansion_seed` 或 `use_for_thermal_field_track`。
- Tier B：優先作為 `use_as_secondary_reference_expansion_seed`。
- Tier C：依軌道分派（polycrystal/thermal/review）或待全文補齊後再進一步處理。
