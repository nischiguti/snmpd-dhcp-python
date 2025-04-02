dhcpd.conf

```# DHCP Server Configuration file for enp2s0

# Specify the DHCP server's interface
INTERFACES="enp2s0";

# Define the subnet and network range
subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.100 192.168.1.200;    # Range of IPs to assign
  option routers 192.168.1.1;            # Default gateway
  option subnet-mask 255.255.255.0;     # Subnet mask
  option domain-name-servers 8.8.8.8, 8.8.4.4;   # DNS servers (Google DNS)
  option broadcast-address 192.168.1.255;    # Broadcast address
  default-lease-time 600;               # Default lease time in seconds
  max-lease-time 7200;                  # Maximum lease time in seconds
}

# Define the DHCP server's hostnames and IP address reservations (optional)
host somehost {
  hardware ethernet 34:ab:95:7f:2c:bf;  # MAC address of the device
  fixed-address 192.168.1.105;           # Fixed IP to assign
}
host somehost2 {
  hardware ethernet 2c:bc:bb:76:0d:ff	;  # MAC address of the device
  fixed-address 192.168.1.107;           # Fixed IP to assign
}


# Additional settings
log-facility local7;                   # Log facility for DHCP events

subnet 192.168.2.0 netmask 255.255.255.0 {
  range 192.168.2.100 192.168.2.200;    # Range of IPs to assign
  option routers 192.168.2.1;            # Default gateway
  option subnet-mask 255.255.255.0;     # Subnet mask
  option domain-name-servers 8.8.8.8, 8.8.4.4;   # DNS servers (Google DNS)
  option broadcast-address 192.168.2.255;    # Broadcast address
  default-lease-time 600;               # Default lease time in seconds
  max-lease-time 7200;                  # Maximum lease time in seconds```
}
