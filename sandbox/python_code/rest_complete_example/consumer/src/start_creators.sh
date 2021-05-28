

typeset -i i
typeset -i MAX_LIMIT

((MAX_LIMIT = 2))

((i = 1))


while ((i <= MAX_LIMIT)); do
    echo "starting creator $i"
    ./security_creator.py $i $i > ../log/security_creator.log.$i 2>&1 &
    ((i += 1))
done

echo "started all $i creators"
