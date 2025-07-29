import socket

def scan_ports(target):
    print(f"Scanning target: {target}")
    print("-" * 50)

    try:
        for port in range(1, 1025):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.2)
            
            result = s.connect_ex((target, port))
            if result == 0:
                print(f"Port {port} is open")
            s.close()

    except KeyboardInterrupt:
        print("\nExiting program.")
    except socket.gaierror:
        print("\nHostname could not be resolved.")
    except socket.error:
        print("\nServer not responding.")

    print("-" * 50)
    print("Scanning finished.")


if __name__ == "__main__":
    target_host = input("Enter the IP address or hostname to scan: ")
    scan_ports(target_host)
