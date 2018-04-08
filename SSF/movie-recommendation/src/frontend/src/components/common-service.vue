<template>
	<button v-on:click="changeLanguage(language)" v-lang.sym></button>
</template>

<script>
/* eslint-disable */
import configService from '../SystemConstant/config.json'
export default {
  data () {
    return {
    	
    }
  },
  methods: {
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
}
</script>