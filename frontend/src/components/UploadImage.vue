<template>
  <div class="detection-upload">
    <div class="upload-image">
    <input type="file" ref="fileInput" @change="onFileChange" />
    <button class="upload-button" @click="uploadImage" :disabled="!selectedFile">Отправить</button>
    </div>

    <div v-if="task" class="image-preview">
      <h3>Превью</h3>
      <div>
      <img :src=result alt="Detected Faces">
      </div>
    </div>
  </div>
</template>


<style>

.detection-upload {
    display: inline-block;
  margin: auto;

  align-items: center;
  gap: 40px;
  width: 50%;
}

.upload-image{
  margin-top: 2%;
  position: relative;
    display: block;
  align-items: center;
}
.upload-button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;

  padding: 10px 16px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
}

.image-preview{
      display: inline-block;

  width: 50%;
}

</style>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedFile: null,
      task: null,
      result: null
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadImage() {
      // Создаем объект формы для отправки файла
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      axios
        .post('http://127.0.0.1:8000/api/face/process', formData)
        .then(response => {
          console.log(response)
          if (response.status === 201)  {
            this.task = response.data;
            this.checkTaskStatus();
            console.log(this.result)
          }
        })
        .catch(error => {
          console.error('Ошибка при загрузке файла:', error);
        });

    },
    checkTaskStatus() {
      const checkStatus = () => {
        axios
          .get(`http://127.0.0.1:8000/api/face/${this.task.id}`)
          .then(response => {
            const status = response.data.status;
            if (status === 'SUCCESS') {
              this.result = `http://127.0.0.1:8000/${response.data.result}`;
            } else if (status === 'PENDING' || status === 'PROCESSING') {
              // Если статус задачи еще не "SUCCESS", продолжаем опрашивать
              setTimeout(checkStatus, 500); // Опрос каждую секунду (1000 мс)
            }
          })
          .catch(error => {
            console.error('Ошибка при проверке статуса задачи:', error);
          });
      };

      // Начинаем опрос статуса задачи
      checkStatus();
    }

  }
};
</script>
