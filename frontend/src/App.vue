<template>
  <img alt="Face Detector"  src="./assets/face.png" style="width: 200px; height: 200px;">
  <UploadImage msg="Please import your file!"/>
  <PredictedImage align="center"></PredictedImage>
</template>

<script>

import UploadImage from './components/UploadImage.vue'
import PredictedImage from "@/components/PredictedImage.vue";
export default {
  name: 'App',
  components: {
    UploadImage,
    PredictedImage
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
