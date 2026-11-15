# Nmap Commands and Results

## 1. Nmap Version
Command:
`nmap --version`

Purpose: Checks the installed Nmap version.

## 2. TCP Connect Scan
Command:
`nmap -sT TARGET`

Purpose: Checks TCP ports using a full TCP connection.

## 3. TCP SYN Scan
Command:
`nmap -sS TARGET`

Purpose: Performs a SYN scan to identify open TCP ports.

## 4. UDP Scan
Command:
`nmap -sU TARGET`

Purpose: Checks UDP ports.

## 5. FIN Scan
Command:
`nmap -sX TARGET`

Purpose: Performs an Xmas scan using FIN, PSH, and URG flags to examine TCP port responses.

## 6. Operating System Detection
Command:
`nmap -O TARGET`

Purpose: Attempts to identify the target operating system.

## 7. Network Discovery
Command:
`nmap -sn NETWORK_RANGE`

Purpose: Discovers active devices on a network without performing a port scan.

**Note:** Replace TARGET and NETWORK_RANGE with authorized targets. Actual results should be added after performing each scan.
