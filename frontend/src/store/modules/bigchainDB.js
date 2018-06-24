import * as types from '../mutations'
import BigChainDBService from '@/services/BigChainDBService'
import BlockathonService from '@/services/BlockathonService'

const state = {
  user: {},
  euipo_data: {},
  showRewardPopup: false,
  causes: [],
  donating: false,
  history: {},
  euipoScore: 0,
  recheck: {},
  gs1: {}
}

const getters = {
  gs1: (state) => state.gs1,
  recheck: (state) => state.recheck,
  user: (state) => state.user,
  causes: (state) => state.causes,
  donating: (state) => state.donating,
  euipoScore: (state) => state.euipoScore,
  historyMap: (state) => {
    let historyMap = {}

    state.causes.forEach((cause) => {
      historyMap[cause.pub_key] = {name: cause.name, url: cause.url, amount_donated: state.history[cause.pub_key]}
    })

    return historyMap
  }
}

const actions = {

  loadGS1 ({ commit }, sku) {
    BigChainDBService.loadGS1(sku).then((res) => {
      commit(types.LOAD_GS1, res)
    })
  },

  loadRecheck ({ commit }) {
    BigChainDBService.loadRecheck().then((res) => {
      commit(types.LOAD_RECHECK_DATA, res)
    })
  },

  sendAuthoritiesAlert ({ commit, dispatch }) {
    BigChainDBService.sendAlert("There is something wrong with that stuff").then((res) => {
      dispatch('showSnackBar', { message: 'Alert sent to authorities.' })
    })
  },

  checkEuipo ({ commit }, fields) {
    var scores = []
    fields.forEach((field) => {
      scores.push(BlockathonService.checkFakeEDB(field.key, field.params))
    })
    console.log('all scores ->' + scores)
    commit(types.SET_EUIPO_SCORE, scores)
    // if (~key.indexOf('_')) {
    //   BlockathonService.checkEDBLogistics(key, params).then((res) => {
    //     console.log('RES')
    //     console.log(res)
    //     commit(types.SET_EUIPO_SCORE, {score: res})
    //   })
    // } else {
    //   BlockathonService.checkEDB(key, params).then((res) => {
    //     console.log('RES2')
    //     console.log(res)
    //     commit(types.SET_EUIPO_SCORE, { score: res })
    //   })
    // }
  },

  loadImpactHistory ({ commit }, { installId }) {
    BigChainDBService.loadImpactHistory(installId).then((res) => {
      console.log('update history')
      commit(types.LOAD_HISTORY, res)
    })
  },

  loadCauses ({ commit }) {
    BigChainDBService.loadCauses().then((res) => {
      commit(types.LOAD_CAUSES, res)
    })
  },

  donateToCause ({ commit, dispatch }, { installId, amount, publicKey }) {
    commit(types.DONATION_START)
    BigChainDBService.donateToCause(installId, amount, publicKey).then((res) => {
      commit(types.DONATION_DONE)
      commit(types.DONATE_POINTS, amount)
      dispatch('loadImpactHistory', { installId })
      dispatch('showSnackBar', {message: `${amount} Impact points donated!`})
    }).catch((err) => {
      console.log(err)
      commit(types.DONATION_DONE)
    })
  },

  createScanEvent ({ commit, dispatch }, {message, uid, lat, lng, installId}) {
    BigChainDBService.createScanEvent({message, uid, lat, lng, installId}).then((scan) => {
      if (scan.points_awarded) {
        commit(types.AWARD_POINTS, scan.code_value)
        dispatch('showSnackBar', {message: `${scan.code_value} Impact points earned.`})
      }
    })
  },

  initUserBDB ({ commit }, { installId }) {
    let keyPair = BigChainDBService.loadKeys(installId)

    return new Promise((resolve, reject) => {
      if (!keyPair) {
        BigChainDBService.generateKeys(installId).then(() => {
          BigChainDBService.onboardUser(installId).then((user) => {
            commit(types.LOAD_USER_DATA, { user })
            resolve()
          })
        })
      } else {
        BigChainDBService.onboardUser(installId).then((user) => {
          commit(types.LOAD_USER_DATA, { user })
          resolve()
        })
      }
    }).catch((err) => {
      console.log('err init user')
      reject()
    })
  }
}

const mutations = {
  [types.LOAD_USER_DATA] (state, { user }) {
    state.user = { ...user }
  },

  [types.DISPLAY_REWARD_POPUP] (state, { user }) {
    state.showRewardPopup = true
  },

  [types.HIDE_REWARD_POPUP] (state) {
    state.showRewardPopup = false
  },

  [types.LOAD_CAUSES] (state, causes) {
    state.causes = causes
  },

  [types.AWARD_POINTS] (state, points) {
    state.user.points += points
  },

  [types.DONATE_POINTS] (state, amount) {
    state.user.points -= amount
  },

  [types.DONATION_DONE] (state) {
    state.donating = false
  },

  [types.DONATION_START] (state) {
    state.donating = true
  },

  [types.LOAD_HISTORY] (state, history) {
    state.history = history
  },

  [types.LOAD_RECHECK_DATA] (state, recheck) {
    state.recheck = recheck
  },

  [types.LOAD_GS1] (state, gs1) {
    state.gs1 = gs1
  },

  [types.SET_EUIPO_SCORE] (state, scores) {
    var sum = 0
    scores.forEach((nb) => {
      sum += parseInt(nb)
    })
    state.euipoScore = sum / scores.length
  } 
}

export default {
  state,
  getters,
  actions,
  mutations
}
