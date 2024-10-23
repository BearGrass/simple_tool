import os
import shutil
from datetime import datetime
import platform
from typing import Optional

class HostsBackup:
    def __init__(self):
        self.backup_dir = self._get_backup_dir()
        os.makedirs(self.backup_dir, exist_ok=True)
        
    def _get_backup_dir(self) -> str:
        """获取备份目录路径"""
        system = platform.system().lower()
        if system == "windows":
            return os.path.join(os.getenv('APPDATA'), 'HostsManager', 'backups')
        elif system in ("linux", "darwin"):
            return os.path.expanduser('~/.hosts_manager/backups')
        else:
            raise OSError(f"Unsupported operating system: {system}")

    def create_backup(self, hosts_path: str) -> Optional[str]:
        """创建hosts文件备份"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(self.backup_dir, f'hosts_backup_{timestamp}')
            shutil.copy2(hosts_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Backup failed: {str(e)}")
            return None

    def restore_backup(self, backup_path: str, hosts_path: str) -> bool:
        """从备份恢复hosts文件"""
        try:
            shutil.copy2(backup_path, hosts_path)
            return True
        except Exception as e:
            print(f"Restore failed: {str(e)}")
            return False

    def list_backups(self) -> list:
        """列出所有备份文件"""
        try:
            return sorted([f for f in os.listdir(self.backup_dir) 
                         if f.startswith('hosts_backup_')])
        except Exception as e:
            print(f"Failed to list backups: {str(e)}")
            return []