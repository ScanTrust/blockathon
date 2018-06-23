<template>
  <div class="links">
    <div :key="`link-${index}`" v-on:click="redirectTo(link.url)" v-for="(link, index) in this.getSmartLabelTab('links').data.items" class="outer-link roboto Grid -middle">
      <div class="Cell -fill">
        {{link.label}}
      </div>
      <div v-if="outIcon" v-html="outIcon" class="Cell icon"></div>
    </div>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'

export default {
  name: 'links',
  computed: mapGetters(['getSmartLabelTab']),
  data () {
    return {
      outIcon: require('@/assets/icons/out-link.svg')
    }
  },
  methods: {
    redirectTo: function (url) {
      var answer = confirm('Warning, you are about to leave the smart label website, do you want to proceed?')

      if (answer) {
        window.location = url
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.outer-link{
  padding: 15px;
  font-size: calc(12px + 1vw);
  color: #21409a;
  text-decoration: underline;
  border-bottom: 1px solid #f1f1f1;
}

.icon{
  width: 24px;
  margin-bottom: -5px;
}

</style>
