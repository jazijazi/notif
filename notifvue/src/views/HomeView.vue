<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <h1>Simple Vue3 Notification</h1>
    <h3>Please Register or Login to get Notifications</h3>
    <p>Or you can chat with other user(if exist) with WebSocket</p>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  components: {
    
  }
}
</script>

<style scoped>
.home{
  height: 70vh;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}
</style>
