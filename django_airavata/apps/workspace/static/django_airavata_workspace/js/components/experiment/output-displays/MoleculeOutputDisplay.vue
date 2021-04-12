<template>
  <div>
    <b-dropdown v-if="showMenu" :text="currentPdb" class="m-md-2">
      <b-dropdown-item
      v-for="(value, name) in viewData['pdb']"
      :key="name"
      @click="setCurrentPdb(name)"
      >{{ name }}
      </b-dropdown-item>
    </b-dropdown>
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
    mounted(){
      this.$nextTick(function(){
        if(!document.getElementById("chemdoodle-script")){
          var link = document.createElement("link");
          link.rel = "styleSheet";
          link.href = "../../../static/glmol/ChemDoodleWeb.css"
          link.type = "text/css";

          var script = document.createElement("script");
          script.type = "text/javascript";
          script.src = "../../../static/glmol/ChemDoodleWeb.js";
          script.id = "chemdoodle-script";
          
          var head = document.getElementsByTagName("head")[0];
          
          head.append(script);
          head.append(link);
        }
      })
    },
    beforeUpdate(){
      if (this.moleculeViewer === undefined) {
        this.moleculeViewer = this.createMoleculeViewer();
      }
    },
    data() {
      return {
        currentPdb: undefined,
        moleculeViewer: undefined
      }
    },
    watch: {
      currentPdb: function () {
        this.changePdb(this.currentPdb);
      }
    },
    computed: {
      showMenu() {
        let size = 0
        for (var tempKey in this.viewData["pdb"]) {
          if (this.viewData["pdb"].hasOwnProperty(tempKey)){
            if(size === 0){
              this.setCurrentPdb(tempKey);
            }
            size++;
          }
        }
        return size > 1;
      }
    },
    methods: {
      createMoleculeViewer() {
        let viewer = new ChemDoodle.TransformCanvas3D(
          "transformBallAndStick", 500, 500);
        viewer.styles.set3DRepresentation("Ball and Stick");
        viewer.styles.atoms_useVDWDiameters_3D = false;
        viewer.styles.backgroundColor = "black";
        return viewer;
      },
      setCurrentPdb(key){
        this.currentPdb = key;
      },
      changePdb(name) {
        let molecule = ChemDoodle.readPDB(this.viewData["pdb"][name].join(""));
        this.moleculeViewer.loadMolecule(molecule);
      },
    }
  };
</script>