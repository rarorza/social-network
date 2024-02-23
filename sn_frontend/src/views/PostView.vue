<script>
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import axios from 'axios';
import FeedCard from '@/components/FeedCard.vue';

export default {
  name: 'PostView',
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedCard
  },
  data() {
    return {
      post: {},
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
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div v-if="post.id" class="p-4 bg-white border border-gray-200 rounded-lg">
        <FeedCard :post="post" />
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>