// ST Enpoint calls

import axios from 'axios'
import Config from '../config.js'

var Promise = require('promise-polyfill')

var scantrustAxios = axios.create({
  baseURL: Config.st_config.API_BASE_URL
})

export default {

  setAuthorizationHeader: function (apiKey) {
    scantrustAxios.defaults.headers.common['X-ScanTrust-Consumer-Api-Key'] = apiKey
  },

  getCombinedInfos: function (uid) {
    return new Promise((resolve, reject) => {
      scantrustAxios.get('scan/' + uid + '/combined-info/').then((res) => {
        resolve(res.data)
      }).catch((err) => {
        reject(err)
      })
    })
  },

  getCodeInfos: function (qr) {
    return new Promise((resolve, reject) => {
      scantrustAxios.get(qr + '/details/').then((res) => {
        resolve(res.data)
      }).catch((err) => {
        reject(err)
      })
    })
  },

  getScanInfos: function (uid) {
    return new Promise((resolve, reject) => {
      scantrustAxios.get('scan/' + uid + '/info/').then((res) => {
        resolve(res.data)
      }).catch((err) => {
        reject(err)
      })
    })
  },

  sendScanPosition: function (options) {
    return new Promise((resolve, reject) => {
      scantrustAxios.post('scan/' + options.uid + '/geotag/', {lat: options.position.coords.latitude, lng: options.position.coords.longitude}).then((data) => {
        resolve()
      }).catch((err) => {
        reject(err)
      })
    })
  },

  getCampaignInfos: function (options) {
    return new Promise((resolve, reject) => {
      scantrustAxios.get('campaign/').then((res) => {
        resolve(res.data)
      }).catch((err) => {
        reject(err)
      })
    })
  }
}
