<template>
	<div id="app">
        <!-- set progressbar -->
        <vue-progress-bar></vue-progress-bar>
		<b-navbar toggleable="md" type="dark" variant="dark" sticky>
		  <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
		  <b-navbar-brand href="#">LOGO</b-navbar-brand>
		  <b-collapse is-nav id="nav_collapse">
		    <b-navbar-nav>
		      <b-nav-item href="#"><span v-text="uiLabel.home"></span></b-nav-item>
		      <b-nav-item href="#"><span v-text="uiLabel.movies"></span></b-nav-item>
		      <b-nav-item href="#"><span v-text="uiLabel.publicFavorite"></span></b-nav-item>
		      <b-nav-item href="#"><span v-text="uiLabel.contactUs"></span></b-nav-item>
		    </b-navbar-nav>
		    
		    <!-- Right aligned nav items -->
		    <b-navbar-nav class="ml-auto">
				<b-navbar-nav v-if="!tokenStorage">
			      <b-nav-item href="#" v-b-modal.signIn><span v-text="uiLabel.signIn"></span></b-nav-item>
			      <b-nav-item href="#" v-b-modal.signUp><span v-text="uiLabel.signUp"></span></b-nav-item>
			    </b-navbar-nav>
			    <b-navbar-nav v-if="tokenStorage">
			      <b-nav-item><span v-text="user_token.username"></span></b-nav-item>
			      <b-nav-item href="#"><span v-text="uiLabel.signOut" v-on:click="signOut()"></span></b-nav-item>
			    </b-navbar-nav>
				<b-button :size="size" :variant="variant" v-on:click="changeLanguage(language)" v-lang.sym></b-button>
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
	            <b-form>
					<b-form-group>
						<b-form-input type="email"
					                 :placeholder="uiLabel.email"
					                 v-model.trim="signUp.email"></b-form-input>
					</b-form-group>
					<b-form-group>
						<b-form-input type="text"
					                 :placeholder="uiLabel.username"
					                 v-model.trim="signUp.username"></b-form-input>
					</b-form-group>
					<b-form-group v-bind:class="{ 'form-group--error': $v.signUp.password.$error }">
					    <b-form-input type="password"
				                    :placeholder="uiLabel.password" @input="$v.signUp.password.$touch()"
				                    v-model.trim="signUp.password"></b-form-input>
				                    <span class="form-group__message" v-if="!$v.signUp.password.required && $v.signUp.password.$dirty">Password is required.</span>
				                   <span class="form-group__message" v-if="!$v.signUp.password.minLength">Password must have at least {{ $v.signUp.password.$params.minLength.min }} letters.</span>
					</b-form-group>
					<b-form-group v-bind:class="{ 'form-group--error': $v.signUp.password.$error }">
					    <b-form-input type="password"
				                    :placeholder="uiLabel.rePassword" @input="$v.signUp.rePassword.$touch()"
				                    v-model.trim="signUp.rePassword"></b-form-input>
				                    <span class="form-group__message" v-if="!$v.signUp.rePassword.required && $v.signUp.password.$dirty">Re-password is required.</span>
				                    <span class="form-group__message" v-if="!$v.signUp.rePassword.sameAsPassword">Passwords must be identical.</span>
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
        <!-- for router view -->
        {{$v}}
        <router-view v-if="progress == false"></router-view>
    </div>
</template>

<script>
/* eslint-disable */
import configService from './SystemConstant/config.json'
import { vueTopprogress } from 'vue-top-progress'
import auth from './auth/'
import $ from 'jquery'
import { validationMixin } from "vuelidate"
import { required, minLength, sameAs } from "vuelidate/lib/validators"
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
		tokenStorage: localStorage.getItem('token') ? localStorage.getItem('token') : undefined
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
		this.language = lang == 'EN' ? 'TH' : 'EN' 
		this.$Progress.start()
		this.uiLabel = require("./i18n/app-master-"+this.language+".json")
		this.$children[4].setUiLabel(this.language)
		this.$Progress.decrease(10)
		this.$Progress.finish()
	},
	/* getMovieListByUserId (userId, lang){
		this.$refs.topProgress.start()
	    this.$http.get(configService.movieService + '/getMovieByUserId/', {params: {id: userId, language: lang}}).then(response => {
	      // get body data
			this.movieList = response.body.movieList
			this.$Progress.decrease(10)
			this.$refs.topProgress.done()
			this.progress = false
	    }, response => {
	      // error callback
			this.$refs.topProgress.fail()
			this.progress = false
	    });
	}, */
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
        this.signUp.email = ''
        this.signUp.username = ''
        this.signUp.password = ''
        this.signUp.rePassword = ''
   		this.$refs.signUp.hide()
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
    	this.getAuthHeader()
        this.signUp.language = this.language
    	this.signup(this, this.signUp, '/')
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
    }
  },
  created () {
	  	this.language.toUpperCase()
		var vm = this;
		vm.setSignInButtonSize()
		vm.uiLabel = require("./i18n/app-master-"+vm.language+".json")
  },
  beforeCreate() {
	  var vm = this
	  if(!localStorage.getItem('token')){
	  	vm.$router.push('/')
	  }else{
	 	vm.$Progress.start()
		vm.$http.post(configService.userService + '/authenByToken', {token: localStorage.getItem('token')}).then(response => {
		  // get body data
			vm.user_token = response.body.user
			vm.$http.get(configService.movieService + '/getMovieByUserId/', {params: {id: this.user_token.userId, language: localStorage['vue-lang']}}).then(response => {
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
			vm.$refs.topProgress.fail()
			vm.progress = false
	    });
	  }
  },
  components: {
    vueTopprogress
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.getWindowWidth);
    window.removeEventListener('resize', this.getWindowHeight);
  },
  mixins: [
      validationMixin
  ],
  validations: {
    signUp: {
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

</style>
