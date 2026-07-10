import os
import time
from dataclasses import dataclass
from datetime import datetime


# ============================================================
# Data Models
# ============================================================

@dataclass
class FolderInfo:
    path: str
    size: int


@dataclass
class FileInfo:
    path: str
    size: int


@dataclass
class ScanStatistics:
    total_files: int = 0
    total_folders: int = 0
    total_size: int = 0


# ============================================================
# Utility Functions
# ============================================================

def format_size(size_bytes):

    if size_bytes == 0:
        return "0 B"

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB"
    ]

    size = float(size_bytes)

    for unit in units:

        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


# ============================================================
# Folder Scanner
# ============================================================

class FolderScanner:

    def __init__(self):

        self.statistics = ScanStatistics()

        self.folder_results = []

        self.file_results = []

        self.start_time = None


    def scan(self, root_folder):

        self.start_time = time.time()

        print()
        print("=" * 70)
        print("Folder Size Analyzer")
        print("=" * 70)

        print(f"Scanning Folder:")
        print(root_folder)

        print("-" * 70)


        self._scan_folder(root_folder)


        return self.folder_results



    def _scan_folder(self, folder_path):

        folder_size = 0


        try:

            self.statistics.total_folders += 1


            with os.scandir(folder_path) as entries:


                for entry in entries:

                    try:

                        if entry.is_file(
                            follow_symlinks=False
                        ):


                            size = entry.stat().st_size


                            folder_size += size


                            self.statistics.total_files += 1

                            self.statistics.total_size += size


                            self.file_results.append(
                                FileInfo(
                                    path=entry.path,
                                    size=size
                                )
                            )


                        elif entry.is_dir(
                            follow_symlinks=False
                        ):


                            subfolder_size = self._scan_folder(
                                entry.path
                            )


                            folder_size += subfolder_size



                    except PermissionError:
                        pass
                    

                    except Exception as error:

                        print(
                            f"Skipped {entry.path}: {error}"
                        )


            self.folder_results.append(
                FolderInfo(
                    path=folder_path,
                    size=folder_size
                )
            )



        except PermissionError:
            pass


        except Exception as error:

            print(
                f"Error scanning {folder_path}: {error}"
            )


        return folder_size



    def get_scan_time(self):

        return time.time() - self.start_time



# ============================================================
# Display Results in Terminal
# ============================================================

def display_results(scanner):


    print()

    print("=" * 70)
    print("SCAN STATISTICS")
    print("=" * 70)


    print(
        f"Total Files   : {scanner.statistics.total_files:,}"
    )


    print(
        f"Total Folders : {scanner.statistics.total_folders:,}"
    )


    print(
        f"Total Size    : {format_size(scanner.statistics.total_size)}"
    )


    print(
        f"Scan Time     : {scanner.get_scan_time():.2f} seconds"
    )


    print()

    print("=" * 70)
    print("TOP 20 LARGEST FOLDERS")
    print("=" * 70)


    sorted_folders = sorted(
        scanner.folder_results,
        key=lambda x: x.size,
        reverse=True
    )


    for index, folder in enumerate(
        sorted_folders[:20],
        start=1
    ):

        print(
            f"{index:02d}. "
            f"{format_size(folder.size):>12} "
            f"{folder.path}"
        )



def display_largest_files(scanner):


    print()

    print("=" * 70)
    print("TOP 20 LARGEST FILES")
    print("=" * 70)


    sorted_files = sorted(
        scanner.file_results,
        key=lambda x: x.size,
        reverse=True
    )


    for index, file in enumerate(
        sorted_files[:20],
        start=1
    ):

        print(
            f"{index:02d}. "
            f"{format_size(file.size):>12} "
            f"{file.path}"
        )



# ============================================================
# Save Output Report
# ============================================================

def create_output_file(scanner, folder):


    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    output_file = os.path.join(
        desktop,
        "output.txt"
    )


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as report:


        report.write("=" * 70 + "\n")
        report.write("Folder Size Analyzer Report\n")
        report.write("=" * 70 + "\n\n")


        report.write(
            f"Generated Time : {datetime.now()}\n"
        )


        report.write(
            f"Scan Time      : {scanner.get_scan_time():.2f} seconds\n\n"
        )


        report.write("=" * 70 + "\n")
        report.write("SCAN STATISTICS\n")
        report.write("=" * 70 + "\n\n")


        report.write(
            f"Total Files   : {scanner.statistics.total_files:,}\n"
        )


        report.write(
            f"Total Folders : {scanner.statistics.total_folders:,}\n"
        )


        report.write(
            f"Total Size    : {format_size(scanner.statistics.total_size)}\n"
        )


        report.write("\n\n")


        report.write("=" * 70 + "\n")
        report.write("TOP 20 LARGEST FOLDERS\n")
        report.write("=" * 70 + "\n\n")


        sorted_folders = sorted(
            scanner.folder_results,
            key=lambda x: x.size,
            reverse=True
        )


        for index, folder_info in enumerate(
            sorted_folders[:20],
            start=1
        ):

            report.write(
                f"{index:02d}. "
                f"{format_size(folder_info.size):>12} "
                f"{folder_info.path}\n"
            )


        report.write("\n\n")


        report.write("=" * 70 + "\n")
        report.write("TOP 20 LARGEST FILES\n")
        report.write("=" * 70 + "\n\n")


        sorted_files = sorted(
            scanner.file_results,
            key=lambda x: x.size,
            reverse=True
        )


        for index, file_info in enumerate(
            sorted_files[:20],
            start=1
        ):

            report.write(
                f"{index:02d}. "
                f"{format_size(file_info.size):>12} "
                f"{file_info.path}\n"
            )


    return output_file



# ============================================================
# Main Application
# ============================================================

def main():


    print("=" * 70)
    print("Folder Size Analyzer v0.5.1")
    print("=" * 70)


    folder = input(
        "\nEnter folder path to scan: "
    ).strip()

    # Convert drive letters like "C:" into "C:\"
    if (
        len(folder) == 2
        and folder[1] == ":"
        and folder[0].isalpha()
    ):
        folder += "\\"

    folder = os.path.abspath(folder)




    if not os.path.exists(folder):

        print(
            "Folder does not exist."
        )

        return



    scanner = FolderScanner()


    scanner.scan(folder)


    display_results(scanner)

    display_largest_files(scanner)


    print()

    print("=" * 70)
    print("Scan completed.")
    print("=" * 70)


    input(
        "\nPress Enter to save output.txt and exit..."
    )


    output_file = create_output_file(
        scanner,
        folder
    )


    print()

    print(
        "Report saved:"
    )

    print(
        output_file
    )


    print()

    print(
        "Completed Successfully"
    )



if __name__ == "__main__":

    main()