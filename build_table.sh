# Build Table

cd `dirname $0`

# NOTE you must have postgres installed and running

# create database for data
createdb usda
if [ $? -ne 0 ]; then
  echo "########################"
  echo "Failed to create database."
  echo
  echo "Please make sure postgres is running and that there is not"
  echo "already a database called 'usda'."
  echo "########################"
  exit 1
fi


# load data to newly created db and run in background
psql -f usda.sql usda &
