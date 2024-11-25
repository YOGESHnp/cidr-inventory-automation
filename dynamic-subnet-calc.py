import ipaddress
import os
import re
import csv

def get_new_prefix(cidr_prefix):
    division_map = {
        16: 19, # /16 to /19
        17: 20, # /17 to /20
        18: 21, # /18 to /21
        19: 22, # /19 to /22
        20: 23, # /20 to /23
        21: 24, # /21 to /24
        22: 25, # /22 to /25
        23: 26, # /23 to /26
        24: 27, # /24 to /27
        25: 28, # /25 to /28
        26: 29, # /26 to /29
        27: 30, # /27 to /30
        28: 31, # /28 to /31
    }
    return division_map.get(cidr_prefix, None)

def subnet_calculator(cidr):
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        new_prefix = get_new_prefix(network.prefixlen)
        if new_prefix is None:
            return []
        
        subnets = list(network.subnets(new_prefix=new_prefix))
        results = []
        for subnet in subnets:
            subnet_info = {
                "Subnet Address": str(subnet),
                "Range of Addresses": f"{subnet.network_address} - {subnet.broadcast_address}",
                "Usable IPs": f"{subnet.network_address + 1} - {subnet.broadcast_address - 1}",
                "Hosts": subnet.num_addresses - 2,
                "Divide": "Divide",
                "Join": ""
            }
            results.append(subnet_info)
        
        return results
    except ValueError as e:
        return []

def process_vpc_files(directory, output_file):
    all_results = []

    for filename in os.listdir(directory):
        if filename.endswith("output.txt"):
            # Extract profile and account name from filename
            parts = filename.replace('_output.txt', '').split('_')
            profile = "_".join(parts[:-1]) #All parts except last
            account_name = parts[-1] #Last part

            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                for line in file:
                    # Extract VPC ID, CIDR and Region
                    match = re.search(r'VPC ID: (\S+), IPv4 CIDR: (\d+\.\d+\.\d+\.\d+/\d+), Region: (\S+)', line)
                    if match:
                        vpc_id = match.group(1)
                        cidr = match.group(2)
                        region = match.group(3)

                        print(f"\n Processing CIDR: {cidr} from {filename}")
                        subnet_results = subnet_calculator(cidr)

                        for result in subnet_results:
                            result_info = {
                                "Account Name": profile,
                                "Profile": account_name,
                                "Region": region,
                                "VPC ID": vpc_id,
                                "VPC CIDR": cidr,
                                **result
                            }
                            all_results.append(result_info)
    
    # Write results to CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Profile', 'Account Name', 'Region', 'VPC ID', 'VPC CIDR', 'Subnet Address', 'Range of Addresses', 'Usable IPs', 'Hosts', 'Divide', 'Join']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in all_results:
            writer.writerow(result)
    
    print(f"\nResults saved to {output_file}")

def main():
    directory = "./VPC_Details" #Directory containing the text files
    output_file = "subnets.csv" #Output CSV file name
    process_vpc_files(directory, output_file)

if __name__ == "__main__":
    main()
