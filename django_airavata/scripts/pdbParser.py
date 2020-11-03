import Bio.PDB
from PDBParser.myPDBParser import PDBParser
import sys
#sys.path.insert(1,'/PDBParser')
#import PDBParser.py
def validate_pdb(file_name):
    try:
        parser = PDBParser(PERMISSIVE=0)
        structure_id = "1fat"
        filename  = file_name
        structure = parser.get_structure(structure_id,filename)
        atoms = structure.get_atoms()
        for atom in atoms:
            a_info = atom.get_full_id()
            a_name = atom.get_name()
            a_chain_id = a_info[2]
            a_res_seq = a_info[3][1]            
            print(a_name+ ": " +a_chain_id + ", " + str(a_res_seq)) 
        
        return True

    except (Exception) as e:
        print("File contains irregularities, Running with permissive mode.")
        print(e)
        try:
            parser = PDBParser(PERMISSIVE=1)
            structure_id = "1fat"
            filename  = file_name
            structure = parser.get_structure(structure_id,filename)
            atoms = structure.get_atoms()
            for atom in atoms:
                a_info = atom.get_full_id()
                a_name = atom.get_name()
                a_chain_id = a_info[2]
                a_res_seq = a_info[3][1]            
                print(a_name+ ": " +a_chain_id + ", " + str(a_res_seq)) 
            
            return True
        except:
            print("File contains errors.")
            return False
                
def main():
    validate_pdb("input.pdb")
    return 0

if __name__ == "__main__":
    main()
