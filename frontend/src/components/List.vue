<template>
  <div class="list">
    <div :key="`list-${item.value}-${index}`" v-if="items.length" v-for="(item, index) in items">
      <div class="name roboto">{{item.value}}</div>
      <div class="description roboto-light" :key="`child-${childIndex}`" v-for="(child, childIndex) in item.children">{{child.value}}</div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'list',
  props: ['items']
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.name{
  font-size: calc(14px + 1vw);
  padding: 10px 5px 10px 17px;
  color: black;
}

.description{
  font-size: calc(12px + 1vw);
  background: #f1f1f1;
  padding: 10px 5px 10px 30px;
  color: black;
}

</style>
