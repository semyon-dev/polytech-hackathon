import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import VueRouter from 'vue-router'
import index from './components/home'
import announces from './components/poll'
Vue.use(VueRouter);

Vue.config.productionTip = false;

var router = new VueRouter({
  routes: [
    {path: '/', component: index},
    {path: '/announces', component: announces},
  ]
});
//
// Vue.use(vuetify, {
//   theme: {
//     primary: '#000000',
//     secondary: '#424242',
//     accent: '#82B1FF',
//     error: '#FF5252',
//     info: '#2196F3',
//     success: '#4CAF50',
//     warning: '#FFC107'
//   }
// });

new Vue({
  render: h => h(App),
  router: router
}).$mount('#app')
