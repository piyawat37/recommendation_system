<template>
  <div>
  	<h1>Let's Try It Up.</h1>
  	<h1>Your Turn.</h1>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      randomNumber: 0
    }
  },
  methods: {
    getRandomInt (min, max) {
      min = Math.ceil(min)
      max = Math.floor(max)
      return Math.floor(Math.random() * (max - min + 1)) + min
    },
    getRandomFromBackend () {
      const path = `http://localhost:5000/api/random`
      axios.get(path)
      .then(response => {
        this.randomNumber = response.data.randomNumber
      })
      .catch(error => {
        console.log(error)
      })
    },
    getRandom () {
      this.randomNumber = this.getRandomFromBackend()
    }
  },
  created () {
    this.getRandom()
  }
}
</script>