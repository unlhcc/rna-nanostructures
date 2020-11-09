from PDBParser.myPDBParser import PDBParser


def validate_pdb(file_name):
    try:
        parser = PDBParser(PERMISSIVE=0)
        structure_id = "inputFile"
        filename = file_name
        structure = parser.get_structure(structure_id, filename)
        atoms = structure.get_atoms()
        atomCount = 0
        for atom in atoms:
            atomCount += 1
        print("Anount of atoms: " + str(atomCount))
        return True
    except (Exception) as e:
        print("File contains irregularities, Running with permissive mode.")
        print(e)
        try:
            parser = PDBParser(PERMISSIVE=1)
            structure_id = "inputFile"
            filename = file_name
            parser.get_structure(structure_id, filename)
            return True
        except (Exception) as e:
            print("File contains errors.")
            print(e)
            return False


def main():
    validate_pdb("1re2.pdb")
    return 0


if __name__ == "__main__":
    main()
