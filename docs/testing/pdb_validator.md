## Requirements
1. Python version 3.6 or higher
	- [Download](https://www.python.org/downloads/)
3. Biopython version 1.77
	- [Installation Instructions](https://biopython.org/wiki/Download)

## Installation Instructions
1. Clone the project's Github repository:
	- `git clone https://github.com/cseseniordesign/rna-nanostructures.git`
2. Navigate into the project directory:
	- `cd rna-nanostructures`
3. Checkout the `develop` branch:
	- `git checkout develop`
4. Navigate to the directory containing the validator script:
	- `cd django_airavata/scripts`
5. Add the PDB file that should be parsed into the current directory
6. To run the parser/validator run the following command:
	- `python -c 'from pdbParser import validate_pdb; validate_pdb("FILENAME.pdb")` where `"FILENAME"` is replaced with the respective with the PDB filename
7. The expected output should be one of the following things:
	- A count of atoms that were within the file
	- An output containing the errors that exist in the file, such as formatting errors.
		* [NOTE] The parser is currently aware of many record types, but if a specific record type is currently unknown then it will display an warning message to indicate if a certain record is unknown/misaligned.
	- An example error output may look similar to the following:
		```Ignoring unrecognized record ' ATOM' at line 23```
		or for records that do not exist yet:
		```Ignoring unrecognized record 'EXPDTA' at line 24```
