// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'

import App from './App'
import router from './router'
import store from './store'

import 'grd/grd.css'
import './main.css'

Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use(VueMaterial)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: { App }
})
