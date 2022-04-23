import axios from 'axios';
import store from '@/store';
import router from '@/router';

class AuthService {
  async login(user) {
    try{
      console.log('Loging in request')
      const response = await axios.post('/api/auth/login/' , user)
      if(response.status == 200){
        store.commit('setUserLogin' , response.data.access) 
        store.commit('setUserData' , response.data.user)
        store.dispatch('autoRefresh') //start refreshing token in time
        // store.dispatch('joinToAllNotifictionGroup') //join to Notification websocket
      }
    }
    catch(error){
      console.log('error in loging request')
      console.log(error)
      throw error
    }
  }

  async logout() {
    try{
      console.log('loging out request')
      const response = await axios.post('/api/auth/logout/')
      store.commit('setUserLogout')
      router.push({name:'login'})
    }
    catch(error){
      console.log('error in loging out request')
      console.log(error)
      throw error
    }
  }
  
  async register(newUser) {
    try{
      console.log('error in registration request')
      const response = await axios.post('/api/auth/register/' , newUser)
      if(response.status == 201){
        router.push("/login")
      }
    }
    catch(error){
      console.log("error in registration request")
      console.log(error)
      throw error
    }
  }

  async getNewToken(){
    try{
      console.log('get new token request')
      let response = await axios.post('/api/auth/token/refresh/')
      if(response.status == 200){
        store.commit('setUserLogin' , response.data.access)
        response = await axios.get('/api/auth/user/')
        if(response.status == 200){
          store.commit('setUserData' , response.data)
        }
      }
    }
    catch(error){
      console.log('error in get new token request')
      console.log(error)
      store.commit('setUserLogout')
      throw error
    }
  }

  async verify(){
    try{
      let response = await axios.get('/api/auth/user/')
      if(response.status == 200){
        return true
      }
      else{
        return false
      }
      //return response
    }
    catch(error){
      
      throw error
    }
  }
}
export default new AuthService();
