<template>
  <div id="molecule" style="width: 500px; height: 500px; background-color: red;"></div>
</template>

<link rel="stylesheet" href="<%= BASE_URL %>/static/glmol/ChemDoodleWeb.css" type="text/css">
<script type="text/javascript" src="<%= BASE_URL %>/static/glmol/ChemDoodleWeb.js">
  export default {
    name: "molecule-output-display",
    description: "A molecule Viewer",
    props: {
      viewData: {
        type: Object,
        required: true,
      },
    },
    computed: {
      dataContainer() {
        if (this.viewData) {
          let transformer = new ChemDoodle.TransformCanvas3D('transformer', 500, 500, true);
          transformer.styles.set3DRepresentation('Ball and Stick');
          transformer.styles.backgroundColor = 'black';

          ChemDoodle.io.file.content(this.viewData["pdb"], function(fileContent) {
            var mol = ChemDoodle.readPDB(fileContent);
            transformer.loadMolecule(mol);
          }); 
          
          return transformer;
        } else {
          return null;
        }
      },
    },
  };
</script>