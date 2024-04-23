import socket
import struct
import threading

def send_dns_requests(target_host, dns_server, num_requests, num_threads):
    # Create a lock to synchronize access to shared resources (like stdout)
    print_lock = threading.Lock()

    def worker():
        nonlocal num_requests
        while num_requests > 0:
            try:
                # Craft DNS query packet
                query = craft_dns_query(target_host)
                
                # Send DNS query to the specified DNS server
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as resolver:
                    resolver.settimeout(5)
                    resolver.sendto(query, (dns_server, 53))
                    response, _ = resolver.recvfrom(1024)
                
                # Parse DNS response to extract IP address
                ip_address = parse_dns_response(response)
                
                # Print result using thread-safe printing
                with print_lock:
                    print(f"{target_host} resolved to {ip_address} using DNS server {dns_server}")
                
            except Exception as e:
                with print_lock:
                    print(f"Error resolving {target_host} using DNS server {dns_server}: {e}")
            
            num_requests -= 1

    # Create and start worker threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def craft_dns_query(target_host):
    # DNS query structure:
    # Header (12 bytes) + Question (length varies)
    qname = b''
    for part in target_host.split('.'):
        qname += struct.pack('B', len(part)) + part.encode('utf-8')
    qname += b'\x00'  # Null terminator for domain name
    
    header = struct.pack('!HHHHHH', 0x1234, 0x0100, 1, 0, 0, 0)
    question = qname + struct.pack('!HH', 1, 1)  # QTYPE = A (IPv4), QCLASS = IN (Internet)
    
    return header + question

def parse_dns_response(response):
    # Parse DNS response to extract IP address
    # Assuming this is a simple A record response (IPv4 address)
    ip_address = '.'.join(str(byte) for byte in response[-4:])
    return ip_address

if __name__ == "__main__":
    target_host = input("Enter the target host name: ")
    dns_server = input("Enter the DNS server IP address: ")
    num_requests = int(input("Enter number of requests per thread: "))
    num_threads = int(input("Enter number of threads: "))

    send_dns_requests(target_host, dns_server, num_requests, num_threads)
