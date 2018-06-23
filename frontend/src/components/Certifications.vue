<template>
  <div class="certifications">
    <generic-infos :disclaimer="disclaimer" :items="this.getSmartLabelTab('certifications').data.items"></generic-infos>
  </div>
</template>

<script>

import GenericInfos from '@/components/GenericInfos'
import { mapGetters } from 'vuex'

export default {
  name: 'certifications',
  computed: mapGetters(['getSmartLabelTab']),
  components: {
    'generic-infos': GenericInfos
  },
  data: function () {
    return {
      disclaimer: 'SmartLabel™ only includes certifications from independent organizations that have meaningful and consistent standards for the certification.'
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
