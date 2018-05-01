<template>
	<div class="container-main">
		<div class="container-manage">
			<b-container fluid class="text-left">
				<b-row>
					<b-col cols="8">
						<h1 v-text="uiLabel.screenTitle"></h1>
					</b-col>
					<b-col cols="4" class="text-right">
						<b-button v-b-modal.createAccount variant="primary"><i class="fa fa-plus-square" aria-hidden="true"></i> <span v-text="uiLabel.createAccount"></span></b-button>
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
			             :items="users"
			             :fields="fields"
			             :current-page="currentPage"
			             :per-page="perPage"
			             :filter="filter"
			             :sort-by.sync="sortBy"
			             :sort-desc.sync="sortDesc"
			             @filtered="onFiltered"
			    >
			      <template slot="name" slot-scope="row">{{row.value.first}} {{row.value.last}}</template>
			      <template slot="status" slot-scope="row">
			      	<!-- <toggle-button @change="..."/> -->
					<!-- <toggle-button v-model="row.value" :sync="true" :labels="{checked: 'Active', unchecked: 'Inactive'}"/> -->
			      	{{row.value === 'A'?'Active':'Inactive'}}
			      </template>
			      <template slot="actions" slot-scope="row">
			        <!-- We use @click.stop here to prevent a 'row-clicked' event from also happening -->
			        <b-button size="md" @click.stop="info(row.item, row.index, $event.target)" class="mr-1" variant="success">
			          <i class="fa fa-pencil-square-o" aria-hidden="true"></i>
			        </b-button>
			        <b-button size="md" @click.stop="deleteUser(row.item, row.index)" variant="danger">
			          <i class="fa fa-trash" aria-hidden="true"></i>
			        </b-button>
			      </template>
			    </b-table>
			
			    <!-- Info modal -->
			    <b-modal class="modal-edit" id="userInfo" :title="userInfo.title"
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
							                 v-model="userInfo.content.email"></b-form-input>
							</b-form-group>
							<b-form-group>
								<b-form-input type="text" disabled
							                 v-model="userInfo.content.username"></b-form-input>
							</b-form-group>
							
							<b-form-group>
								<b-form-select v-model="userInfo.content.status" :options="options" class="mb-3" />
							</b-form-group>
			           		<div slot="modal-footer" class="w-100">
					       		 <b-row>
					       		 	<b-col lg="6" md="12" cols="12">
					       		 		<label style="padding-top: 15px;">
					       		 			<b-link href="#forgot" v-text="uiLabel.forgot"></b-link>
					       		 		</label>
						         	</b-col>
					       		 	<b-col lg="6" md="12"  cols="12">
					       		 		<b-btn class="float-right" variant="secondary" @click="handleEditOk(userInfo.content)" v-text="uiLabel.submit" style="margin-left: 5px;"></b-btn>
					       		 		<b-btn class="float-right" variant="danger" @click="resetModal" v-text="uiLabel.cancel"></b-btn>
					       		 	</b-col>
					       		 </b-row>
						     </div>
						</b-form>
		       		</b-container>
			    </b-modal>
			    
			    <b-modal  id="createAccount" v-bind:title="uiLabel.createAccount"
					ref="createAccount"
					header-bg-variant="dark" header-text-variant="light"
					body-bg-variant="dark" body-text-variant="light"
					footer-bg-variant="dark" footer-text-variant="light"
					:ok-title="uiLabel.createAccount" hide-footer hide-header
		            no-close-on-backdrop no-close-on-esc>
		           	<b-container fluid>
		           		<div slot="modal-header" class="w-100">
				       		 <b-row>
				       		 	<b-col cols="12" class="text-left">
				       		 		<h4 v-text="uiLabel.createAccount"></h4>
				       		 	</b-col>
				       		 </b-row>
					     </div>
					     <hr style="background-color: rgb(255, 255, 255);"/>
			            <b-form class="text-left">
							<b-form-group v-bind:class="{ 'form-group--error': $v.createAccount.email.$error }">
								<b-form-input type="email"
							                 :placeholder="uiLabel.email" @input="$v.createAccount.email.$touch()"
							                 v-model.trim="createAccount.email"></b-form-input>
							    <span class="form-group__message require" v-if="!$v.createAccount.email.required && $v.createAccount.email.$dirty">This field is required.</span>
							</b-form-group>
							<b-form-group v-bind:class="{ 'form-group--error': $v.createAccount.username.$error }">
								<b-form-input type="text"
							                 :placeholder="uiLabel.username" @input="$v.createAccount.username.$touch()"
							                 v-model.trim="createAccount.username"></b-form-input>
							    <span class="form-group__message require" v-if="!$v.createAccount.username.required && $v.createAccount.username.$dirty">This field is required.</span>
							</b-form-group>
							<b-form-group>
								<b-form-select v-model=createAccount.role :options="optionsRole" class="mb-3" />
							</b-form-group>
			           		<div slot="modal-footer" class="w-100">
					       		 <b-row>
					       		 	<b-col cols="12" class="text-right">
					       		 		<b-btn class="float-right" variant="secondary" @click="handleCreateAccount" v-text="uiLabel.submit" style="margin-left: 5px;"></b-btn>
					       		 		<b-btn class="float-right" variant="danger" @click="clearCreateAccount" v-text="uiLabel.cancel"></b-btn>
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
	  users: {},
	  totalRows: '',
      currentPage: 1,
      perPage: 5,
      pageOptions: [ 5, 10, 15 ],
      sortBy: null,
      sortDesc: false,
      filter: null,
      userInfo: { title: '', content: '' },
      progress: true,
      options: [
          { value: 'A', text: 'Active' },
          { value: 'I', text: 'Inactive' },
        ],
      optionsRole: [
          { value: 'admin', text: 'Admin' },
          { value: 'user', text: 'User' },
        ],
      createAccount:{
		email: '',
		username: '',
		role: 'user',
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
		vm.uiLabel = require("../i18n/accountmgt-"+this.language+".json")
		vm.setField(vm)
	},
	setField(vm){
		vm.fields = [
	        { key: 'username', label: vm.uiLabel.username, sortable: true, 'class': 'text-left', 'thClass': 'text-center' },
	        { key: 'email', label: vm.uiLabel.email, sortable: true, 'class': 'text-left', 'thClass': 'text-center' },
	        { key: 'status', label: vm.uiLabel.status },
	        { key: 'actions', label: ''}
	    ]	
	},
	info (item, index, button) {
      this.userInfo.title = `Row index: ${index}`
      var content = JSON.stringify(item, null, 2)
      this.userInfo.content = JSON.parse(content)
      this.$root.$emit('bv::show::modal', 'userInfo', button)
    },
    resetModal () {
      var vm = this
      vm.userInfo.title = ''
      vm.userInfo.content = {'email': '', 'username': '', 'status': ''}
   	  vm.$root.$emit('bv::hide::modal', 'userInfo')
      vm.$v.$reset()
    },
    onFiltered (filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
      this.currentPage = 1
    },
    deleteUser (user,index){
    	var vm = this;
   		vm.$swal({
   		  title: 'Are you sure?',
   		  text: 'You will not be able to recover this account !',
   		  type: 'warning',
   		  showCancelButton: true,
   		  confirmButtonText: 'Yes, delete it!',
   		  cancelButtonText: 'No, keep it'
   		}).then((result) => {
		  if (result) {
			  vm.$Progress.start()
              vm.$http.delete(configService.userService + '/deleteAccount/'+ user.userId + '/').then(response => {
            	  vm.$swal("Success", "Account deleted.", "success");   
            	  vm.$http.get(configService.userService + '/getAllUser/').then(response => {
	           	      // get body data
	           			vm.users = response.body.users
	           			vm.totalRows = vm.users.length
	           			/* $.each(vm.users, function(key, value) {
	           				value.status = value.status == 'A' ? 'Active' : 'Inactive'
	           		   	}); */
	           			vm.$Progress.finish()
	           	  }, response => {
	           	      // error callback
	           			vm.$Progress.fail()
	           	  });
                  vm.$Progress.finish()
				  vm.progress = false
              }, response => {
        	      // error callback
             	  vm.$swal("Cancelled", "This account has not been deleted !", "error");   
             	  vm.$Progress.finish()
				  vm.progress = false
			  });
           }
   		});
    },
    handleEditOk (userContext){
    	var vm = this;
   		vm.$http.post(configService.userService + '/updateStatus', userContext).then(response => {
         	var user = response.body.user
         	var content = "User "+user.username
         	content += " ,Updated Status to " 
         	content += user.status == "A" ? 'Active' : 'Inactive'
         	vm.$swal('Success!', content, 'success')
        	vm.getAllUser(vm)
         	// Redirect to a specified route
         }, response => {
        	vm.$swal('Error!', response.bodyText, 'error')
        	vm.getAllUser(vm)
     		console.log(response.statusText)
         });
    },
    getAllUser(vm) {
    	vm.$http.get(configService.userService + '/getAllUser/').then(response => {
   	      // get body data
   			vm.users = response.body.users
   			vm.totalRows = vm.users.length
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
    handleCreateAccount(){
    	var vm = this;
    	vm.createAccount.language = vm.language
    	if(!vm.$v.createAccount.$invalid){
	    	vm.$http.post(configService.userService + '/createAccount', vm.createAccount).then(response => {
	          	var user = response.body.user
	          	var content = "Account "
	          	content += user.username
	          	content += " created."
	          	this.$swal('Success!', content, 'success')
	          	vm.getAllUser(vm)
	          	vm.clearCreateAccount()
	          	// Redirect to a specified route
	          }, response => {
	       	  	this.$swal('Error!', response.bodyText, 'error')
	       	  	vm.getAllUser(vm)
	      		console.log(response.statusText)
	          });
    	}else{
        	this.$swal('Error!', this.uiLabel.required, 'error')
        }
    },
    clearCreateAccount(){
    	var vm = this;
    	vm.createAccount = {'email': '', 'username': '', 'role': 'user'}
 	   	vm.$root.$emit('bv::hide::modal', 'createAccount')
        vm.$v.$reset()
    }
  },
  beforeCreate() {
	var vm = this;
	vm.$http.get(configService.userService + '/getAllUser/').then(response => {
      // get body data
		vm.users = response.body.users
		vm.totalRows = vm.users.length
		/* $.each(vm.users, function(key, value) {
			value.status = value.status == 'A' ? 'Active' : 'Inactive'
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
	vm.uiLabel = require("../i18n/accountmgt-"+vm.language+".json")
  },
  validations: {
    createAccount: {
   	  email:{
  		  required
  	  },
	  username:{
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
.modal-edit{
	color: #151515;
}
</style>