<template>
  <div class="loading flex flex-vertical-align">
    <div class="sk-double-bounce">
        <div class="sk-child sk-double-bounce1"></div>
        <div class="sk-child sk-double-bounce2"></div>
      </div>
  </div>
</template>

<script>

export default {
  name: 'loading'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.loading{
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  z-index: 9999;
}

.sk-double-bounce {
  width: 40px;
  height: 40px;
  position: relative;
  margin: 40px auto;
}

.sk-child {
  background-color: #21409A;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  opacity: 0.6;
  position: absolute;
  top: 0;
  left: 0;
  -webkit-animation: sk-doubleBounce 2s infinite ease-in-out;
  animation: sk-doubleBounce 2s infinite ease-in-out;
}

.sk-double-bounce2 {
  -webkit-animation-delay: -1.0s;
  animation-delay: -1.0s;
}

@-webkit-keyframes sk-doubleBounce {
  0%, 100% {
    -webkit-transform: scale(0);
            transform: scale(0); }
  50% {
    -webkit-transform: scale(1);
            transform: scale(1); } }

@keyframes sk-doubleBounce {
  0%, 100% {
    -webkit-transform: scale(0);
            transform: scale(0); }
  50% {
    -webkit-transform: scale(1);
            transform: scale(1); } }

</style>
