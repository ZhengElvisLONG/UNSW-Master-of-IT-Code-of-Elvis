import socket
import time
import random
import sys

# 参数检查
if len(sys.argv) != 3:
    print("Usage: python3 PingClient.py <host> <port>")
    sys.exit(1)

# 获取主机和端口
host = sys.argv[1]
port = int(sys.argv[2])

# 创建UDP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(0.6)  # 设置超时时间为600ms

# 初始化统计变量
total_packets = 15
seq_start = random.randint(10000, 20000)
rtt_list = []
packets_acknowledged = 0
start_time = time.time()

# 发送15个Ping请求
for i in range(total_packets):
    seq_num = seq_start + i
    send_time = time.time()
    message = f"PING {seq_num} {send_time}"
    client_socket.sendto(message.encode(), (host, port))

    try:
        # 接收响应
        response, server_address = client_socket.recvfrom(1024)
        recv_time = time.time()
        rtt = (recv_time - send_time) * 1000  # 转换为毫秒
        rtt_list.append(rtt)
        packets_acknowledged += 1
        print(f"PING to {host}, seq={seq_num}, rtt={rtt:.2f} ms")
    except socket.timeout:
        print(f"PING to {host}, seq={seq_num}, rtt=timeout")

# 计算统计信息
end_time = time.time()
total_transmission_time = (end_time - start_time) * 1000  # 转换为毫秒
packet_loss = (total_packets - packets_acknowledged) / total_packets * 100

# 计算最小、最大和平均RTT
min_rtt = min(rtt_list) if rtt_list else 0
max_rtt = max(rtt_list) if rtt_list else 0
avg_rtt = sum(rtt_list) / len(rtt_list) if rtt_list else 0

# 计算抖动（Jitter）
jitter = 0
if len(rtt_list) > 1:
    jitter = sum(abs(rtt_list[i] - rtt_list[i - 1]) for i in range(1, len(rtt_list))) / (len(rtt_list) - 1)

# 输出统计信息
print("\n--- Ping statistics ---")
print(f"Total packets sent: {total_packets}")
print(f"Packets acknowledged: {packets_acknowledged}")
print(f"Packet loss: {packet_loss:.2f}%")
print(f"Minimum RTT: {min_rtt:.2f} ms, Maximum RTT: {max_rtt:.2f} ms, Average RTT: {avg_rtt:.2f} ms")
print(f"Total transmission time: {total_transmission_time:.2f} ms")
print(f"Jitter: {jitter:.2f} ms")

# 关闭套接字
client_socket.close()