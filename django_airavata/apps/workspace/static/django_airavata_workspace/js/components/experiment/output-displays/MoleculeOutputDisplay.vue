<template>
  <div style="width: 500px; height: 500px; background-color: black;">{{ dataContainer }}</div>
</template>

<script>
  import "./static/css/css/ChemDoodleWeb.css"
  // import * as ChemDoodle from "./static/ChemDoodleWeb/install/ChemDoodleWeb.js"
  import ChemDoodle from "./static/js/ChemDoodleWeb.js"

  export default {
    name: "molecule-output-display",
    description: "Molecule Viewer",
    props: {
      viewData: {
        type: Object,
        required: true,
      },
    },
    computed: {
      dataContainer: function() {
        if (this.viewData) {
          let transformer = new ChemDoodle.TransformCanvas3D('transformer', 500, 500, true);
          transformer.styles.set3DRepresentation('Ball and Stick');
          transformer.styles.backgroundColor = 'black';
          var mol = ChemDoodle.readPDB(this.viewData["pdb"]);
          transformer.loadMolecule(mol);

          // ChemDoodle.io.file.content(this.viewData["pdb"], function(fileContent) {
          //   var mol = ChemDoodle.readPDB(fileContent);
          //   transformer.loadMolecule(mol);
          // }); 

          return transformer;
        } else {
          return null;
        }
      },
    },
  };
</script>