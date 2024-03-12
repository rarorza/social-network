<script>
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import axios from 'axios';
import FeedCard from '@/components/FeedCard.vue';

export default {
  name: 'FeedView',
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedCard
  },
  data() {
    return {
      posts: [],
    }
  },
  mounted() {
    this.getFeed()
  },
  watch: {
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
      axios.get(`/api/posts/?trend=${this.$route.params.id}`).then(response => {
        console.log('data', response.data)
        this.posts = response.data
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
      <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h2 class="text-xl">#{{ $route.params.id }}</h2>
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