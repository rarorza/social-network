<script>
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue'
import Trends from '@/components/Trends.vue'
import axios from 'axios'
import FeedCard from '@/components/FeedCard.vue'
import FormCreatePost from '@/components/FormCreatePost.vue'

export default {
  name: 'FeedView',
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedCard,
    FormCreatePost
  },
  data() {
    return {
      posts: [],
    }
  },
  mounted() {
    this.getFeed()
  },
  methods: {
    getFeed() {
      axios.get('/api/posts/').then(response => {
        this.posts = response.data
      }).catch(error => {
        console.log('Error', error);
      })
    },
    deletePost(id) {
      axios.delete(`/api/posts/delete/${id}/`).then(response => {
        if (response.data.message == 'post deleted') {
          this.posts = this.posts.filter(post => post.id !== id)
        }
      }).catch(error => {
        console.log('error', error)
      })
    },
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div class="bg-white border border-gray-200 rounded-lg">
        <FormCreatePost :user="null" :posts="posts" />
      </div>

      <div class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts" :key="post.id">
        <FeedCard :post="post" @deletePost="deletePost" />
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>