
echo "starting!"

file_name=record.csv

python main.py > $file_name

tail -1 $file_name > record.log

sed -i '$d' $file_name

rm -rf __pycache__
