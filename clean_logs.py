def celsius_converter(f_temp):
     c_temp = (float(f_temp) - 32) * 5 / 9
     return round(c_temp, 2)

def parse_and_clean(line):
     parts = line.split("|")

     if len(parts) != 5:
          return None

     cleaned_parts = []
     for part in parts:
          cleaned_parts.append(part.strip())

     timestamp, station_id, f_temp, humidity, sensor_status = cleaned_parts

     if not timestamp or not station_id or not f_temp or not humidity:
          return None

     if sensor_status != "ACTIVE":
          return None

     temp_check = f_temp.lstrip("-").replace(".", "", 1)
     humidity_check = humidity.replace(".", "", 1)

     if not temp_check.isdigit() or not humidity_check.isdigit():
          return None

     return timestamp, station_id, f_temp, humidity

skipped_count = 0

with open("environmental_raw.txt", "r") as input_file:
     with open("clean_logs.csv", "w") as output_file:
          output_file.write("Timestamp,StationID,Temp(C),Humidity(%)\n")

          for line in input_file:
               cleaned_row = parse_and_clean(line)

               if cleaned_row is None:
                    skipped_count += 1
                    continue

               timestamp, station_id, f_temp, humidity = cleaned_row
               c_temp = celsius_converter(f_temp)

               output_file.write(f"{timestamp},{station_id},{c_temp},{humidity}\n")

print(f"Skipped {skipped_count} invalid or inactive lines.")