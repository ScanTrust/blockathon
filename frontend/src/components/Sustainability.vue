<template>
  <div class="sustainability flex flex-vertical flex-space-between">
    <div class="flex-1">
      <div class="disclaimer roboto">
        <span>Lindt works to ensure our packages are recyclable.</span>
        <br><br>
        <span>Please recycle following the below guidance.</span>
      </div>
      <list :items="this.getSmartLabelTab('sustainability').data.items"></list>
    </div>
    <app-footer v-if="!hideFooter"></app-footer>
  </div>
</template>

<script>

import Footer from '@/components/Footer'
import List from '@/components/List'
import { mapGetters } from 'vuex'

export default {
  name: 'sustainability',
  props: ['hideFooter'],
  computed: mapGetters(['getSmartLabelTab']),
  data () {
    return {}
  },
  components: {
    'app-footer': Footer,
    'list': List
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.sustainability{
  height: 100%;
}

.disclaimer{
  color: #999;
  font-size: calc(12px + 1vw);
  padding: 17px;
}

</style>
