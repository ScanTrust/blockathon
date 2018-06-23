<template>
  <div class="gmo">
    <generic-infos :disclaimer="disclaimer[this.getSmartLabelTab('GMO').data.text]" :items="this.getSmartLabelTab('GMO').data.items"></generic-infos>
  </div>
</template>

<script>

import GenericInfos from '@/components/GenericInfos'
import { mapGetters } from 'vuex'

export default {
  name: 'gmo',
  computed: mapGetters(['getSmartLabelTab']),
  components: {
    'generic-infos': GenericInfos
  },
  data: function () {
    return {
      disclaimer: {
        '0': 'This product DOES NOT include ingredients sourced from genetically engineered (GE) crops, commonly known as GMOs.',
        '1': 'This product does include ingredients sourced from genetically engineered (GE) crops, commonly known as GMOs.'
      }
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
