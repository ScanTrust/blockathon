<template>
  <div class="scm">
    <div class="disclaimer roboto">
      Trace & Trace data listed in SmartLabel™ are provided by ScanTrust SA, leading provider of secure cloud-based product authentication and supply chain traceability solutions.
    </div>
    <div :key="scm.key" v-show="scm.value" v-for="scm in code.scm_data" class="scm-field">
      <div class="label roboto-medium">{{scm.name}}</div>
      <div class="value roboto">{{scm.value}}</div>
    </div>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'scm',
  computed: mapGetters(['code']),
  data () {
    return {
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

.scm{
  padding: 10px 17px;
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

</style>
