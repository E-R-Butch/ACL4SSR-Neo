import sys
import time

def log(msg):
    # 强制刷新输出缓冲区，防止终端长时间无响应
    print(f"[*] {msg}", flush=True)

def main():
    log("Starting environment diagnostic...")
    log(f"Python interpreter: {sys.executable}")
    log(f"Python version: {sys.version}")
    
    # 模拟简单的逻辑处理
    log("Testing memory operations...")
    test_data = ["apple", "banana", "apple", "cherry"]
    unique_data = sorted(list(set(test_data)))
    log(f"Logic test (deduplication): {unique_data}")
    
    log("Diagnostic completed successfully!")

if __name__ == "__main__":
    main()
