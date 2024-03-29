<script>
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue'
import Trends from '@/components/Trends.vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import axios from 'axios'
import ProfileCard from '@/components/ProfileCard.vue'
import FeedCard from '@/components/FeedCard.vue'
import FormCreatePost from '@/components/FormCreatePost.vue'

export default {
  name: 'ProfileView',
  setup() {
    const userStore = useUserStore()
    const toastStore = useToastStore()
    return {
      userStore,
      toastStore
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
    deletePost(id) {
      axios.delete(`/api/posts/delete/${id}/`).then(response => {
        if (response.data.message == 'post deleted') {
          this.posts = this.posts.filter(post => post.id !== id)
          this.user.posts_count -= 1
          this.toastStore.showToast(
            5000,
            'The post was deleted.',
            'bg-emerald-500'
          )
        }
      }).catch(error => {
        console.log('error', error)
      })
    },
    reportPost(id) {
      axios.post(`/api/posts/report/${id}/`).then(response => {
        if (response.data.message == 'post reported') {
          this.toastStore.showToast(
            5000,
            'The post was reported.',
            'bg-emerald-500'
          )
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
    <ProfileCard :user="user" />

    <div class="main-center col-span-2 space-y-4">
      <div v-if="userStore.user.id === user.id"
        class="bg-white border border-gray-200 rounded-lg">
        <FormCreatePost :user="user" :posts="posts" />
      </div>

      <div class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts" :key="post.id">
        <FeedCard :post="post" @deletePost="deletePost" @reportPost="reportPost"/>
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