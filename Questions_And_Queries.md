

```python
import pandas as pd
# import psycopg2 as pg
from sqlalchemy import create_engine, exc

import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline

sns.set_style('darkgrid')
plt.rcParams['figure.figsize'] = (16,12)
pd.options.display.float_format = lambda x : '{:,.2f}'.format(x)
pd.options.display.max_columns = 30
```


```python
# changes these as needed
host='0.0.0.0'
port=5432
dbname='usda'
user='rick.shapiro'
password=''

eng = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")



```

## Intro and Exploration

___Basic Selection___

How many different foods are in the db? How many food groups?


```python
df = pd.read_sql('''
SELECT 
    COUNT(DISTINCT ndb_no) n_foods, 
    COUNT(DISTINCT fdgrp_cd) n_fgroups
FROM food_des FULL OUTER JOIN fd_group
USING(fdgrp_cd);
''', eng)

df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>n_foods</th>
      <th>n_fgroups</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7146</td>
      <td>24</td>
    </tr>
  </tbody>
</table>
</div>



__Joins__

Which food groups have the most types of food?


```python
df = pd.read_sql('''
SELECT 
    fddrp_desc f_group, 
    COUNT(DISTINCT ndb_no) n_foods
FROM food_des 
FULL OUTER JOIN fd_group USING(fdgrp_cd)
GROUP BY 1
ORDER BY 2 DESC
;
''', eng)

df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>f_group</th>
      <th>n_foods</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Vegetables and Vegetable Products</td>
      <td>788</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Beef Products</td>
      <td>782</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Baked Products</td>
      <td>523</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Breakfast Cereals</td>
      <td>403</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Soups, Sauces, and Gravies</td>
      <td>394</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Poultry Products</td>
      <td>346</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Lamb, Veal, and Game Products</td>
      <td>343</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Sweets</td>
      <td>325</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Fruits and Fruit Juices</td>
      <td>306</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Baby Foods</td>
      <td>293</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Fast Foods</td>
      <td>285</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Beverages</td>
      <td>264</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Finfish and Shellfish Products</td>
      <td>255</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Fats and Oils</td>
      <td>236</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Legumes and Legume Products</td>
      <td>233</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Sausages and Luncheon Meats</td>
      <td>232</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Pork Products</td>
      <td>222</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Dairy and Egg Products</td>
      <td>216</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Cereal Grains and Pasta</td>
      <td>169</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Meals, Entrees, and Sidedishes</td>
      <td>138</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Nut and Seed Products</td>
      <td>128</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Snacks</td>
      <td>118</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Ethnic Foods</td>
      <td>89</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Spices and Herbs</td>
      <td>58</td>
    </tr>
  </tbody>
</table>
</div>



___Subqueries___

Are any foods in multiple food groups?


```python
df = pd.read_sql('''
SELECT DISTINCT n_food_group distinct_num_food_groups FROM (
    SELECT 
        long_desc food_name,
        COUNT(DISTINCT fdgrp_cd) n_food_group
    FROM food_des 
    FULL OUTER JOIN fd_group USING(fdgrp_cd)
    GROUP BY 1
) ct_groups
;
''', eng)

# each food in 1 food group only
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>distinct_num_food_groups</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



### Nutritional Data

What's the average _number_ of nutrients measured for each food?


```python
df = pd.read_sql("""
    SELECT 
        AVG(n_nutr) AS avg_num_nutrients_measured_per_food,
        MIN(n_nutr) AS min_num_nutrients_measured_per_food,
        MAX(n_nutr) AS max_num_nutrients_measured_per_food
    FROM (
        SELECT fd.long_desc, COUNT(DISTINCT ndf.nutrdesc) n_nutr
        FROM food_des fd 
        LEFT JOIN nut_data USING (ndb_no)
        JOIN nutr_def ndf USING (nutr_no)
        WHERE ndf.nutrdesc NOT LIKE '%%:%%'
        GROUP BY 1
    ) n_measured
    
""", eng)
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>avg_num_nutrients_measured_per_food</th>
      <th>min_num_nutrients_measured_per_food</th>
      <th>max_num_nutrients_measured_per_food</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>28.23</td>
      <td>1</td>
      <td>83</td>
    </tr>
  </tbody>
</table>
</div>



___Slightly more complex joins___

Which food(s) had only 1 nutrient measured?


```python
df = pd.read_sql("""
    SELECT 
        fd.long_desc food, 
        ndf.nutrdesc nutrient, 
        nd.nutr_val nutrient_val, 
        ndf.units units
    FROM food_des fd 
    JOIN nut_data nd USING (ndb_no)
    JOIN nutr_def ndf USING (nutr_no)
    RIGHT JOIN (
        SELECT long_desc, COUNT(DISTINCT nutrdesc) n_nutr
        FROM food_des
        LEFT JOIN nut_data USING (ndb_no)
        JOIN nutr_def USING (nutr_no)
        WHERE nutrdesc NOT LIKE '%%:%%'
        GROUP BY 1
        HAVING COUNT(DISTINCT nutrdesc) = 1
    ) lonely_nutrients USING(long_desc)
    """, eng)

df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>food</th>
      <th>nutrient</th>
      <th>nutrient_val</th>
      <th>units</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Candies, NESTLE, CHUNKY Bar</td>
      <td>Carbohydrate, by difference</td>
      <td>57.10</td>
      <td>g</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Candies, NESTLE, DEMET'S TURTLES Candy</td>
      <td>Carbohydrate, by difference</td>
      <td>58.00</td>
      <td>g</td>
    </tr>
  </tbody>
</table>
</div>



___Case Statements___

Make views for easier querying


```python
# These return nothing and THROW AN ERROR because of pandas but they do work! 

# Make a view for standardized (to mcg) unit measurements
try:
    pd.read_sql("""
        CREATE OR REPLACE VIEW standardized_quantities AS (
            SELECT 
                f.long_desc AS food_name, 
                fg.fddrp_desc AS food_group, 
                ndf.nutrdesc AS nutrient,
                -- convert to same measurment units
                CASE
                    WHEN ndf.units = 'mg' THEN nd.nutr_val * 1000 
                    WHEN ndf.units = 'g' THEN nd.nutr_val * 1000000
                    WHEN ndf.units = 'IU' AND ndf.nutrdesc = 'Vitamin A, IU' THEN nd.nutr_val*3.33333
                    WHEN ndf.units = 'IU' AND ndf.nutrdesc = 'Vitamin D' THEN nd.nutr_val*40
                    WHEN ndf.nutrdesc = 'Energy' THEN 0  -- don't have equivalence
                    ELSE nd.nutr_val
                END AS nutrient_val,
                'mcg' AS units
            FROM food_des f
            JOIN nut_data nd USING(ndb_no)
            JOIN nutr_def ndf USING(nutr_no)
            JOIN fd_group fg USING(fdgrp_cd)
            WHERE ndf.nutrdesc NOT LIKE '%%:%%'
        )
    """, eng)
except exc.ResourceClosedError:
    pass

df = pd.read_sql('SELECT * FROM standardized_quantities', eng)
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>food_name</th>
      <th>food_group</th>
      <th>nutrient</th>
      <th>nutrient_val</th>
      <th>units</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Butter, salted</td>
      <td>Dairy and Egg Products</td>
      <td>Carbohydrate, by difference</td>
      <td>60,000.00</td>
      <td>mcg</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Butter, salted</td>
      <td>Dairy and Egg Products</td>
      <td>Energy</td>
      <td>0.00</td>
      <td>mcg</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Butter, salted</td>
      <td>Dairy and Egg Products</td>
      <td>Caffeine</td>
      <td>0.00</td>
      <td>mcg</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Butter, salted</td>
      <td>Dairy and Egg Products</td>
      <td>Theobromine</td>
      <td>0.00</td>
      <td>mcg</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Butter, salted</td>
      <td>Dairy and Egg Products</td>
      <td>Sugars, total</td>
      <td>60,000.00</td>
      <td>mcg</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Make a view for default (unstandardized) measurements per food-nutrient
try:
    pd.read_sql("""
        CREATE OR REPLACE VIEW nutr_quantities AS (
            SELECT 
                f.long_desc AS food_name, 
                fg.fddrp_desc AS food_group, 
                ndf.nutrdesc AS nutrient,
                nd.nutr_val AS nutrient_val,
                ndf.units AS units
            FROM food_des f
            JOIN nut_data nd USING(ndb_no)
            JOIN nutr_def ndf USING(nutr_no)
            JOIN fd_group fg USING(fdgrp_cd)
            WHERE ndf.nutrdesc NOT LIKE '%%:%%'
        )
    """, eng)
except exc.ResourceClosedError:
    pass

df = pd.read_sql('SELECT * FROM nutr_quantities', eng)
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>food_name</th>
      <th>food_group</th>
      <th>nutrient</th>
      <th>nutrient_val</th>
      <th>units</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Butter, salted</td>
      <td>Dairy and Egg Products</td>
      <td>Carbohydrate, by difference</td>
      <td>0.06</td>
      <td>g</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Butter, salted</td>
      <td>Dairy and Egg Products</td>
      <td>Energy</td>
      <td>717.00</td>
      <td>kcal</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Butter, salted</td>
      <td>Dairy and Egg Products</td>
      <td>Caffeine</td>
      <td>0.00</td>
      <td>mg</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Butter, salted</td>
      <td>Dairy and Egg Products</td>
      <td>Theobromine</td>
      <td>0.00</td>
      <td>mg</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Butter, salted</td>
      <td>Dairy and Egg Products</td>
      <td>Sugars, total</td>
      <td>0.06</td>
      <td>g</td>
    </tr>
  </tbody>
</table>
</div>



Which foods have the most 

    - Alcohol
    - Caffiene
    - Lactose
    - Potassium
    - Sodium
    - Sugars, total
    - Tryptophan


___Window Functions___


```python
df = pd.read_sql(""" 
   SELECT nutrient, food_name, nutrient_val, units FROM (
       SELECT 
           nutrient, 
           food_name, 
           nutrient_val, 
           units,
           MAX(nutrient_val) OVER (PARTITION BY nutrient) max_val
        FROM nutr_quantities
   ) mvals
   WHERE nutrient_val = max_val
   AND nutrient IN ('Alcohol, ethyl', 'Caffeine', 'Lactose', 'Potassium, K', 'Sodium, NA', 'Sugars, total', 'Tryptophan');
   
""", eng)
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>nutrient</th>
      <th>food_name</th>
      <th>nutrient_val</th>
      <th>units</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Alcohol, ethyl</td>
      <td>Alcoholic beverage, martini, prepared-from-recipe</td>
      <td>33.90</td>
      <td>g</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Caffeine</td>
      <td>Tea, instant, unsweetened, powder</td>
      <td>3,680.00</td>
      <td>mg</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Lactose</td>
      <td>Infant formula, MEAD JOHNSON, ENFAMIL, low iro...</td>
      <td>56.00</td>
      <td>g</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Lactose</td>
      <td>Infant formula, MEAD JOHNSON, ENFAMIL, with ir...</td>
      <td>56.00</td>
      <td>g</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Lactose</td>
      <td>Infant formula, MEAD JOHNSON, ENFAMIL, PROSOBE...</td>
      <td>56.00</td>
      <td>g</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Lactose</td>
      <td>Infant formula, MEAD JOHNSON, ENFAMIL LIPIL, l...</td>
      <td>56.00</td>
      <td>g</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Lactose</td>
      <td>Infant formula, MEAD JOHNSON, ENFAMIL LIPIL, w...</td>
      <td>56.00</td>
      <td>g</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Potassium, K</td>
      <td>Tea, instant, unsweetened, powder, decaffeinated</td>
      <td>6,040.00</td>
      <td>mg</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Potassium, K</td>
      <td>Tea, instant, unsweetened, powder</td>
      <td>6,040.00</td>
      <td>mg</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Sugars, total</td>
      <td>Sugars, granulated</td>
      <td>99.91</td>
      <td>g</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Tryptophan</td>
      <td>Soy protein isolate, PROTEIN TECHNOLOGIES INTE...</td>
      <td>1.10</td>
      <td>g</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Tryptophan</td>
      <td>Soy protein isolate, PROTEIN TECHNOLOGIES INTE...</td>
      <td>1.10</td>
      <td>g</td>
    </tr>
  </tbody>
</table>
</div>



Assuming all nutrients equal, which foods have the most nutritional value?


```python
# Using recommended nutritional values from here: 'https://www.netrition.com/rdi_page.html'
nutrient_recs = pd.read_html('https://www.netrition.com/rdi_page.html')[1]\
                  .set_axis(['nutrient', 'units', 'recommended_daily_value'], 1, inplace=False)\
                  .drop(0)\
                  .assign(recommended_daily_value=lambda f: f.recommended_daily_value.astype(float))\
                  .reset_index(drop=True)\
                  .sort_values('nutrient')
                    
# For mapping nutrients to the names in db
name_map = {
    'Calcium' : 'Calcium, Ca',
    'Copper' : 'Copper, Cu',
    'Folate' : 'Folate, total',
    'Iron': 'Iron, Fe',
    'Magnesium' : 'Magnesium, Mg',
    'Manganese' : 'Manganese, Mn',
    'Niacin' : 'Niacin',
    'Pantothenic acid' : 'Pantothenic acid',
    'Phosphorus' : 'Phosphorus, P',
    'Riboflavin' : 'Riboflavin',
    'Selenium' : 'Selenium, Se',
    'Thiamin' : 'Thiamin',
    'Vitamin A' : 'Vitamin A, IU', 
    'Vitamin B12' : 'Vitamin B-12',
    'Vitamin B6' : 'Vitamin B-6',
    'Vitamin C' : 'Vitamin C, total ascorbic acid',
    'Vitamin D' : 'Vitamin D',
    'Vitamin E' : 'Vitamin E (alpha-tocopherol)',
    'Vitamin K' : 'Vitamin K (phylloquinone)',
    'Zinc' : 'Zinc, Zn'
}

# for standardizing values (converting to micrograms)
value_map = {
    'micrograms (µg)' : 1, 
    'milligrams (mg)' : 1000, 
    'International Unit (IU)' : 3.333
}

# rename nutrients
nutrient_recs['nutrient'] = nutrient_recs.nutrient.map(lambda n: name_map[n] if n in name_map else n)
# create standard values in micrograms
nutrient_recs['recommended_daily_value_mcg'] = nutrient_recs.recommended_daily_value \
                                                            * nutrient_recs.units.map(value_map)

# store a list of all nutrients for later use
nutrients = nutrient_recs.nutrient.values

# make sql table
nutrient_recs.to_sql('daily_dose', eng, if_exists='replace')
nutrient_recs
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>nutrient</th>
      <th>units</th>
      <th>recommended_daily_value</th>
      <th>recommended_daily_value_mcg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>13</th>
      <td>Biotin</td>
      <td>micrograms (µg)</td>
      <td>300.00</td>
      <td>300.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Calcium, Ca</td>
      <td>milligrams (mg)</td>
      <td>1,000.00</td>
      <td>1,000,000.00</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Chloride</td>
      <td>milligrams (mg)</td>
      <td>3,400.00</td>
      <td>3,400,000.00</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Chromium</td>
      <td>micrograms (µg)</td>
      <td>120.00</td>
      <td>120.00</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Copper, Cu</td>
      <td>milligrams (mg)</td>
      <td>2.00</td>
      <td>2,000.00</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Folate, total</td>
      <td>micrograms (µg)</td>
      <td>400.00</td>
      <td>400.00</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Iodine</td>
      <td>micrograms (µg)</td>
      <td>150.00</td>
      <td>150.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Iron, Fe</td>
      <td>milligrams (mg)</td>
      <td>18.00</td>
      <td>18,000.00</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Magnesium, Mg</td>
      <td>milligrams (mg)</td>
      <td>400.00</td>
      <td>400,000.00</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Manganese, Mn</td>
      <td>milligrams (mg)</td>
      <td>2.00</td>
      <td>2,000.00</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Molybdenum</td>
      <td>micrograms (µg)</td>
      <td>75.00</td>
      <td>75.00</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Niacin</td>
      <td>milligrams (mg)</td>
      <td>20.00</td>
      <td>20,000.00</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Pantothenic acid</td>
      <td>milligrams (mg)</td>
      <td>10.00</td>
      <td>10,000.00</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Phosphorus, P</td>
      <td>milligrams (mg)</td>
      <td>1,000.00</td>
      <td>1,000,000.00</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Riboflavin</td>
      <td>milligrams (mg)</td>
      <td>1.70</td>
      <td>1,700.00</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Selenium, Se</td>
      <td>micrograms (µg)</td>
      <td>70.00</td>
      <td>70.00</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Thiamin</td>
      <td>milligrams (mg)</td>
      <td>1.50</td>
      <td>1,500.00</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Vitamin A, IU</td>
      <td>International Unit (IU)</td>
      <td>5,000.00</td>
      <td>16,665.00</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Vitamin B-12</td>
      <td>micrograms (µg)</td>
      <td>6.00</td>
      <td>6.00</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Vitamin B-6</td>
      <td>milligrams (mg)</td>
      <td>2.00</td>
      <td>2,000.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Vitamin C, total ascorbic acid</td>
      <td>milligrams (mg)</td>
      <td>60.00</td>
      <td>60,000.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Vitamin D</td>
      <td>International Unit (IU)</td>
      <td>400.00</td>
      <td>1,333.20</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Vitamin E (alpha-tocopherol)</td>
      <td>International Unit (IU)</td>
      <td>30.00</td>
      <td>99.99</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Vitamin K (phylloquinone)</td>
      <td>micrograms (µg)</td>
      <td>80.00</td>
      <td>80.00</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Zinc, Zn</td>
      <td>milligrams (mg)</td>
      <td>15.00</td>
      <td>15,000.00</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Take the total/sum standard unit nutrient values for all foods for the above mentioned nutrients
df = pd.read_sql(""" 
   SELECT food_name, food_group, SUM(nutrient_val)/1000 total_nutrients_mg
   FROM standardized_quantities
   WHERE nutrient IN %(nutr_list)s
   GROUP BY 1,2
   HAVING SUM(nutrient_val) > 0
   ORDER BY 3 DESC
   LIMIT 10;
   
""", eng, params = {'nutr_list':tuple(nutrients)})
# save food list
foods = df.food_name.unique()
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>food_name</th>
      <th>food_group</th>
      <th>total_nutrients_mg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Orange-flavor drink, KRAFT, TANG SUGAR FREE Lo...</td>
      <td>Beverages</td>
      <td>4,843.54</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Orange-flavor drink, breakfast type, low calor...</td>
      <td>Beverages</td>
      <td>4,843.54</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, Whole Gra...</td>
      <td>Breakfast Cereals</td>
      <td>4,649.68</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, TOTAL Cor...</td>
      <td>Breakfast Cereals</td>
      <td>4,207.81</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, TOTAL Bro...</td>
      <td>Breakfast Cereals</td>
      <td>4,025.70</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Fruit-flavored drink mix, powder, unsweetened</td>
      <td>Beverages</td>
      <td>2,704.95</td>
    </tr>
    <tr>
      <th>6</th>
      <td>KRAFT, KOOL-AID Unsweetened Soft Drink Mix Tro...</td>
      <td>Beverages</td>
      <td>2,614.01</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Spearmint, dried</td>
      <td>Spices and Herbs</td>
      <td>2,516.95</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Puddings, all flavors except chocolate, low ca...</td>
      <td>Sweets</td>
      <td>2,516.73</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Puddings, KRAFT, JELL-O Brand Fat Free Sugar F...</td>
      <td>Sweets</td>
      <td>2,515.08</td>
    </tr>
  </tbody>
</table>
</div>



These foods are the most jam packed with nutrients.

___Pivot Table___

Lets examine the distribution of each.

You can do pivot tables in postgres using crosstab, but let's do it manually.


```python

# Create columns based on nutrients
case_stmnts = ',\n'.join([
    f"SUM(CASE WHEN nutrient = '{n}' THEN nutrient_val ELSE NULL END) AS \"{n}\""
    for n in nutrients
])

# Pivot for selected foods/nutrients
df = pd.read_sql(""" 
   SELECT food_name, food_group,
       {case_stmts}
   FROM nutr_quantities
   WHERE food_name IN %(foods)s
   AND nutrient IN %(nutrs)s
   GROUP BY 1,2
   
""".format(case_stmts=case_stmnts), eng, params={
                'foods':tuple(df.food_name.values),
                'nutrs':tuple(nutrients)
}).dropna(1,'all')
   
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>food_name</th>
      <th>food_group</th>
      <th>Calcium, Ca</th>
      <th>Copper, Cu</th>
      <th>Folate, total</th>
      <th>Iron, Fe</th>
      <th>Magnesium, Mg</th>
      <th>Manganese, Mn</th>
      <th>Niacin</th>
      <th>Pantothenic acid</th>
      <th>Phosphorus, P</th>
      <th>Riboflavin</th>
      <th>Selenium, Se</th>
      <th>Thiamin</th>
      <th>Vitamin A, IU</th>
      <th>Vitamin B-12</th>
      <th>Vitamin B-6</th>
      <th>Vitamin C, total ascorbic acid</th>
      <th>Vitamin D</th>
      <th>Vitamin E (alpha-tocopherol)</th>
      <th>Vitamin K (phylloquinone)</th>
      <th>Zinc, Zn</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, TOTAL Bro...</td>
      <td>Breakfast Cereals</td>
      <td>3,333.00</td>
      <td>0.13</td>
      <td>1,333.00</td>
      <td>60.00</td>
      <td>53.00</td>
      <td>nan</td>
      <td>66.70</td>
      <td>33.30</td>
      <td>200.00</td>
      <td>5.67</td>
      <td>nan</td>
      <td>5.00</td>
      <td>1,667.00</td>
      <td>20.00</td>
      <td>6.67</td>
      <td>200.00</td>
      <td>133.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>50.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, TOTAL Cor...</td>
      <td>Breakfast Cereals</td>
      <td>3,333.00</td>
      <td>0.00</td>
      <td>1,333.00</td>
      <td>60.00</td>
      <td>26.00</td>
      <td>0.10</td>
      <td>66.70</td>
      <td>33.00</td>
      <td>366.00</td>
      <td>5.67</td>
      <td>5.10</td>
      <td>5.00</td>
      <td>1,426.00</td>
      <td>20.00</td>
      <td>6.67</td>
      <td>200.00</td>
      <td>114.00</td>
      <td>45.00</td>
      <td>0.20</td>
      <td>50.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, Whole Gra...</td>
      <td>Breakfast Cereals</td>
      <td>3,680.00</td>
      <td>0.43</td>
      <td>1,590.00</td>
      <td>74.50</td>
      <td>131.00</td>
      <td>3.96</td>
      <td>88.10</td>
      <td>35.50</td>
      <td>296.00</td>
      <td>8.06</td>
      <td>3.90</td>
      <td>7.03</td>
      <td>1,667.00</td>
      <td>21.40</td>
      <td>9.41</td>
      <td>200.00</td>
      <td>133.00</td>
      <td>45.00</td>
      <td>0.60</td>
      <td>58.20</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Fruit-flavored drink mix, powder, unsweetened</td>
      <td>Beverages</td>
      <td>1,105.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.03</td>
      <td>0.00</td>
      <td>0.01</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>509.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>1,090.90</td>
      <td>nan</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>KRAFT, KOOL-AID Unsweetened Soft Drink Mix Tro...</td>
      <td>Beverages</td>
      <td>1,105.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>0.01</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>509.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>0.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>1,000.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orange-flavor drink, KRAFT, TANG SUGAR FREE Lo...</td>
      <td>Beverages</td>
      <td>1,378.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.07</td>
      <td>275.00</td>
      <td>nan</td>
      <td>80.00</td>
      <td>0.00</td>
      <td>629.00</td>
      <td>6.80</td>
      <td>nan</td>
      <td>0.00</td>
      <td>20,000.00</td>
      <td>0.00</td>
      <td>8.00</td>
      <td>2,400.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Orange-flavor drink, breakfast type, low calor...</td>
      <td>Beverages</td>
      <td>1,378.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.07</td>
      <td>275.00</td>
      <td>nan</td>
      <td>80.00</td>
      <td>0.00</td>
      <td>629.00</td>
      <td>6.80</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>20,000.00</td>
      <td>0.00</td>
      <td>8.00</td>
      <td>2,400.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Puddings, KRAFT, JELL-O Brand Fat Free Sugar F...</td>
      <td>Sweets</td>
      <td>147.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>0.08</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>2,368.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>0.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>0.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Puddings, all flavors except chocolate, low ca...</td>
      <td>Sweets</td>
      <td>143.00</td>
      <td>0.04</td>
      <td>1.00</td>
      <td>0.38</td>
      <td>5.00</td>
      <td>0.04</td>
      <td>0.01</td>
      <td>0.05</td>
      <td>2,368.00</td>
      <td>0.02</td>
      <td>0.80</td>
      <td>0.01</td>
      <td>0.00</td>
      <td>0.05</td>
      <td>0.01</td>
      <td>0.00</td>
      <td>nan</td>
      <td>0.08</td>
      <td>1.70</td>
      <td>0.10</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Spearmint, dried</td>
      <td>Spices and Herbs</td>
      <td>1,488.00</td>
      <td>1.54</td>
      <td>530.00</td>
      <td>87.47</td>
      <td>602.00</td>
      <td>11.48</td>
      <td>6.56</td>
      <td>1.40</td>
      <td>276.00</td>
      <td>1.42</td>
      <td>nan</td>
      <td>0.29</td>
      <td>10,579.00</td>
      <td>0.00</td>
      <td>2.58</td>
      <td>0.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>2.41</td>
    </tr>
  </tbody>
</table>
</div>



However, this methodology is biased towards nutrients that are measured in large values. For example, the recommended dose for Calcium is 1g whereas the recommended dose of Vitamin K is 80 µg.


```python
df.T.set_axis(df.food_name, axis=1, inplace=False)\
    .drop(['food_name','food_group'])\
    .assign(temp = lambda f: f.sum(1))\
    .sort_values('temp')\
    .drop('temp', axis=1)\
    .plot.barh(stacked=True)

plt.legend(loc = 'lower right')
plt.xlabel('Nutritional Value (varying units!)');
```


![png](Questions_And_Queries_files/Questions_And_Queries_33_0.png)


___Lastly___


Instead of taking the total sum of nutrient values, lets take the __relative distance__ from the recommended daily values mentioned above.


```python
# Most nutritionally balanced foods
df = pd.read_sql(""" 
    -- All combos of foods and specified nutrients
    WITH food_nutrient AS (
        SELECT food_name, nutrient FROM (
            SELECT DISTINCT food_name FROM standardized_quantities
        ) uniq_foods
        CROSS JOIN daily_dose
    )
    -- Select the pct deviance from the recommended values
    SELECT food_name, AVG(pct_diff) AS nutrition_balance_score FROM (
        SELECT 
            food_name, nutrient,  COALESCE(nutrient_val, 0) nutrient_val, recommended_daily_value_mcg, 
            ABS(COALESCE(nutrient_val, 0) - recommended_daily_value_mcg)/recommended_daily_value_mcg AS pct_diff
        -- all values in micrograms
        FROM standardized_quantities sq
        RIGHT JOIN food_nutrient fn USING(food_name, nutrient)
        LEFT JOIN daily_dose dd USING(nutrient)
    ) diff_from_rec
    GROUP BY 1
    ORDER BY 2
    LIMIT 10


        
""", eng)

foods = df.food_name.unique()
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>food_name</th>
      <th>nutrition_balance_score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Cereals ready-to-eat, chocolate-flavored frost...</td>
      <td>0.62</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cereals ready-to-eat, KRAFT, POST 100% BRAN Ce...</td>
      <td>0.67</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, Corn CHEX</td>
      <td>0.69</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Cereals ready-to-eat, MALT-O-MEAL, Apple Multi...</td>
      <td>0.69</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, COCOA PUFFS</td>
      <td>0.70</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Cereals ready-to-eat, KELLOGG, KELLOGG'S RICE ...</td>
      <td>0.70</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, FRANKENBERRY</td>
      <td>0.71</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Cereals ready-to-eat, Ralston Crispy Rice</td>
      <td>0.71</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Cereals ready-to-eat, QUAKER, Cranberry Macada...</td>
      <td>0.72</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Cereals ready-to-eat, KELLOGG, KELLOGG'S Shred...</td>
      <td>0.73</td>
    </tr>
  </tbody>
</table>
</div>



These are the most well balanced foods, containing the closest to the daily recommended values for the given nutrients. Looks like cereal is the way to go!

Let's check the _Normalized_ distribution (scaled to between 0 and 1)


```python
# case statments used to pivot
# Scales all nutrients to between 0 and 1!
case_stmnts = ',\n'.join([
    f"""CASE WHEN nutrient = '{n}' THEN 
        (nutrient_val-MIN(nutrient_val) OVER (PARTITION BY nutrient))/
            (MAX(nutrient_val) OVER (PARTITION BY nutrient) - MIN(nutrient_val) OVER (PARTITION BY nutrient))
        ELSE NULL END AS \"{n}\"
    """
    for n in nutrients
])

# select all nutrients listed previously
agg_stmnt = ','.join([f'SUM("{n}") as "{n}"' for n in nutrients])

df = pd.read_sql(""" 
    SELECT food_name, food_group, {agg_stmnt}
    FROM (
       SELECT food_name, food_group,
           {case_stmts}
       FROM nutr_quantities
       WHERE food_name IN %(foods)s
       AND nutrient IN %(nutrs)s
    ) zscored
    GROUP BY 1,2
""".format(case_stmts=case_stmnts,
           agg_stmnt=agg_stmnt), eng, params={
                'foods':tuple(foods),
                'nutrs':tuple(nutrients)
}).dropna(1,'all')
                 
print(df.shape)
df

```

    (10, 22)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>food_name</th>
      <th>food_group</th>
      <th>Calcium, Ca</th>
      <th>Copper, Cu</th>
      <th>Folate, total</th>
      <th>Iron, Fe</th>
      <th>Magnesium, Mg</th>
      <th>Manganese, Mn</th>
      <th>Niacin</th>
      <th>Pantothenic acid</th>
      <th>Phosphorus, P</th>
      <th>Riboflavin</th>
      <th>Selenium, Se</th>
      <th>Thiamin</th>
      <th>Vitamin A, IU</th>
      <th>Vitamin B-12</th>
      <th>Vitamin B-6</th>
      <th>Vitamin C, total ascorbic acid</th>
      <th>Vitamin D</th>
      <th>Vitamin E (alpha-tocopherol)</th>
      <th>Vitamin K (phylloquinone)</th>
      <th>Zinc, Zn</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, COCOA PUFFS</td>
      <td>Breakfast Cereals</td>
      <td>0.77</td>
      <td>0.07</td>
      <td>0.00</td>
      <td>0.34</td>
      <td>0.07</td>
      <td>0.00</td>
      <td>0.32</td>
      <td>0.11</td>
      <td>0.00</td>
      <td>0.26</td>
      <td>0.28</td>
      <td>0.34</td>
      <td>0.00</td>
      <td>0.78</td>
      <td>0.26</td>
      <td>0.31</td>
      <td>nan</td>
      <td>0.75</td>
      <td>1.00</td>
      <td>0.86</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, Corn CHEX</td>
      <td>Breakfast Cereals</td>
      <td>0.77</td>
      <td>0.83</td>
      <td>1.00</td>
      <td>0.90</td>
      <td>0.07</td>
      <td>0.13</td>
      <td>0.32</td>
      <td>0.00</td>
      <td>0.01</td>
      <td>0.26</td>
      <td>0.45</td>
      <td>0.34</td>
      <td>0.38</td>
      <td>0.78</td>
      <td>0.26</td>
      <td>0.31</td>
      <td>nan</td>
      <td>0.60</td>
      <td>0.67</td>
      <td>0.86</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Cereals ready-to-eat, GENERAL MILLS, FRANKENBERRY</td>
      <td>Breakfast Cereals</td>
      <td>0.15</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.34</td>
      <td>0.00</td>
      <td>0.01</td>
      <td>0.32</td>
      <td>0.11</td>
      <td>0.00</td>
      <td>0.26</td>
      <td>1.00</td>
      <td>0.34</td>
      <td>0.00</td>
      <td>0.78</td>
      <td>0.26</td>
      <td>0.31</td>
      <td>nan</td>
      <td>0.80</td>
      <td>1.00</td>
      <td>0.86</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Cereals ready-to-eat, KELLOGG, KELLOGG'S RICE ...</td>
      <td>Breakfast Cereals</td>
      <td>0.01</td>
      <td>0.13</td>
      <td>0.37</td>
      <td>0.00</td>
      <td>0.06</td>
      <td>0.24</td>
      <td>0.67</td>
      <td>0.30</td>
      <td>0.04</td>
      <td>0.70</td>
      <td>0.58</td>
      <td>1.00</td>
      <td>0.39</td>
      <td>0.95</td>
      <td>1.00</td>
      <td>0.37</td>
      <td>nan</td>
      <td>0.20</td>
      <td>0.00</td>
      <td>0.04</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Cereals ready-to-eat, KELLOGG, KELLOGG'S Shred...</td>
      <td>Breakfast Cereals</td>
      <td>0.09</td>
      <td>0.26</td>
      <td>0.04</td>
      <td>0.75</td>
      <td>0.41</td>
      <td>1.00</td>
      <td>0.36</td>
      <td>1.00</td>
      <td>0.32</td>
      <td>0.30</td>
      <td>nan</td>
      <td>0.37</td>
      <td>nan</td>
      <td>0.81</td>
      <td>0.27</td>
      <td>0.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>nan</td>
      <td>0.27</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Cereals ready-to-eat, KRAFT, POST 100% BRAN Ce...</td>
      <td>Breakfast Cereals</td>
      <td>0.17</td>
      <td>1.00</td>
      <td>0.04</td>
      <td>0.82</td>
      <td>1.00</td>
      <td>nan</td>
      <td>0.35</td>
      <td>nan</td>
      <td>1.00</td>
      <td>0.28</td>
      <td>nan</td>
      <td>0.36</td>
      <td>0.59</td>
      <td>0.00</td>
      <td>0.29</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>nan</td>
      <td>nan</td>
      <td>0.89</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Cereals ready-to-eat, MALT-O-MEAL, Apple Multi...</td>
      <td>Breakfast Cereals</td>
      <td>1.00</td>
      <td>0.06</td>
      <td>0.05</td>
      <td>0.41</td>
      <td>0.10</td>
      <td>0.17</td>
      <td>0.51</td>
      <td>nan</td>
      <td>0.08</td>
      <td>0.55</td>
      <td>0.70</td>
      <td>0.38</td>
      <td>0.63</td>
      <td>1.00</td>
      <td>0.69</td>
      <td>0.93</td>
      <td>1.00</td>
      <td>1.00</td>
      <td>1.00</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Cereals ready-to-eat, QUAKER, Cranberry Macada...</td>
      <td>Breakfast Cereals</td>
      <td>0.29</td>
      <td>0.24</td>
      <td>0.59</td>
      <td>0.42</td>
      <td>0.21</td>
      <td>0.38</td>
      <td>0.00</td>
      <td>0.41</td>
      <td>0.15</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.29</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.28</td>
      <td>0.35</td>
      <td>nan</td>
      <td>nan</td>
      <td>0.32</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Cereals ready-to-eat, Ralston Crispy Rice</td>
      <td>Breakfast Cereals</td>
      <td>0.00</td>
      <td>0.08</td>
      <td>0.82</td>
      <td>1.00</td>
      <td>0.05</td>
      <td>0.24</td>
      <td>1.00</td>
      <td>0.31</td>
      <td>0.04</td>
      <td>1.00</td>
      <td>0.90</td>
      <td>0.90</td>
      <td>0.53</td>
      <td>0.85</td>
      <td>0.38</td>
      <td>1.00</td>
      <td>nan</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.05</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Cereals ready-to-eat, chocolate-flavored frost...</td>
      <td>Breakfast Cereals</td>
      <td>0.15</td>
      <td>0.19</td>
      <td>0.06</td>
      <td>0.37</td>
      <td>0.10</td>
      <td>0.03</td>
      <td>0.38</td>
      <td>0.10</td>
      <td>0.10</td>
      <td>0.30</td>
      <td>0.28</td>
      <td>0.39</td>
      <td>1.00</td>
      <td>0.82</td>
      <td>0.30</td>
      <td>0.82</td>
      <td>nan</td>
      <td>0.25</td>
      <td>1.00</td>
      <td>0.00</td>
    </tr>
  </tbody>
</table>
</div>




```python
plt.figure(figsize=(24,18))

ax = sns.heatmap(
        df.set_index(['food_name'])
          .drop('food_group', axis=1)
          .fillna(0),
    cmap='BuGn')
ax.xaxis.tick_top()
plt.xticks(rotation=45, ha='left', fontsize=15)
plt.yticks(fontsize=14)
plt.ylabel('Food Name', fontsize=14)
plt.xlabel('Nutrient', fontsize = 14)
```




    Text(0.5,142,'Nutrient')




![png](Questions_And_Queries_files/Questions_And_Queries_39_1.png)



```python
df.T.set_axis(df.food_name, axis=1, inplace=False)\
    .drop(['food_name','food_group'])\
    .assign(temp = lambda f: f.sum(1))\
    .sort_values('temp')\
    .drop('temp', axis=1)\
    .plot.barh(stacked=True)

plt.legend(loc = 'lower right')
plt.xlabel('Nutritional Value (varying units!)')
```




    Text(0.5,0,'Nutritional Value (varying units!)')




![png](Questions_And_Queries_files/Questions_And_Queries_40_1.png)



```python

```


```python

```
