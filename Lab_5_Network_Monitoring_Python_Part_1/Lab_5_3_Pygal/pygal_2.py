import pygal

line_chart = pygal.Pie()
line_chart.title = "Protocol Breakdown"
line_chart.add('TCP', 10)
line_chart.add('UDP', 30)
line_chart.add('ICMP', 50)
line_chart.add('Others', 10)
line_chart.render_to_file('pygal_example_2.svg')