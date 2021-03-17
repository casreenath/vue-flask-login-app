<template>
  <div>
    <p>Pipeline Component</p>
  </div>
</template>
<script>
export default {
  name: "Pipeline",
  created() {
    console.log("Created Pipeline component");
  },
  destroyed() {
    console.log("Destroyed Pipeline Component");
  }
};
</script>
<style scoped>
/* .hometest {
  padding: 100px;
  margin: 400px;
} */
</style>