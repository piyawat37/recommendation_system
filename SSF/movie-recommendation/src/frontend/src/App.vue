<template>
	<div id="app">
        <!-- set progressbar -->
        <vue-progress-bar></vue-progress-bar>
		<b-navbar toggleable="md" type="dark" variant="dark" sticky>
		  <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
		  <b-navbar-brand href="#"><span v-text="uiLabel.logo"></span></b-navbar-brand>
		  <b-collapse is-nav id="nav_collapse">
		    <b-navbar-nav>
		      <b-nav-item>
		      	<router-link to="/" tag="div">
				    <i class="fa fa-home" aria-hidden="true"></i> <span v-text="uiLabel.home"></span>
				</router-link></b-nav-item>
		      <b-nav-item href="#"><span v-text="uiLabel.movies"></span></b-nav-item>
		      <b-nav-item href="#"><span v-text="uiLabel.publicFavorite"></span></b-nav-item>
		    </b-navbar-nav>
		    
		    <!-- Right aligned nav items -->
		    <b-navbar-nav class="ml-auto">
		    	<b-navbar-nav style="padding-right: 2%">
		    	  <autocomplete
		    	  	url="http://localhost:4996/movie-service/searchByString/"
				    anchor="title"
				    label="writer"
				    id="searchMovies"
				    :classes="{ wrapper: 'form-wrapper', input: 'form-control', list: 'data-list', item: 'data-list-item' }"
				    placeholder="Search"
				    :options="optionsSearch"
    				:onSelect="getData"
    				:onInput="searchString"
				    :onShouldGetData="searchString">
				  </autocomplete>
		    	</b-navbar-nav>
				<b-navbar-nav v-if="!tokenStorage">
			      <b-nav-item href="#" v-b-modal.signIn style="white-space:nowrap !important;"><span v-text="uiLabel.signIn"></span></b-nav-item>
			      <b-nav-item href="#" v-b-modal.signUp style="white-space:nowrap !important;"><span v-text="uiLabel.signUp"></span></b-nav-item>
			    </b-navbar-nav>
			    <b-navbar-nav v-if="tokenStorage">
			      <b-nav-item-dropdown :text="user_token.username" right>
			        <b-dropdown-item v-if= "user_token.role === 'admin'">
			        	<router-link to="/moviemgt" tag="div">
						    <i class="fa fa-cog" aria-hidden="true"></i> <span v-text="uiLabel.manageMovie"></span>
						</router-link>
			        </b-dropdown-item>
			        <b-dropdown-item v-if= "user_token.role === 'admin'">
			        	<router-link to="/accountmgt" tag="div">
						    <i class="fa fa-cog" aria-hidden="true"></i> <span v-text="uiLabel.manageAccount"></span>
						</router-link>
			        </b-dropdown-item>
			        <b-dropdown-item href="#"><i class="fa fa-key" aria-hidden="true"></i> <span v-text="uiLabel.changePassword"></span></b-dropdown-item>
			        <b-dropdown-item href="#" v-on:click="signOut()"><i class="fa fa-sign-out" aria-hidden="true"></i> <span v-text="uiLabel.signOut"></span></b-dropdown-item>
			      </b-nav-item-dropdown>
			    </b-navbar-nav>
				<b-button :size="size" :variant="variant" v-on:click="changeLanguage(language)" v-text="langBtn" style="margin-left: 5%"></b-button>
		    </b-navbar-nav>
		  </b-collapse>
		</b-navbar>
		
		<b-modal  id="signIn" v-bind:title="uiLabel.signIn"
			ref="signIn"
			header-bg-variant="dark" header-text-variant="light"
			body-bg-variant="dark" body-text-variant="light"
			footer-bg-variant="dark" footer-text-variant="light"
			:ok-title="uiLabel.signIn" hide-footer hide-header
            no-close-on-backdrop no-close-on-esc>
           	<b-container fluid>
           		<div slot="modal-header" class="w-100">
		       		 <b-row>
		       		 	<b-col cols="12" class="text-left">
		       		 		<h4 v-text="uiLabel.signIn"></h4>
		       		 	</b-col>
		       		 </b-row>
			     </div>
			     <hr style="background-color: rgb(255, 255, 255);"/>
	            <b-form>
					<b-form-group>
						<b-form-input type="text"
					                 :placeholder="uiLabel.username"
					                 v-model="user.username"></b-form-input>
					</b-form-group>
					<b-form-group>
					    <b-form-input type="password"
				                    :placeholder="uiLabel.password"
				                    v-model="user.password"></b-form-input>
					</b-form-group>
	           		<div slot="modal-footer" class="w-100">
			       		 <b-row>
			       		 	<b-col lg="6" md="12" cols="12" v-bind:class="signInRpsClass">
			       		 		<label style="padding-top: 15px;">
			       		 			<b-link href="#forgot" v-text="uiLabel.forgot"></b-link>
			       		 		</label>
				         	</b-col>
			       		 	<b-col lg="6" md="12"  cols="12" v-bind:class="signInRpsClass">
			       		 		<b-btn :size="signInSize" class="float-right" variant="secondary" @click="handleOk" v-text="uiLabel.signInBtn" style="margin-left: 5px;"></b-btn>
			       		 		<b-btn :size="signInSize" class="float-right" variant="danger" @click="clearSignIn" v-text="uiLabel.cancel"></b-btn>
			       		 	</b-col>
			       		 </b-row>
				     </div>
				</b-form>
       		</b-container>
		</b-modal>
		
		
		<b-modal  id="signUp" v-bind:title="uiLabel.signUp"
			ref="signUp"
			header-bg-variant="dark" header-text-variant="light"
			body-bg-variant="dark" body-text-variant="light"
			footer-bg-variant="dark" footer-text-variant="light"
			:ok-title="uiLabel.signIn" hide-footer hide-header
            no-close-on-backdrop no-close-on-esc>
           	<b-container fluid>
           		<div slot="modal-header" class="w-100">
		       		 <b-row>
		       		 	<b-col cols="12" class="text-left">
		       		 		<h4 v-text="uiLabel.signUp"></h4>
		       		 	</b-col>
		       		 </b-row>
			     </div>
			     <hr style="background-color: rgb(255, 255, 255);"/>
	            <b-form class="text-left">
					<b-form-group v-bind:class="{ 'form-group--error': $v.signUp.email.$error }">
						<b-form-input type="email"
					                 :placeholder="uiLabel.email" @input="$v.signUp.email.$touch()"
					                 v-model.trim="signUp.email"></b-form-input>
		                <span class="form-group__message require" v-if="!$v.signUp.email.required && $v.signUp.email.$dirty">This field is required.</span>
					</b-form-group>
					<b-form-group v-bind:class="{ 'form-group--error': $v.signUp.username.$error }">
						<b-form-input type="text"
					                 :placeholder="uiLabel.username" @input="$v.signUp.username.$touch()"
					                 v-model.trim="signUp.username"></b-form-input>
					                 <span class="form-group__message require" v-if="!$v.signUp.username.required && $v.signUp.username.$dirty">This field is required.</span>
					</b-form-group>
					<b-form-group v-bind:class="{ 'form-group--error': $v.signUp.password.$error }">
					    <b-form-input type="password"
				                    :placeholder="uiLabel.password" @input="$v.signUp.password.$touch()"
				                    v-model.trim="signUp.password"></b-form-input>
				                   <span class="form-group__message require" v-if="!$v.signUp.password.required && $v.signUp.password.$dirty">This field is required.</span>
				                   <span class="form-group__message require" v-if="!$v.signUp.password.minLength">Password must have at least {{ $v.signUp.password.$params.minLength.min }} letters.</span>
					</b-form-group>
					<b-form-group v-bind:class="{ 'form-group--error': $v.signUp.password.$error }">
					    <b-form-input type="password"
				                    :placeholder="uiLabel.rePassword" @input="$v.signUp.rePassword.$touch()"
				                    v-model.trim="signUp.rePassword"></b-form-input>
				                    <span class="form-group__message require" v-if="!$v.signUp.rePassword.required && $v.signUp.password.$dirty">This field is required.</span>
				                    <span class="form-group__message require" v-if="!$v.signUp.rePassword.sameAsPassword">Passwords must be identical.</span>
					</b-form-group>
	           		<div slot="modal-footer" class="w-100">
			       		 <b-row>
			       		 	<b-col cols="12" class="text-right" v-bind:class="signInRpsClass">
			       		 		<b-btn :size="signInSize" class="float-right" variant="secondary" @click="handleSignUp" v-text="uiLabel.signUpBtn" style="margin-left: 5px;"></b-btn>
			       		 		<b-btn :size="signInSize" class="float-right" variant="danger" @click="clearSignUp" v-text="uiLabel.cancel"></b-btn>
			       		 	</b-col>
			       		 </b-row>
				     </div>
				</b-form>
       		</b-container>
		</b-modal>
		<b-modal  id="movieInfoAutoComplete" v-bind:title="movieInfoAutoComplete.title"
			ref="movieInfoAutoComplete"
			header-bg-variant="dark" header-text-variant="light"
			body-bg-variant="dark" body-text-variant="light"
			footer-bg-variant="dark" footer-text-variant="light"
            no-close-on-backdrop no-close-on-esc
            ok-only ok-title="Close">
            <p style="text-align: left"><span>{{movieInfoAutoComplete.genres}}</span></p>
      		<star-rating v-if="tokenStorage" :star-size="40" :border-width="3" @rating-selected ="setRating($event, movieInfoAutoComplete.movieId)" @click="addRatings()" :show-rating="false" :increment="0.5"inactive-color="#FFDDCB" active-color="#ff9900"></star-rating>
		</b-modal>
        <!-- for router view -->
        <router-view v-if="!progress"></router-view>
        <footer-master v-if="!progress"></footer-master>
    </div>
</template>

<script>
/* eslint-disable */
import configService from './SystemConstant/config.json'
import { vueTopprogress } from 'vue-top-progress'
import $ from 'jquery'
import { required, minLength, sameAs, between } from "vuelidate/lib/validators"
import footerMaster from './components/Footer'
import Autocomplete from 'vue2-autocomplete-js'
export default {
  name: 'app',
  data () {
    return {
		size: 'sm',
		variant: 'secondary',
		progress: true,
		movieList: [],
		signInSize: 'md',
		signInRpsClass: 'text-left',
		windowWidth: 0,
     	windowHeight: 0,
     	name: '',
        age: 0,
		user: {
			username: '',
			password: '',
			is_authenticated: false,
			language: this.language
		},
		signUp:{
			email: '',
			username: '',
			password: '',
			rePassword: '',
			language: this.language
		},
		user_token: {},
		error: '',
		tokenStorage: localStorage.getItem('token') ? localStorage.getItem('token') : undefined,
		optionsSearch: [],
		movieInfoAutoComplete: {},
		rating: 0,
		ratedContext:{},
		langBtn: 'EN'
    }
  },
  mounted () {
		this.$nextTick(function(){
			window.addEventListener('resize', this.getWindowWidth);
			window.addEventListener('resize', this.getWindowHeight);
			
			//Init
			this.getWindowWidth()
			this.getWindowHeight()
		})
  },
  methods: {
	changeLanguage (lang){
		var vm = this
		vm.language = lang == 'EN' ? 'TH' : 'EN'
		vm.isBE = vm.language != 'EN'
		vm.langBtn = vm.isBE ? 'EN' : 'TH'
		vm.$Progress.start()
		vm.uiLabel = require("./i18n/app-master-"+vm.language+".json")
		$.each(vm.$children, function(key, value){
			if(value.setUiLabel){
				value.setUiLabel(vm.language)
			}
		})
		/* this.$children[5].setUiLabel(this.language) */
		this.$Progress.decrease(10)
		this.$Progress.finish()
	},
	setSignInButtonSize (){
		if (window.matchMedia('(max-width: 576px)').matches) {
	        this.signInSize = 'sm';
	        this.signInRpsClass = 'text-right';
	      } else if (window.matchMedia('(max-width: 991px)').matches) {
	        this.signInSize = 'md';
	        this.signInRpsClass = 'text-right';
	      } else if (window.matchMedia('(max-width:992px)').matches) {
	        this.signInSize = 'md';
	        this.signInRpsClass = 'text-left';
	      } else {
	        this.signInSize = 'md';
	        this.signInRpsClass = 'text-left';
	      }
	},
	clearSignIn () {
      this.user.username = ''
      this.user.password = ''
   	  this.$refs.signIn.hide()
    },
    clearSignUp () {
    	var vm = this
        vm.signUp.email = ''
        vm.signUp.username = ''
        vm.signUp.password = ''
        vm.signUp.rePassword = ''
        vm.$v.$reset()
   		vm.$refs.signUp.hide()
    },
    handleOk (evt) {
      // Prevent modal from closing
      evt.preventDefault()
      if (!this.user.username || !this.user.password) {
   	      this.$swal('Error!', this.uiLabel.require, 'error')
      } else {
        this.user.language = this.language
        this.handleSignIn()
      }
    },
   	handleSignUp(){
    	var vm = this
    	vm.getAuthHeader()
        vm.signUp.language = vm.language
        if(!vm.$v.signUp.$invalid){
	    	vm.signup(this, vm.signUp, '/')
        }else{
        	this.$swal('Error!', this.uiLabel.required, 'error')
        }
    },
    handleSignIn () {
    	this.getAuthHeader()
    	this.login(this, this.user, '/')
    },
    getWindowWidth(event) {
        this.windowWidth = document.documentElement.clientWidth;
		this.setSignInButtonSize()
    },
    getWindowHeight(event) {
      this.windowHeight = document.documentElement.clientHeight;
    },
    login(context, creds, redirect) {
      context.$http.post(configService.userService + '/signIn', creds).then(response => {
      	localStorage.setItem('token', response.body.user.token)
      	this.user = response.body.user
      	// Redirect to a specified route
      	if(redirect) {
      		this.$router.go(redirect)
      		this.$forceUpdate();
      	}
      }, response => {
   	  	this.$swal('Error!', response.bodyText, 'error')
   	  	localStorage.removeItem('token');
      	context.error = response.statusText
  		console.log(response.statusText)
      });
    },
    signup(context, creds, redirect) {
    	context.$http.post(configService.userService + '/signUp', creds).then(response => {
          	localStorage.setItem('token', response.body.user.token)
          	this.user = response.body.user
          	// Redirect to a specified route
          	if(redirect) {
          		this.$router.go(redirect)
          		this.$forceUpdate();
          	}
          }, response => {
       	  	this.$swal('Error!', response.bodyText, 'error')
       	  	localStorage.removeItem('token');
          	context.error = response.statusText
      		console.log(response.statusText)
          });
    },

    logout() {
      localStorage.removeItem('token')
      this.user.authenticated = false
    },

    checkAuth() {
      var jwt = localStorage.getItem('token')
      if(jwt) {
        this.user.authenticated = true
      }
      else {
        this.user.authenticated = false      
      }
    },
    getAuthHeader() {
      return {
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      }
    },
    signOut(){
    	if(localStorage.getItem('token')){
	    	localStorage.removeItem('token');
	    	this.$router.go('/')
	    	this.$forceUpdate();
    	}else{
	    	this.$router.go('/')
	    	this.$forceUpdate();
    	}
    },
    searchString(value){
    	var vm = this
    	vm.$http.get(configService.movieService + '/searchByString/', {params: {searchString: value}}).then(response => {
  	      // get body data
  	      	vm.optionsSearch = response.body.movies
  	    }, response => {
  	      // error callback
  	      console.log(response.statusText)
  	    });
    },
    getData(value){
    	var vm = this;
    	vm.movieInfoAutoComplete = value
    	vm.$refs.movieInfoAutoComplete.show()
    },
    setRating: function(rating, movieId){
        var vm = this
        vm.rating= rating
        vm.ratedContext.rating = vm.rating
        vm.ratedContext.token = localStorage.getItem('token')
        vm.ratedContext.movieId = movieId 
    	  vm.$Progress.start()
        vm.$http.post(configService.movieService + '/addRating', vm.ratedContext).then(response => {
  	  		// get body data
  			//vm.user_token = response.body.user
  			vm.$router.go('/')
  			vm.$Progress.finish()
  	    }, response => {
  	      // error callback
  			vm.$Progress.fail()
  			localStorage.removeItem('token');
  	      	vm.$router.go('/')
  	    });
     },
  },
  created () {
	  	this.language = this.language.toUpperCase()
		var vm = this;
	  	vm.isBE = vm.language != 'EN'
		vm.setSignInButtonSize()
		vm.uiLabel = require("./i18n/app-master-"+vm.language+".json")
		vm.langBtn = vm.isBE ? 'EN' : 'TH'
  },
  beforeCreate() {
	  var vm = this
	  require('vue2-autocomplete-js/dist/style/vue2-autocomplete.css')
	  if(!localStorage.getItem('token')){
	  	vm.$router.push('/')
	  	vm.$http.get(configService.movieService + '/getMovie/').then(response => {
	      // get body data
			vm.movieList = response.body.movies
			vm.$Progress.decrease(10)
			vm.$Progress.finish()
			vm.progress = false
	    }, response => {
	      // error callback
			vm.$Progress.fail()
			vm.progress = false
	    });
	  }else{
	 	vm.$Progress.start()
		vm.$http.post(configService.userService + '/authenByToken', {token: localStorage.getItem('token')}).then(response => {
		  // get body data
			vm.user_token = response.body.user
			vm.$http.get(configService.movieService + '/getMovie/', {params: {id: this.user_token.userId}}).then(response => {
		      // get body data
				vm.movieList = response.body.movieList
				vm.$Progress.decrease(10)
				vm.$Progress.finish()
				vm.progress = false
		    }, response => {
		      // error callback
				vm.$Progress.fail()
				vm.progress = false
		    });
	    }, response => {
	      // error callback
			vm.$Progress.fail()
			vm.progress = false
			localStorage.removeItem('token');
	      	vm.$router.push('/')
	    });
	  }
  },
  components: {
    vueTopprogress,
    footerMaster,
    Autocomplete
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.getWindowWidth);
    window.removeEventListener('resize', this.getWindowHeight);
  },
  validations: {
    signUp: {
   	  email:{
  		  required
  	  },
	  username:{
		  required
	  },
      password:{
    	  required,
    	  minLength: minLength(8)
      },
	  rePassword: {
		  required,
		  sameAsPassword: sameAs('password')
	  } 
    }
  }
}
</script>

<style>
body{
  margin: 0;
  padding: 0;
  background-color: #191919;
}
body, html{
  height: 100%;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #FFFFFF;
}
a{
	color: #ff9900;
}
.require{
	color: #FFA53E;
}
</style>
