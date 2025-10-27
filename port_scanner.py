import socket
import sys
import time

def scan_ports(target_ip, start_port, end_port):
    print("-" * 50)
    print(f"Scanning Target: {target_ip}")
    print("-" * 50)

    t_start = time.time()
    
    for port in range(start_port, end_port + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5) 
            
            result = s.connect_ex((target_ip, port))

            if result == 0:
                try:
                    service = socket.getservbyport(port, 'tcp')
                    print(f"Port {port}: OPEN  ({service})")
                except OSError:
                    print(f"Port {port}: OPEN")
            
            s.close()

        except socket.gaierror:
            print("Error: Hostname could not be resolved (Invalid IP or Hostname)")
            sys.exit()
        except socket.error:
            pass 
    
    t_end = time.time()  
    print("-" * 50)
    print(f"Scan Completed. Duration: {round(t_end - t_start, 2)} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python port_scanner.py <target_address> <start_port> <end_port>")
        print("Example: python port_scanner.py localhost 80 100")
        sys.exit()

    try:
        target = sys.argv[1]
        start_p = int(sys.argv[2])
        end_p = int(sys.argv[3])
        
        target_ip = socket.gethostbyname(target)
        
        scan_ports(target_ip, start_p, end_p)

    except ValueError:
        print("Error: Port values must be integers.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    
