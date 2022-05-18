#!/bin/bash
rm -r X
rm -r Y1
mkdir "X"
cd X || exit

RANDOM=2137
for l in [ ":" '"' "." ";" "*" ]; do
  echo $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM > "$RANDOM$l$RANDOM"
done
for i in {1..10}; do
    echo $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM > "$RANDOM"
done
for i in {1..3}; do
    echo $RANDOM $RANDOM $RANDOM $RANDOM > "$RANDOM.tmp"
done
for i in {1..3}; do
    touch "$RANDOM"
done
chmod 706 ./1235
chmod 777 ./12884

for k in {1..3}; do
  b="$RANDOM"
  mkdir "$b"
  cd $b || exit
  for i in {1..5}; do
      echo $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM > "$RANDOM"
  done
  for i in {1..1}; do
      echo $RANDOM $RANDOM $RANDOM $RANDOM > "$RANDOM.tmp"
  done
  for i in {1..1}; do
      touch "$RANDOM"
  done
  cd ../ || exit
done

cd ../ || exit
cp -r X Y1

rm X/19872/335
cp X/6146 X/6146_2
echo $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM > "Y1/28864"
