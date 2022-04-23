<template>
  <div class="Chat">
    <div class="container" >
      <div class="row text-center">
        <div class="col-8  mx-auto my-4 shadow p-4 rounded">
          
          <div class="alert alert-danger" v-if="errorE">{{errorEM}}</div>

          <div class="input-group w-50 mx-auto">
              <div class="input-group-prepend"><span class="input-group-text">@</span></div>
              <input ref="targetUserInput" @blur="doConnect" v-model="targetUser" type="text" class="form-control" placeholder="Username">
          </div>

          <div class="input-group w-50 mx-auto">
              <input ref="yourMessageInput" v-model="yourMessage" type="text" class="form-control" placeholder="YourMessage...">
              <div class="input-group-append">
                <button @click="doSendMessage" class="btn btn-success">Send</button>
              </div>
          </div>

          <div id="messages-list" class="border p-2 my-4" style="height: 400px; overflow-y: scroll">
            <div class="media" v-for="message in messages" :key="message.user">
              <div class="media-body">
                <h6 class="my-0"><strong>{{message.user}}</strong></h6>
                <p>{{message.content}}</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Chat',
  data(){
    return{
      targetUser:'',
      yourMessage:'' ,
      messages : [] ,
      errorEM : '' ,
      errorE : false ,
      socket : null ,
    }
  },
  methods:{
    doConnect(){
      this.errorEM = ''
      this.errorE = false

      if(this.targetUser){
        this.socket = new WebSocket(
        `ws://127.0.0.1:8000/ws/chat/${this.targetUser}/`);
                
        this.socket.onmessage = (e) => {
          const message = JSON.parse(e.data);
          console.log(message)
          //console.log(message['type'])
          switch (message['type']) {
            case "send_to_user":
              this.messages.unshift({user:message['data']['sender'] , content:message['data']['content']})
          }
        }

        this.socket.onopen = (e)=>{
          this.$refs.yourMessageInput.disabled = false;
          this.$refs.targetUserInput.classList.add("is-valid")
          this.$refs.targetUserInput.classList.remove("is-invalid")
        }
        this.socket.onclose = (e)=>{
          this.errorE = true
          this.$refs.yourMessageInput.disabled = true;
          this.$refs.targetUserInput.classList.add("is-invalid")
          this.$refs.targetUserInput.classList.remove("is-valid")
          if(e.code == 4004){
            this.errorEM = 'User Not Found'
          }
          else{
            this.errorEM = 'Error in connection'
          }
        }
      }
      else{
        this.errorE = true
        this.errorEM = 'fill username...'
      }
    },
    doSendMessage(){
      this.socket.send(JSON.stringify({'type': 'message' , 'content' : this.yourMessage}))
      this.messages.unshift({user:'You' , content:this.yourMessage})
    },
  },
  unmounted(){
    if(this.socket){
      this.socket.send(JSON.stringify({'type': 'message' , 'content' : 'this user not avalible anymore'}))
      this.socket.close()
    }
  },
}
</script>