#!/bin/bash
# SETUP PROJECT
# Create and load db
# Install CLI

echo "========================================="
echo "Rick Shapiro"
echo "USDA Database Explorer"
echo "========================================="

INFO="./install.sh;
      Run this file to setup the tool.
      Will connect to postgresql, (delete and) recreate database called 'usda',
      setup tables, load in data and install the tool."

TOOL_USAGE="
    usda_explore [
                    --db_creds_fp
                    --nfoods-groups
                    --list-foods [food_group_id|food_group_name]
                    --list-food-groups
                    --nfoods-in-group [food_group_id|food_group_name]
                    --nutrients-measured food_id|food_name
                    --avg-num-nutrients
                    --foods-1nutr
                    --max-nutrient nutrien_id|nutrient_name
                  ]

    This is a command line tool used to get info on the USDA database.

    Options
    ------

      --db_creds_fp:
        If specified, use json file specified at `db_creds_fp`
        as source of credentials to connect to database.
        Keys must include [host,port,dbname,user,password]

      --nfoods-groups:
        Display number of unique foods and food groups in DB.

      --list-foods [food_group_id|food_group_name]:
          List all unique foods and food ids (optionally within a foodgroup)

      --list-food-groups:
        Display all food groups

      --nfoods-in-group [food_group_id|food_group_name]:
        List number of foods per food group. Optionally in a specific group only.

      --nutrients-measured food_id|food_name:
        List number of nutrients measured for a given food.

      --avg-num-nutrients:
        List average, min and max number of nutrients measured accross all foods.

      --foods-1nutr:
        List all foods that only had 1 nutrient measured.

      --max-nutrient nutrien_id|nutrient_name
        Returns the food(s) with highest measured nutrient.

    To uninstall this tool. Enter 'pip uninstall usda-explorer' in the terminal.
"
# NOTE you must have postgres installed and running

# change to directory of file
cd `dirname $0`

# get users approval to drop a database
echo "This script will connect to postgres and DELETE any database in the public
     schema called 'usda'!"
echo "Continue? (y/n)"
read YN
if [ $YN == 'y' ]; then
 :
else
 echo "Aborting Install"
 exit 1;
fi


# echo "Starting Postgres Daemon at /usr/local/var/postgres"
# postgres -D /usr/local/var/postgres > usda_explorer/log/postgreslog 2>&1 &
# PGID=$!
# echo "Postgres Server Started. To stop the server run `kill $PID`"
#

# Start Fresh
echo
echo 'DROPPING usda Database'
echo '----------------'
psql -c "DROP DATABASE IF EXISTS usda;"
if [ $? -ne 0 ]; then
  echo "Could not connect to Postgres."
  echo "Please make sure your postgres server is running!"
  exit 1
fi


# create database for data
echo
echo 'CREATING usda database...'
echo '----------------'
createdb usda
if [ $? -ne 0 ]; then
  echo "########################"
  echo "Failed to create database."
  echo
  echo "Please make sure postgres is running."
  echo "########################"
  exit 1
fi
# load data to newly created db
echo 'Loading Data...'
psql -d usda -f usda_explorer/usda.sql
psql -d usda -f usda_explorer/create_views.sql

echo
echo 'INSTALLING TOOL...'
# NOT SURE HOW TO HANDLE THIS? --user or not?
pip install .
echo "TOOL INSTALLED!"
echo "-----------------------------------------------"
echo
echo "TOOL USAGE:"
echo "$TOOL_USAGE"
echo "-----------------------------------------------"
echo "Thank you for your consideration!"
echo "Rick Shapiro"
echo "rick.shapirony@gmail.com"
echo "917-453-5799"
