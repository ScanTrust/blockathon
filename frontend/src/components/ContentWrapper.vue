<template>
  <div id="main-content" class="main">
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'content-wrapper',
  data () {
    return {
    }
  },
  methods: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.main{
  height: calc(100% - 62px);
}

</style>
