i=-128

while [ "$i" -lt "128" ]
do
	../byte_rep -i $i -b 1
	i=`expr $i + 1`
done
