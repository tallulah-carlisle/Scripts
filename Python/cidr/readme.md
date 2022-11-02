# Update Inbound Cidrs for YAML Ingress

This Python script will update the kubernetes annotation "alb.ingress.kubernetes.io/inbound-cidrs" of a specific kubernetes ingress resource. It allows the **cidrs.yaml** file to maintain the list of allowed inbound cidrs that can access the application load balancer.

## Prerequisites

You will need to have install:
- python 3
- pip3 
- pyyaml

## Usage

Copy the contents of this folder or clone the repository. For the script to work, you will need the **main.py**, **cidrs.yaml** and **ingress.yaml** files. 
Make sure the script is executable and run the script.

```
chmod +x ./main.py
python3 ./main.py
```

To change the targetted ingress, you will need to update the **ingress.yaml** file for your personal resource (name, namespace) and also in line 8 of **main.py**: ```kubectl get ing <ingress-name>``` 

## How it works

The script will run **kubectl** and output the current inbound cidrs configured on a particular ingress to the **CIDRIngressOP.txt** file. 
These inbound cidr's will then be compared against the list in the **cidrs.yaml** file, which should manage the list of allowed inbound cidr's. If there are any changes, the updated list from **cidrs.yaml** will then be checked for duplicates and any invalid formatting.
Once all checks are complete, the **cidrs.yaml** file will be updated to remove any duplicates/invalid cidr's. The inbound-cidrs will also be updated in the **ingress.yaml** manifest and deployed to the cluster.