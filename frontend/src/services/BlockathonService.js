// ST Enpoint calls

import axios from 'axios'
import Config from '../config.js'

var Promise = require('promise-polyfill')

var blockathonAxios = axios.create({
  baseURL: Config.euipo_config.EUIPO_URL
})

export default {

  setAuthorizationHeader: function (apiKey) {
    blockathonAxios.defaults.headers.common['X-ScanTrust-Consumer-Api-Key'] = apiKey
  },

  getLogistics: function (name) {
    return new Promise((resolve, reject) => {
      blockathonAxios.get('/api/blockathon/edb/logistics/' + name).then((res) => {
        resolve(res.data)
      }).catch((err) => {
        reject(err)
      })
    })
  },
  getEDB: function (name, options) {
    return new Promise((resolve, reject) => {
      blockathonAxios.get('/api/blockathon/edb/' + name, options).then((res) => {
        resolve(res.data)
      }).catch((err) => {
        reject(err)
      })
    })
  }
}
