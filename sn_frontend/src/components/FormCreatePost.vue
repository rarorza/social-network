<script>
import axios from 'axios'

export default {
  props: {
    user: {
      type: Object,
      default: null,
    },
    posts: {
      type: Array,
      default: []
    }
  },
  data() {
    return {
      body: '',
      url: null,
      isPrivate: false,
    }
  },
  methods: {
    submitForm() {
      let formData = new FormData()
      formData.append('image', this.$refs.file.files[0])
      formData.append('body', this.body)
      formData.append('is_private', this.isPrivate)

      if (this.body !== '') {
        axios.post('/api/posts/create/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        }).then(response => {
          console.log('data', response)

          this.posts.unshift(response.data)
          this.body = ''
          this.url = null
          this.isPrivate = false
          this.$refs.fiels.value = null
          
          if (this.user) {
            this.user.posts_count += 1
          }
        }).catch(error => {
          console.log('Error', error);
        })
      }
    },
    onFileChange(event) {
      const file = event.target.files[0]
      this.url = URL.createObjectURL(file)
    },
  }
}
</script>

<template>
  <form @submit.prevent="submitForm" method="post">
    <div class="p-4">
      <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
        placeholder="What are you thinking about?"></textarea>

      <label>
        <input type="checkbox" v-model="isPrivate"> Private
      </label>
    </div>

    <div class="preview" v-if="url">
      <img :src="url" class="w-[100px] my-3 mx-4 rounded-xl">
    </div>

    <div class="p-4 border-t border-gray-100 flex justify-between">
      <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
        <input type="file" ref="file" @change="onFileChange" accept="image/*"
          class="file-input py-2"> Attach image
      </label>

      <button href="#"
        class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
    </div>
  </form>
</template>

<style scoped>
input[type="file"] {
  display: none;
}
</style>