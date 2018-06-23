<template>
  <div class="nutrition">
    <div class="header-numbers Grid">
      <div class="number-ctn Cell -fill">
        <div class="number roboto-medium">
          {{this.getSmartLabelTab('nutrition').data.calories || 0}}
        </div>
        <div class="unit roboto">
          Calories
        </div>
      </div>

      <div :key="`key-${index}`" v-for="(key, index) in header" class="number-ctn Cell -fill">
        <div class="number roboto-medium">
          {{getNutrient(key).serving}}
        </div>
        <div class="unit roboto">
          {{getNutrient(key).name}}
        </div>
      </div>
    </div>

    <div class="serving-ctn">
      <div class="Grid -between">
        <span class="Cell label">Serving Size</span>
        <span class="Cell value">{{this.getSmartLabelTab('nutrition').data.serving.size}}</span>
      </div>
      <div class="Grid -between">
        <div class="Cell label">Serving per Container</div>
        <div class="Cell value">{{this.getSmartLabelTab('nutrition').data.serving.count}}</div>
      </div>
      <div class="Grid -between">
        <span class="Cell label">Total Calories</span>
        <span class="Cell value">{{this.getSmartLabelTab('nutrition').data.calories}}</span>
      </div>
    </div>
    <div class="nutrition-table">
      <div class="header Grid -between">
        <div class="name"></div>
        <div class="serving">Amount per Serving</div>
        <div class="daily">% Daily Value*</div>
      </div>
      <template v-for="(nutrient, nutrientIndex) in this.getSmartLabelTab('nutrition').data.table">
        <div :key="`nutrient-${nutrientIndex}`" class="row Grid">
          <div class="name Cell bold">{{nutrient.name}}</div>
          <div class="Cell serving">{{nutrient.serving}}</div>
          <div class="Cell daily">{{nutrient.daily || 0}}%</div>
        </div>
        <div :key="`nutrient-${nutrientIndex}-child-${childIndex}`" class="row Grid" v-if="nutrient.children" v-for="(children, childIndex) in nutrient.children">
          <div class="name Cell">{{children.name}}</div>
          <div class="Cell serving">{{children.serving}}</div>
          <div class="Cell daily">{{children.daily || 0}}%</div>
        </div>
      </template>

    </div>

    <app-footer></app-footer>
  </div>
</template>

<script>

import Footer from '@/components/Footer'
import { mapGetters } from 'vuex'

export default {
  name: 'nutrition',
  computed: {
    ...mapGetters(['getSmartLabelTab'])
  },
  data () {
    return {
      header: ['saturated-fat', 'sodium', 'sugar']
    }
  },
  methods: {
    getNutrient (key) {
      return this.$store.getters.getNutrient(key)
    }
  },
  components: {
    'app-footer': Footer
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.header-numbers{
  padding-bottom: 10px;
  border-bottom: 1px solid #f1f1f1;
}

.number-ctn{
  padding: 20px 5px;
  text-align: center;
  border-left: 1px solid #f1f1f1;
}

.number-ctn:first-child{
  border-left: none;
}

.number{
  color: #60ab97;
  font-size: calc(25px + 1vw);
}

.unit{
  color: black;
  text-transform: capitalize;
  font-size: calc(8px + 1vw);
}

.serving-ctn{
  padding: 15px 10px;
  color: black;
}

.label{
  padding: 5px 5px;
  font-size: calc(11px + 1vw);
  font-family: 'Roboto Medium';
}

.serving-ctn .value{
  padding: 5px 5px;
  font-size: calc(10px + 1vw);
  font-family: 'Roboto Light';
}

.name{
  font-family: 'Roboto Light';
  width: 60%;
}

.daily{
  width: 20%;
  text-align: right;
}

.serving{
  width: 20%;
}

.nutrition-table{
  padding: 10px 17px;
}

.nutrition-table .header{
  margin-bottom: 15px;
  background-color: #f1f1f1;
  padding: 5px 5px;
  margin-left: -17px;
  margin-right: -17px;
}
.header .serving{
  position: relative;
  left: -4px;
}

.nutrition-table .row{
  padding: 5px 0px;
  text-align: left;
  font-size: calc(10px + 1vw);
  font-family: 'Roboto Light';
  color: black;
}

.header .daily, .header .serving{
  font-family: 'Roboto Medium';
  font-size: calc(5px + 1vw);
}

.bold{
  font-size: calc(11px + 1vw);
  font-family: 'Roboto Medium';
}

.disclaimer{
  padding: 10px 17px;
  color: #666666;
  font-size: calc(9px + 1vw);
  font-style: italic;
}

</style>
