#!/bin/bash
#emreYbs(e3re)
# Intended to work on Linux and scan local IP addresses. But you can also scan the public IP address with minor change in the code and usage
# I scan my own local network, so it asks the user the last octet of the last IP address (e.g., 254)
# The script uses nmap to scan for open ports on a range of IP addresses, you can also scan only one port or port ranges

show_banner() {
    echo "----------------------------------------"
    echo "       Local Port Scanner"
    echo "     ➶➶➶➶➶ by emreybs ➷➷➷➷➷"
    echo "----------------------------------------"
    echo "This script scans a range of IP addresses"
    echo "for open ports on a specified port number."
    echo "----------------------------------------"
}

# Call the function to show the banner
show_banner

# Function to validate IP address
validate_ip() {
    if [[ ! $1 =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]; then
        echo "Invalid IP address. Please enter a valid IP address."
        exit 1
    fi
}

# Function to validate port range
validate_port_range() {
    local port_range=$1
    local valid_port_range_regex="^([0-9]+-[0-9]+|[0-9]+)$"
    if [[ ! $port_range =~ $valid_port_range_regex ]]; then
        echo "Invalid port range or port number. Please enter a valid port range (e.g., 1-100) or a single port number."
        exit 1
    fi
}

echo "Please enter the starting IP address to scan (e.g., 192.168.0.1):  "
read -r FirstIP
validate_ip "$FirstIP"

echo "Please enter the last octet of the last IP address (e.g., 254):  "
read -r LastOctetIP
IPRange=$(echo "$FirstIP" | awk -F. -v last="$LastOctetIP" '{print $1"."$2"."$3"."$4"-"last}')

echo "Do you want to scan a single port or a range of ports? (Enter 'single' or 'range'): "
read -r PortChoice

if [[ $PortChoice == "single" ]]; then
    echo "Enter the port number to scan (e.g., 21): "
    read -r PortNumber
    validate_port_range "$PortNumber"
else
    echo "Enter the port range to scan (e.g., 1-100): "
    read -r PortRange
    validate_port_range "$PortRange"
    PortNumber="$PortRange"
fi

echo "Scanning $IPRange for open ports on port $PortNumber"
echo "This may take a few minutes..."

#You may need to use sudo to run the nmap command if you are scanning a range of ports
sudo nmap -T4 -n --min-rate 1000 -p"$PortNumber" "$IPRange" | grep open >openPorts.txt

if [[ -s openPorts.txt ]]; then
    echo "The open ports are: "
    echo "-------------------"
    cat openPorts.txt
    echo "-------------------"
else
    echo "No open ports found."
fi

echo "The open ports have been saved to openPorts.txt"
echo "Thank you for using the Local Port Scanner"
exit 0
