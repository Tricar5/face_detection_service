<template>
  <div>
    <table class="custom-table">
      <thead>
        <tr>
          <th>Task ID</th>
          <th>Status</th>
          <th>Result</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.id">
          <td>{{ task.id }}</td>
          <td>{{ task.status }}</td>
          <td><a :href="task.result" target="_blank">Ссылка</a></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style>
.custom-table {
  width: 80%;
  border-collapse: collapse;
}

.custom-table th,
.custom-table td {
  border: 1px solid black;
  padding: 8px;
}
</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tasks: []
    };
  },
  mounted() {
    this.fetchTasks();
  },
  methods: {
    fetchTasks() {
      axios.get('/face/tasks/list')
        .then(response => {
          this.tasks = response.data;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
  }
};
</script>
