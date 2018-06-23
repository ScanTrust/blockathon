import Vue from 'vue'
import Vuex from 'vuex'
import scantrust from './modules/scantrust'
import snackbar from './modules/snackbar'
import bigchainDB from './modules/bigchainDB'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  modules: {
    scantrust,
    snackbar,
    bigchainDB
  },
  strict: debug
})
