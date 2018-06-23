<template>
  <div class="ingredients flex flex-vertical flex-space-between">
    <div class="flex-1">
      <list :items="this.getSmartLabelTab('ingredients').data.items"></list>
    </div>
    <app-footer v-if="!hideFooter"></app-footer>
  </div>
</template>

<script>

import Footer from '@/components/Footer'
import List from '@/components/List'
import { mapGetters } from 'vuex'

export default {
  name: 'ingredients',
  props: ['hideFooter'],
  computed: mapGetters(['getSmartLabelTab']),
  data () {
    return {
      msg: 'Ingredients'
    }
  },
  components: {
    'app-footer': Footer,
    'list': List
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.ingredients{
  height: 100%;
}

</style>
