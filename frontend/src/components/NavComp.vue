<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark" fixed="top">
      <b-navbar-brand href="#">BlackBox</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item-dropdown href="#" text="JigManager">
            <b-dropdown-item>View Jigs</b-dropdown-item>
            <b-dropdown-item>Add Jigs</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item>JigManager</b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <em>Username</em>
            </template>
            <b-dropdown-item href="#">Account</b-dropdown-item>
            <b-dropdown-item @click="postlogout">Log Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <!-- <p class="hometest">Component</p> -->
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
Vue.use(VueAxios, axios);
export default {
  name: "Navigation",
  data() {
    return {
      error: []
    };
  },
  methods: {
    postlogout(e) {
      console.log("logging out");
      this.error = [];
      this.axios
        .post("/logout")
        .then(result => {
          console.log(result);
          if (result.data.loggedin == false) {
            console.log("Logout is validated");
            this.$router.replace({ path: "/login" });
          } else {
            this.error.push(result.data.error);
          }
        })
        .catch(error => {
          console.error(error);
        });
      e.preventDefault();
    }
  }
};
</script>

<style scoped>
.hometest {
  padding: 100px;
  margin: 400px;
}
</style>

