/* eslint-disable */
import Vue from 'vue'
import Router from 'vue-router'
import VueEvents from 'vue-event-handler';
import VueResource from 'vue-resource';
import VueSession from 'vue-session'
import VueProgressBar from 'vue-progressbar'
import MultiLanguage from 'vue-multilanguage'

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
Vue.use(VueProgressBar, {
  color: 'rgb(143, 255, 199)',
  failedColor: 'red',
  height: '2px'
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
    component: () => import(`@/components/${route.component}.vue`)
  }
});

export default new Router({
  routes,
  mode: 'history'
})
