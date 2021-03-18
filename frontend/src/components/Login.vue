<template>
  <div class="login">
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <div class="card">
            <form class="box" @submit="postLoginData">
              <h1>Login</h1>
              <p class="text-muted">Please enter your login and password!</p>
              <p class="text_warning" v-for="item in error" :key="item.id">{{ item }}</p>
              <input
                type="text"
                name="username"
                placeholder="Username"
                v-model="LoginForm.username"
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                v-model="LoginForm.password"
              />
              <input type="submit" name="login" value="Login" href="#" />
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
Vue.use(VueAxios, axios);
export default {
  name: "Login",
  data() {
    return {
      LoginForm: {
        username: null,
        password: null
      },
      error: []
    };
  },
  methods: {
    postLoginData(e) {
      this.error = [];
      if (!this.LoginForm.username) {
        this.error.push("Username is required");
      }
      if (!this.LoginForm.password) {
        this.error.push("Password is required");
      }
      if (this.LoginForm.username && this.LoginForm.password) {
        console.log(this.LoginForm);
        this.axios
          .post("/login", this.LoginForm)
          .then(result => {
            console.log(result);
            if (result.data.loggedin == true) {
              console.log("Login is validated");
              this.$store.commit("addUserData", {
                username: this.LoginForm.username
              });
              this.$router.replace({ path: "/" });
            } else {
              this.error.push(result.data.error);
            }
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
      e.preventDefault();
    }
  }
};
</script>
<style>
.login {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
  background: linear-gradient(to right, #b92b27, #1565c0);
}

.box {
  width: 500px;
  padding: 40px;
  position: absolute;
  top: 50%;
  left: 50%;
  background: #191919;
  text-align: center;
  transition: 0.25s;
  margin-top: 100px;
}

.box input[type="text"],
.box input[type="password"] {
  border: 0;
  background: none;
  display: block;
  margin: 20px auto;
  text-align: center;
  border: 2px solid #3498db;
  padding: 10px 10px;
  width: 250px;
  outline: none;
  color: white;
  border-radius: 24px;
  transition: 0.25s;
}

.box h1 {
  color: white;
  text-transform: uppercase;
  font-weight: 500;
}

.box input[type="text"]:focus,
.box input[type="password"]:focus {
  width: 300px;
  border-color: #2ecc71;
}

.box input[type="submit"] {
  border: 0;
  background: none;
  display: block;
  margin: 20px auto;
  text-align: center;
  border: 2px solid #2ecc71;
  padding: 14px 40px;
  outline: none;
  color: white;
  border-radius: 24px;
  transition: 0.25s;
  cursor: pointer;
}

.box input[type="submit"]:hover {
  background: #2ecc71;
}

.forgot {
  text-decoration: underline;
}

ul.social-network {
  list-style: none;
  display: inline;
  margin-left: 0 !important;
  padding: 0;
}

ul.social-network li {
  display: inline;
  margin: 0 5px;
}

.social-network a.icoFacebook:hover {
  background-color: #3b5998;
}

.social-network a.icoTwitter:hover {
  background-color: #33ccff;
}

.social-network a.icoGoogle:hover {
  background-color: #bd3518;
}

.social-network a.icoFacebook:hover i,
.social-network a.icoTwitter:hover i,
.social-network a.icoGoogle:hover i {
  color: #fff;
}

a.socialIcon:hover,
.socialHoverClass {
  color: #44bcdd;
}

.social-circle li a {
  display: inline-block;
  position: relative;
  margin: 0 auto 0 auto;
  border-radius: 50%;
  text-align: center;
  width: 50px;
  height: 50px;
  font-size: 20px;
}

.social-circle li i {
  margin: 0;
  line-height: 50px;
  text-align: center;
}

.social-circle li a:hover i,
.triggeredHover {
  transform: rotate(360deg);
  transition: all 0.2s;
}

.social-circle i {
  color: #fff;
  transition: all 0.8s;
  transition: all 0.8s;
}
</style>