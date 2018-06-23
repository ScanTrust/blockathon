<template>
  <div class="claims">
    <generic-infos :disclaimer="disclaimer" :items="this.getSmartLabelTab('claims').data.items"></generic-infos>
  </div>
</template>

<script>

import GenericInfos from '@/components/GenericInfos'
import { mapGetters } from 'vuex'

export default {
  name: 'claims',
  computed: mapGetters(['getSmartLabelTab']),
  components: {
    'generic-infos': GenericInfos
  },
  data: function () {
    return {
      disclaimer: 'Claims listed within SmartLabel™ are those that are governed by entities such as FDA, EPA, FIFRA, etc. Claims are a blend of both required (e.g., structure function claims and qualified health claims) and voluntary attributes (e.g., "Does not contain"/"Free from" statements).'
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
