<template>
<button class="clickAble" :class="cssClasses" v-text="label"
	@click="clicked()"></button>
</template>
<script>
/* eslint-disable */
export default {
  props: {
    id: {
      type: String,
      required: true
    },
    url: {
      type: String,
      required: true
    },
    message: {
      type: String,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    cssClasses: {
      type: String,
      required: false
    }
  },
  mounted() { 
      this.$events.listen('remove-dialog-' + this.id + '-called', (data) => {
          window.location.reload(true);
      });
  },
  methods: {
    clicked() { 
      this.$events.fire('top-confirm', {
          id: 'remove-dialog-' + this.id,
          message: this.message,
          url: this.url
      });
      /* alert('a') */
    }
  }
}
</script>