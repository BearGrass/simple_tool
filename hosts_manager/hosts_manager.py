import os
import platform
import shutil
from typing import List, Tuple

class HostsManager:
    def __init__(self):
        self.hosts_path = self._get_hosts_path()
        
    def _get_hosts_path(self) -> str:
        """根据操作系统返回hosts文件路径"""
        system = platform.system().lower()
        if system == "windows":
            return r"C:\Windows\System32\drivers\etc\hosts"
        elif system in ("linux", "darwin"):  # Linux or macOS
            return "/etc/hosts"
        else:
            raise OSError(f"Unsupported operating system: {system}")

    def read_hosts(self) -> List[str]:
        """读取hosts文件内容"""
        try:
            with open(self.hosts_path, 'r') as f:
                return f.readlines()
        except Exception as e:
            raise Exception(f"Error reading hosts file: {str(e)}")

    def write_hosts(self, content: List[str]) -> None:
        """写入hosts文件内容"""
        try:
            with open(self.hosts_path, 'w') as f:
                f.writelines(content)
        except Exception as e:
            raise Exception(f"Error writing hosts file: {str(e)}")

    def add_host(self, ip: str, domain: str) -> bool:
        """添加一条hosts记录"""
        content = self.read_hosts()
        new_entry = f"{ip}\t{domain}\n"
        
        # 检查是否已存在
        for line in content:
            if line.strip() and not line.startswith('#'):
                if domain in line:
                    return False
                
        content.append(new_entry)
        self.write_hosts(content)
        return True

    def remove_host(self, domain: str) -> bool:
        """删除指定域名的hosts记录"""
        content = self.read_hosts()
        new_content = []
        found = False
        
        for line in content:
            if line.strip() and not line.startswith('#'):
                if domain not in line:
                    new_content.append(line)
                else:
                    found = True
            else:
                new_content.append(line)
                
        if found:
            self.write_hosts(new_content)
        return found

    def list_hosts(self) -> List[Tuple[str, str]]:
        """列出所有hosts记录"""
        content = self.read_hosts()
        hosts_list = []
        
        for line in content:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 2:
                    hosts_list.append((parts[0], parts[1]))
                    
        return hosts_list
    