# Reference Assembly Script

A simple Python CLI script to generate reference assemblies in bulk,
using [JetBrains Refasmer](https://github.com/JetBrains/Refasmer).

## Usage

> All arguments:

```bash
python create_ref_assemblies.py --inp ./some_dir --out ./output_dir --fil ./filter_file.txt
```

> Minimal example:

```bash
python create_ref_assemblies.py --inp ./some_dir
```

## Arguments

- `--inp`: Input directory containing assemblies to be processed.
- `--out`: Output directory to store the generated reference assemblies.
    - Default: `input directory` + `/refs`
- `--fil`: Filter file containing a list of strings to filter out assemblies from processing.
    - Default: `"unityengine"`, `"system."`, `"hbao"`, `"mono."`, `"mscorlib"`, `"visualscripting"`, `"netstandard.dll"`

## Requirements

- Python 3.12 (probably works with older versions too)
- [JetBrains Refasmer](https://github.com/JetBrains/Refasmer)
  - The dotnet tool: `dotnet tool install -g JetBrains.Refasmer.CliTool`