import os
import shutil
import toml

class BackupService:
    def backup(self, config_file_path):
        backup_file_path = config_file_path + '.bak'
        if os.path.exists(backup_file_path):
            os.remove(backup_file_path)
        shutil.copyfile(config_file_path, backup_file_path)

    def rollback(self, config_file_path):
        backup_file_path = config_file_path + '.bak'
        if not os.path.exists(backup_file_path):
            raise FileNotFoundError(f"No backup file found for {config_file_path}")
        os.remove(config_file_path)
        shutil.copyfile(backup_file_path, config_file_path)
