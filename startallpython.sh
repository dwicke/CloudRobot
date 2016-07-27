for i in `cat ipaddresses.txt`
do
ssh dwicke@$i python $1 &
done
