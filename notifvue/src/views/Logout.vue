<template>
  <div class="Login">
    <div class="row">
      <div calss="col-md-8">
        <h1>Logout?</h1>
        <button class="btn btn-danger btn-lg" @click="doLogout">Logout</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import AuthService from '@/services/auth.js'

export default {
  name: 'Logout',
  data(){
    return{
      
    }
  },
  methods: {
    doLogout(){
      AuthService.logout()
    }
  }
}
</script>