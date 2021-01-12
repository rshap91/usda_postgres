#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import argparse
import pkg_resources as pr
import numpy as np
import pandas as pd

root_dir = pr.resource_filename("usda_explorer", '/')
os.chdir(root_dir)
import usda_explorer.cli as cli

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--db_creds_fp',
                        type=str,
                        default=None,
                        help="""If specified, use json file specified at `db_creds_fp`
                            as source of credentials to connect to database.
                            Keys must include [host,port,dbname,user,password]
                        """)
    parser.add_argument('--nfoods-groups',
                        action='store_true',
                        help='Display number of unique foods and food groups in DB.')
    parser.add_argument('--list-foods',
                        const = 'all',
                        nargs = '?',
                        help='''
                            --list-foods {food_group_id|food_group_name|all}
                            List all unique foods and food ids (optionally within a foodgroup).
                            ''')
    parser.add_argument('--list-food-groups',
                        action='store_true',
                        help='''
                            Display all food groups
                        ''')
    parser.add_argument('--nfoods-in-group',
                        const = 'all',
                        nargs = '?',
                        help="""
                        List number of foods per food group. Optionally in a specific group only.
                        """)
    parser.add_argument('--nutrients-measured',
                        help="""
                        List number of nutrients measured for a given food.
                        """)
    parser.add_argument('--food-nutrients',
                        help="Shows all nutrient measurements for passed food.")
    parser.add_argument('--avg-num-nutrients',
                        action='store_true',
                        help="""
                        List average, min and max number of nutrients measured accross all foods.
                        """)
    parser.add_argument('--foods-1nutr',
                        action='store_true',
                        help="""
                        List all foods that only had 1 nutrient measured.
                        """)
    parser.add_argument('--max-nutrient',
                        help="""
                        Returns the food(s) with highest measurements for passed nutrient.
                        """)




    args = parser.parse_args()

    db_creds_fp = args.db_creds_fp or os.path.join(root_dir, 'config','db_creds.json')
    assert os.path.exists(db_creds_fp), 'Please add a json credential file to {}.'.format(os.path.abspath(db_creds_fp))
    eng = cli.create_eng(db_creds_fp)

    if args.nfoods_groups:
        df = cli.get_nfoods_ngroups(eng)
        print('Number of Foods and Food Groups:')
        print(df)
        print()

    if args.list_foods:
        df = cli.list_foods(eng, args.list_foods)
        print(df)
        print()

    if args.list_food_groups:
        df = cli.list_food_groups(eng)
        print(df) # Dataframe (name, avg_dur)
        print()

    if args.nfoods_in_group:
        df = cli.get_nfoods_per_group(eng, args.nfoods_in_group)
        print(df)
        print()

    if args.nutrients_measured:
        df = cli.get_nnutrients_measured(eng, args.nutrients_measured)
        print(df)
        print()

    if args.food_nutrients:
        df = cli.get_food_nutrients(eng, args.food_nutrients)
        print(df)
        print()

    if args.avg_num_nutrients:
        df = cli.get_avg_num_nutrients(eng)
        print(df)
        print()

    if args.foods_1nutr:
        df = cli.get_foods_1nutr(eng)
        print(df)
        print()

    if args.max_nutrient:
        df = cli.most_of_nutrient(eng, args.max_nutrient)
        print(df)
        print()



    print('------------------------------------------------------------------')

if __name__ == '__main__':
    main()
