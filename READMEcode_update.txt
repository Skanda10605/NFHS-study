updated our code and regenerated the outputs. 

What changed : 

Glucose classification now follows the NFHS rule: 
Fasting ≥ 126 mg/dL, Non-fasting ≥ 220 mg/dL (using PR fasting/drinking hours to decide).

Recomputed all five abnormality flags and the “healthy” control (= women normal on all five among those with all five measures).

Instead of an arbitrary “top-10”, we now pick common co-morbidities (CCMs) using a principled rule:

include every combo with weighted prevalence ≥ 1%, then keep combos until we cover about 85% cumulative.

With this run the set is: HGB, BMI+WAIST+HGB, BMI+WAIST, WAIST+HGB, WAIST.

Figures (each with two controls: “All women” and “Healthy (all 5 normal)”):
wealth_<combo>_with_controls.png
education_<combo>_with_controls.png

Tables feeding the plots:
ccm_selected_weighted.csv (the chosen CCMs, with coverage)
ccm_all_combos_weighted.csv (full combo prevalence)
ccm_by_wealth.csv and ccm_by_education.csv (group-wise, weighted %)

also 
Wealth gradient: BMI and Waist abnormalities rise from poorest → richest; HGB abnormality falls with wealth; BP increases modestly.
Education: BP abnormality drops with higher education; HGB abnormality is lowest in higher education; BMI/Waist are a bit higher in the “Higher” group than “Secondary.”
Glucose (with the NFHS fasting/non-fasting thresholds) sits around ~1% and is relatively flat across groups (small bars by design).