<script>
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue'
import Trends from '@/components/Trends.vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import ProfileCard from '@/components/ProfileCard.vue'
import FeedCard from '@/components/FeedCard.vue'
import FormCreatePost from '@/components/FormCreatePost.vue'

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
    FeedCard,
    FormCreatePost
  },
  data() {
    return {
      posts: [],
      user: {
        id: null,
      },
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
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <ProfileCard :user="user" />

    <div class="main-center col-span-2 space-y-4">
      <div v-if="userStore.user.id === user.id"
        class="bg-white border border-gray-200 rounded-lg">
        <FormCreatePost :user="user" :posts="posts" />
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