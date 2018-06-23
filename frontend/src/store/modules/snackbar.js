import * as types from '../mutations'

const state = {
  show: false,
  message: ''
}

const getters = {
  snackBar: state => state,
  showSnackbar: state => state.show,
  snackBarMessage: state => state.message
}

const actions = {
  showSnackBar ({ commit, dispatch }, { message, duration }) {
    commit(types.SHOW_SNACK_BAR, { message })
    setTimeout(() => {
      dispatch('dissmissSnackBar')
    }, duration || 4000)
  },

  dissmissSnackBar ({ commit }) {
    commit(types.DISSMISS_SNACK_BAR)
  }
}

const mutations = {

  [types.SHOW_SNACK_BAR] (state, { message, duration }) {
    state.show = true
    state.message = message
  },

  [types.DISSMISS_SNACK_BAR] (state) {
    state.show = false
  }

}

export default {
  state,
  getters,
  actions,
  mutations
}
