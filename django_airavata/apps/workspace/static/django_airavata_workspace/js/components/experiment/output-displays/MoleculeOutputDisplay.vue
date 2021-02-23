<template>
  <img :src="dataUrl" />
</template>

<script>
//THIS IS CODE PULLED FROM ImageOutputDisplay.vue to be filler so it can be imported into OutputDisplayContainer.vue
//TODO: Write this code correctly.
export default {
  name: "molecule-output-display",
  props: {
    viewData: {
      type: Object,
      required: true,
    },
  },
  computed: {
    dataUrl() {
      if (this.viewData) {
        return `data:${this.viewData["mime-type"]};base64,${this.viewData["image"]}`;
      } else {
        return null;
      }
    },
  },
};
</script>