import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import WelcomeView from '../views/WelcomeView.vue'
import SettingsView from '../views/SettingsView.vue'
import HomeView from '../views/HomeView.vue'
import UserHomeView from '../views/UserHomeView.vue'


import { UserStore } from "@/stores/user.js"



const routes = [
  {
    path: '/',
    name: 'init',
    redirect: '/login'
  },
  {
    path: '/:userId',
    name: 'home',
      component: HomeView,
      meta: { requiresAuth: true , requiresAdmin: true }
  },
  {
    path: '/member/:userId',
    name: 'userhome',
      component: UserHomeView,
      meta: { requiresAuth: true , requiresAdmin: false }
  },
  {
    path: '/login',
    name: 'login',
      component: LoginView,
      meta: { requiresAuth: false , requiresAdmin: false }
  },
  {
    path: '/welcome',
    name: 'welcome',
      component: WelcomeView,
      meta: { requiresAuth: false, requiresAdmin: false }
  },
  {
    path: '/settings/:userId',
    name: 'settings',
      component: SettingsView,
      meta: { requiresAuth: true , requiresAdmin: false }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to) => {

  const user = UserStore()
  console.log(user.isLoggedIn)
  if (to.meta.requiresAuth && !user.isLoggedIn) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    return {
      path: '/login',
      // save the location we were at to come back later
      //query: { redirect: to.fullPath },
    }
  }
})


/* eslint-disable */


export default router
