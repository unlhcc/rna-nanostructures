<template>
  <div style="width: 500px; height: 500px; background-color: white;"  >
    {{ dataContainer }}
    <div id="container"></div>
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
          const files = this.viewData['pdb'];
          let transformBallAndStick = new ChemDoodle.TransformCanvas3D('transformBallAndStick', 500, 500);
          transformBallAndStick.styles.set3DRepresentation('Ball and Stick');
          transformBallAndStick.styles.atoms_useVDWDiameters_3D = false;
          transformBallAndStick.styles.backgroundColor = 'black';
          let changePdb = function(name) {
            let molecule = ChemDoodle.readPDB(files[name].join(''));
            try {
              transformBallAndStick.loadMolecule(molecule);
            } catch(error) {
              // // eslint-disable-next-line no-console
              // console.error(error)
            }
          }
          var select = document.createElement("select")
          select.name = "pdbs"
          select.id = "pdbs"
          select.onchange = function(value) {
            changePdb(value.target.selectedOptions[0].label)
          }
          
          let flag = false
          for (var key in files) {
            if (files.hasOwnProperty(key)) {      
              if (!flag){
                changePdb(key)
                flag = true
              }     
              var option = document.createElement("option");
              option.value = key;
              option.text = key;
              select.appendChild(option);
            }
            
          }        
          document.getElementById("container").appendChild(select);
        }
        return null;
      }
    }
  };
</script>

n