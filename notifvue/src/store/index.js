import axios from 'axios'
import { createStore } from 'vuex'
import AuthService from '@/services/auth.js'
import Socket from '@/services/socket.js'

export default createStore({
  state: {
    newNotification : false,
    notificationSocket : null ,
    user : null,
    loggedIn : false,
    accessToken : '',
    refreshTask : null ,
  },
  getters: {
  },
  mutations: {
    setUserLogin(state,accessToken){
      state.loggedIn = true
      state.accessToken = accessToken
      if(state.notificationSocket == null){
        Socket.joinToAllNotifictionGroup() // Join to Notification Websocket After user Logged in Successfully
      }
    },
    setUserData(state , user){
      state.user = user
      localStorage.setItem('user' , JSON.stringify(user))
    },
    setUserLogout(state){
      console.log("LOGING OUT....")
      state.loggedIn = false
      state.accessToken = ''
      state.user = null

      clearTimeout( state.refreshTask ) //stop onging refresh token task

      if(state.notificationSocket){
        state.notificationSocket.close() //close notif socket
        state.notificationSocket = null ;
      }
    }
  },
  actions: {
    onStart(context){
      Promise.resolve(AuthService.getNewToken()) //after this then >>>> socket reconnent
      .then(
        //Socket.joinToAllNotifictionGroup()
        console.log("get new token in start")
      )
    },

    refreshTokens(context){
      console.log("Refresh token ....")

      Promise.resolve(AuthService.getNewToken())
      .then(response =>{
        //user now in
        console.log("call auto refresh>>>>>>>")
        context.dispatch('autoRefresh')

      })
      .catch(error =>{
        //now use logout
        console.log("User loged out so stop get new token...")
        clearTimeout( context.state.refreshTask )
      })
    },

    autoRefresh(context){
      context.state.refreshTask = setTimeout(() => context.dispatch('refreshTokens'),120000)
    },

    
  },
  modules: {
  }
})
