<template>
  <div class="chat-box">
    <input type="text" v-model="messageBox" v-on:keyup.enter="onEnterClick"/>
  </div>
</template>

<script>
  export default {
    name: 'ChatBox',
    methods: {
      onEnterClick: function () {
        console.log(this.messageBox)
      }
    },
    data: function () {
      return {
        messageBox: ''
      }
    }
  }
</script>

<style scoped>

</style>
