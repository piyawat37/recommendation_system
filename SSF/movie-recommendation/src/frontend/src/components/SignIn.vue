<template>
	<div>
		<transition-group name="movie-fade" appear mode="out-in">
			<div v-for="value, key in movieList" v-bind:key="key" style="text-align: left;">
				<span v-text="key"></span>
				<Slider v-bind:id="key" v-bind:content-data="value"/>
			</div>
		</transition-group>
	</div>
</template>

<script>
/* eslint-disable */
import configService from '../SystemConstant/config.json'
import Slider from './Slider'
export default {
  data () {
    return {
    	msg: 'Welcome to Your Vue.js App',
    	criteria: {
    		name: 'Piyawat',
    	},
    	movieList: this.$parent.movieList,
    	showMessage: true,
    }
  },
  mounted (){
	  
  },
  methods: {
	enlarge(event) {
	   	/* event.currentTarget.classList.add('large'); */
    },
	setUiLabel (lang){
		this.uiLabel = require("../i18n/home-"+this.language+".json")
	}
  },
  created () {
	var vm = this;
	vm.uiLabel = require("../i18n/home-"+vm.language+".json")
	
  },
  components: {
		Slider,
  },
  beforeCreate() {
	  if(!localStorage.getItem('token')){
		  this.$router.push('/')
	  }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div{
	margin: 0;
	padding: 0;
}
h1, h2 {
	font-weight: normal;
}

ul {
	list-style-type: none;
	padding: 0;
}

li {
	display: inline-block;
	margin: 0px;
	padding: 0px;
}

a {
	color: #42b983;
}

.movie-fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.movie-fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
