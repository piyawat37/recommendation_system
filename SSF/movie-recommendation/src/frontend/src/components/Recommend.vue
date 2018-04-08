
<template>
	<div>
		<h1>{{ msg }}</h1>
		<h2>{{criteria.name}}</h2>
		<ul>
			<li v-for="n in movieList">{{ n }}</li>
		</ul>
	    <!-- <call-dialog-link
	       :id="id"
	       :url="url"
	       message="Are you sure you wish to remove this record?"
	       label="Remove"
	       css-classes="alert">
	    </call-dialog-link> -->
	</div>
</template>

<script>
/* eslint-disable */
import axios from 'axios'
import CallDialogLink from './CallDialogLink.vue';
import uiLabel from '../i18n/home-EN.json'
export default {
  data () {
    return {
    	msg: 'Welcome to Your Vue.js App',
    	criteria: {
    		name: 'Piyawat'
    	},
    	movieList: [],
    }
  },
  methods: {
	getMovieListByUserId (userId){
	    this.$http.get('http://localhost:5000/movie-service/getMovieByUserId/'+ userId).then(response => {
	      // get body data
	      this.movieList = response.body.movieList;
	    }, response => {
	      // error callback
	    });
	},
  },
  created () {
	this.getMovieListByUserId(1)
  },
  props: {
      id: {
          type: String,
          required: true
      },
      url: {
          type: String,
          required: true
      }
  },
  components: {
      'call-dialog-link': CallDialogLink
  }
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
