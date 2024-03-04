<script>
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import ProfileCard from '@/components/ProfileCard.vue';

export default {
  name: 'FriendsView',
  setup() {
    const userStore = useUserStore()
    return {
      userStore
    }
  },
  components:{
    PeopleYouMayKnow,
    Trends,
    ProfileCard,
  },
  data() {
    return {
      user: {},
      friendshipRequests: [],
      friends: [],
    }
  },
  mounted() {
    this.getFriends()
  },
  methods: {
    getFriends() {
      axios.get(`/api/friends/${this.$route.params.id}/`).then(response => {
        console.log('data', response.data)

        this.friendshipRequests = response.data.requests
        this.friends = response.data.friends
        this.user = response.data.user
      }).catch(error => {
        console.log('Error', error);
      })
    },
    handleFriendshipRequest(status, pk) {
      axios.post(`/api/friends/${pk}/${status}/`).then(response => {
        console.log(response.data);
      }).catch(error => {
        console.log('Error', error);
      })
    }
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <ProfileCard :user="user" />

    <div class="main-center col-span-2 space-y-4">
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-if="friendshipRequests.length">
        <h2 class="mb-6 text-xl">Friendship requests</h2>


        <div class="p-4 text-center bg-gray-100 rounded-lg" v-for="friendshipRequest in friendshipRequests"
          :key="friendshipRequest.id">
          <img src="https://i.pravatar.cc/100?img=45" class="mb-6 mx-auto rounded-full">

          <p>
            <strong>
              <RouterLink :to="{ name: 'profile', params: { 'id': friendshipRequest.created_by.id } }">{{
                friendshipRequest.created_by.name }}</RouterLink>
            </strong>
          </p>

          <div class="mt-6 flex space-x-8 justify-around">
            <p class="text-xs text-gray-500">{{ friendshipRequest.created_by.friends_count }} friends</p>
            <p class="text-xs text-gray-500">{{ friendshipRequest.created_by.posts_count }} posts</p>
          </div>

          <div class="mt-6 space-x-4">
            <button @click="handleFriendshipRequest('accepted', friendshipRequest.created_by.id)" class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Accept</button>
            <button @click="handleFriendshipRequest('rejected', friendshipRequest.created_by.id)" class="inline-block py-4 px-6 bg-red-600 text-white rounded-lg">Reject</button>
          </div>
        </div>
        <hr>
      </div>

      <div
        class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-3 gap-4"
        v-if="friends.length">
        <div class="p-4 text-center bg-gray-100 rounded-lg" v-for="friend in friends"
          :key="friend.id">
          <img src="https://i.pravatar.cc/300?img=45" class="mb-6 rounded-full">

          <p>
            <strong>
              <RouterLink :to="{ name: 'profile', params: { 'id': friend.id } }">{{
                friend.name }}</RouterLink>
            </strong>
          </p>

          <div class="mt-6 flex space-x-8 justify-around">
            <p class="text-xs text-gray-500">{{ friend.friends_count }} friends</p>
            <p class="text-xs text-gray-500">{{ friend.posts_count }} posts</p>
          </div>
        </div>
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <Trends />
    </div>
  </div>
</template>