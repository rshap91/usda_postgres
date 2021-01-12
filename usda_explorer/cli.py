#!/usr/bin/env python
from __future__ import print_function
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.width', None)

def create_eng(creds_fp):

    with open(creds_fp, 'r') as f:
        db_creds = json.load(f)

    host = db_creds['host']
    port = db_creds['port']
    dbname = db_creds['dbname']
    user = db_creds['user']
    password = db_creds['password']

    # if user is not specified, use the environmental variable '$USER'
    if not user:
        user = os.environ['USER']
    eng = create_engine('postgresql://{user}:{password}@{host}:{port}/{dbname}'.format(
                                                                        user=user,
                                                                        password=password,
                                                                        host=host,
                                                                        port=port,
                                                                        dbname=dbname))
    return eng

def filter_food_group(group):
    """
    Used to add optional filters to queries
    """
    if group == 'all':
        return ''
    try:
        group = int(group)
        where_clause = 'WHERE LOWER(fdgrp_cd) = LOWER(%s)'
    except ValueError:
        where_clause = 'WHERE LOWER(fddrp_desc) = LOWER(%s)'
    else:
        where_clause = ''
    return where_clause



def check_table_exists(table,eng):
    q= """
        SELECT EXISTS (
            SELECT 1
            FROM pg_tables
            WHERE tablename = %(tablename)
        );
    """
    exists = pd.read_sql(q,eng, params={'tablename':table})
    return exists


def get_nfoods_ngroups(eng):
    'Returns Number of unique foods and number of unique food groups.'

    q = '''
        SELECT
            COUNT(DISTINCT ndb_no) n_foods,
            COUNT(DISTINCT fdgrp_cd) n_fgroups
        FROM food_des FULL OUTER JOIN fd_group
        USING(fdgrp_cd);
        '''
    df = pd.read_sql(q, eng)
    return df

def list_foods(eng, fgroup=None):
    'Lists unique foods. Optionally only list foods in food group `fgroup`.'

    where_clause = filter_food_group(fgroup)

    q = """
        SELECT DISTINCT fd.ndb_no as food_id, fd.long_desc as food_name
        FROM food_des fd JOIN fd_group fg USING(fdgrp_cd)
        {}
        ORDER BY 2;
    """.format(where_clause)
    df = pd.read_sql(q,eng, params=(fgroup,))
    return df

def list_food_groups(eng):
    q = """
        SELECT DISTINCT fdgrp_cd as fg_id, fddrp_desc as food_goup
        FROM fd_group
        ORDER BY 2;
    """
    df = pd.read_sql(q,eng)
    return df


def get_nfoods_per_group(eng, fgroup=None):
    "Returns the number of foods in each food group."

    where_clause = filter_food_group(fgroup)

    q = '''
        SELECT
            fddrp_desc f_group,
            COUNT(DISTINCT ndb_no) n_foods
        FROM food_des
        {}
        FULL OUTER JOIN fd_group USING(fdgrp_cd)
        GROUP BY 1
        ORDER BY 2 DESC
    '''.format(where_clause)
    df = pd.read_sql(q, eng, params=(fgroup,))
    return df

def get_nnutrients_measured(eng, food):
    "Returns number of nutrients measured for passed food"
    try:
        food = int(food)
        col = 'ndb_no'
    except ValueError:
        col='long_desc'

    q = """
        SELECT fd.ndb_no, fd.long_desc, COUNT(DISTINCT ndf.nutrdesc) n_nutr
        FROM food_des fd
        LEFT JOIN nut_data USING (ndb_no)
        JOIN nutr_def ndf USING (nutr_no)
        WHERE ndf.nutrdesc NOT LIKE '%%:%%'
        AND LOWER(fd.{}) = LOWER(%s::TEXT)
        GROUP BY 1
        ORDER BY 3 DESC;
    """.format(col)

    df = pd.read_sql(q, eng, params=(food,))
    return df

def get_food_nutrients(eng, food):
    try:
        food = int(food)
        col = 'food_id'
    except ValueError:
        col='food_name'

    q = """
        SELECT * FROM nutr_quantities
        WHERE LOWER({}) = LOWER(%s::TEXT)
        ORDER BY nutrient DESC;
    """.format(col)

    df = pd.read_sql(q,eng, params=(food,))
    return df

def get_avg_num_nutrients(eng):
    """
    Returns info on the average, min, and max number of nutrients measured
    across all foods
    """

    q = '''
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
        ) n_measured;
    '''
    df = pd.read_sql(q, eng)
    return df


def get_foods_1nutr(eng):
    'Returns foods that only had 1 nutrient measured'

    q = """
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
    """

    df = pd.read_sql(q, eng)
    return df

def most_of_nutrient(eng, nutrient):
    "Returns the food with the highest measured value of the passed nutrient"
    try:
        nutrient = int(nutrient)
        col = 'nutrient_id'
    except ValueError:
        col='nutrient'

    q = """
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
            AND LOWER({}) = LOWER(%s);
    """.format(col)
    df = pd.read_sql(q, eng, params=(nutrient,))
    return df
