<template>
  <div>
    <input type="file" ref="fileInput" accept="image/*" />
    <button @click="uploadPhoto">Отправить</button>
    <div v-if="task !== null">
      <h5>Результат предсказания</h5>
      <span>{{task}}</span>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      task: null
    };
  },
  methods: {
    uploadPhoto() {
      const file = this.$refs.fileInput.files[0];
      const formData = new FormData();
      formData.append('files', file);
      this.task = async (newUser) => {
        try {
          const response = axios.post('http://localhost:8000/api/face/process', formData,
            {headers: {"Content-Type": "multipart/form-data"}}
          )
          return response.data
        }
        except
      };


    },
    fetchPhoto() {
      const detectionUrl = `http://localhost:8000/api/face/result/${this.task.id}/detection`;

      axios.get(detectionUrl, { responseType: 'blob' })
        .then(response => {
          if (response.status === 200) {
            const result = response.data;
            this.task.detection = URL.createObjectURL(result);
          } else {
            console.error('Error fetching detection photo');
          }
        })
        .catch(error => {
          console.error('Error fetching detection photo', error);
        });
    }
  }
};
</script>
