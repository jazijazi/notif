<template>
  <div class="Notification">
    <div class="container" v-if="notifications">
      
      <div class="row text-center">
        <div class="col-8  mx-auto my-4 shadow p-4 rounded">
          <h3>Delete all Notifications?</h3>
          <button @click="doDeleteNotifications" class="btn btn-danger">Delete</button>
        </div>
      </div>

      <!-- <div class="row text-center"> -->
      <transition-group tag="div" class="row text-center" name="notif-list" appear>
        <div v-for="notif in notifications" :key="notif.title">
          <div class="col-8 mx-auto mb-4">
            <div class="card text-center shadow">
              <div class="card-header">Notification</div>
              <div class="card-body">
                <h5 class="card-title">{{notif.title}}</h5>
                <p class="card-text">{{ notif.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </transition-group>
      <!-- </div> -->

    </div>
    <div class="container" v-else>
      <h2>No Notification</h2>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Notification',
  data(){
    return{
        notifications : null,
    }
  },
  methods:{
    doDeleteNotifications(){
      // let allnotif = localStorage.getItem("notifications")
      // allnotif = ''
      // localStorage.setItem('notifications' , allnotif)
      // this.notifications = ''
      localStorage.removeItem("notifications")
      this.notifications = ''
    }
  },
  mounted(){
    this.$store.state.newNotification = false
    let nft = localStorage.getItem("notifications")
    //if(nft){
      nft = JSON.parse(nft)
      this.notifications = nft
    //}
  }
}
</script>

<style>
  /* notif-list */
  .notif-list-enter-from{
    opacity: 0;
    transform: scale(0.6);
    transform: translateY(50px);
  }
  .notif-list-enter-to{
    opacity: 1;
    transform: scale(1);
    transform: translateY(0px);
  }
  .notif-list-enter-active{
    transition: all 1.3s ease;
  }
  .notif-list-leave-from{
    opacity: 1;
    transform: scale(1);
    transform: translateY(0px);
  }
  .notif-list-leave-to{
    opacity: 0;
    transform: scale(0.6);
    transform: translateY(50px);
  }
  .notif-list-leave-active{
    transition: all 1s ease;
    position: absolute; /* for move up */
  }
  .notif-list-move{
    transition: all 0.7s ease;
  }
</style>