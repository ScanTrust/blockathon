<template>
  <div class="consumer-impact">
    <div class="balance-ctn">
      <div class="title">Balance:</div>
      <div class="balance">{{this.user.points}} Impact Points</div>
    </div>

    <div class="organizations-ctn">
      <md-card class="organization" :key="cause.pub_key" v-for="cause in causes">
        <md-card-media class="reward-image">
          <img :src="cause.image_url" alt="organization img">
        </md-card-media>

        <md-card-header>
            <div class="md-title md-layout-item">
              {{cause.name}}
            </div>
        </md-card-header>

        <md-card-content class="card-content">
          <div class="description">
            {{cause.description}}
          </div>

          <div class="goals">
            {{cause.goal}}
          </div>

        </md-card-content>

        <md-card-actions>
          <md-button :disabled="donating || parseInt(cause.donation_value) > user.points" @click="donate(cause.pub_key, parseInt(cause.donation_value))" class="md-primary">Donate {{cause.donation_value}} points</md-button>
        </md-card-actions>
      </md-card>
    </div>

    <div class="history">
      <div class="title">Impact History: </div>
      <div v-for="obj in historyMap" :key="obj.name" class="transfer-list-ctn">
        <div v-if="obj && obj.amount_donated" class="transfer md-layout-item md-layout md-alignment-center-left">
          <div class="transfer-infos md-layout-item">
            <div class="transfer-name">
             You donated {{obj.amount_donated}} Impact Points to <a :href="obj.url">{{obj.name}}</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'

export default {
  name: 'consumer-impact',
  computed: mapGetters(['user', 'causes', 'donating', 'historyMap']),
  methods: {
    donate (publicKey, amount) {
      console.log('DONATE TO -> ' + publicKey)
      this.$store.dispatch('donateToCause', {installId: this.$route.query.install_id, publicKey: publicKey, amount: parseInt(amount)})
    }
  },
  data: function () {
    return {
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.organizations-ctn, .history{
  padding: 10px;
}

.organization{
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  border-radius: 4px;
  perspective: 1px;
  overflow: hidden;
  margin-top: 10px;
}

button{
  font-family: 'Roboto Medium';
}

.organization img{
  width: 100%;
  object-fit: cover;
  height: 200px;
}

.goals{
  font-family: 'Roboto Medium';
  color: black;
  margin-top: 10px;
}

.title{
  font-family: 'Roboto Medium';
  font-size: calc(12px + 1vw);
  color: black;
}

.organization .infos .description{
  font-family: 'Roboto Light';
  font-size: calc(12px + 1vw);
  margin: 5px 5px 10px 10px;
  color: black;
}

.organization .action{
  text-align: right;
  padding: 10px;
}

.organization .action button{
  font-family: 'Roboto Medium';
  text-transform: uppercase;
  font-size: calc(12px + 1vw);
  color: white;
  background: #60ab97;
  padding: 8px;
  border: none;
  border-radius: 2px;
  outline: none;
}

.balance-ctn{
  font-family: 'Roboto';
  font-size: calc(14px + 1vw);
  padding: 10px 5px 10px 17px;
  color: black;
}
.balance-ctn .balance{
  color:#60ab97;
  font-family: 'Roboto';
  font-size: calc(25px + 1vw);
}

.transfer-list-ctn{
  margin-top: 10px;
}

.transfer{
  padding: 8px 0px;
}

</style>
