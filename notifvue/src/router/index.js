import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import AuthService from '@/services/auth'

import HomeView from '../views/HomeView.vue'
import Login from '@/views/Login.vue'
import Logout from '@/views/Logout.vue'
import Register from '@/views/Register.vue'
import Chat from '@/views/Chat.vue'
import Notification from '@/views/Notification.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    }
  },
  {
    path: '/login',
    name: 'login',
    component: Login ,
    meta: { loginRedirect:true }
  },
  {
    path: '/register',
    name: 'register',
    component: Register ,
    meta: { loginRedirect:true }
  },
  {
    path: '/logout',
    name: 'logout',
    component: Logout,
    meta: { loginRequired:true }
  },
  {
    path: '/notification',
    name: 'notification',
    component: Notification,
    meta: { loginRequired:true }
  },
  {
    path: '/chat',
    name: 'chat',
    component: Chat,
    meta: { loginRequired:true }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

//Limit pages for authorized users
router.beforeEach(async(to,from,next)=>{
  //virify authent
  let access = null
  try{
    access = await AuthService.verify()
  }
  catch(error){
    access = false
  }
  console.log(access)

    
  if(to.matched.some(record => record.meta.loginRequired)){
    if(access){
      next()
    }
    else{
      next('/login')
    }
  }

  else if (to.matched.some(record => record.meta.loginRedirect)){ 
    if(!access){
      next()
    }
    else{
      next('/')
    }
  }
  else{
    next()
  }
})

export default router
