for i in `cat ipaddresses.txt`
do
ssh dwicke@$i killall -9 python &
done
