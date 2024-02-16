<script>
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import axios from 'axios';
import ProfileCard from '@/components/ProfileCard.vue';
import FeedCard from '@/components/FeedCard.vue';

export default {
  name: 'FeedView',
  components:{
    PeopleYouMayKnow,
    Trends,
    ProfileCard,
    FeedCard
  },
  data() {
    return {
      posts: [],
      body: '',
    }
  },
  mounted() {
    this.getFeed()
  },
  methods: {
    getFeed() {
      axios.get('/api/posts/').then(response => {
        console.log('data', response.data)
        this.posts = response.data
      }).catch(error => {
        console.log('Error', error);
      })
    },
    submitForm() {
      axios.post('/api/posts/create/', {
        'body': this.body
      }).then(response => {
        console.log('data', response)

        this.posts.unshift(response.data)
        this.body = ''
      }).catch(error => {
        console.log('Error', error);
      })
    }
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div class="bg-white border border-gray-200 rounded-lg">
        <form @submit.prevent="submitForm" method="post">
          <div class="p-4">
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
            placeholder="What are you thinking about?"></textarea>
          </div>
          
          <div class="p-4 border-t border-gray-100 flex justify-between">
            <a href="#"
            class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach
            image</a>
            
            <button href="#"
            class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
          </div>
        </form>
      </div>

      <div 
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts" :key="post.id"
      >
        <FeedCard :post="post"/>
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>