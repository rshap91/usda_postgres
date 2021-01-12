-- CREATE VIEWS

CREATE OR REPLACE VIEW standardized_quantities AS (
    SELECT
        f.ndb_no AS food_id,
        f.long_desc AS food_name,
        fg.fdgrp_cd AS food_group_id,
        fg.fddrp_desc AS food_group,
        ndf.nutr_no AS nutrient_id,
        ndf.nutrdesc AS nutrient,
        CASE
            WHEN ndf.units = 'mg' THEN nd.nutr_val * 1000
            WHEN ndf.units = 'g' THEN nd.nutr_val * 1000000
            WHEN ndf.units = 'IU' AND ndf.nutrdesc = 'Vitamin A, IU' THEN nd.nutr_val*3.33333
            WHEN ndf.units = 'IU' AND ndf.nutrdesc = 'Vitamin D' THEN nd.nutr_val*40
            WHEN ndf.nutrdesc = 'Energy' THEN 0  -- don't have equivalence
            ELSE nd.nutr_val
        END AS nutrient_val,
        'mcg'::TEXT AS units
    FROM food_des f
    JOIN nut_data nd USING(ndb_no)
    JOIN nutr_def ndf USING(nutr_no)
    JOIN fd_group fg USING(fdgrp_cd)
    WHERE ndf.nutrdesc NOT LIKE '%%:%%'
);

CREATE OR REPLACE VIEW nutr_quantities AS (
    SELECT
        f.long_desc AS food_name,
        f.ndb_no AS food_id,
        fg.fddrp_desc AS food_group,
        fg.fdgrp_cd AS food_group_id,
        ndf.nutrdesc AS nutrient,
        ndf.nutr_no AS nutrient_id,
        nd.nutr_val AS nutrient_val,
        ndf.units AS units
    FROM food_des f
    JOIN nut_data nd USING(ndb_no)
    JOIN nutr_def ndf USING(nutr_no)
    JOIN fd_group fg USING(fdgrp_cd)
    WHERE ndf.nutrdesc NOT LIKE '%%:%%'
);
