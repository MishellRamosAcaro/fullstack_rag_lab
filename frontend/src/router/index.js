import { createRouter, createWebHistory } from "vue-router";
import { getAuthToken } from "../services/authToken";
import LoginView from "../views/LoginView.vue";
import RagConsoleView from "../views/RagConsoleView.vue";

const routes = [
  { path: "/login", name: "login", component: LoginView },
  {
    path: "/",
    name: "home",
    component: RagConsoleView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !getAuthToken()) {
    next({ name: "login" });
    return;
  }
  if (to.name === "login" && getAuthToken()) {
    next({ name: "home" });
    return;
  }
  next();
});

export default router;
