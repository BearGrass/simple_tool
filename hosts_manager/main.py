from hosts_manager import HostsManager
from hosts_validator import HostsValidator
from hosts_backup import HostsBackup
import argparse

def main():
    parser = argparse.ArgumentParser(description='Hosts File Manager')
    parser.add_argument('action', choices=['add', 'remove', 'list', 'backup', 
                                         'restore', 'test', 'validate'])
    parser.add_argument('--ip', help='IP address for the hosts entry')
    parser.add_argument('--domain', help='Domain for the hosts entry')
    parser.add_argument('--backup-file', help='Backup file to restore from')
    
    args = parser.parse_args()

    hosts_manager = HostsManager()
    hosts_validator = HostsValidator()
    hosts_backup = HostsBackup()

    try:
        if args.action == 'add':
            if not all([args.ip, args.domain]):
                print("Both --ip and --domain are required for add action")
                return
                
            # 验证格式
            valid, message = hosts_validator.validate_hosts_entry(args.ip, args.domain)
            if not valid:
                print(f"Validation failed: {message}")
                return
                
            if hosts_manager.add_host(args.ip, args.domain):
                print(f"Successfully added {args.domain} -> {args.ip}")
            else:
                print(f"Entry for {args.domain} already exists")

        elif args.action == 'remove':
            if not args.domain:
                print("--domain is required for remove action")
                return
                
            if hosts_manager.remove_host(args.domain):
                print(f"Successfully removed entry for {args.domain}")
            else:
                print(f"No entry found for {args.domain}")

        elif args.action == 'list':
            hosts_list = hosts_manager.list_hosts()
            if hosts_list:
                print("Current hosts entries:")
                for ip, domain in hosts_list:
                    print(f"{ip}\t{domain}")
            else:
                print("No hosts entries found")

        elif args.action == 'backup':
            backup_path = hosts_backup.create_backup(hosts_manager.hosts_path)
            if backup_path:
                print(f"Backup created at: {backup_path}")
            else:
                print("Backup failed")

        elif args.action == 'restore':
            if not args.backup_file:
                print("--backup-file is required for restore action")
                return
                
            if hosts_backup.restore_backup(args.backup_file, hosts_manager.hosts_path):
                print("Hosts file restored successfully")
            else:
                print("Failed to restore hosts file")

        elif args.action == 'test':
            if not all([args.ip, args.domain]):
                print("Both --ip and --domain are required for test action")
                return
                
            effective, message = hosts_validator.test_host_effectiveness(
                args.domain, args.ip)
            print(f"Test result: {message}")

        elif args.action == 'validate':
            if not all([args.ip, args.domain]):
                print("Both --ip and --domain are required for validate action")
                return
                
            valid, message = hosts_validator.validate_hosts_entry(args.ip, args.domain)
            print(f"Validation result: {message}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()