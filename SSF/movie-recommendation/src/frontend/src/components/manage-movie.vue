<template>
	<div class="container-main">
		<div class="container-manage">
			<b-container fluid class="text-left">
				<b-row>
					<b-col cols="8">
						<h1 v-text="uiLabel.screenTitle"></h1>
					</b-col>
					<b-col cols="4" class="text-right">
						<b-button v-b-modal.createMovie variant="primary"><i class="fa fa-plus-square" aria-hidden="true"></i> <span v-text="uiLabel.createMovie"></span></b-button>
					</b-col>
				</b-row>
			</b-container>
			<hr class="style-manage"/>
			 <b-container fluid v-if="!progress">
			    <!-- User Interface controls -->
			    <b-row dark>
			      <b-col md="6" class="my-1">
			        <b-form-group horizontal :label="uiLabel.filter" class="mb-0">
			          <b-input-group>
			            <b-form-input v-model="filter" placeholder="Type to Search" />
			            <b-input-group-append>
			              <b-btn :disabled="!filter" @click="filter = ''"><span v-text="uiLabel.clear"></span></b-btn>
			            </b-input-group-append>
			          </b-input-group>
			        </b-form-group>
			      </b-col>
			      <b-col md="6" class="my-1">
			        <b-form-group horizontal :label="uiLabel.sort" class="mb-0">
			          <b-input-group>
			            <b-form-select v-model="sortBy" :options="sortOptions">
			              <option slot="first" :value="null">-- none --</option>
			            </b-form-select>
			            <b-form-select :disabled="!sortBy" v-model="sortDesc" slot="append">
			              <option :value="false"><span v-text="uiLabel.orderASC"></span></option>
			              <option :value="true"><span v-text="uiLabel.orderDESC"></span></option>
			            </b-form-select>
			          </b-input-group>
			        </b-form-group>
			      </b-col>
			      <b-col md="6" class="my-1">
			        <b-pagination :total-rows="totalRows" :per-page="perPage" v-model="currentPage" class="my-0" />
			      </b-col>
			      <b-col md="6" class="my-1">
			        <b-form-group horizontal :label="uiLabel.perPage" class="mb-0">
			          <b-form-select :options="pageOptions" v-model="perPage" />
			        </b-form-group>
			      </b-col>
			    </b-row>
			
			    <!-- Main table element -->
			    <b-table show-empty
			             stacked="md"
			             dark
			             :items="movies"
			             :fields="fields"
			             :current-page="currentPage"
			             :per-page="perPage"
			             :filter="filter"
			             :sort-by.sync="sortBy"
			             :sort-desc.sync="sortDesc"
			             @filtered="onFiltered">
			      <template slot="actions" slot-scope="row">
			        <!-- We use @click.stop here to prevent a 'row-clicked' event from also happening -->
			        <b-button size="md" @click.stop="info(row.item, row.index, $event.target)" class="mr-1" variant="success">
			          <i class="fa fa-pencil-square-o" aria-hidden="true"></i>
			        </b-button>
			        <b-button size="md" @click.stop="deleteMovie(row.item, row.index)" variant="danger">
			          <i class="fa fa-trash" aria-hidden="true"></i>
			        </b-button>
			      </template>
			    </b-table>
			
			    <!-- Info modal -->
			    <b-modal class="modal-edit" id="movieInfo" :title="movieInfo.title"
				    	hide-footer hide-header
						header-bg-variant="dark" header-text-variant="light"
						body-bg-variant="dark" body-text-variant="light"
						footer-bg-variant="dark" footer-text-variant="light"
	           			no-close-on-esc no-close-on-backdrop>
				      	<b-container fluid>
			           		<div slot="modal-header" class="w-100">
					       		 <b-row>
					       		 	<b-col cols="12" class="text-left">
					       		 		<h4 v-text="uiLabel.editpanel"></h4>
					       		 	</b-col>
					       		 </b-row>
						     </div>
						     <hr style="background-color: rgb(255, 255, 255);"/>
				            <b-form>
								<b-form-group>
									<b-form-input type="text" disabled
								                 v-model="movieInfo.content.movieId"></b-form-input>
								</b-form-group>
								<b-form-group v-bind:class="{ 'form-group--error': $v.movieInfo.title.$error }">
									<b-form-input type="text" @input="$v.movieInfo.title.$touch()"
								                 v-model="movieInfo.content.title"></b-form-input>
								    <span class="form-group__message require" v-if="!$v.movieInfo.title.required && $v.movieInfo.title.$dirty">This field is required.</span>
								</b-form-group>
								
								</b-form-group>
								<b-form-group class="text-left">
								  <b><label v-text="uiLabel.genres"></label></b>
							      <b-form-checkbox-group id="genresCheckbox" name="flavour2" v-model="movieInfo.content.genresList">
							        <b-row>
							        	<b-col cols="3">
									        <b-form-checkbox value="Adventure">Adventure</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
									        <b-form-checkbox value="Animation">Animation</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="Comedy">Comedy</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="Fantasy">Fantasy</b-form-checkbox>
							        	</b-col>
							        </b-row>
							        <b-row>
							        	<b-col cols="3">
									        <b-form-checkbox value="Romance">Romance</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
									        <b-form-checkbox value="Drama">Drama</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="Crime">Crime</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="Thriller">Thriller</b-form-checkbox>
							        	</b-col>
							        </b-row>
							        <b-row>
							        	<b-col cols="3">
									        <b-form-checkbox value="Horror">Horror</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
									        <b-form-checkbox value="Sci-Fi">Sci-Fi</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="Mystery">Mystery</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="War">War</b-form-checkbox>
							        	</b-col>
							        </b-row>
							        <b-row>
							        	<b-col cols="3">
									        <b-form-checkbox value="Action">Action</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
									        <b-form-checkbox value="Musical">Musical</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        	</b-col>
							        	<b-col cols="3">
							        	</b-col>
							        </b-row>
							      </b-form-checkbox-group>
							    </b-form-group>
				           		<div slot="modal-footer" class="w-100">
						       		 <b-row>
						       		 	<b-col lg="6" md="12" cols="12">
						       		 		<label style="padding-top: 15px;">
						       		 			<b-link href="#forgot" v-text="uiLabel.forgot"></b-link>
						       		 		</label>
							         	</b-col>
						       		 	<b-col lg="6" md="12"  cols="12">
						       		 		<b-btn class="float-right" variant="secondary" @click="handleEditOk(movieInfo.content)" v-text="uiLabel.submit" style="margin-left: 5px;"></b-btn>
						       		 		<b-btn class="float-right" variant="danger" @click="resetModal" v-text="uiLabel.cancel"></b-btn>
						       		 	</b-col>
						       		 </b-row>
							     </div>
							</b-form>
			       		</b-container>
				    </b-modal>
				     <b-modal  id="createMovie" v-bind:title="uiLabel.createMovie"
						ref="createMovie"
						header-bg-variant="dark" header-text-variant="light"
						body-bg-variant="dark" body-text-variant="light"
						footer-bg-variant="dark" footer-text-variant="light"
						:ok-title="uiLabel.createMovie" hide-footer hide-header
			            no-close-on-backdrop no-close-on-esc>
			           	<b-container fluid>
			           		<div slot="modal-header" class="w-100">
					       		 <b-row>
					       		 	<b-col cols="12" class="text-left">
					       		 		<h4 v-text="uiLabel.createMovie"></h4>
					       		 	</b-col>
					       		 </b-row>
						     </div>
						     <hr style="background-color: rgb(255, 255, 255);"/>
				            <b-form class="text-left">
								<b-form-group v-bind:class="{ 'form-group--error': $v.createMovie.title.$error }">
									<b-form-input type="text"
								                 :placeholder="uiLabel.title" @input="$v.createMovie.title.$touch()"
								                 v-model.trim="createMovie.title"></b-form-input>
								    <span class="form-group__message require" v-if="!$v.createMovie.title.required && $v.createMovie.title.$dirty">This field is required.</span>
								</b-form-group>
								<b-form-group class="text-left">
								  <b><label v-text="uiLabel.genres"></label></b>
							      <b-form-checkbox-group id="genresCheckbox" name="flavour2" v-model="createMovie.genresList">
							        <b-row>
							        	<b-col cols="3">
									        <b-form-checkbox value="Adventure">Adventure</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
									        <b-form-checkbox value="Animation">Animation</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="Comedy">Comedy</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="Fantasy">Fantasy</b-form-checkbox>
							        	</b-col>
							        </b-row>
							        <b-row>
							        	<b-col cols="3">
									        <b-form-checkbox value="Romance">Romance</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
									        <b-form-checkbox value="Drama">Drama</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="Crime">Crime</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="Thriller">Thriller</b-form-checkbox>
							        	</b-col>
							        </b-row>
							        <b-row>
							        	<b-col cols="3">
									        <b-form-checkbox value="Horror">Horror</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
									        <b-form-checkbox value="Sci-Fi">Sci-Fi</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="Mystery">Mystery</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        		<b-form-checkbox value="War">War</b-form-checkbox>
							        	</b-col>
							        </b-row>
							        <b-row>
							        	<b-col cols="3">
									        <b-form-checkbox value="Action">Action</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
									        <b-form-checkbox value="Musical">Musical</b-form-checkbox>
							        	</b-col>
							        	<b-col cols="3">
							        	</b-col>
							        	<b-col cols="3">
							        	</b-col>
							        </b-row>
							      </b-form-checkbox-group>
							    </b-form-group>
				           		<div slot="modal-footer" class="w-100">
						       		 <b-row>
						       		 	<b-col cols="12" class="text-right">
						       		 		<b-btn class="float-right" variant="secondary" @click="handleCreateMovie" v-text="uiLabel.submit" style="margin-left: 5px;"></b-btn>
						       		 		<b-btn class="float-right" variant="danger" @click="clearCreateMovie" v-text="uiLabel.cancel"></b-btn>
						       		 	</b-col>
						       		 </b-row>
							     </div>
							</b-form>
			       		</b-container>
					</b-modal>
			  </b-container>
		</div>
	</div>
</template>
<script>
/* eslint-disable */
import configService from '../SystemConstant/config.json'
import $ from 'jquery'
import { required, minLength, sameAs, between } from "vuelidate/lib/validators"
export default {
  data () {
    return {
	  movies: {},
	  totalRows: '',
      currentPage: 1,
      perPage: 5,
      pageOptions: [ 5, 10, 15 ],
      sortBy: null,
      sortDesc: false,
      filter: null,
      movieInfo: { title: '', content: '' },
      progress: true,
      createMovie:{
  		title: '',
  		genresList: [],
  		genres: '',
  		language: this.language
  	  },
    }
  },
  computed: {
    sortOptions () {
      // Create an options list from our fields
      return this.fields
        .filter(f => f.sortable)
        .map(f => { return { text: f.label, value: f.key } })
    }
  },
  mounted (){
	  var vm = this;
  },
  methods: {
	enlarge(event) {
	   	/* event.currentTarget.classList.add('large'); */
    },
	setUiLabel (lang){
    	var vm = this
    	vm.language = lang
		vm.uiLabel = require("../i18n/moviemgt-"+this.language+".json")
		vm.setField(vm)
	},
	setField(vm){
		vm.fields = [
	        { key: 'movieId', label: vm.uiLabel.movieId},
	        { key: 'title', label: vm.uiLabel.title, sortable: true, 'class': 'text-left', 'thClass': 'text-center' },
	        { key: 'genres', label: vm.uiLabel.genres, sortable: true, 'class': 'text-left', 'thClass': 'text-center'  },
	        { key: 'actions', label: ''}
     	]
	},
	info (item, index, button) {
	  var vm = this
      vm.movieInfo.title = `Row index: ${index}`
   	  var content = JSON.stringify(item, null, 2)
      vm.movieInfo.content = JSON.parse(content)
      vm.movieInfo.content.genresList = vm.movieInfo.content.genres.split("|") 
      vm.$root.$emit('bv::show::modal', 'movieInfo', button)
    },
    resetModal () {
      var vm = this
      vm.movieInfo.title = ''
      vm.movieInfo.content = {'title': '', 'genres': '', 'genresList':[]}
   	  vm.$root.$emit('bv::hide::modal', 'movieInfo')
   	  vm.$v.$reset()
    },
    onFiltered (filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
      this.currentPage = 1
    },
    deleteMovie (movie,index){
    	var vm = this;
   		vm.$swal({
   		  title: 'Are you sure?',
   		  text: 'You will not be able to recover this movie !',
   		  type: 'warning',
   		  showCancelButton: true,
   		  confirmButtonText: 'Yes, delete it!',
   		  cancelButtonText: 'No, keep it'
   		}).then((result) => {
		  if (result) {
			  vm.$Progress.start()
              vm.$http.delete(configService.movieService + '/deleteMovie/'+ movie.movieId + '/').then(response => {
            	  vm.$swal("Success", "Movie deleted.", "success");   
            	  vm.getAllMovie(vm)
             	  vm.$Progress.finish()
              }, response => {
        	      // error callback
             	  vm.$swal("Cancelled", "This movie has not been deleted !", "error");   
             	  vm.$Progress.finish()
				  vm.progress = false
			  });
           }
   		});
    },
    getAllMovie (vm){
    	vm.$http.get(configService.movieService + '/getAllMovie/').then(response => {
   	      // get body data
   			vm.movies = response.body.movies
   			vm.totalRows = vm.movies.length
   			/* $.each(vm.movies, function(key, value) {
   				value.genres = value.genres == 'A' ? 'Active' : 'Inactive'
   		   	}); */
   		   	vm.setField(vm)
   		    vm.$Progress.decrease(10)
   			vm.$Progress.finish()
   			vm.progress = false
   	    }, response => {
   	      // error callback
   			vm.$Progress.fail()
   			vm.progress = false
   	    });
    },
    handleEditOk (movieContext){
    	var vm = this;
    	movieContext.language = vm.language
    	var strGenres = ''
   		var symbol = '|'
   		var genresLength = movieContext.genresList.length
   		
   		if(movieContext.title && genresLength > 0){
   			$.each(movieContext.genresList, function(key, value){
	    		strGenres += value
	    		if(key < genresLength-1){
	    			strGenres += symbol
	    		}
	    	})
	    	movieContext.genres = strGenres
   			vm.$http.post(configService.movieService + '/update', movieContext).then(response => {
   	         	var movie = response.body.movie
   	         	var content = "Movie ID "+movie.movieId 
   	         	content += " ["+movie.title+"]" 
   	         	content += " updated"
   	         	vm.$swal('Success!', content, 'success')
   	         	vm.resetModal()
   	        	vm.getAllMovie(vm)
   	         	// Redirect to a specified route
   	         }, response => {
   	        	vm.$swal('Error!', response.bodyText, 'error')
   	         	vm.resetModal()
   	        	vm.getAllMovie(vm)
   	     		console.log(response.statusText)
   	         });
   		}else{
   			this.$swal('Error!', this.uiLabel.required, 'error')
   		}
   		
    },
    handleCreateMovie (){
    	var vm = this
    	vm.createMovie.language = vm.language
   		var strGenres = ''
   		var symbol = '|'
   		var genresLength = vm.createMovie.genresList.length
    	if(!vm.$v.createMovie.$invalid && genresLength > 0){
	    	$.each(vm.createMovie.genresList, function(key, value){
	    		strGenres += value
	    		if(key < genresLength-1){
	    			strGenres += symbol
	    		}
	    	})
	    	vm.createMovie.genres = strGenres
    		vm.$http.post(configService.movieService + '/createMovie', vm.createMovie).then(response => {
             	var movie = response.body.movie
             	var content = "Movie "
             	content += movie.title
             	content += ' ['+movie.genres+']'
             	content += " created."
             	this.$swal('Success!', content, 'success')
             	vm.getAllMovie(vm)
              	vm.clearCreateMovie()
             	// Redirect to a specified route
             }, response => {
          	  	this.$swal('Error!', response.bodyText, 'error')
          	  	vm.getAllMovie(vm)
         		console.log(response.statusText)
             });
    	}else{
    		this.$swal('Error!', this.uiLabel.required, 'error')
    	}
    },
    clearCreateMovie(){
    	var vm = this;
    	vm.createMovie = {'title': '', 'genres': '', 'genresList' : []}
 	   	vm.$root.$emit('bv::hide::modal', 'createMovie')
 	   	vm.$v.$reset()
    }
  },
  beforeCreate() {
	var vm = this;
	vm.$http.get(configService.movieService + '/getAllMovie/').then(response => {
      // get body data
		vm.movies = response.body.movies
		vm.totalRows = vm.movies.length
		/* $.each(vm.movies, function(key, value) {
			value.genres = value.genres == 'A' ? 'Active' : 'Inactive'
	   	}); */
	   	vm.setField(vm)
	    vm.$Progress.decrease(10)
		vm.$Progress.finish()
		vm.progress = false
    }, response => {
      // error callback
		vm.$Progress.fail()
		vm.progress = false
    });
  },
  created () {
	var vm = this;
	vm.uiLabel = require("../i18n/moviemgt-"+vm.language+".json")
  },
  validations: {
    createMovie: {
   	  title:{
  		  required
  	  }
    },
    movieInfo: {
   	  title:{
  		  required
  	  }
    }
  }
}
</script>
<style>
.container-main{
	padding: 10%;
	padding-top: 5%;
}
.container-manage{
}
hr.style-manage {
	height: 10px;
	border: 0;
	box-shadow: 0 10px 10px -10px #FFFFFF inset;
	color: white;
}
</style>