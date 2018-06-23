<template>
  <div class="generic-infos">
    <div class="disclaimer roboto">
      {{disclaimer}}
    </div>

    <ul v-if="items">
      <li class="roboto-medium" :key="`infos-${index}`" v-for="(item, index) in items">{{item.value}}</li>
    </ul>

  </div>
</template>

<script>

export default {
  name: 'generic-infos',
  props: ['items', 'disclaimer']
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.generic-infos{
  padding: 10px 17px;
}

.disclaimer{
  color: #666666;
  font-size: calc(11px + 1vw);
  font-style: italic;
}

li{
  color: black;
  font-size: calc(11px + 1vw);
  padding: 5px 5px 5px 15px;
}

</style>
