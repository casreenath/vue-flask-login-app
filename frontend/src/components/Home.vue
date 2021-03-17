<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark" fixed="top">
      <b-navbar-brand href="#">BlackBox</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item @click="updateComponent('JigManager')">JigManager</b-nav-item>
          <b-nav-item @click="updateComponent('Pipeline')">Pipeline</b-nav-item>
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
    <component class="body-component" v-bind:is="displayComponent"></component>
    <!-- <p class="hometest">Component</p> -->
    <!-- <p class="hometest">Home Component</p> -->
  </div>
</template>
<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
Vue.use(VueAxios, axios);
import JigManager from "./JigManager";
import Pipeline from "./Pipeline";
export default {
  name: "home",
  components: {
    JigManager: JigManager,
    Pipeline: Pipeline
  },
  data() {
    return {
      error: [],
      displayComponent: "Pipeline"
    };
  },
  methods: {
    postlogout(e) {
      console.log("logging out");
      this.error = [];
      this.axios
        .get("/logout")
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
    },
    updateComponent(item) {
      console.log("Changing component to ", item);
      this.displayComponent = item;
    }
  }
  //   beforeCreate() {
  //     if (this.$store.state.isLogged) {
  //       this.$router.push({ name: "login" });
  // }
  //   }
};
</script>
<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
  background: whitesmoke !important;
}

.hometest {
  padding: 100px;
  margin: 400px;
}
.navigation-link {
  text-decoration: none;
}
.body-component {
  margin-top: 65px;
}
</style>