<template>
  <div class="task-container">
        <button @click="refresh" class="refresh-button">Refresh</button>
    <div v-for="task in tasksData" :key="task.id" class="task">
      <div class="task-info">
        <span :class="['task-status', { 'success': task.status === 'SUCCESS' }]">
          {{ task.status }}
        </span>
        <span class="task-id">
          {{ task.id }}
        </span>
      </div>
      <div class="task-actions">
        <button @click="togglePhoto(task)">{{ task.showPhoto ? 'Hide' : 'Show' }}</button>
      </div>
      <div v-if="task.showPhoto" class="task-photo">
        <img :src="task.photo" alt="Photo" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.task-container {
  width: 80%;
  margin: 0 auto;
  margin-top: 30px;
}

.task {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  display: flex;
  text-align: left;

}

.task-info {
  flex: 1;
}

.task-id {
  text-align: left;
  font-weight: bold;
}

.task-status {
  font-weight: bold;
  margin-right: 10px;
}

.task-status.success {
  color: green;
}

.task-actions {
  position: absolute;
  margin-left: 68%;
}

.butt
.task-photo {
  position: relative;
  left: 0;
  right: 0;
  margin-bottom: 1%;
  margin-top: 3%;
  text-align: center;
}
.task.show-photo .task-photo {
  display: block;
}
</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tasksData: []
    };
  },
  mounted() {
    this.fetchTasks();
  },
  methods: {
    fetchTasks() {
      axios.get('http://localhost:8000/api/face/tasks/list')
        .then(response => {
          this.tasksData = response.data.data.map(task => ({
            ...task,
            showPhoto: false
          }));
        })
        .catch(error => {
          console.error('Error fetching tasks', error);
        });
    },
    togglePhoto(task) {
      task.showPhoto = !task.showPhoto;
      if (task.showPhoto && !task.photo) {
        this.fetchPhoto(task);
      }
    },
    fetchPhoto(task) {
      axios.get(`http://localhost:8000/api/face/result/${task.id}`, { responseType: 'arraybuffer' })
        .then(response => {
          const base64Image = btoa(
            new Uint8Array(response.data)
              .reduce((data, byte) => data + String.fromCharCode(byte), '')
          );
          task.photo = `data:${response.headers['content-type']};base64,${base64Image}`;
        })
        .catch(error => {
          console.error('Error fetching photo', error);
        });
    },
    refresh() {
      this.fetchTasks();
    }
  }
};
</script>
