<template>
  <div class="login-shell">
    <Card class="login-card">
      <template #title>
        <div class="login-title">
          <i class="pi pi-lock"></i>
          <span>Secure Access</span>
        </div>
      </template>
      <template #subtitle>
        <p class="subtitle">Sign in to access the laboratory console.</p>
      </template>
      <template #content>
        <form class="login-form" @submit.prevent="onSubmit">
          <div class="field">
            <label for="identifier">Username or Email</label>
            <InputText
              id="identifier"
              v-model.trim="form.identifier"
              placeholder="lab.user@example.com"
              :class="{ 'p-invalid': identifierError }"
              autocomplete="username"
            />
            <small v-if="identifierError" class="p-error">{{ identifierError }}</small>
          </div>

          <div class="field">
            <label for="password">Password</label>
            <Password
              id="password"
              v-model="form.password"
              :feedback="false"
              toggleMask
              placeholder="••••••••"
              :class="{ 'p-invalid': passwordError }"
              autocomplete="current-password"
            />
            <small v-if="passwordError" class="p-error">{{ passwordError }}</small>
          </div>

          <Message v-if="errorMessage" severity="error" class="login-error">{{ errorMessage }}</Message>

          <Button type="submit" label="Sign in" icon="pi pi-sign-in" :loading="loading" class="w-full" />
        </form>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "../services/authService";

const router = useRouter();
const loading = ref(false);
const errorMessage = ref("");
const form = reactive({
  identifier: "",
  password: "",
});

const identifierError = computed(() => {
  if (!form.identifier) return "Identifier is required";
  if (form.identifier.length < 3) return "Enter at least 3 characters";
  return "";
});

const passwordError = computed(() => {
  if (!form.password) return "Password is required";
  if (form.password.length < 8) return "Password must be at least 8 characters";
  return "";
});

const isValid = computed(() => !identifierError.value && !passwordError.value);

const onSubmit = async () => {
  errorMessage.value = "";
  if (!isValid.value) return;
  loading.value = true;
  try {
    await login({ identifier: form.identifier, password: form.password });
    router.push({ name: "home" });
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || "Unable to sign in. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-shell {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: radial-gradient(circle at top, rgba(14, 116, 144, 0.15), transparent 55%),
    linear-gradient(180deg, #f8fafc, #ffffff 70%);
}

.login-card {
  width: min(420px, 100%);
  border-radius: 18px;
  box-shadow: 0 24px 60px rgba(15, 118, 110, 0.12);
}

.login-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
}

.subtitle {
  margin: 0;
  color: var(--muted);
}

.login-form {
  display: grid;
  gap: 1rem;
}

.field {
  display: grid;
  gap: 0.35rem;
}

.login-error {
  margin-bottom: 0.5rem;
}
</style>
