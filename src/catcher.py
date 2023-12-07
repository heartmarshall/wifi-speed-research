import psutil
import time
import csv
import argparse

def get_network_stats(interface):
    net_stats = psutil.net_io_counters(pernic=True).get(interface)
    if not net_stats:
        print(f"Interface {interface} not founded.")
        return None
    return net_stats

def bytes_to_mbits(bytes):
    return round(bytes * 0.000008, 2)

def start_traffic_moniotring(interface, interval, output_file, output_format_func=bytes_to_mbits, max_timestaps=1000000):
    """
    Monitors network traffic on the specified interface and writes the statistics to a CSV file.
    """
    try:
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['Timestep', 'DownloadSpeed', 'UploadSpeed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            timestap = 0 
            old_net_stats = get_network_stats(interface)
            print(f"Monitoring traffic speed of {interface}. Press Ctrl+C to stop.\n")

            while True:
                time.sleep(interval)

                net_stats = get_network_stats(interface)
                if not net_stats:
                    break

                download_speed = (net_stats.bytes_recv - old_net_stats.bytes_recv) / interval
                upload_speed = (net_stats.bytes_sent - old_net_stats.bytes_sent) / interval

                writer.writerow({
                    'Timestep': timestap,
                    'DownloadSpeed': output_format_func(download_speed),
                    'UploadSpeed': output_format_func(upload_speed)
                })

                print(f"Download Speed (Mbit/s): {output_format_func(download_speed):^6} | Upload Speed (Mbit/s): {output_format_func(upload_speed):^4}", end='\r')
                old_net_stats = net_stats
                timestap += 1
                if timestap >= max_timestaps:
                    return

    except KeyboardInterrupt:
        print("\nUser interrupt")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network interface traffic monitoring")
    parser.add_argument("interface", help="Name of the network interface")
    parser.add_argument("interval", type=int, default=1, help="Interval between traffic measurements specified in seconds")
    parser.add_argument("-f", "--output_file", default="data.csv", help="Name of the CSV file to write statistics to")
    args = parser.parse_args()


    start_traffic_moniotring(args.interface, args.interval, args.output_file)