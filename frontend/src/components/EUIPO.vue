<template>
  <div class="euipo">
    <!-- <form novalidate > -->
      <md-list v-for="(value, key) in euipo_data">
        <md-subheader>packaging</md-subheader>

        <md-list-item v-for="(value2, key2) in euipo_data[key]">
          <span class="md-list-item-text" :class="{'line-through': toggleTracker[key][key2]}">
            {{key2}}: {{value2}}
          </span>
          <md-switch v-model="toggleTracker[key][key2]" @click="toggleTracker[key][key2] = !toggleTracker[key][key2]" class="md-primary" />
        </md-list-item>
        <hr class="hr">
      </md-list>
      
      <md-button type="submit" class="md-primary" :disabled="sending">Check list</md-button>
    </form>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'

export default {
  name: 'euipo',
  // computed: mapGetters(['getSmartLabelTab']),
  mounted: function () {
    this.initToggleTracker()  
  },
  methods: {
    initToggleTracker: function () {
      for (var key in this.euipo_data) {
        this.toggleTracker[key] = JSON.parse(JSON.stringify(this.euipo_data[key]))
        for (var itemKey in this.toggleTracker[key]) {
          this.toggleTracker[key][itemKey] = true
        }
      }
      console.log('toggle track')
      console.log(this.toggleTracker)
    }
  },
  data: function () {
    return {
      toggleTracker: {},
      euipo_data: {
        packaging: {
          product_id: "product",
          type: "type",
          origin: "origin",
          items: 10
        },
        marketprice: {
          product_id: "product",
          country: "country",
          price: 65
        }
      }
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .hr{
    border-color: #000;
    width: 100%;
  }
  .line-through{
    text-decoration: line-through;
    background-color: #e0e0e0
  }
</style>
