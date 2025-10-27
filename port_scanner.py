import socket
import sys
import time

def scan_ports(target_ip, start_port, end_port):
    """Belirtilen IP adresindeki port aralığını tarar."""
    print("-" * 50)
    print(f"Scanning Target: {target_ip}")
    print("-" * 50)

    t_start = time.time()  # Başlangıç zamanı kaydı
    
    # Port aralığında döngü başlat
    for port in range(start_port, end_port + 1):
        try:
            # TCP bağlantısı için soket oluşturma (IPv4 ve TCP)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Bağlantı zaman aşımını ayarla (Yavaşlamayı önler)
            s.settimeout(0.5) 
            
            # Bağlantı kurmayı dene. 0 başarılı anlamına gelir.
            result = s.connect_ex((target_ip, port))

            if result == 0:
                # Bağlantı başarılıysa port açıktır
                try:
                    # Portun hangi hizmete ait olduğunu bulmaya çalış (Opsiyonel)
                    service = socket.getservbyport(port, 'tcp')
                    print(f"Port {port}: OPEN  ({service})")
                except OSError:
                    # Hizmetin adı bulunamazsa sadece 'OPEN' yazdır
                    print(f"Port {port}: OPEN")
            
            s.close() # Kontrolden sonra soketi kapatma

        except socket.gaierror:
            # Alan adı çözümlenemezse programı durdur
            print("Error: Hostname could not be resolved (Invalid IP or Hostname)")
            sys.exit()
        except socket.error:
            # Bağlantı hatalarını bu aşamada görmezden gel (Sadece açık portlara odaklan)
            pass 
    
    t_end = time.time()  # Bitiş zamanı kaydı
    print("-" * 50)
    print(f"Scan Completed. Duration: {round(t_end - t_start, 2)} seconds")

if __name__ == "__main__":
    # Programın doğru sayıda argümanla çalışıp çalışmadığını kontrol et
    if len(sys.argv) != 4:
        print("Usage: python port_scanner.py <target_address> <start_port> <end_port>")
        print("Example: python port_scanner.py localhost 80 100")
        sys.exit()

    try:
        # Komut satırı argümanlarını al ve tiplerini tam sayıya dönüştür
        target = sys.argv[1]
        start_p = int(sys.argv[2])
        end_p = int(sys.argv[3])
        
        # Alan adını IP adresine çevir (eğer IP değilse)
        target_ip = socket.gethostbyname(target)
        
        scan_ports(target_ip, start_p, end_p)

    except ValueError:
        print("Error: Port values must be integers.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    