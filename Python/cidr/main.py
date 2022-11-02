import os
import yaml

def main():
    print("Currently configured CIDR's from the Ingress: ")

    # Get current CIDR's & Output
    os.system("kubectl get ing test-ingress -o=json | jq '.metadata.annotations[\"alb.ingress.kubernetes.io/inbound-cidrs\"]' > CIDRIngressOP.txt")
    os.system("cat CIDRIngressOP.txt")
    
    # Create List of Current CIDR's
    print("\nList of Current CIDR's: ")
    with open("CIDRIngressOP.txt",'r') as file:
        #  Go through each line, separate by comma and remove white-space/chars
        for line in file:
            current_cidrs = line.strip(' ,\"\n').split(',')
            print(current_cidrs)
    
    # Create List of New CIDR's
    print("\nList of New CIDR's to Update the Ingress: ")
    with open("cidrs.yaml", 'r') as stream:
        out = yaml.load(stream, Loader=yaml.Loader)
        print(out['cidrs'])
        new_cidrs=(out['cidrs'])
    # Check if there are differences between the Lists of CIDR's
        checkDifference(current_cidrs, new_cidrs)

def checkDifference(list1, list2):
    print("\nChecking if there are updates to the CIDR's list...")
    if(list1==list2):
        print ("There are no changes to the CIDR's list")
    else:
        print ("Changes have been made to the CIDR's list")
        checkDuplicates(list2)

def checkDuplicates(list):
    # Use len() and set() modules to compare length against set length.
    # If they don't match there is a duplicate.
    print("\nChecking for duplicates in the updated list of CIDR's...")
    print("\nNumber of elements in the list: ", len(list))
    checkSet = set(list)
    print("\nIf this number does not match the number of elements, there are duplicates: ",len(checkSet))
    
    # If duplicates found, create new list without the duplicate, else continue
    if len(list) != len(checkSet):
        print("\nDuplicates found in the list")
        newlist = []
        duplicates = []
        for i in list:
            if i not in newlist:
                newlist.append(i)
            else:
                duplicates.append(i)
        print("\nList of duplicates: ", duplicates)
        print("\nList of CIDRs after removing duplicates: ", newlist)
        validateCidrs(newlist)
    else: 
        print("\nNo duplicates found in the list")
        validateCidrs(list)

def validateCidrs(list):
    # Validate the CIDR's against formatting rules..
    print("\nValidating the list of CIDR's...")
    newlist = []
    removed = []
    for i in list:
        if i == '0.0.0.0/24':
            removed.append(i)
        else:
            newlist.append(i)
    print("\nInvalid CIDRs: ", removed)
    print("\nValid CIDRs: ", newlist)
    updateYaml(newlist)


def updateYaml(list):
    print("\nUpdating the YAML Manifest...")
    with open("cidrs.yaml", 'r') as stream:
        out = yaml.load(stream, Loader=yaml.Loader)
        print(out['cidrs'])
        (out['cidrs']) = list
        print(out['cidrs'])
        with open("cidrs.yaml", 'w+') as stream:
            yaml.dump(out, stream)
    document = "ingress.yaml"
    # Load yaml file (ingress.yaml) from current directory
    docs = yaml.load(open(document, "rt"), Loader=yaml.Loader)

    # Output current value for alb.ingress.kubernetes.io/inbound-cidrs annotation
    print("\nCurrent value for the 'alb.ingress.kubernetes.io/inbound-cidrs' annotations is: ")
    print(docs['metadata']['annotations']['alb.ingress.kubernetes.io/inbound-cidrs'])
    
    # Update and ouput the annotation value with the new, validated list of CIDR's
    docs['metadata']['annotations']['alb.ingress.kubernetes.io/inbound-cidrs'] = ','.join(list)
    print("\nThe updated value for the 'alb.ingress.kubernetes.io/inbound-cidrs' annotation is:")
    print(docs['metadata']['annotations']['alb.ingress.kubernetes.io/inbound-cidrs'])
    # Save the ingress.yaml with the updated list and output it
    with open('ingress.yaml', 'w') as f:
        yaml.dump(docs, f)
    print("\nSee the updated manifest below: ")
    print(docs)
    # os.system("kubectl apply -f ingress.yaml")

main()
