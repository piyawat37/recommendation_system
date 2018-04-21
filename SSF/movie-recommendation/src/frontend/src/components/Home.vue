<template>
	<div>
		<transition-group name="movie-fade" appear mode="out-in">
			<div v-for="value, key in movieList" v-if="key == 'movieTopRate'" v-bind:key="key" style="text-align: left; margin-top: 15px">
				<label class="control-label">
					<span v-text="uiLabel.movieTopList"></span>
				</label>
				<Slider v-bind:id="key" v-bind:data-list="value"/>
			</div>
		</transition-group>
		<!-- <transition-group name="movie-fade" appear mode="out-in">
			<div v-for="value, key in movieList" v-if="key == 'Recommended'" v-bind:key="key" style="text-align: left; margin-top: 15px">
				<label class="control-label">
					<span v-text="uiLabel.recommended"></span>
				</label>
				<Slider v-bind:id="key" v-bind:data-list="value"/>
			</div>
		</transition-group> -->
		<transition-group name="movie-fade" appear mode="out-in">
			<div v-for="value, key in movieList" v-if="key != 'movieTopRate' && key != 'Recommended'" v-bind:key="key" style="text-align: left; margin-top: 15px">
				<label class="control-label">
					<span v-text="key"></span>
				</label>
				<Slider v-bind:id="key" v-bind:data-list="value"/>
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
    	this.language = lang
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
