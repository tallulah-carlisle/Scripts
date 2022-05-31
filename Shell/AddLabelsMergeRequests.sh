#!/bin/bash
# ./script.sh filename
# read through json file, select iid value and through webhook add labels 

while read -r line; do
if [[ $line == *iid* ]]
then 
  newline=$(echo "$line" | awk '{print substr($2, 1, length($2)-1)}')
  echo "$newline"
  arr+=($newline)
fi
done < "$1"

for i in "${arr[@]}"
do
  curl -X 'PUT' --header "PRIVATE-TOKEN: pVFqy3kC1EiXnzAXqkaf" "https://git.altemista.cloud/api/v4/projects/5122/merge_requests/$i?labels=keep-alive"
done
