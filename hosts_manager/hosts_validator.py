import re
import socket
import ping3
from typing import Tuple

class HostsValidator:
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """验证IP地址格式"""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
            
        # 验证每个数字是否在0-255之间
        numbers = ip.split('.')
        return all(0 <= int(num) <= 255 for num in numbers)

    @staticmethod
    def validate_domain(domain: str) -> bool:
        """验证域名格式"""
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
        return bool(re.match(pattern, domain))

    @staticmethod
    def validate_hosts_entry(ip: str, domain: str) -> Tuple[bool, str]:
        """验证hosts记录格式"""
        if not HostsValidator.validate_ip(ip):
            return False, "Invalid IP address format"
            
        if not HostsValidator.validate_domain(domain):
            return False, "Invalid domain format"
            
        return True, "Valid hosts entry"

    @staticmethod
    def test_host_effectiveness(domain: str, expected_ip: str) -> Tuple[bool, str]:
        """测试hosts是否生效"""
        try:
            resolved_ip = socket.gethostbyname(domain)
            if resolved_ip == expected_ip:
                # 测试连通性
                response_time = ping3.ping(domain)
                if response_time is not None:
                    return True, f"Host is effective and responding (ping: {response_time:.2f}ms)"
                return True, "Host is effective but not responding to ping"
            return False, f"Host resolution mismatch: got {resolved_ip}, expected {expected_ip}"
        except socket.gaierror:
            return False, "Failed to resolve domain"
        except Exception as e:
            return False, f"Error testing host: {str(e)}"