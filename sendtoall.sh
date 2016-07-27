for i in `cat ipaddresses.txt`
do
scp $1 dwicke@$i:/home/dwicke/$1 &
done
