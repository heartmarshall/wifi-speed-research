import re
import csv
import sys

def parse_iperf_output(output):
    results = re.findall(r'(\d+)+\.\d+-\d+\.\d+\s+sec\s+(\d+\.*\d+)\s+\w*\s+(\d+\.*\d+)\s+Mbits/sec', output, re.DOTALL)
    return results

def write_to_csv(data, csv_filename):
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Interval', 'Transfer (MBytes)', 'Bitrate (Mbits/sec)'])

        for interval, transfer, bitrate in data:
            writer.writerow([interval, transfer, bitrate])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: need filename")
        sys.exit(1)

    input_filename = 'iperf_data.txt'  
    output_filename = sys.argv[1]

    with open(input_filename, 'r') as file:
        log_data = file.read()

    parsed_data = parse_iperf_output(log_data)

    write_to_csv(parsed_data, output_filename)

    print(f"CSV file '{output_filename}' has been created.")
