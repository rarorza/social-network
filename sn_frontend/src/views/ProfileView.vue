<script>
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import ProfileCard from '@/components/ProfileCard.vue';
import FeedCard from '@/components/FeedCard.vue';

export default {
  name: 'ProfileView',
  setup() {
    const userStore = useUserStore()
    return {
      userStore
    }
  },
  components: {
    PeopleYouMayKnow,
    Trends,
    ProfileCard,
    FeedCard
  },
  data() {
    return {
      posts: [],
      user: {
        id: null,
      },
      body: '',
      url: null,
    }
  },
  mounted() {
    this.getFeed()
  },
  watch: {
    // watching if url change, ex when user visit someone else profile and click
    // to go for another profile
    '$route.params.id': {
      handler: function () {
        this.getFeed()
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    getFeed() {
      axios.get(`/api/posts/profile/${this.$route.params.id}/`).then(response => {
        console.log('data', response.data)

        this.posts = response.data.posts
        this.user = response.data.user
      }).catch(error => {
        console.log('Error', error);
      })
    },
    submitForm() {
      let formData = new FormData()
      formData.append('image', this.$refs.file.files[0])
      formData.append('body', this.body)

      if (this.body != '') {
        axios.post('/api/posts/create/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        }).then(response => {
          console.log('data', response)

          this.posts.unshift(response.data)
          this.body = ''
          this.url = null
          this.$refs.fiels.value = null
          this.user.posts_count += 1
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
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <ProfileCard :user="user" />

    <div class="main-center col-span-2 space-y-4">
      <div v-if="userStore.user.id === user.id"
        class="bg-white border border-gray-200 rounded-lg">
        <form @submit.prevent="submitForm" method="post">
          <div class="p-4">
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
              placeholder="What are you thinking about?"></textarea>
          </div>

          <div class="preview" v-if="url">
            <img :src="url" class="w-[100px] my-3 mx-4 rounded-xl">
          </div>

          <div class="p-4 border-t border-gray-100 flex justify-between">
            <label
              class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
              <input type="file" ref="file" @change="onFileChange"
                accept="image/*" class="file-input py-2"> Attach image
            </label>

            <button href="#"
              class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
          </div>
        </form>
      </div>

      <div class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts" :key="post.id">
        <FeedCard :post="post" />
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>

<style scoped>
input[type="file"] {
  display: none;
}
</style>