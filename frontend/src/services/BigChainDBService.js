import axios from 'axios'
import Config from '../config.js'
import * as driver from 'bigchaindb-driver'
import bip39 from 'bip39'

var connection = new driver.Connection(Config.bdb_config.API_BASE_URL)
var STProxyAxios = axios.create({
  baseURL: Config.st_proxy_config.API_BASE_URL
})

export default {

  loadImpactHistory: function (installId) {
    const keyPair = this.loadKeys(installId)
    return new Promise((resolve) => {
      STProxyAxios.post('users/history/', {pub_key: keyPair.publicKey}).then(function (res) {
        resolve(res.data)
      })
    })
  },

  loadCauses: function () {
    return new Promise((resolve) => {
      STProxyAxios.get('causes/').then(function (res) {
        resolve(res.data)
      })
    })
  },

  onboardUser: function (installId) {
    let keyPair = this.loadKeys(installId)

    return new Promise((resolve, reject) => {
      STProxyAxios.post('users/info/', {pub_key: keyPair.publicKey}).then(function (res) {
        resolve(res.data)
      }).catch((err) => {
        reject(err)
      })
    })
  },

  generateKeys: function (installId) {
    return new Promise((resolve) => {
      const seed = bip39.mnemonicToSeed(installId).slice(0, 32)
      const keyPair = new driver.Ed25519Keypair(seed)

      localStorage.setItem('keypair_' + installId, JSON.stringify(keyPair))
      resolve(keyPair)
    })
  },

  createScanEvent: function (options) {
    const keyPair = this.loadKeys(options.installId)
    return new Promise((resolve, reject) => {
      STProxyAxios.post('scans/add/', {message: options.message, uuid: options.uid, pub_key: keyPair.publicKey, lat: options.lat, lng: options.lng}).then(function (res) {
        resolve(res.data)
      }).catch((err) => {
        reject(err)
      })
    })
  },

  createWallet: function (installId) {
    const keyPair = this.loadKeys(installId)

    return new Promise((resolve, reject) => {
      STProxyAxios.post('wallets/register/', { pub_key: keyPair.publicKey }).then(function (res) {
        localStorage.setItem('wallet_' + installId, JSON.stringify(res.data.wallet_id))
        resolve()
      })
    })
  },

  isOnboard: function (installId) {
    return localStorage.getItem('onboard_' + installId)
  },

  loadKeys: function (installId) {
    return JSON.parse(localStorage.getItem('keypair_' + installId))
  },

  // searches assets in BDB based on a text input
  searchScans: function (search, name) {
    return new Promise((resolve, reject) => {
      connection.searchAssets(search).then(function (assetList) {
        const scansList = []

        for (const asset of assetList) {
          if (asset.data.name === 'scan') {
            scansList.push(asset)
          }
        }
        resolve(scansList)
      })
    })
  },

  // returns the blockchain history of an asset
  // under the hood, gets a list of metadata objects of all transfers of the asset
  getAssetHistory (assetId) {
    var that = this
    return new Promise((resolve, reject) => {
      connection.getTransaction(assetId).then((transaction) => {
        const assetData = transaction
        const metadataArr = []

        that.searchScans(assetId, 'scan').then((scans) => {
          for (var tx of scans) {
            metadataArr.push(tx.data)
          }

          resolve({
            'code': assetData,
            'history': metadataArr
          })
        })
      })
    })
  },

  getOutputs: async function (publicKey, spent = false) {
    await connection.listOutputs(publicKey, spent)
  },

  getTransaction: async function (assetId) {
    await connection.getTransaction(assetId)
  },

  transferMultipleAssets: async function (unspentTxs, keypair, outputs, metadata) {
    const transferOutputs = []
    if (outputs.length > 0) {
      for (const output of outputs) {
        let condition = driver.Transaction.makeEd25519Condition(output.publicKey)
        let transferOutput
        if (output.amount > 0) {
          transferOutput = driver.Transaction.makeOutput(condition, output.amount.toString())
        } else {
          transferOutput = driver.Transaction.makeOutput(condition)
        }
        transferOutput.public_keys = [output.publicKey]
        transferOutputs.push(transferOutput)
      }
    }
    const txTransfer = driver.Transaction.makeTransferTransaction(
      unspentTxs,
      transferOutputs,
      metadata
    )
    const txSigned = driver.Transaction.signTransaction(txTransfer, keypair.privateKey)
    let transaction = await connection.postTransactionCommit(txSigned)
    return transaction
  },

  donateToCause: async function (installId, amount, toPublicKey, transferMetadata = {}) {
    let keypair = this.loadKeys(installId)

    let tokenId = Config.bdb_config.TOKEN_ID
    const balances = []
    const outputs = []
    let cummulativeAmount = 0
    let sufficientFunds = false
    const trAmount = parseInt(amount)
    const unspents = await this.getOutputs(keypair.publicKey, false)
    if (unspents && unspents.length > 0) {
      for (const unspent of unspents) {
        const tx = await this.getTransaction(unspent.transaction_id)
        let assetId
        if (tx.operation === 'CREATE') {
          assetId = tx.id
        }
        if (tx.operation === 'TRANSFER') {
          assetId = tx.asset.id
        }
        if (assetId === tokenId) {
          const txAmount = parseInt(tx.outputs[unspent.output_index].amount)
          cummulativeAmount += txAmount
          balances.push({
            tx: tx,
            output_index: unspent.output_index
          })
        }
        if (cummulativeAmount >= trAmount) {
          sufficientFunds = true
          break
        }
      }
      if (!sufficientFunds) {
        throw new Error('Transfer failed. Not enough token balance!')
      }
      outputs.push({
        publicKey: toPublicKey,
        amount: trAmount
      })
      if (cummulativeAmount - trAmount > 0) {
        outputs.push({
          publicKey: keypair.publicKey,
          amount: cummulativeAmount - trAmount
        })
      }
      const metadata = {
        event: 'StakeTransfer',
        date: new Date(),
        timestamp: Date.now()
      }

      metadata.details = {
        ...transferMetadata
      }

      const transfer = await this.transferMultipleAssets(balances, keypair, outputs, metadata)
      return transfer
    }
  }
}
