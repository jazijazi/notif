<template>
  <div class="Navbar">
    <nav class="navbar navbar-expand-sm navbar-dark">
    <router-link class="navbar-brand" to="/">Notif</router-link>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavDropdown">
      <ul class="navbar-nav">
      <li class="nav-item active">
          <router-link class="nav-link" :to="{name:'home'}">Home</router-link>
      </li>
      <li class="nav-item">
          <router-link class="nav-link" :to="{name:'about'}">About</router-link>
      </li>
      <li class="nav-item">
          <router-link class="nav-link" :to="{name:'chat'}" v-if="$store.state.loggedIn">Chat</router-link>
      </li>
      <li class="nav-item">
          <router-link class="nav-link" :to="{name:'login'}" v-if="!$store.state.loggedIn">Login</router-link>
      </li>
      <li class="nav-item">
          <router-link class="nav-link" :to="{name:'register'}" v-if="!$store.state.loggedIn">Register</router-link>
      </li>
      <li class="nav-item">
          <router-link class="nav-link" :to="{name:'logout'}" v-if="$store.state.loggedIn">Logout</router-link>
      </li>
      <li class="nav-item">
          <router-link class="nav-link" :to="{name:'notification'}" v-if="$store.state.loggedIn">
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="text-danger bi bi-bell-fill" viewBox="0 0 16 16">
              <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z"/>
            </svg>
            <span class="badge bg-danger" v-if="$store.state.newNotification">+1</span>
          </router-link>
      </li>
      </ul>

    </div>
    </nav>
  </div>
</template>

<script>
export default {
  name:"Navbar",
  data(){
    return{
    }
  },
  methods:{
  },
}
</script>