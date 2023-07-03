<template>
  <div>
    <input type="file" ref="fileInput" @change="handleFileUpload">
    <button @click="uploadFile">Загрузить</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const selectedFile = ref(null);

const handleFileUpload = (event) => {
  selectedFile.value = event.target.files[0];
};

const uploadFile = () => {
  const formData = new FormData();
  formData.append('file', selectedFile.value);

  axios.post('/api/face/process', formData)
    .then(response => {
      console.log('Success:', response.data);
      // Дополнительные действия после успешной загрузки
    })
    .catch(error => {
      console.error('Error:', error);
      // Обработка ошибок
    });
};
</script>
