import ScantrustService from '@/services/ScantrustService'
import * as types from '../mutations'

const state = {
  code: {},
  scan: {},
  campaign: {},
  smartlabel: {
    data: []
  },
  loaded: false,
  apiKey: '',
  uid: '',
  qr: '',
  installId: ''
}

const getters = {
  scan: state => state.scan,
  code: state => state.code,
  uid: state => state.uid,
  qr: state => state.qr,
  smartlabel: state => state.smartlabel,
  isLoaded: state => state.loaded,
  updated_at: state => state.smartlabel.updated_at,

  getUrlParameters: (state) => {
    return {uid: state.uid, qr: state.qr, api_key: state.apiKey, installId: state.installId}
  },

  getSmartLabelTab: (state, getters) => (key) => {
    return JSON.parse(JSON.stringify(getters.smartlabel.data.find(obj => obj.key === key)))
  },

  getMainSections: (state, getters) => {
    let tabs = []
    getters.smartlabel.data.forEach(function (tab) {
      if (tab.is_enabled === true) {
        tabs.push(tab.key)
      }
    })

    let main = tabs.slice(0, 4)

    if (tabs.length > 5) {
      main.push('more')
    }

    return main
  },

  getMoreSection: (state, getters) => {
    let tabs = []

    getters.smartlabel.data.forEach((tab) => {
      if (tab.is_enabled === true) {
        tabs.push(tab.key)
      }
    })

    let more = tabs.slice(4)

    return more
  },

  getNutrient: (state, getters) => (key) => {
    let item = {}

    getters.getSmartLabelTab('nutrition').data.table.forEach((obj) => {
      if (obj.key === key) {
        item = obj
      } else if (obj.children) {
        obj.children.forEach((child) => {
          if (child.key === key) {
            item = child
          }
        })
      }
    })

    if (!item) {
      item = {serving: 'N/A', key: key, name: key}
    }

    return JSON.parse(JSON.stringify(item))
  }
}

const actions = {

  saveUrlParameters ({ commit }, { uid, qr, apiKey, installId }) {
    commit(types.SAVE_URL_PARAMETERS, { uid, qr, apiKey, installId })
  },

  getCombinedInfos ({ commit }, { uid }) {
    return new Promise((resolve, reject) => {
      ScantrustService.getCombinedInfos(uid).then((combinedInfos) => {
        commit(types.LOAD_SCAN_DATA, { scan: combinedInfos.scan })
        commit(types.LOAD_CODE_DATA, { code: combinedInfos.code })
        commit(types.LOAD_CAMPAIGN_DATA, { campaign: combinedInfos.campaign })
        commit(types.LOAD_SMARTLABEL_DATA, { smartlabel: combinedInfos.smartlabel })
        resolve()
      })
    })

  },

  getScanData ({ commit }, { uid }) {
    ScantrustService.getScanInfos(uid).then((scan) => {
      commit(types.LOAD_SCAN_DATA, { scan })
    })
  },

  getCodeData ({ commit }, { qr }) {
    ScantrustService.getCodeInfos(qr).then((code) => {
      commit(types.LOAD_CODE_DATA, { code })
    })
  },

  getCampaignData ({ commit }) {
    ScantrustService.getCampaignInfos().then((campaign) => {
      commit(types.LOAD_CAMPAIGN_DATA, { campaign })
    })
  }
}

const mutations = {

  [types.LOAD_SCAN_DATA] (state, { scan }) {
    state.scan = { ...scan }
    state.loaded = true
  },

  [types.LOAD_SMARTLABEL_DATA] (state, { smartlabel }) {
    state.smartlabel = { ...smartlabel }
  },

  [types.LOAD_CODE_DATA] (state, { code }) {
    state.code = { ...code }
  },

  [types.SAVE_URL_PARAMETERS] (state, { uid, qr, apiKey, installId }) {
    state.uid = uid
    state.qr = qr
    state.apiKey = apiKey
    state.installId = installId
  },

  [types.LOAD_CAMPAIGN_DATA] (state, { campaign }) {
    state.campaign = { ...campaign }
  }

}

export default {
  state,
  getters,
  actions,
  mutations
}
