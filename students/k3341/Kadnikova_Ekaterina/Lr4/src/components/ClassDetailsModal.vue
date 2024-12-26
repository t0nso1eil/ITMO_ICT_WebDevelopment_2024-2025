<template>
  <div class="modal">
    <div class="modal-content">
      <h3>Class Details</h3>

      <div class="details">
        <p><strong>Class Name:</strong> {{ klass.parallel }}-{{ klass.class_number }}</p>
        <p><strong>Class Teacher:</strong> {{ klassTeacherName }}</p>
        <p><strong>Number of Students:</strong> {{ studentCount }}</p>
      </div>

      <button @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script>
import API from "@/axios";

export default {
  props: {
    klass: Object,
  },
  data() {
    return {
      teacher: null,
      students: [],
    };
  },
  computed: {
    klassTeacherName() {
      return this.teacher ? `${this.teacher.first_name} ${this.teacher.last_name}` : 'Loading teacher...';
    },
    studentCount() {
      return this.students.filter(student => student.class_id === this.klass.id).length;
    },
  },
  methods: {
    async fetchTeacher() {
      try {
        const teacherResponse = await API.get(`/teachers/${this.klass.class_teacher}`);
        this.teacher = teacherResponse.data;
      } catch (error) {
        console.error("Error fetching teacher:", error);
      }
    },
    async fetchStudents() {
      try {
        const studentResponse = await API.get("/students/");
        this.students = studentResponse.data.Students;
      } catch (error) {
        console.error("Error fetching students:", error);
      }
    },
  },
  created() {
    this.fetchTeacher();
    this.fetchStudents();
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.details {
  margin-bottom: 20px;
}

button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
