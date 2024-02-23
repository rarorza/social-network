<script>
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import axios from 'axios';
import FeedCard from '@/components/FeedCard.vue';
import CommentCard from '@/components/CommentCard.vue';

export default {
  name: 'PostView',
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedCard,
    CommentCard,
},
  data() {
    return {
      post: {},
      body: '',
    }
  },
  mounted() {
    this.getPost()
  },
  methods: {
    getPost() {
      axios.get(`/api/posts/${this.$route.params.id}/`).then(response => {
        console.log('data', response.data)
        this.post = response.data.post
      }).catch(error => {
        console.log('Error', error);
      })
    },
    submitForm() {
      if (this.body != '') {
        axios.post(`/api/posts/comment/${this.$route.params.id}/`, {
          'body': this.body
        }).then(response => {
          console.log('data', response)

          this.post.comments.push(response.data)
          this.post.comments_count += 1
          this.body = ''
        }).catch(error => {
          console.log('Error', error);
        })
      }
    },
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div class="bg-white border border-gray-200 rounded-lg">
        <div v-if="post.id" class="p-4">
          <FeedCard :post="post" />
          <hr>
        </div>
  
        <div v-for="comment in post.comments" :key="comment.id" class="p-4 ml-6">
          <CommentCard :comment="comment" />
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-lg">
        <form @submit.prevent="submitForm" method="post">
          <div class="p-4">
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
              placeholder="What are you think?"></textarea>
          </div>

          <div class="p-4 border-t border-gray-100">
            <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Comment</button>
          </div>
        </form>
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>