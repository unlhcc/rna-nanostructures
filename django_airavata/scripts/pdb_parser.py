import warnings
from Bio.File import as_handle
from Bio.PDB.PDBExceptions import PDBConstructionException
from Bio.PDB.StructureBuilder import StructureBuilder
import logging

logger = logging.getLogger(__name__)

# Import required BIOPython dependencies
try:
    import numpy
except ImportError:
    from Bio import MissingPythonDependencyError

    raise MissingPythonDependencyError(
        'Install NumPy if you want to use the PDB parser.'
    ) from None


class PDBParser:
    '''Parse a PDB file and return a Structure object.'''

    def __init__(
        self,
        structure_builder=None
    ):

        # get_header is not used but is left in for API compatibility
        if structure_builder is not None:
            self.structure_builder = structure_builder
        else:
            self.structure_builder = StructureBuilder()
        self.header = None
        self.line_counter = 0

    # NOTE: Public methods
    def get_structure(self, id, file):
        '''Return the structure.
        Arguments:
         - id - string, the id that will be used for the structure
         - file - name of the PDB file OR an open filehandle
        '''
        with warnings.catch_warnings():
            # Make a StructureBuilder instance
            # (pass id of structure as parameter)
            self.structure_builder.init_structure(id)

            with as_handle(file) as handle:
                lines = [line.decode() for line in handle.readlines()]
                if not lines:
                    raise PDBConstructionException('Empty file.')
                self._parse(lines)

            self.structure_builder.set_header(self.header)
            # Return the Structure instance
            # structure = self.structure_builder.get_structure()
        return

    # NOTE: Private methods
    def _parse(self, header_coords_trailer):
        '''Parse the PDB file (PRIVATE).'''
        # Parse the atomic data; return the PDB file trailer
        self.trailer = self._parse_coordinates(header_coords_trailer)

    def _parse_coordinates(self, coords_trailer):
        '''Parse the atomic data in the PDB file (PRIVATE).'''
        allowed_records = {
            'ATOM  ',
            'HETATM',
            'MODEL ',
            'ENDMDL',
            'TER   ',
            'ANISOU',
            # These are older 2.3 format specs:
            'SIGATM',
            'SIGUIJ',
            # bookkeeping records after coordinates:
            'MASTER',
            # Additional records to not worry about:
            'REMARK',
            'JRNL  ',
            'LINK  ',
            'HELIX ',
            'HETNAM',
            'FORMUL',
            'SOURCE',
            'SEQRES',
            'KEYWDS',
            'SCALE1',
            'SCALE2',
            'SCALE3',
            'SSBOND',
            'HEADER',
            'TITLE ',
            'CRYST1',
            'ORIGX1',
            'ORIGX2',
            'ORIGX3',
            'SHEET ',
            'HET   ',
            'COMPND',
            'REVDAT',
            'AUTHOR',
            'EXPDTA',
            'DBREF ',
            'HETSYN',
        }

        local_line_counter = 0
        structure_builder = self.structure_builder
        current_model_id = 0

        # Flag we have an open model
        model_open = 0
        current_chain_id = None
        current_segid = None
        current_residue_id = None
        current_resname = None

        for i in range(0, len(coords_trailer)):
            line = coords_trailer[i].rstrip('\n')
            record_type = line[0:6]
            global_line_counter = self.line_counter + local_line_counter + 1
            structure_builder.set_line_counter(global_line_counter)
            if not line.strip():
                continue  # skip empty lines
            elif record_type.startswith('ATOM'):
                # Initialize the Model - there was no explicit MODEL record
                if len(line) > 80:
                    raise PDBConstructionException(
                        f'Record on line {i+1} of PBD is greater than 80 '
                        'characters in length'
                    )
                if not model_open:
                    structure_builder.init_model(current_model_id)
                    current_model_id += 1
                    model_open = 1
                fullname = line[12:16]
                try:
                    # check if starts with number
                    int(fullname)
                except Exception:
                    # if does not, continue
                    pass
                else:
                    raise PDBConstructionException(
                        f'Atom name on line {i+1} of PDB is formated incorrectly. '
                        f'Received: "{fullname}". '
                        'Expected an atom name beginning with a letter.'
                    )
                # get rid of whitespace in atom names
                split_list = fullname.split()
                if len(split_list) != 1:
                    # atom name has internal spaces, e.g. ' N B ', so
                    # we do not strip spaces
                    name = fullname
                else:
                    # atom name is like ' CA ', so we can strip spaces
                    name = split_list[0]
                altloc = line[16]
                resname = line[17:20].strip()
                chainid = line[21]
                try:
                    serial_number = int(line[6:11])
                except Exception:
                    serial_number = 0

                try:
                    resseq = int(line[22:26].split()[0])  # sequence identifier
                except Exception:
                    raise PDBConstructionException(
                        f'Residue sequence number on line {i+1} of PDB '
                        'formated incorrectly. Received: '
                        f'{line[22:26].split()[0]}'
                    )
                icode = line[26]  # insertion code
                hetero_flag = ' '
                residue_id = (hetero_flag, resseq, icode)
                # atomic coordinates
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                except Exception:
                    raise PDBConstructionException(
                        f'Invalid or missing coordinate(s) on line {i+1}. '
                        'X, Y, and Z coordinates should be provided as floats. '
                        f'Received: X: {line[30:38]}, Y: {line[38:46]}, '
                        f'Z: {line[46:54]}.'
                    )
                coord = numpy.array((x, y, z), 'f')

                # occupancy & B factor
                try:
                    occupancy = float(line[54:60])
                except Exception:
                    # Set the occupancy to 0.00 as a default if the provided
                    # value is incorrect
                    occupancy = 0.0

                    # NOTE: Uncomment to throw an exception for invalid
                    #       occupancy
                    # raise PDBConstructionException(
                    #     f'Invalid or missing occupancy on line {i+1}. '
                    #     'The occupancy should be provided as a float value. '
                    #     f'Received: {line[54:60]}.'
                    # )

                if occupancy is not None and occupancy < 0:
                    raise PDBConstructionException(
                        f'Negative occupancy on line {i+1}. '
                        'The expected occupancy should be non-negative.'
                    )

                try:
                    bfactor = float(line[60:66])
                except Exception:
                    # Set the B Factor to 0.00 as a default if the provided
                    # value is incorrect
                    bfactor = 0.0

                    # NOTE: Uncomment to throw an exception for invalid
                    #       B Factor
                    # raise PDBConstructionException(
                    #     f'Invalid or missing B factor on line {i+1}. '
                    #     'The B factor should be provided as a float value. '
                    #     f'Received: {line[60:66]}.'
                    # )

                segid = line[72:76]
                element = line[76:78].strip().upper()
                if current_segid != segid:
                    current_segid = segid
                    structure_builder.init_seg(current_segid)
                if current_chain_id != chainid:
                    current_chain_id = chainid
                    structure_builder.init_chain(current_chain_id)
                    current_residue_id = residue_id
                    current_resname = resname
                    try:
                        structure_builder.init_residue(
                            resname, hetero_flag, resseq, icode
                        )
                    except PDBConstructionException as message:
                        raise PDBConstructionException(
                            message + f' on line {i+1}.'
                        )
                elif(current_residue_id != residue_id or
                     current_resname != resname):

                    current_residue_id = residue_id
                    current_resname = resname

                    try:
                        structure_builder.init_residue(
                            resname, hetero_flag, resseq, icode
                        )
                    except PDBConstructionException as message:
                        raise PDBConstructionException(
                            message + f' on line {i+1}.'
                        )
                try:
                    structure_builder.init_atom(
                        name,
                        coord,
                        bfactor,
                        occupancy,
                        altloc,
                        fullname,
                        serial_number,
                        element,
                    )
                except PDBConstructionException as message:
                    raise PDBConstructionException(
                        message + f' on line {i+1}.'
                    )

            elif (record_type.startswith('END') or
                  record_type.startswith('CONECT') or
                  record_type.startswith('ENDMDL')):
                # End of atomic data, return the trailer
                self.line_counter += local_line_counter
                return coords_trailer[local_line_counter:]

            elif record_type not in allowed_records:
                # NOTE: The following code enables Users to determine
                #       whether an invalid record has been used

                # raise PDBConstructionException(
                #     f'Ignoring unrecognized record "{record_type}" '
                #     f'at line {i+1}'
                # )
                pass
            local_line_counter += 1

        # EOF (does not end in END or CONECT)
        self.line_counter = self.line_counter + local_line_counter
        return []


def validate_pdb(file):
    try:
        parser = PDBParser()
        structure_id = 'input_file'
        parser.get_structure(structure_id, file)
        return None
    except PDBConstructionException as pbd_e:
        return (
            str(pbd_e) +
            '\nExpected line formatting is as follows: '
            '"ATOM    220  OP2   A A 153     -20.313 -77.715  '
            '95.647  1.00 97.97           O1-"'
        )

    except Exception as e:
        # Catch all for alternative exceptions for non-handled exceptions
        logger.error(type(e), e, e.__traceback__)
        return
