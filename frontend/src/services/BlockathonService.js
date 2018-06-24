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

  getEDBLogistics: function (name, params) {
    var newParams = {}

    params.forEach((param) => {
      newParams[params.key] = params.value
    })
    return new Promise((resolve, reject) => {
      blockathonAxios.post('/api/blockathon/edb/logistics/' + name + '/', newParams).then((res) => {
        resolve(res.data)
      }).catch((err) => {
        reject(err)
      })
    })
  },
  checkEDB: function (name, params) {
    var newParams = {}

    params.forEach((param) => {
      newParams[params.key] = params.value
    })

    return new Promise((resolve, reject) => {
      blockathonAxios.post('/api/blockathon/edb/' + name + '/', newParams).then((res) => {
        resolve(res.data)
      }).catch((err) => {
        reject(err)
      })
    })
  },

  checkFakeEDB: function (name, params) {
    var newParams = {}
    var nbField = params.length
    var nbFieldWithValue = params.length

    params.forEach((param) => {
      newParams[param.key] = param.value
      if (!param.value) {
        nbFieldWithValue--
      }
    })

    if (params.length - nbFieldWithValue >= 2) {
      nbFieldWithValue = 0
    }

    var percent = nbFieldWithValue / nbField * 100
    // return new Promise((resolve, reject) => {
    return percent.toFixed(0)
    // })
  }
}
