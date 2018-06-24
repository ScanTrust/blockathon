<template>
  <div class="euipo flex flex-vertical flex-space-between">
    <div class="flex-1">
      <md-list v-for="(item, index) in euipo_arr" >
        <md-subheader>{{item.name}}</md-subheader>

        <md-list-item v-for="(child, indexChild) in item.children"
          v-if="child.value != '' && child.name != 'Product' && child.name != 'Location'">
          <span class="md-list-item-text">
            {{child.name}}:
          </span>
          <span class="md-list-item-text">
            {{child.value}}
          </span>
          <div class="checkboxFive">
            <input :id="'id-' + index + '-' + indexChild" type="checkbox" @click="child.selected = !child.selected" checked />
            <label :for="'id-' + index + '-' + indexChild"></label>
          </div>
          
        </md-list-item>
      </md-list>
    </div>

    <div class="column space-around">
      <md-button class="md-raised md-primary" @click="callToService()">Send</md-button>
      <div class="column score-block" :class="[euipoScore > '0' ? 'visible' : 'hide' ]">
        <span>EUIPO confidence score: </span>
        <span class="score" :class="[euipoScore >= '50' ? 'green' : 'red' ]">{{this.euipoScore}}%</span>
        <span>This product has {{this.euipoScore}}% chance to be counterfeit</span>
      </div>
      
    </div>
    <div class="row space-around link-block">
      <a @click="sendAuthorities()">Report to the authorities</a>
    </div>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'

export default {
  name: 'euipo',
  computed: mapGetters(['euipoScore']),  
  data() {
    return {
      score: 50,
      product: 53,
      euipo_arr : [{'children': [{'key': 'product', 'name': 'Product', 'value': '53'},
                                    {'key': 'location', 'name': 'Location', 'value': '3190538'},
                                    {'key': 'country', 'name': 'Country', 'value': 'Slovenia'},
                                    {'key': 'city', 'name': 'City', 'value': ''},
                                    {'key': 'type', 'name': 'Type', 'value': 'General agency'}],
                       'key': 'logistics_distribution',
                       'name': 'Logistics Distribution'},
                      {'children': [{'key': 'product', 'name': 'Product', 'value': '53'},
                                    {'key': 'country', 'name': 'Country', 'value': 'DE'},
                                    {'key': 'country_name', 'name': 'Country name', 'value': 'Germany'},
                                    {'key': 'price', 'name': 'Price', 'value': 24.4}],
                       'key': 'marketprice',
                       'name': 'Market price'},
                      {'children': [{'key': 'product', 'name': 'Product', 'value': '53'},
                                    {'key': 'name', 'name': 'Name', 'value': 'Ninja Delivery'},
                                    {'key': 'country', 'name': 'Country', 'value': 'SK'},
                                    {'key': 'country_name',
                                     'name': 'Country_name',
                                     'value': 'Slovakia'},
                                    {'key': 'function', 'name': 'Function', 'value': 'Distributor'}],
                       'key': 'operators',
                       'name': 'Operators'},
                      {'children': [{'key': 'product', 'name': 'Product', 'value': '53'},
                                    {'key': 'type', 'name': 'Type', 'value': 'Bunch'},
                                    {'key': 'origin', 'name': 'Origin', 'value': 'Packaging for direct consumers'},
                                    {'key': 'items', 'name': 'Items', 'value': 6}],
                       'key': 'packaging',
                       'name': 'Packaging'},
                      {'children': [{'key': 'product', 'name': 'Product', 'value': '53'},
                                    {'key': 'market', 'name': 'Market', 'value': 'Public markets'},
                                    {'key': 'packaging',
                                     'name': 'Packaging',
                                     'value': 'Company branded packaging'}],
                       'key': 'sellingstrategy',
                       'name': 'Selling strategy'}],
    }
  },
  beforeMount () {
    this.euipo_arr.forEach((item) => {
      item.children.forEach((child) => {
        child.selected = true
      })
    })
    console.log('all selected')
    console.log(this.euipo_arr)
  },
  methods: {
    sendAuthorities () {
      this.$store.dispatch('sendAuthoritiesAlert')
    },
    callToService () {
      var params = []
      this.euipo_arr.forEach((item) => {
        let selectedChildren = []
        item.children.forEach((child) => {          
          if (child.selected) {
            selectedChildren.push(child);
          } else {
            var tempChild = JSON.parse(JSON.stringify(child)); 
            tempChild.value = '';
            selectedChildren.push(tempChild);
          }
        })
        console.log(selectedChildren)
        console.log('selected children :')
        params.push({key: item.key, params: selectedChildren})
      })
      this.$store.dispatch('checkEuipo', params)

    },
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .row{
    flex-direction: row;
    display: flex;
    align-items: center;
  }
  .column{
    flex-direction: column;
    display: flex;
    align-items: center;
  }
  .space-around{
    justify-content: space-around;
  }
  .link-block{
    text-transform: capitalize;
    padding: 10px;
  }
  .score {
    font-size: 2em;
  }
  .red{ 
    color: red;
  }
  .green{ 
    color: green;
  }
  .md-list-item-text{
    white-space: initial;
    padding-right: 5px;
    font-size: 1.5rem;
  }
  .hide{ display: none}
  .visible{ display: flex}
  .score-block{
    margin-top: 5px;
  }
  .checkboxFive {
    width: 20px;
    position: relative;
  }
  .checkboxFive label {
    cursor: pointer;
    position: absolute;
    width: 20px;
    height: 20px;
    top: 0;
    left: 0;
    background: #fff;
    border:1px solid #5f99ab;
  }
  .checkboxFive label:after {
    opacity: 0;
    content: '';
    position: absolute;
    width: 9px;
    height: 5px;
    background: transparent;
    top: 6px;
    left: 5px;
    border: 3px solid #5f99ab;
    border-top: none;
    border-right: none;

    transform: rotate(-45deg);
  }
  .checkboxFive label:hover::after {
    opacity: 0;
  }
  .checkboxFive input[type=checkbox]:checked + label:after {
    opacity: 1;
  } 
</style>
