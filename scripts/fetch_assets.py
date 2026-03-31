import os
import sys
import urllib.request
import time

# 资源链接
SOURCES = {
    "GFWLIST": "https://raw.githubusercontent.com/gfwlist/gfwlist/refs/heads/master/list.txt",
    "CHINA_IP": "https://raw.githubusercontent.com/mayaxcn/china-ip-list/refs/heads/master/chnroute.txt",
    "CHINA_IPV6": "https://raw.githubusercontent.com/mayaxcn/china-ip-list/refs/heads/master/chnroute_v6.txt"
}

# 目标文件
TARGETS = {
    "GFWLIST": "Clash/Core/ProxyGFWlist.list",
    "CHINA_IP": "Clash/Ingredients/China/ChinaIp.list",
    "CHINA_IPV6": "Clash/Ingredients/China/ChinaIpV6.list"
}

def log(msg):
    print(f"[*] {msg}", flush=True)

def fetch(url):
    log(f"Fetching from {url}...")
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        log(f"Error fetching URL: {str(e)}")
        return None

def process_gfwlist(content):
    # 此处省略复杂的 GFWList Base64 解码，目前先模拟简单同步逻辑
    # 实际应用中需要 base64 和本地 MyList 合并
    log("Processing GFWList (Simulated manual sync logic)...")
    return content # 此处需要集成之前的 parse_gfwlist 逻辑

def process_ip(content, is_v6=False):
    prefix = "IP-CIDR6" if is_v6 else "IP-CIDR"
    lines = content.strip().split("\n")
    processed = []
    
    # 添加文件头
    processed.append(f"# 内容：中国{'IPv6' if is_v6 else 'IPv4'}地址段")
    processed.append(f"# 更新：{time.strftime('%Y-%m-%d %H:%M:%S')}")
    processed.append("")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        processed.append(f"{prefix},{line},no-resolve")
    
    return "\n".join(processed)

def main():
    log("Asset Fetcher Started")
    
    # 1. 处理 IPV4
    raw_ip = fetch(SOURCES["CHINA_IP"])
    if raw_ip:
        formatted = process_ip(raw_ip, is_v6=False)
        with open(TARGETS["CHINA_IP"], "w", encoding="utf-8") as f:
            f.write(formatted)
        log("Updated China IPv4 List")

    # 2. 处理 IPV6
    raw_ipv6 = fetch(SOURCES["CHINA_IPV6"])
    if raw_ipv6:
        formatted = process_ip(raw_ipv6, is_v6=True)
        with open(TARGETS["CHINA_IPV6"], "w", encoding="utf-8") as f:
            f.write(formatted)
        log("Updated China IPv6 List")

    log("Asset Fetcher Completed")

if __name__ == "__main__":
    main()
