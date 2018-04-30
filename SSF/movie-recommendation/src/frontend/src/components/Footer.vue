<template>
    <footer>
        <div>Copyright &copy; 2018 Version {{version}}</div>
    </footer>
</template>
<script>
/* eslint-disable */
import configService from '../SystemConstant/config.json'
export default {
    data(){
        return{
        	version: '',
        	poc_version: '',
        }
    },
    mounted (){
    	var vm = this;
    	vm.$http.get(configService.commonService + '/getVersion/').then(response => {
  	      // get body data
  			vm.version = response.body.version
  			vm.poc_version = response.body.poc_version
  			vm.$Progress.decrease(10)
  			vm.$Progress.finish()
  			vm.progress = false
  	    }, response => {
  	      // error callback
  			vm.$Progress.fail()
  			vm.progress = false
  	    });
    }
}
</script>
<style scoped>
footer{
	position: fixed;
	width: 100%;
	bottom: 0;
	height: 5%;
    padding: 25px;;
  	background-color: #151515;
  	z-index: 10;
}
</style>