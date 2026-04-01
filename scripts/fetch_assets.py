import base64
import os
import re
import sys
import time
import urllib.request

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

def ensure_parent_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def extract_manual_proxy_rules(path):
    if not os.path.exists(path):
        return ["# 代理列表", ""]

    manual_lines = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("# GFW list (Synced from official gfwlist/gfwlist)"):
                break
            manual_lines.append(line.rstrip("\n"))

    while manual_lines and manual_lines[-1] == "":
        manual_lines.pop()

    if not manual_lines:
        return ["# 代理列表", ""]
    return manual_lines

def decode_gfwlist(content):
    text = content.strip()
    if "[AutoProxy" in text:
        return text

    normalized = "".join(text.split())
    padding = (-len(normalized)) % 4
    if padding:
        normalized += "=" * padding

    decoded = base64.b64decode(normalized).decode("utf-8", errors="ignore")
    return decoded

def normalize_domain(value):
    value = value.strip()
    value = re.sub(r"^[a-zA-Z]+://", "", value)
    value = value.split("/")[0]
    value = value.split(":")[0]
    value = value.lstrip(".")
    if not value or "*" in value or " " in value:
        return None
    if "." not in value:
        return None
    return value.lower()

def convert_gfw_rule(line):
    line = line.strip()
    if not line or line.startswith("!") or line.startswith("["):
        return None
    if line.startswith("@@") or line.startswith("/") or line.startswith("|http://127.0.0.1"):
        return None

    if line.startswith("||"):
        domain = normalize_domain(line[2:])
        if domain:
            return f"DOMAIN-SUFFIX,{domain}"
        return None

    if line.startswith("|"):
        domain = normalize_domain(line[1:])
        if domain:
            return f"DOMAIN,{domain}"
        return None

    domain = normalize_domain(line)
    if domain:
        return f"DOMAIN-SUFFIX,{domain}"
    return None

def process_gfwlist(content, existing_target):
    log("Processing GFWList...")
    decoded = decode_gfwlist(content)

    synced_rules = set()
    for line in decoded.splitlines():
        rule = convert_gfw_rule(line)
        if rule:
            synced_rules.add(rule)

    manual_lines = extract_manual_proxy_rules(existing_target)
    output_lines = list(manual_lines)
    if output_lines and output_lines[-1] != "":
        output_lines.append("")
    output_lines.extend([
        "# GFW list (Synced from official gfwlist/gfwlist)",
        *sorted(synced_rules),
        "",
    ])

    return "\n".join(output_lines), len(synced_rules)

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

    # 1. 处理 GFWList
    raw_gfwlist = fetch(SOURCES["GFWLIST"])
    if raw_gfwlist:
        formatted, count = process_gfwlist(raw_gfwlist, TARGETS["GFWLIST"])
        ensure_parent_dir(TARGETS["GFWLIST"])
        with open(TARGETS["GFWLIST"], "w", encoding="utf-8") as f:
            f.write(formatted)
        log(f"Updated GFWList with {count} synced rules")

    # 2. 处理 IPV4
    raw_ip = fetch(SOURCES["CHINA_IP"])
    if raw_ip:
        formatted = process_ip(raw_ip, is_v6=False)
        ensure_parent_dir(TARGETS["CHINA_IP"])
        with open(TARGETS["CHINA_IP"], "w", encoding="utf-8") as f:
            f.write(formatted)
        log("Updated China IPv4 List")

    # 3. 处理 IPV6
    raw_ipv6 = fetch(SOURCES["CHINA_IPV6"])
    if raw_ipv6:
        formatted = process_ip(raw_ipv6, is_v6=True)
        ensure_parent_dir(TARGETS["CHINA_IPV6"])
        with open(TARGETS["CHINA_IPV6"], "w", encoding="utf-8") as f:
            f.write(formatted)
        log("Updated China IPv6 List")

    log("Asset Fetcher Completed")

if __name__ == "__main__":
    main()
