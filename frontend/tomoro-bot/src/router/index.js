import { createRouter, createWebHistory } from 'vue-router'
import AboutView from '../views/AboutView.vue'
import LikeView from '../views/LikeView.vue'
import RobotControlsView from '../views/RobotControlsView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
        path: '/',
        name: 'robot-controls',
        component: RobotControlsView,
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
    },
    {
        path: '/likes',
        name: 'likes',
        component: LikeView,
    },
  ],
})

export default router