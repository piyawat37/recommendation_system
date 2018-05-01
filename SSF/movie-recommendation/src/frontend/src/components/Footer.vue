<template>
    <footer>
       	<p><b>Copyright &copy; 2018 Version {{version}} Development by</b> <span>Piyawat Pemwattana</span> and <span>Sarawut Ekakoon</span> <b>Supervisor</b> <span>Thanapol Phungtuaeng</span></p>
       	<p>Rajamangala University of Technology Tawan-Ok : Chakrabongse Bhuvanarth Campus</p>
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
	font-size: 11px;
	position: fixed;
	width: 100%;
	bottom: 0;
    padding: 1%;
  	background-color: #151515;
  	z-index: 10;
}
footer > p{
	padding: 0;
	margin: 0;
}
footer > p > span{
	color: #ff9900;
}
</style>