<template>
  <div style="width: 500px; height: 500px; background-color: white;" >
    {{ dataContainer }}
    <canvas id="transformBallAndStick"></canvas>
  </div>
</template>

<script>
  /* globals ChemDoodle */

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
      dataContainer() {
        if (this.viewData['pdb']) {
          let transformBallAndStick = new ChemDoodle.TransformCanvas3D('transformBallAndStick', 500, 500);
          transformBallAndStick.styles.set3DRepresentation('Ball and Stick');
          transformBallAndStick.styles.backgroundColor = 'black';
          let molecule = ChemDoodle.readPDB(this.viewData["pdb"].join(''), 1);
          transformBallAndStick.loadMolecule(molecule);  
        }

        return null;
      }
    }
  };
</script>

