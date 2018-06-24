<template>
  <div class="scm">
    <div class="disclaimer roboto">
      Trace & Trace data listed in SmartLabel™ are provided by ScanTrust SA, leading provider of secure cloud-based product authentication and supply chain traceability solutions.
    </div>
    <div :key="scm.key" v-show="scm.value" v-for="scm in code.scm_data" class="scm-field">
      <div class="label roboto-medium">{{scm.name}}</div>
      <div class="value roboto">{{scm.value}}</div>
    </div>

    <div v-if="recheck.order" class="recheck">
      <img src="../assets/recheck-logo.png" alt="recheck">
      <div class="recheck-content">
        <div class="section-title">
          Recheck Journey Overview
        </div>
        
        <div class="overview-section">
          <div class="title">
            Sender
          </div>
          <div class="Grid -between text">
            <div class="Cell Grid">
              <div class="icon" v-html="icons.location"></div>
              {{recheck.sender.name}}
            </div>
            <div class="Cell">{{recheck.sender.address}}</div>
          </div>
          <div>
            {{this.formatDate(recheck.transit_events[0].date)}}
          </div>
          <div class="identifier">
            {{recheck.sender.identifier}}
          </div>
        </div>
        <div class="overview-arrow">
          <div class="icon" v-html="icons.arrow"></div>
        </div>

        <div class="overview-section">
          <div class="title">
            Shipping Provider
          </div>
          <div class="Grid -between text">
            <div class="Cell Grid">
              <div class="icon" v-html="icons.location"></div>
              {{recheck.shipping_provider.name}}
            </div>
            <div class="Cell">{{recheck.shipping_provider.address}}</div>
          </div>
          <div>
            {{this.formatDate(recheck.transit_events[1].date)}}
          </div>
          <div class="identifier">
            {{recheck.shipping_provider.identifier}}
          </div>
        </div>
        <div class="overview-arrow">
          <div class="icon" v-html="icons.arrow"></div>
        </div>

        <div class="overview-section">
          <div class="title">
            Receipient
          </div>
          <div class="Grid -between text">
            <div class="Cell Grid">
              <div class="icon" v-html="icons.location"></div>
              {{recheck.reciever.name}}
            </div>
            <div class="Cell">{{recheck.reciever.address}}</div>
          </div>
          <div>
            {{this.formatDate(recheck.transit_events[3].date)}}
          </div>
          <div class="identifier">
            {{recheck.reciever.identifier}}
          </div>
        </div>
      </div>
    </div>

    <div class="gs1">
      <img src="../assets/gs1-logo.png" alt="gs1">

      <div class="title">GS1 Status: <strong>{{gs1.status}}</strong></div>
      <div>{{gs1.message}}</div>
      <div><strong>{{gs1.fields.company}}</strong></div>

    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'scm',
  computed: mapGetters(['code', 'recheck', 'gs1']),
  methods: {
    formatDate (string) {
      let date
      
      date = new Date(Date.parse(string.replace(/-/g, '/').replace(/[a-z]+/gi, ' ')))

      let minutes = date.getMinutes() <= 9 ? '0' + date.getMinutes() : date.getMinutes()
      let days = date.getDate() <= 9 ? '0' + date.getDate() : date.getDate()
      let months = date.getMonth() + 1 <= 9 ? '0' + (date.getMonth()) : date.getMonth()

      return `${date.getFullYear()}-${months}-${days} ${date.getHours()}:${minutes}`
    }
  },
  data () {
    return {
      icons: {
        arrow: require('@/assets/icons/arrow.svg'),
        location: require('@/assets/icons/location.svg')
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.disclaimer{
  color: #666666;
  font-size: calc(11px + 1vw);
  font-style: italic;
}

.overview-arrow{
  transform: rotateX(180deg);
}

.scm{
  padding: 10px 17px;
}

.gs1{
  text-align: center;
}

.gs1 img{
  width: 150px;
}

.identifier{
  background: #dedede;
  font-family: monospace;
  word-wrap: break-word;
}

.overview-arrow .icon{
  margin-left: auto;
  margin-right: auto;
  width: 20px !important;
}

.recheck{
  padding: 10px 8px;
}

.scm-field{
  color: black;
  padding-top: 20px;
}

.label{
  font-size: calc(12px + 1vw);
}

.value{
  font-size: calc(11px + 1vw);

}

.recheck{
  text-align: center;
}

.recheck-content{
  text-align: left;
}

.section-title{
  color: #21409a;
  font-size: calc(18px + 1vw);
  padding: 8px 14px;
  text-align: center;
  font-family: 'Roboto';
}
.overview-ctn{
  padding: 16px 14px 0px 14px;
}
.overview-arrow{
  padding: 8px 0px;
}
.overview-arrow .icon{
  width: calc(8px + 1vw);
  padding-left: 2px;
}
.overview-section .title{
  font-size: calc(11px + 1vw);
  color: black;
  font-family: 'Roboto';
  font-weight: bold;
  padding-bottom: 5px;
}
.address-ctn{
  padding-left: 14px;
  padding-top: 11px;
}
.text{
  font-family: 'Roboto';
  font-size: calc(9px + 1vw);
  color: #444;
}
.icon{
  padding-right: 5px;
}

</style>
