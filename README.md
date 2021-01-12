### Postgres_USDA_SQL_Project

CLI I built that answers some basic questions on the
[USDA Food Database](https://github.com/vrajmohan/pgsql-sample-data).
Note this tool runs on a mac/linux computer with psql installed. To install
psql run download [homebrew](https://brew.sh/) or [linuxbrew](http://linuxbrew.sh/)
and run `brew install postgresql`

There is also a video included that demos how to install and use the tool.

___Installation___:

  1. Open a terminal and navigate to the project directory ('path/to/Rick_Shapiro_Portfolio/Postgres_USDA_SQL_Project/')
  2. Start your psql daemon (`postgres -D /usr/local/var/postgres > usda_explorer/log/postgreslog 2>&1 &`)
    - Note that this starts the daemon in the _background_ and prints out the process id.
      To stop the daemon run `kill PID` where PID is whatever pid was printed.
  3. Run `./install.sh`.  
    - This will delete any postgres database you have named 'usda'. Enter `y` to proceed.
  4. You're done! See usage below.


Usage:

The tool can be used by calling `usda_explore [--options...]` where options include:

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

    --food-nutrients:
      Shows all nutrient measurements for given food.

    --avg-num-nutrients:
      List average, min and max number of nutrients measured across all foods.

    --foods-1nutr:
      List all foods that only had 1 nutrient measured.

    --max-nutrient nutrien_id|nutrient_name
      Returns the food(s) with highest measured nutrient.

To uninstall this tool. Enter 'pip uninstall usda-explorer' in the terminal.
