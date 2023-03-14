import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { Inkline, components } from '@inkline/inkline';
import { createPinia } from 'pinia'
import { GlobalCmComponent } from "codemirror-editor-vue3";

import '@imengyu/vue3-context-menu/lib/vue3-context-menu.css'
import ContextMenu from '@imengyu/vue3-context-menu'
import SvgIcon from "vue3-icon";


import '@inkline/inkline/inkline.scss';
import "./assets/styles/tailwind.css";
import "./assets/styles/custom_inkline.scss";

const app = createApp(App)
const pinia = createPinia()


app.use(router)
app.use(pinia)
app.use(Inkline, {components, colorMode: 'dark'});
app.use(ContextMenu)
app.component("svg-icon", SvgIcon);
app.use(GlobalCmComponent)

app.mount('#app')
