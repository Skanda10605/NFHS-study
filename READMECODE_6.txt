Code_6 NFHS5 

+ nfhs5_ir_thin.parquet --> treats impossible BMI values as issing = < 10 or ≥ 60.
this hide 904 bad BMI values.
After cleaning, we have 699,362 valid BMI numbers.

The biomarker measurements (BP, glucose, waist, Hb) are stored in the PR file, not the IR file. so had to load that in for more actual data.= IAPR7EFL.DTA
the PR file has 530 variables

nfhs5_ir_thin_clean.parquet-->
ha56 (adjusted hemoglobin) ≈ all rows available
sh305 (waist) ≈ 707k.
shb74 (glucose) ≈ 702k.
shb18s/d, shb25s/d, shb29s/d (BP readings) ≈ 699k down to 651k.
ha53 (raw Hb) ≈ 702k; ha57 (anemia level) ≈ 690k.

meaning its loaded and read properly. 

Hb non-missing: 52 → red flag. almost all Hb got dropped.

Waist non-missing: 697562 → good.

Glucose non-missing: 690636 → good.

and was porbably the problem with code_5 so I just 
Hb non-missing after scaling & cleaning: 688803
Saved with corrected Hb → nfhs5_women_biomarkers.parquet #cell 12
BMI ≥ 23, SBP ≥ 140 or DBP ≥ 90, Glucose ≥ 200 mg/dL, Waist ≥ 80 cm, Hb < 12 g/dL.

-----------------------------------------------------------------------------------------

Total women: 724,115 / All five measures present: 682,775 / Per-metric abnormality (****unweighted***):BMI 35.38%, BP 9.87%, Glucose 1.09%, Waist 37.47%, Hemoglobin 54.29%


Fully normal (strict): % among those with all 5 present: 19.03% / % among all women: 17.94%           *****FIRST RESULTS/NOT THE MAIN RESULTS ***** CELL#14

------------------------------------------------------------------------------------------------------------


Totals: 724,115 : / All five measures present: 682,775 / Per-metric abnormality (correct denominators, still unweighted):BMI: 256,165 / 699,362 → 36.63% / BP: 71,505 / 698,956 → 10.23% / Glucose: 7,924 / 690,636 → 1.15% / Waist: 271,354 / 697,562 → 38.90% Hemoglobin: 393,111 / 688,803 → 57.07%
Fully normal (strict): 129,928 → 19.03% among those with all five present.

                                                                                                           *****SECOND RESULTS/NOT THE MAIN RESULTS ***** CELL#15
--------------------------------------------------------------------------------------------------------------------------------------------------
ps: about glucose -> I am using random capillary glucose ≥ 200 mg/dL as the abnormal cutoff.

That threshold is very specific for overt diabetes but not sensitive. Many diabetics won’t cross 200 at a random time (especially if controlled or measured post-meal timing is variable).

So ~1–2% positive on a single random reading ≥200.unweighted 1.15% (later ~1.42% weighted) fits that pattern.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

*******MAIN RESULT********** (WEIGHTED) nfhs5_women_flags.parquet.



Per-metric abnormality (weighted):BMI: 37.95% / BP: 9.88% / Glucose: 1.42% / Waist: 41.04% / Hemoglobin: 57.89% / Fully normal (strict, weighted, among all five present): 18.25% / 17.01% among all women (NOT IMPORTANT)

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Top 15 co-abnormality combinations (weighted, base; among women with all five measures)

BMI+WAIST+HGB = ~12.84% → the most common cluster (nutritional/adiposity + anemia).

BMI+WAIST = ~10.66% → overweight/central adiposity without anemia.

BMI+BP+WAIST = ~2.36% and BMI+BP+WAIST+HGB = ~2.12% → cardiometabolic clusters.

All five abnormal = ~0.16% → rare.

PS:these percentages are within the 5-measures-present group. the “NONE” combo (fully normal) is not listed here but is 18.25% in the base scenario.


Rows like BMI+WAIST+HGB are common: obs 12.84%, exp 7.99%, enrichment 1.61×.

BMI+WAIST: obs 10.66% vs exp 5.82% → 1.83× (frequent and enriched).

BMI+BP+WAIST: obs 2.36% vs exp 0.61% → 3.90× (strong clustering).

Rare but tightly clustered patterns (tiny expected) show very high ratios:

All five: obs 0.16%, exp 0.01%, 13.74×.

BMI+BP+GLU+WAIST: obs 0.20%, exp ~0.01%, 22.97×.

HGB ~ 29.22% → among women with ≥1 abnormal metric (and all five present), ~29% have anemia only.

BMI+WAIST+HGB ~ 12.84% and BMI+WAIST ~ 10.66% are very common clusters.

BMI+BP+WAIST ~ 2.36%, etc.


BMI+BP+WAIST: obs 2.36% vs exp 0.61% → 3.90× more common than chance.

BMI+GLU+WAIST: 3.74×; BMI+GLU+WAIST+HGB: 2.82×.

BMI+WAIST: obs 10.66% vs exp 5.82% → 1.83×.

BMI+WAIST+HGB: 1.61×.

HGB only and NONE (fully normal) also show enrichment > 1, meaning “anemia-only” and “completely normal” occur a bit more than naïve independence predicts.

combos like WAIST+HGB (0.48×), BMI only (0.42×), WAIST only (0.47×) are less common than chance, implying these tend to co-occur with other issues instead of appearing alone.

Hb abnormal (weighted):

Base Hb<12.0: 57.89%

Liberal Hb<11.5: 45.35%
 As expected, lowering the anemia threshold to 11.5 reduces the abnormal Hb rate
Fully normal across all 5 (weighted, among all five present):

Base Hb<12.0: 18.25%

Liberal Hb<11.5: 24.25%
→ Making the Hb rule stricter (11.5) increases the share of women counted as fully normal.


BP abnormal (weighted):

Base 140/90: 9.88%

Tight 130/80: 39.11% ← much higher (as expected).

Fully normal across all 5 (weighted, among all five present):

Base with 140/90: 18.25%

Tight with 130/80: 13.11% ← fewer women count as “fully normal”  tighten BP.

Liberal Hb (11.5) lowers Hb abnormal → fully normal goes up (18.25 → 24.25).

Tight BP (130/80) raises BP abnormal a lot → fully normal goes down (18.25 → 13.11).

Doing both lands in between (17.64).


| Scenario         | BP abnormal % (w) | Hb abnormal % (w) | Fully normal % (w, all 5 present) |
| ---------------- | ----------------: | ----------------: | --------------------------------: |
| BP140/90, Hb12.0 |          **9.88** |         **57.89** |                         **18.25** |
| BP140/90, Hb11.5 |          **9.88** |         **45.35** |                         **24.25** |
| BP130/80, Hb12.0 |         **39.11** |         **57.89** |                         **13.11** |
| BP130/80, Hb11.5 |         **39.11** |         **45.35** |                         **17.64** |


Scenario: liberal_hgb (Hb<11.5)

Hb abnormal: 45.35% (down from 57.89)

Fully normal: 24.25% (up from 18.25)

Scenario: tight_bp (BP≥130/80)

BP abnormal: 39.11% (up from 9.88)

Fully normal: 13.11% (down from 18.25)

Scenario: tight_bp__liberal_hgb

BP abnormal: 39.11%, Hb abnormal: 45.35%

Fully normal: 17.64% (in-between the two single changes)


base: matches earlier (BMI 37.95, BP 9.88, GLU 1.42, Waist 41.04, HGB 57.89; fully-normal 18.25%).

bmi25: raising BMI cutoff to 25 drops BMI abnormal to 23.88%; fully-normal rises to 20.55% (others unchanged).

waist88: raising waist cutoff to 88 cm drops waist abnormal to 20.42%; fully-normal 21.68%.

bmi25__waist88: both changes → fully-normal 26.07%.

…__tight_bp: tightening BP to 130/80 with BMI25+Waist88 knocks fully-normal back down to 17.80% (BP abnormal jumps to 39.11%).

…__tight_bp__liberal_hgb: same tight BP but Hb<11.5 → fully-normal 23.81% (Hb abnormal falls to 45.35%).

liberal_hgb / tight_bp: identical to earlier runs (24.25% and 13.11% fully-normal, respectively).

These internal checks (unchanged metrics stay the same across scenarios) show the logic is wired correctly.














