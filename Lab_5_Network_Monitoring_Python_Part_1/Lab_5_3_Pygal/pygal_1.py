import pygal


x_time = []
out_octets = []
out_packets = []
in_octets = []
in_packets = []

with open('results.txt', 'r') as f:
    for line in f.readlines():
        # eval(line) reads in each line as dictionary instead of string
        line = eval(line)
        x_time.append(line['Time'])
        out_packets.append(float(line['Eth0-1_Out_uPackets']))
        out_octets.append(float(line['Eth0-1_Out_Octet']))
        in_packets.append(float(line['Eth0-1_In_uPackets']))
        in_octets.append(float(line['Eth0-1_In_Octet']))

line_chart = pygal.Line()
line_chart.title = "IOS_R_1.TEST E0/1"
line_chart.x_labels = x_time
line_chart.add('out_octets', out_octets)
line_chart.add('out_packets', out_packets)
line_chart.add('in_octets', in_octets)
line_chart.add('in_packets', in_packets)
line_chart.render_to_file('pygal_example_1.svg')