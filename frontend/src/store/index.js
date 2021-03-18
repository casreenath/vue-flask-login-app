import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        userData: {
            username: "Admin"
        }
    },
    getters: {},
    mutations: {
        addUserData(state, data) {
            // state.userData.assign(data)
            state.userData = Object.assign({}, data);
        }
    },
    actions: {}
});