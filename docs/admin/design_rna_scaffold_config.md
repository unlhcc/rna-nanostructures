# These are the values used to configure the Design RNA Scaffold application in the workspace

The configuration of the application was also shown in a tutorial on Box.

## Inputs

### PDB input
#### Title: Base Input PDB
#### Type: URI
#### Application Input: `--pdb`
#### Metadata
```
{
    "editor": {
        "validations": [{"type": "pdbfile"}]
    }
}
```

### Start base pair
#### Title: Start Base Pair
#### Type: STRING
#### Application Input: `--start_bp`

### End base pair
#### Title: End Base Pair
#### Type: STRING
#### Application Input: `--end_bp`

### Designs
#### Title: Number of Designs
#### Type: INTEGER
#### Application Input: `--designs`

### Sequences
#### Title: Number of Design Sequences
#### Type: INTEGER
#### Application Input: `--sequences_per_design`

### CLI Args
#### Title: Other CLI Args
#### Type: STRING
#### Default Value: `--search_type mc --motif_path flex_helices,twoway,flex_helices,twoway,flex_helices --dump_pdbs --thermo_fluc`
#### Readonly: true

## Outputs

### Scores
#### Title: Design Statistics
#### Type: URI
#### Value: default.scores
#### Metadata:
```
{
    "file-metadata": {"mime-type": "text/plain"}
    "output-view-providers": ["pdb_table_viewer"]
}
```

### PDBs
#### Title: Designed Structures
#### Type: URI COLLECTION
#### Value: design.*.pdb
#### Metadata:
```
{
    "file-metadata": {"mime-type": "text/plain"}
    "output-view-providers": ["molecule_viewer"]
}
```

## Deployment

### Binary
`/RNAMake/bin/design_rna_scaffold`

### PreJob Commands
- `+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/djw8605/rnamake:latest"`
- `requirements = isUndefined(GLIDEIN_ResourceName) == False && HAS_SINGULARITY == TRUE`
- `transfer_executable = false`
