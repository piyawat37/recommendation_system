/* eslint-disable */
import Vue from 'vue'
import Router from 'vue-router'
import VueEvents from 'vue-event-handler'
import VueResource from 'vue-resource'
import VueSession from 'vue-session'
import VueProgressBar from 'vue-progressbar'
import MultiLanguage from 'vue-multilanguage'
import FontAwesome from 'font-awesome/css/font-awesome.min.css'
import vueTopprogress from 'vue-top-progress'
import VueSweetAlert from 'vue-sweetalert'
import BootstrapVue from 'bootstrap-vue/dist/bootstrap-vue.esm';
import Vuelidate from 'vuelidate'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

var corsHeaders = {
	  origin: ["*"],
	  headers: ["Access-Control-Allow-Origin","Access-Control-Allow-Headers","Origin, X-Requested-With, Content-Type", "CORELATION_ID"],
	  credentials: true,
	  additionalHeaders: ['access-control-allow-headers', 'Access-Control-Allow-Origin, Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, CORRELATION_ID'],
	  additionalExposedHeaders: ['access-control-allow-headers', 'Access-Control-Allow-Origin, Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, CORRELATION_ID']
	};

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/about', component: 'About' },
  { path: '/recommend', component: 'Recommend' },
  { path: '*', component: 'NotFound' }
]
Vue.use(Router)
Vue.use(VueEvents)
Vue.use(VueResource)
Vue.use(VueSession)
Vue.use(BootstrapVue)
Vue.use(FontAwesome)
Vue.use(vueTopprogress)
Vue.use(VueSweetAlert)
Vue.use(Vuelidate)
Vue.use(VueProgressBar, {
  color: 'rgb(255, 255, 255)',
  failedColor: 'red',
  height: '3px'
})

Vue.use(MultiLanguage, {
	default: 'EN',
	EN: {
		sym: 'EN'
	},
	TH: {
		sym: 'TH'
	},
})

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`),
  }
});

export default new Router({
  routes,
  mode: 'history',
})
