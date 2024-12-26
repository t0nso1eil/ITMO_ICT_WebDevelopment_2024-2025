<template>
  <div class="app">
    <h1>Портал информации о войнах в онлайн РПГ</h1>
    <button v-on:click="fetchWarriors">Получить список войнов</button>
    <warrior-form />
    <div v-if="!warriors.length">
      <p>Список войнов пока пуст или произошла ошибка.</p>
    </div>
    <warrior-list v-else v-bind:warriors="warriors" />
  </div>
</template>

<script>
import WarriorForm from "@/components/WarriorForm.vue";
import WarriorList from "@/components/WarriorList.vue";
import axios from "axios";

export default {
  components: { WarriorForm, WarriorList },
  data() {
    return {
      warriors: [],
    };
  },
  methods: {
    async fetchWarriors() {
      try {
        const response = await axios.get(
            "http://62.109.28.95:8890/warriors/list/"
        );
        console.log(response.data);
        this.warriors = response.data.results || response.data;
      } catch (e) {
        console.error(e);
        alert("Ошибка при загрузке списка войнов.");
      }
    },
  },
  mounted() {
    this.fetchWarriors();
  },
};
</script>

<style scoped></style>
