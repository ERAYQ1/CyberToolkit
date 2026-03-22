import os
import shutil
import tempfile

class DiskCleaner:
    def scan(self):
        """Scans common temporary/cache directories and returns found files with sizes."""
        targets = [
            (tempfile.gettempdir(), "Windows Temp"),
            (os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp"), "Kullanıcı Temp"),
            (os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "INetCache"), "Internet Önbelleği"),
            (os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "User Data", "Default", "Cache"), "Chrome Önbelleği"),
        ]

        results = []
        total_size = 0

        for path, label in targets:
            if not os.path.exists(path):
                continue
            folder_size = 0
            file_count = 0
            try:
                for root, dirs, files in os.walk(path):
                    for f in files:
                        try:
                            fp = os.path.join(root, f)
                            s = os.path.getsize(fp)
                            folder_size += s
                            file_count += 1
                        except (OSError, PermissionError):
                            pass
            except (OSError, PermissionError):
                pass

            results.append({
                "label": label,
                "path": path,
                "size_mb": round(folder_size / (1024 * 1024), 2),
                "files": file_count
            })
            total_size += folder_size

        return results, round(total_size / (1024 * 1024), 2)

    def clean(self, path):
        """Deletes files inside a given directory (does not delete the directory itself)."""
        deleted = 0
        errors = 0
        for root, dirs, files in os.walk(path):
            for f in files:
                try:
                    os.remove(os.path.join(root, f))
                    deleted += 1
                except (OSError, PermissionError):
                    errors += 1
            for d in dirs:
                try:
                    shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                except (OSError, PermissionError):
                    errors += 1
        return deleted, errors
