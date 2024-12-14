"""
Python 3.12 CLI script to create C# reference assemblies for provided input directories

- Author: MaxWasUnavailable
- Licence: MIT
"""

import os
import argparse
import subprocess


class ReferenceCreator:
    """
    Class to create reference assemblies for provided filepaths
    """
    @staticmethod
    def create_reference_assemblies(_input_files: list[str], _out_dir: str):
        """
        Create reference assemblies from provided filepaths
        :param _input_files: List of input filepaths
        :param _out_dir: Output directory for reference assemblies
        """
        subprocess.run(["refasmer", "-v", "-O", _out_dir, "-c", "--all"] + _input_files)


class DLLFilter:
    """
    Class to filter .dll files from provided directory
    """
    default_filter = ["unityengine", "system.", "hbao", "mono.", "mscorlib", "visualscripting", "netstandard.dll"]

    @staticmethod
    def filter_dll_files(_input_dir: str, _filter: list[str] = None) -> list[str]:
        """
        Filter .dll files from provided directory
        :param _input_dir: Input directory to filter .dll files from
        :param _filter: List of partial strings to exclude from .dll files
        :return: List of .dll filepaths
        """
        dll_files = []
        for root, dirs, files in os.walk(_input_dir):
            for file in files:
                if file.endswith(".dll") and not any([partial in file.lower() for partial in _filter if _filter is not None]):
                    dll_files.append(os.path.join(root, file))

        return dll_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create C# reference assemblies from provided .dll files.')
    parser.add_argument('--inp', metavar='input', type=str, nargs='?', help='Input directory for .dll files.')
    parser.add_argument('--out', metavar='output', type=str, nargs='?', help='Output directory for reference assemblies.')
    parser.add_argument('--fil', metavar='filter', type=str, nargs='?', help=f"File with newline separated filter strings of .dll files to exclude. Uses partial matching.")
    parser.add_argument('--default_filter', action='store_true', help='Use default filter for .dll files.')
    args = parser.parse_args()

    # Check if input directory is provided
    if args.inp is None:
        raise ValueError("Input directory must be provided.")
    else:
        input_dir = args.inp

    # Check if input directory exists
    if not os.path.exists(input_dir):
        raise FileNotFoundError("Input directory does not exist.")

    # Check if output directory is provided
    if args.out is None:
        out_dir = os.path.join(input_dir, "refs")
    else:
        out_dir = args.out

    # Check if output directory exists
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    alt_filter = None

    # Check if default filter is enabled
    if args.default_filter:
        alt_filter = DLLFilter.default_filter

    # Check if filter file is provided
    if args.fil is not None:
        if not args.default_filter and alt_filter is not None:
            raise ValueError("Cannot provide filter file and use default filter at the same time.")
        if not os.path.exists(args.fil):
            raise FileNotFoundError("Filter file does not exist.")
        with open(args.fil, "r") as f:
            alt_filter = f.read().splitlines()

    # Gather input files
    input_files = DLLFilter.filter_dll_files(input_dir, alt_filter)

    print(f"Found {len(input_files)} .dll files in input directory.")

    # Create reference assemblies
    ReferenceCreator.create_reference_assemblies(input_files, out_dir)

    print(f"Reference assemblies created in {out_dir}.")
