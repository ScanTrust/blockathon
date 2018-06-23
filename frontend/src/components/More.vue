<template>
  <div class="more">
    <div :key="component" v-for="component in this.moreSections" class="">
      <div class="title roboto">
        {{component}}
      </div>
      <component :hide-footer="true" v-bind:is="component">
      </component>
    </div>
    <app-footer></app-footer>
  </div>
</template>

<script>

// Sections
import Allergens from '@/components/Allergens'
import Certifications from '@/components/Certifications'
import Claims from '@/components/Claims'
import GMO from '@/components/GMO'
import Ingredients from '@/components/Ingredients'
import OuterLinks from '@/components/OuterLinks'
import Sustainability from '@/components/Sustainability'
import Scm from '@/components/ScmData'
import Usage from '@/components/Usage'

// footer
import Footer from '@/components/Footer'

import { mapGetters } from 'vuex'

export default {
  name: 'more',
  computed: mapGetters({
    product: 'product',
    moreSections: 'getMoreSection'
  }),
  created () {
  },
  components: {
    'app-footer': Footer,
    'allergens': Allergens,
    'certifications': Certifications,
    'claims': Claims,
    'GMO': GMO,
    'ingredients': Ingredients,
    'links': OuterLinks,
    'sustainability': Sustainability,
    'SCM': Scm,
    'usage': Usage
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.title{
  background: #f1f1f1;
  color: #21409a;
  font-size: calc(14px + 1vw);
  text-transform: capitalize;
  padding: 9px 17px;
  margin-top: 15px;
}

</style>
