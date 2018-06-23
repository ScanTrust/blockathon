<template>
  <div class="usage">
    <div :key="`usage-${index}`" v-for="(usage, index) in this.getSmartLabelTab('usage').data.items" class="usage-field">
      <div class="title roboto-medium">{{usage.value}}</div>
      <div :key="`usage-description${descriptionIndex}`" v-for="(description, descriptionIndex) in usage.children" class="description roboto">{{description.value}}</div>
    </div>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'
export default {
  name: 'usage',
  computed: mapGetters(['getSmartLabelTab']),
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.usage{
  color: black;
  padding: 12px 18px;
}

.usage-field{
  padding-bottom: 28px;
}

.title{
  padding-bottom: 10px;
  font-size: calc(12px + 1vw);
}

.description{
  padding-top: 5px;
  font-size: calc(11px + 1vw);

}

</style>
