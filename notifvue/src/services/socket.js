import axios from 'axios';
import store from '@/store';

class Socket{
  joinToAllNotifictionGroup(){
    //it calls in Sote.js setUserLogin function after user login
    store.state.notificationSocket = new WebSocket('ws://' + '127.0.0.1:8000' + '/ws/notification/');
      
    store.state.notificationSocket.onmessage = function(e) {
      const message = JSON.parse(e.data);
      console.log(message)
      switch (message['type']) {
        case "chat.notify":
          //save new notification to localstorage
          let notifications = localStorage.getItem('notifications')
          notifications = JSON.parse(notifications)
          let newNotification = {
            'title' : message['notification']['title'],
            'content' : message['notification']['content']
          }
          if(notifications){
            notifications.push(newNotification)
          }
          else{
            notifications = []
            notifications.push(newNotification)
          }
          notifications = JSON.stringify(notifications)
          localStorage.setItem('notifications' , notifications)
          
          //set new notification true
          store.state.newNotification = true

          //send ack for this notif
          store.state.notificationSocket.send(JSON.stringify({'type': 'ack_message' , 'id' : message['notification']['id']}));
          break;
      
      }
    }
    
    store.state.notificationSocket.onclose = function(e) {
      console.dir(e)
      console.error('Notification Socket closed unexpectedly');
      store.state.notificationSocket = null
    }
  }
}

export default new Socket();
