import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import RegisterView from '@/views/RegisterView.vue';
import LoginView from '@/views/LoginView.vue';
import TeacherList from "@/views/TeacherList.vue";
import ProfileView from "../views/ProfileView.vue";
import StudentList from "../views/StudentList.vue";
import ClassList from "../views/ClassList.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView
    },
    {
      path: '/profile',
      name: 'Profile',
      component: ProfileView
    },
    {
      path: '/teachers',
      name: 'Teachers',
      component: TeacherList
    },
    {
      path: '/students',
      name: 'Students',
      component: StudentList
    },
    {
      path: '/classes',
      name: 'Classes',
      component: ClassList
    },
  ],
})

export default router
