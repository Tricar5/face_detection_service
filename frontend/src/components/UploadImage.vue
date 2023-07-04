<template>
  <div>
    <input type="file" ref="fileInput" multiple @change="handleFileChange">
    <button @click="uploadImages">Загрузить</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFiles: [],
      fileNames: []
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFiles = Array.from(event.target.files);
      this.fileNames = this.selectedFiles.map(file => file.name);
    },
    uploadImages() {
      const formData = new FormData();
      this.selectedFiles.forEach(file => {
        formData.append('files', file);
      });

      axios.post('http://localhost:8000/api/face/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        console.log('Успешно загружено', response);
      })
      .catch(error => {
        console.error('Ошибка загрузки', error);
      });
    }
  }
};
</script>
