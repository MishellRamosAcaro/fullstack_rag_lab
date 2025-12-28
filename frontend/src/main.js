import { createApp } from "vue";
import PrimeVue from "primevue/config";
import ToastService from "primevue/toastservice";
import App from "./App.vue";
import router from "./router";

import Button from "primevue/button";
import Card from "primevue/card";
import Divider from "primevue/divider";
import FileUpload from "primevue/fileupload";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import Password from "primevue/password";
import ProgressBar from "primevue/progressbar";
import ScrollPanel from "primevue/scrollpanel";
import Tag from "primevue/tag";
import Textarea from "primevue/textarea";
import Toast from "primevue/toast";

import "primevue/resources/themes/lara-light-blue/theme.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";
import "primeflex/primeflex.css";
import "./styles/theme.css";

const app = createApp(App);
    
app.use(PrimeVue, { ripple: true });
app.use(ToastService);
app.use(router);
app.component("Button", Button);
app.component("Card", Card);
app.component("Divider", Divider);
app.component("FileUpload", FileUpload);
app.component("InputText", InputText);
app.component("Message", Message);
app.component("Password", Password);
app.component("ProgressBar", ProgressBar);
app.component("ScrollPanel", ScrollPanel);
app.component("Tag", Tag);
app.component("Textarea", Textarea);
app.component("Toast", Toast); 
app.mount("#app");
