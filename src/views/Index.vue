<template>
  <div class="index">
    <h1>Websocket test</h1>
    <div>test</div>
    <ChatBox></ChatBox>
    <ChatService></ChatService>
  </div>
</template>

<script>
  import ChatBox from '../components/ChatBox'
  import ChatService from '../components/ChatService'

  export default {
    name: 'Index',
    components: { ChatService, ChatBox }
  }
</script>

<style scoped>

</style>
