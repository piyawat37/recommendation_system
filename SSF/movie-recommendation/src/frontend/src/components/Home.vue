<template>
	<div>
		<h1>{{ msg }}</h1>
		<h2>{{criteria.name}}</h2>
		<button v-on:click="changeLanguage(language)" v-lang.sym></button>
		<ul>
			<li>
				<span v-text="uiLabel.recommended"></span>: <span v-text="movieList.recommended"></span>
			</li>
		</ul>
		<ul v-for="v, k in movieList">
			<li>{{k}}: {{ v }}</li>
		</ul>
	</div>

</template>

<script>
/* eslint-disable */
/* import homeLabel from '../i18n/home-EN.json' */
import configService from '../SystemConstant/config.json'
export default {
  data () {
    return {
    	msg: 'Welcome to Your Vue.js App',
    	criteria: {
    		name: 'Piyawat',
    	},
    	movieList: [],
    }
  },
  methods: {
	getMovieListByUserId (userId, lang){
		this.$Progress.start()
	    this.$http.get(configService.movieService + '/getMovieByUserId/', {params: {id: userId, language: lang}}).then(response => {
	      // get body data
	      this.movieList = response.body.movieList;
	      this.$Progress.decrease(10)
	      this.$Progress.finish()
	    }, response => {
	      // error callback
		  this.$Progress.fail()
	    });
	},
	changeLanguage (lang){
		if(lang == 'EN'){
			this.language = 'TH'
			this.uiLabel = require("../i18n/home-"+this.language+".json")
		}else{
			this.language = 'EN'
			this.uiLabel = require("../i18n/home-"+this.language+".json")
		}
	}
  },
  created () {
	var vm = this;
	vm.getMovieListByUserId(1, vm.language)
	vm.uiLabel = require("../i18n/home-"+vm.language+".json")
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
	font-weight: normal;
}

ul {
	list-style-type: none;
	padding: 0;
}

li {
	display: inline-block;
	margin: 0 10px;
}

a {
	color: #42b983;
}
</style>
