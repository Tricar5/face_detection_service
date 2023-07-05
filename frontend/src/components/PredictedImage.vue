<template>
  <div class="task-refresher">
  <button @click="refresh" class="refresh-button button-3">Refresh</button>
    </div>
  <div class="task-container">
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

.task-refresher{
  margin: auto;
  position: relative;
  display: flex;
  height: 5%;
}
.refresh-button{
  margin-left: 85%;
}

.button-3 {
  appearance: none;
  background-color: #2ea44f;
  border: 1px solid rgba(27, 31, 35, .15);
  border-radius: 6px;
  box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
  box-sizing: border-box;
  color: #fff;
  cursor: pointer;
  display: inline-block;
  font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  padding: 6px 16px;
  text-align: center;
  text-decoration: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: middle;
  white-space: nowrap;
}

.button-3:focus:not(:focus-visible):not(.focus-visible) {
  box-shadow: none;
  outline: none;
}

.button-3:hover {
  background-color: #2c974b;
}

.button-3:focus {
  box-shadow: rgba(46, 164, 79, .4) 0 0 0 3px;
  outline: none;
}

.button-3:disabled {
  background-color: #94d3a2;
  border-color: rgba(27, 31, 35, .1);
  color: rgba(255, 255, 255, .8);
  cursor: default;
}

.button-3:active {
  background-color: #298e46;
  box-shadow: rgba(20, 70, 32, .2) 0 1px 0 inset;
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
