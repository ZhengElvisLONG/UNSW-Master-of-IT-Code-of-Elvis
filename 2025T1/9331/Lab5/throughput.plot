# 设置输出为PNG图像
set terminal png enhanced font "arial,12" size 800,600
set output "TCPThroughput.png"

# 设置图表标题和轴标签
set title "TCP Throughput"
set xlabel "Time [s]"
set ylabel "Throughput [Mbps]"

# 设置图例
set key top right

# 设置网格线使图表更易读
set grid

# 设置x轴和y轴范围
set xrange [0:10]
set yrange [0:1.6]

# 绘制数据
plot "tcp1.tr" using 1:2 title "TCP1 (n0->n5)" with linespoints lc rgb "blue" pt 7, \
     "tcp2.tr" using 1:2 title "TCP2 (n3->n5)" with linespoints lc rgb "red" pt 9
