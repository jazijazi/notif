<template>
  <div class="Login">
    <div class="row">
      <p>
        {{ $store.state.user }}
      </p>
      <div class="col-lg-6 mx-auto rounded shadow p-4 my-4">
        <h1 class="text-center">Login</h1>
        <form @submit.prevent="doLogin">
          <div class="form-group">
            <label for="usernameInput">Username</label>
            <input class="form-control" type="text" id="usernameInput" 
            v-model="username"
            :class="{'is-invalid':usernameE===true , 'is-valid':usernameE===false}"
            >
            <div class="invalid-feedback" v-if="usernameE">{{usernameEM}}</div>
          </div>
          <div class="form-group">
            <label for="passwordInput">Password</label>
            <input class="form-control" type="text" id="passwordInput" v-model="password"
            :class="{'is-invalid':passwordE===true , 'is-valid':passwordE===false}"
            >
            <div class="invalid-feedback" v-if="passwordE">{{passwordEM}}</div>
          </div>
          <button type="submit" class="btn btn-primary btn-lg my-3">Login</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import AuthService from '@/services/auth.js'

export default {
  name: 'Login',
  data(){
    return{
      username:'',
      password:'',
      usernameE:null,
      usernameEM:null,
      passwordE:null,
      passwordEM:null,
    }
  },
  methods: {
    doLogin(){
      let access = true

      //username check
      if(this.username.length < 5){
        this.usernameE = true
        access = false
        if(this.username.length == 0){
          this.usernameEM = 'username reqired'
        }
        else{
          this.usernameEM = 'username can not less than 5 character'
        }
      }
      else{
        this.usernameE = false
        this.usernameEM = ''
      }

      //password check
      if(this.password.length < 8){
        this.passwordE = true
        access = false
        if(this.password.length == 0){
          this.passwordEM = 'password reqired'
        }
        else{
          this.passwordEM = 'password can not less than 8 character'
        }
      }
      else{
        this.passwordE = false
        this.passwordEM = ''
      }
      


      if(access){
        const user = {username:this.username , password:this.password}
        Promise.resolve(AuthService.login(user))
        .then(
          console.log("Login")
        )
        .catch(error => {
          console.log("Error in login")
          console.log(error)
          this.passwordE = true
          this.usernameE = true
        })
      }
    }
  }
}
</script>