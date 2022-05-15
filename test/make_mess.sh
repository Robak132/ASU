#!/bin/bash
rm -r X
rm -r Y1
rm -r Y2
mkdir "X"
cd X || exit

RANDOM=2137
for l in [ ":" '"' "." ";" "*" "?" "$" "#" "‘" "|" ]; do
  echo $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM > "$RANDOM$l$RANDOM"
done
for i in {1..20}; do
    echo $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM > "$RANDOM"
done
for i in {1..5}; do
    echo $RANDOM $RANDOM $RANDOM $RANDOM > "$RANDOM.tmp"
done
for i in {1..5}; do
    touch "$RANDOM"
done

for k in {1..5}; do
  b="$RANDOM"
  mkdir "$b"
  cd $b || exit
  for i in {1..20}; do
      echo $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM $RANDOM > "$RANDOM"
  done
  for i in {1..5}; do
      echo $RANDOM $RANDOM $RANDOM $RANDOM > "$RANDOM.tmp"
  done
  for i in {1..5}; do
      touch "$RANDOM"
  done
  cd ../ || exit
done

cd ../
cp -r X Y1
cp -r X Y2