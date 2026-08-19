import sys
import os
import binascii
import tempfile
from base64 import urlsafe_b64decode
from urllib.request import urlretrieve

def main():
    print("Special Command Protocol Translator")
    print("=" * 50)

    # 1. 检查参数
    if len(sys.argv) != 2:
        sys.exit("Usage: filename <url>")

    full_url = sys.argv
    
    # 2. 解析协议和数据部分
    if "://" not in full_url:
        sys.exit("Invalid URL format. Expected: protocol://base64data")
        
    protocol, b64_data = full_url.split("://", 1)

    # 3. 安全地解码 Base64
    try:
        # urlsafe_b64decode 需要填充 padding，有时需要手动处理
        # 添加必要的 padding
        missing_padding = len(b64_data) % 4
        if missing_padding:
            b64_data += '=' * (4 - missing_padding)
        cmd_bytes = urlsafe_b64decode(b64_data)
        cmd_str = cmd_bytes.decode('utf-8') # 假设命令是 UTF-8 编码
    except Exception as e:
        sys.exit(f"Base64 decoding error: {e}")

    # 4. 执行逻辑 (再次强调：生产环境严禁这样写！)
    if protocol == "cmdp":
        print(f"Warning: Executing command: {cmd_str}")
        # 建议使用 subprocess 替代 os.system 以获得更好的控制和安全性
        import subprocess
        try:
            # shell=True 是危险的，这里仅为了演示原意
            subprocess.run(cmd_str, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e}")
            
    elif protocol == "batp":
        # 获取系统的临时目录，而不是硬编码 %TMP%
        temp_dir = tempfile.gettempdir()
        bat_path = os.path.join(temp_dir, "scpt_temp.bat")
        
        print(f"Downloading batch file to: {bat_path}")
        try:
            # 注意：这里 cmd_str 应该是文件的 URL，而不是命令内容
            # 如果原意是 cmd_str 本身就是 bat 内容，则应写入文件而非 download
            # 假设原意是 urlretrieve 下载一个远程 bat 文件
            urlretrieve(cmd_str, bat_path)
            
            # 执行下载的 bat 文件
            os.system(f'cmd /c "{bat_path}"')
            
            # 清理临时文件
            if os.path.exists(bat_path):
                os.remove(bat_path)
        except Exception as e:
            print(f"Batch execution error: {e}")
    else:
        sys.exit("Unsupported protocol. Use 'cmdp' or 'batp'.")

    print("Done")

if __name__ == "__main__":
    main()
