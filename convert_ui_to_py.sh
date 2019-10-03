#env bash
for fl in *.ui
do
    pyuic5 $fl -o ${fl:0:${#fl}-3}.py
done