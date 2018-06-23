<template>
  <div class="product-infos flex flex-vertical flex-space-between">
    <div class="product-image flex-1 img-ctn" v-bind:style="{ 'background-image' : 'url(' + code.product.image + ')' }">
      <!-- <img class="product-image" v-bind:src="product.images['1']" alt=""> -->
    </div>

    <div class="infos-ctn">
      <div v-bind:class="getScanResult()" class="result roboto-medium">
        <span v-if="getScanResult() == 'genuine'">Genuine</span>
        <span v-if="getScanResult() == 'verified'">Verified</span>
        <span v-if="getScanResult() == 'counterfeit'">Suspected Counterfeit</span>
      </div>

      <div class="Grid -middle">
        <div class="Cell -fill product-name roboto">
          {{code.product.name}}
        </div>
      </div>

      <div class="serial roboto">
        SN - {{code.qrcode.serial_number}}
      </div>
    </div>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'product-infos',
  computed: mapGetters(['code', 'scan']),
  methods: {
    getScanResult: function () {
      if (this.code.qrcode.activation_status === 'inactive' || this.code.qrcode.is_blacklisted || (this.scan.reason === 'auth' && this.scan.result !== 'ok')) {
        return 'counterfeit'
      } else if (this.scan.reason === 'auth' && this.scan.result === 'ok') {
        return 'genuine'
      } else {
        return 'verified'
      }
    }
  },
  data () {
    return {
      result: ''
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.product-infos{
  padding: 15px 0px;
  height: calc(100% - 128px);
}

.weight-infos{
  border-left: 1px solid #bbbbbb;
  padding: 3px 10px;
  color: #bbbbbb;
  font-size: 1.2rem;
}

.serial{
  color: #999;
  font-size: calc(9px + 1vw);
  margin-left: 10px;
}

.weight-infos .number{
  font-size: calc(12px + 1vw);
}

.product-image{
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center center;
  /*max-height: 70%;*/
}

.product-name{
  font-size: calc(16px + 1vw);
  color: black;
  margin-left: 10px;
}

.result{
  margin-left: 10px;
  margin-top: 10px;
  font-size: calc(17px + 1vw);
  border-left: 5px solid #6099ab;
  color:#6099ab;
  padding-left: 5px;
}

.genuine {
  color:green;
  border-color: green;
}

.verified {
  border-color: #6099ab;
  color: #6099ab;
}

.counterfeit {
  color: red;
  border-color: red;
}

</style>
