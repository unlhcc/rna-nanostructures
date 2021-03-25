<template>
  <div>
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
    mounted: function(){
      this.$nextTick(function(){
        var link = document.createElement('link');
        link.rel = "styleSheet";
        link.href = "../../../static/glmol/ChemDoodleWeb.css"
        link.type = "text/css";

        var script = document.createElement('script');
        script.type = "text/javascript";
        script.src = "../../../static/glmol/ChemDoodleWeb.js";
        
        var head = document.getElementsByTagName("head")[0];
        
        head.append(script);
        head.append(link);
      })
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
            transformBallAndStick.loadMolecule(molecule);
          }
          let size = 0;
          for (var tempKey in files) {
              if (files.hasOwnProperty(tempKey)){
                size++;
              }
          }

          // eslint-disable-next-line no-console
          console.log(size);

          if(size === 1) {
              changePdb(tempKey);
          } else {
            var select = document.createElement("select");
            select.name = "pdbs";
            select.id = "pdbs";
            select.style = "margin-bottom: 1em";
            select.onchange = function(value) {
              changePdb(value.target.selectedOptions[0].label);
            }
            
            let flag = false;
            for (var key in files) {
              if (files.hasOwnProperty(key)) {      
                if (!flag){
                  changePdb(key);
                  flag = true;
                }     
                var option = document.createElement("option");
                option.value = key;
                option.text = key;
                select.appendChild(option);
              }
            }        
            document.getElementById("container").appendChild(select);
          }
        }
        return null;
      }
    }
  };
</script>