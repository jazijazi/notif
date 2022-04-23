<template>
  <div class="Login">
    <div class="row">
      <div class="col-lg-8 mx-auto rounded shadow p-4 my-4">
        <h1 class="text-center mb-5">Register</h1>
        <form @submit.prevent="doRegister">

          <div class="form-group mb-4">
            <label for="usernameInput">Username</label>
            <input class="form-control" type="text" id="usernameInput" 
            v-model="username"
            :class="{'is-invalid':usernameE===true , 'is-valid':usernameE===false}"
            >
            <div class="invalid-feedback" v-if="usernameE">{{usernameEM}}</div>
          </div>

          <div class="form-group mb-4">
            <label for="emailInput">Email</label>
            <input class="form-control" type="text" id="emailInput" @keyup="doEmailValidate"
            v-model="email"
            :class="{'is-invalid':emailE===true , 'is-valid':emailE===false}"
            >
            <div class="invalid-feedback" v-if="emailE">{{emailEM}}</div>
          </div>

          <div class="form-group mb-4">
            <label for="passwordInput">Password</label>
            <input class="form-control" type="text" id="passwordInput" v-model="password"
            :class="{'is-invalid':passwordE===true , 'is-valid':passwordE===false}"
            >
            <div class="invalid-feedback" v-if="passwordE">{{passwordEM}}</div>
          </div>

          <div class="form-group mb-4">
            <label for="passwordInput2">Repeat Password</label>
            <input class="form-control" type="text" id="passwordInput2" v-model="password2"
            :class="{'is-invalid':password2E===true , 'is-valid':password2E===false}"
            >
            <div class="invalid-feedback" v-if="password2E">{{password2EM}}</div>
          </div>

          <button type="submit" class="btn btn-primary btn-lg my-3">Signup</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import AuthService from '@/services/auth.js'

export default {
  name: 'Register',
  data(){
    return{
      username:'',
      email:'',
      password:'',
      password2:'',
      usernameE:null,
      usernameEM:null,
      emailE:null,
      emailEM:null,
      passwordE:null,
      passwordEM:null,
      password2E:null,
      password2EM:null,
    }
  },
  methods: {
    doEmailValidate(){
      const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      if(this.email.toLowerCase().match(emailRegex)){
        this.emailE = false
        return true
      }
      else{
        this.emailE = true
        this.emailEM = 'Email Not Valid'
        return false
      }
    },
    doRegister(){
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


      //password2 check
      if(this.password2.length < 8){
        this.password2E = true
        access = false
        if(this.password2.length == 0){
          this.password2EM = 'repeat password reqired'
        }
        else{
          this.password2EM = 'repeat password can not less than 8 character'
        }
      }
      else{
        this.password2E = false
        this.password2EM = ''
      }

      //password & password2 check
      if(this.password != this.password2){
        access = false
        this.passwordE = true
        this.password2E = true
        this.passwordEM = "passwords arent same"
      }
      else{
        if(!this.passwordEM && !this.password2EM){
            this.passwordEM = ""
        }
      }
      

      if(access && this.doEmailValidate()){
        const newUser = {
          username:this.username ,
          email:this.email,
          password:this.password,
        }

        Promise.resolve(AuthService.register(newUser))
          .then(
            console.log("register user seccessfully...")
          )
          .catch(error => {
            console.log(error)
            if(error.response.data.username){
              this.usernameE = true
              this.usernameEM = error.response.data.username.join(" ")
            }
            else if(error.response.data.password){
              this.passwordE = true
              this.password2E = true
              this.passwordEM = error.response.data.password.join(" ")
            }
            else if(error.response.data.email){
              this.emailE = true
              this.emailEM = error.response.data.email.join(" ")
            }
          })
      }
    }
  }
}
</script>