<template>
  <div class="chat-service">
    <div id="message-box">
    </div>
    <button @click="sendMsg">send</button>
  </div>
</template>

<script>
  import Vue from 'vue'
  import VueNativeSock from 'vue-native-websocket'
  import store from '../store'
  import {
    SOCKET_ONOPEN,
    SOCKET_ONCLOSE,
    SOCKET_ONERROR,
    SOCKET_ONMESSAGE,
    SOCKET_RECONNECT,
    SOCKET_RECONNECT_ERROR
  } from '../mutation-types'

  const mutations = {
    SOCKET_ONOPEN,
    SOCKET_ONCLOSE,
    SOCKET_ONERROR,
    SOCKET_ONMESSAGE,
    SOCKET_RECONNECT,
    SOCKET_RECONNECT_ERROR
  }

  // Vue.use(Vuex)
  Vue.use(VueNativeSock, 'ws://192.168.0.10:8080/rooms/10/2/username', {
    format: 'json',
    // connectManually: true,
    mutations: mutations,
    store: store
  })

  // const vm = new Vue()
  // vm.$connect()
  // console.log(vm.$socket)

  // vm.$socket.sendObj({ awesome: 'data' })

  export default {
    name: 'ChatService',
    created () {
      this.$options.sockets.onmessage = (data) => {
        console.log(data)
      }
      // console.log(store.state.socket)
      // this.$options.socket.on = (event) => {
      //   console.log(store.state)
      //   this.$socket.sendObj({ msg: 'hello' })
      // }
    },
    methods: {
      sendMsg () {
        this.$socket.sendObj('{"msg":"hi"}')
        // console.log(store.state.socket.message)
      }
    }
  }
</script>

<style scoped>

</style>
