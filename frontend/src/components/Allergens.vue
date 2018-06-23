<template>
  <div class="allergens roboto flex flex-vertical flex-space-between">

    <div class="flex-1">
      <div class="disclaimer">
        According to the FDA, the most common food allergens are milk, peanuts, eggs, fish, shellfish, soy, tree nuts and wheat.
      </div>

      <div v-if="this.getSmartLabelTab('allergens').data.text == '1' ">
        <div class="contains-text">
          This product contains:
        </div>

        <list :items="this.getSmartLabelTab('allergens').data.items"></list>
      </div>

      <div class="contains-text" v-if="this.getSmartLabelTab('allergens').data.text == '0'">
        This product does not contain any of these allergers.
      </div>
    </div>

    <app-footer v-if="!hideFooter"></app-footer>
  </div>
</template>

<script>

import Footer from '@/components/Footer'
import List from '@/components/List'
import { mapGetters } from 'vuex'

export default {
  name: 'allergens',
  props: ['hideFooter'],
  computed: mapGetters(['getSmartLabelTab']),
  components: {
    'app-footer': Footer,
    'list': List
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.allergens{
  height: 100%;
  color: #999;
  font-size: calc(12px + 1vw);
}

.contains-text{
  padding: 10px 17px;
}

.disclaimer{
  padding: 17px;
}

</style>
