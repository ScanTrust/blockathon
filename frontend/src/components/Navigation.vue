<template>
  <div :style="{height: height + 'px'}">
    <div v-bind:class="{fixed : isFixed}" :style="{height:height+'px'}" id="navigation" class="navigation Grid">
      <router-link :key="tab" v-for="tab in this.sections" v-bind:class="{ 'router-link-active' : currentTab == tab }" v-on:click.native="handleClick" class="navigation-tab Cell -6of12 -fill" :to="'/' + tab + '?uid=' + url.uid + '&api_key=' + url.api_key + '&qr=' + url.qr + '&install_id=' + url.installId"  >
        <div class="icon center" v-html="tabs[tab].icon"></div>
        <div class="title roboto-medium text-center">
          {{ tabs[tab].label }}
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
// import NavigationTab from '@/components/NavigationTab'
import Vue from 'vue'
import router from '@/router'
import Tabs from '@/const/tabs.js'
import { mapGetters } from 'vuex'

const VueScrollTo = require('vue-scrollto')

Vue.use(VueScrollTo)

export default {
  name: 'navigation',
  computed: mapGetters({
    url: 'getUrlParameters',
    smartlabel: 'smartlabel',
    sections: 'getMainSections'
  }),
  data () {
    return {
      navTop: 0,
      height: undefined,
      isFixed: false,
      windowHeight: window.innerHeight,
      window: window,
      currentTab: 'Nutrition',
      tabs: Tabs
    }
  },
  methods: {
    handleClick () {
      this.currentTab = false
      VueScrollTo.scrollTo('#main-content', 400, {offset: -62})
    },
    fixPosition () {
      if (this.isFixed) {
        return
      }
      this.isFixed = true
    },
    resetPosition () {
      if (!this.isFixed) {
        return
      }
      this.isFixed = false
    },
    handleScroll () {
      const offsetTop = this.$el.getBoundingClientRect().top
      if (offsetTop < this.navTop) {
        this.fixPosition()
        return
      }
      this.resetPosition()
    }
  },
  mounted () {
    if (!this.$route.name && this.sections && this.url) {
      router.push({name: this.sections[0], query: this.url})
    }

    this.height = this.$el.getBoundingClientRect().height
    window.addEventListener('touchmove', this.handleScroll, false)
    window.addEventListener('scroll', this.handleScroll)
  },
  destroyed () {
    window.removeEventListener('scroll', this.handleScroll)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

svg{
  fill: "21409A";
}

a{
  text-decoration: none;
  height: 100%;
}
/* #6099ab */

.navigation{
  transform: translate3d(0px,0px,0px);
  z-index: 999;
  max-width: 500px;
}

.navigation-tab {
  box-sizing: border-box;
  height: 6.2rem;
  float: left;
  cursor: pointer;
  background-color: #6099ab;
  color: white !important;
  border: none;
  border-left: 1px solid white;
}

.navigation-tab:first-child{
  border-left: none;
}

.title{
  font-size: calc(9px + 0.2vw);
}

.router-link-active{
  background: white;
  color: #6099ab !important;
  border-top: 0.6rem solid #60ab97;
}

.icon{
  margin-top: 1.2rem;
  width: 3.2rem;
  height: 3.2rem;
}

.router-link-active .icon{
  margin-top: 0.6rem;
}

.fixed{
  position: fixed;
  top: 0px;
  width: 100%;
}

.navigation >>> .router-link-active path{
  fill: #6099ab;
}

</style>
