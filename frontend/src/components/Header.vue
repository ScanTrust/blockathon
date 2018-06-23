<template>
  <div class="header">
    <div v-if="hasBack" v-on:click="goBack()" class="back-btn">
      Back
    </div>
    <h1>{{ title }}</h1>
  </div>
</template>

<script>

import router from '../router'

export default {
  name: 'appHeader',
  props: ['title', 'hasBack', 'backLink'],
  methods: {
    goBack: function () {
      router.go(-1)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
