# Copyright (C) 2002, Thomas Hamelryck (thamelry@binf.ku.dk)
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.

"""Parser for PDB files."""


import warnings

try:
    import numpy
except ImportError:
    from Bio import MissingPythonDependencyError

    raise MissingPythonDependencyError(
        "Install NumPy if you want to use the PDB parser."
    ) from None

from Bio.File import as_handle
from Bio.PDB.PDBExceptions import PDBConstructionException
from Bio.PDB.PDBExceptions import PDBConstructionWarning
from Bio.PDB.StructureBuilder import StructureBuilder

# If PDB spec says "COLUMNS 18-20" this means line[17:20]


class PDBParser:
    """Parse a PDB file and return a Structure object."""

    def __init__(
        self,
        PERMISSIVE=True,
        structure_builder=None
    ):

        # get_header is not used but is left in for API compatibility
        if structure_builder is not None:
            self.structure_builder = structure_builder
        else:
            self.structure_builder = StructureBuilder()
        self.header = None
        self.line_counter = 0
        self.PERMISSIVE = bool(PERMISSIVE)

    # Public methods

    def get_structure(self, id, file):
        """Return the structure.
        Arguments:
         - id - string, the id that will be used for the structure
         - file - name of the PDB file OR an open filehandle
        """
        with warnings.catch_warnings():
            # Make a StructureBuilder instance
            # (pass id of structure as parameter)
            self.structure_builder.init_structure(id)

            with as_handle(file) as handle:
                lines = handle.readlines()
                if not lines:
                    raise ValueError("Empty file.")
                self._parse(lines)

            self.structure_builder.set_header(self.header)
            # Return the Structure instance
            structure = self.structure_builder.get_structure()
        return structure

    # Private methods

    def _parse(self, header_coords_trailer):
        """Parse the PDB file (PRIVATE)."""
        # Parse the atomic data; return the PDB file trailer
        self.trailer = self._parse_coordinates(header_coords_trailer)

    def _parse_coordinates(self, coords_trailer):
        """Parse the atomic data in the PDB file (PRIVATE)."""
        allowed_records = {
            "ATOM  ",
            "HETATM",
            "MODEL ",
            "ENDMDL",
            "TER   ",
            "ANISOU",
            # These are older 2.3 format specs:
            "SIGATM",
            "SIGUIJ",
            # bookkeeping records after coordinates:
            "MASTER",
            # Additional records to not worry about:
            "REMARK",
            "JRNL  ",
            "LINK  ",
            "HELIX ",
            "HETNAM",
            "FORMUL",
            "SOURCE",
            "SEQRES",
            "KEYWDS",
            "SCALE1",
            "SCALE2",
            "SCALE3",
            "SSBOND",
            "HEADER",
            "TITLE ",
            "CRYST1",
            "ORIGX1",
            "ORIGX2",
            "ORIGX3",
            "SHEET ",
            "HET   ",
            "COMPND",
            "REVDAT",
            "AUTHOR",
            "EXPDTA",
            "DBREF ",
            "HETSYN",

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
            line = coords_trailer[i].rstrip("\n")
            record_type = line[0:6]
            global_line_counter = self.line_counter + local_line_counter + 1
            structure_builder.set_line_counter(global_line_counter)
            if not line.strip():
                continue  # skip empty lines
            elif record_type == "ATOM  ":
                # Initialize the Model - there was no explicit MODEL record
                if not model_open:
                    structure_builder.init_model(current_model_id)
                    current_model_id += 1
                    model_open = 1
                fullname = line[12:16]
                # get rid of whitespace in atom names
                split_list = fullname.split()
                if len(split_list) != 1:
                    # atom name has internal spaces, e.g. " N B ", so
                    # we do not strip spaces
                    name = fullname
                else:
                    # atom name is like " CA ", so we can strip spaces
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
                    raise Exception(f'Residue sequence number on line {i+1}' +
                                    ' of pdb not formatted correctly.')
                icode = line[26]  # insertion code
                hetero_flag = " "
                residue_id = (hetero_flag, resseq, icode)
                # atomic coordinates
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                except Exception:
                    # Should we allow parsing to continue in permissive mode?
                    # If so, what coordinates should we default to?
                    #   Easier to abort!
                    raise PDBConstructionException(
                        "Invalid or missing coordinate(s) at line %i."
                        % global_line_counter
                    ) from None
                coord = numpy.array((x, y, z), "f")
                # occupancy & B factor
                # if not self.is_pqr:
                try:
                    occupancy = float(line[54:60])
                except Exception:
                    self._handle_PDB_exception(
                        "Invalid or missing occupancy", global_line_counter
                    )
                    occupancy = None  # Rather than arbitrary zero or one
                if occupancy is not None and occupancy < 0:
                    # TODO - Should this be an error in strict mode?
                    # self._handle_PDB_exception("Negative occupancy",
                    #                            global_line_counter)
                    # This uses fixed text so the warning occurs once only:
                    warnings.warn(
                        "Negative occupancy in one or more atoms",
                        PDBConstructionWarning,
                    )
                try:
                    bfactor = float(line[60:66])
                except Exception:
                    self._handle_PDB_exception(
                        "Invalid or missing B factor", global_line_counter
                    )
                    bfactor = 0.0  # PDB uses a default of zero if missing
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
                        self._handle_PDB_exception(message,
                                                   global_line_counter)
                elif(current_residue_id != residue_id or
                     current_resname != resname):
                    current_residue_id = residue_id
                    current_resname = resname
                    try:
                        structure_builder.init_residue(
                            resname, hetero_flag, resseq, icode
                        )
                    except PDBConstructionException as message:
                        self._handle_PDB_exception(message,
                                                   global_line_counter)
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
                    self._handle_PDB_exception(message, global_line_counter)
            elif record_type == "END   " or record_type == "CONECT":
                # End of atomic data, return the trailer
                self.line_counter += local_line_counter
                return coords_trailer[local_line_counter:]
            elif record_type not in allowed_records:
                warnings.warn(
                    "Ignoring unrecognized record '{}' at line {}".format(
                        record_type, global_line_counter
                    ),
                    PDBConstructionWarning,
                )
            local_line_counter += 1
        # EOF (does not end in END or CONECT)
        self.line_counter = self.line_counter + local_line_counter
        return []

    def _handle_PDB_exception(self, message, line_counter):
        """Handle exception (PRIVATE).
        This method catches an exception that occurs in the StructureBuilder
        object (if PERMISSIVE), or raises it again, this time adding the
        PDB line number to the error message.
        """
        message = "%s at line %i." % (message, line_counter)
        if self.PERMISSIVE:
            # just print a warning - some residues/atoms may be missing
            warnings.warn(
                "PDBConstructionException: %s\n"
                "Exception ignored.\n"
                "Some atoms or residues may be missing in the data structure."
                % message,
                PDBConstructionWarning,
            )
        else:
            # exceptions are fatal - raise again with new message
            # (including line nr)
            raise PDBConstructionException(message) from None
