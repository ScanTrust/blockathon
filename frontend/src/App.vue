<template>
  <div class="app-wrap" id="app">
    <loading v-if="!loaded"></loading>
    <img v-if="loaded" class="top-logo" src="./assets/GoodChain.png" alt="">
    <product-infos v-if="loaded"></product-infos>
    <navigation v-if="loaded"></navigation>
    <router-view v-if="loaded"></router-view>
    <md-snackbar md-position="center" :md-active.sync="snackBar.show" md-persistent>
      <span>{{snackBar.message}}</span>
      <md-button class="md-accent" @click="closeSnackBar()"><span>dismiss</span></md-button>
    </md-snackbar>
  </div>
</template>

<script>

import Loading from '@/components/Loading'
import Navigation from '@/components/Navigation'
import ProductInfos from '@/components/ProductInfos'
import ScantrustService from '@/services/ScantrustService'

import { mapGetters } from 'vuex'

export default {
  name: 'app',
  components: {
    'navigation': Navigation,
    'product-infos': ProductInfos,
    'loading': Loading
  },
  data () {
    return {
      campaign: {},
      scanId: ''
    }
  },

  computed: mapGetters({
    loaded: 'isLoaded',
    sections: 'getSections',
    snackBar: 'snackBar',
    code: 'code'
  }),

  created () {
    if (this.$route.query.api_key) {
      ScantrustService.setAuthorizationHeader(this.$route.query.api_key)
    }

    this.$store.dispatch('saveUrlParameters', {qr: this.$route.query.qr, uid: this.$route.query.uid, apiKey: this.$route.query.api_key, installId: this.$route.query.install_id})
    this.$store.dispatch('getCombinedInfos', {uid: this.$route.query.uid}).then(() => {
      this.$store.dispatch('loadGS1', this.code.product.sku)
    })

    // Blockchain code
    if (this.$route.query.install_id) {
      console.log('dispatching')
      this.$store.dispatch('loadCauses')
      this.$store.dispatch('loadRecheck')
      this.$store.dispatch('initUserBDB', {installId: this.$route.query.install_id}).then(() => {
        this.$store.dispatch('createScanEvent', {message: this.$route.query.qr, uid: this.$route.query.uid, lat: 42, lng: 42, installId: this.$route.query.install_id})
        this.$store.dispatch('loadImpactHistory', {installId: this.$route.query.install_id})
      })
    }
  },

  beforeMount () {
    if (!this.$route.query.uid) {
      alert('Incorrect URL')
    }
  },
  methods: {
    closeSnackBar: function () {
      this.$store.dispatch('dissmissSnackBar', {})
    }
  }
}
</script>

<style lang="scss">

@import "~vue-material/dist/theme/engine";

@include md-register-theme("default", (
  primary: #6099ab,
  accent: #60ab97
));

@import "~vue-material/dist/theme/all";

html {
  font-size: 62.5%;
  height: 100%;
  width: 100%;
}

body {
  height: 100%;
  width: 100%;
  max-width: 500px;
  margin: 0;
  margin-left: auto;
  margin-right: auto;
}

#app {
  height: 100%;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.top-logo{
  padding-top: 15px;
  width: 119px;
  margin-left: 1rem;
}

</style>
