<template>
  <Navbar />
  <p>Loggedin : {{ $store.state.loggedIn }}</p>
  <!-- <router-view/> -->

  <router-view v-slot="{Component}">
    <transition name="route" mode="out-in">
      <component :is="Component"></component>
    </transition>
  </router-view>
</template>



<script>
import Navbar from '@/components/Navbar.vue'

export default {
  name:'App',
  components:{
    Navbar,
  },
  mounted(){
    this.$store.dispatch("onStart") //call when page mount(everytime refresh the page)
    this.$store.dispatch("refreshTokens") //call when page mount(everytime refresh the page)

    //this.$store.dispatch("joinToAllNotifictionGroup")
  }
}
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  background-color: rgb(72, 30, 132);
  padding: 15px;
}

.navbar-brand{
  color: #3ee426 !important;
}

nav a {
  font-weight: bold;
}

nav a.router-link-exact-active {
  color: #9adcb4 !important; 
}

/* route animation */
.route-enter-from{
  opacity: 0;
  transform: translateX(100px);
}
.route-enter-active{
  transition: all 0.3s ease-out;
}
.route-leave-to{
  opacity: 0;
  transform: translateX(-100px);
}
.route-leave-active{
  transition: all 0.3s ease;
}
</style>
