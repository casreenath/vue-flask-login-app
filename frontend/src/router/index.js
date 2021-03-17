import Vue from "vue";
import Router from "vue-router";
// import HelloWorld from "@/components/HelloWorld";
const routerOptions = [
    { path: "/", component: "Home" },
    { path: "/login", component: "Login" },
    { path: "/hello", component: "HelloWorld" },
    { path: "/pipeline", component: "Pipeline" },
    { path: "/jigmanager", component: "JigManager" }
];
const routes = routerOptions.map(route => {
    return {
        ...route,
        component: () =>
            import (`@/components/${route.component}.vue`)
    };
});
Vue.use(Router);

export default new Router({
    routes,
    mode: "history"
});