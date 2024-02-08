<template>
  <div class="flex justify-center items-center h-full min-h-screen bg-primary-500">
    <form @submit.prevent="login" class="w-96 p-8 m-8 bg-white rounded-lg shadow-lg">
      <h1 class="text-lg">Welcome to</h1>
      <h2 class="text-2xl font-bold mb-4">WebbiSkools QuizManager</h2>
      <div class="mb-4">
        <label for="username" class="block font-bold">Username</label>
        <input
          v-model="username"
          id="username"
          type="text"
          autocomplete="username"
          required
          placeholder="Enter your username"
          class="w-full px-4 py-2 border border-gray-300 rounded-md"
        />
      </div>
      <div class="mb-4">
        <label for="password" class="block font-bold">Password</label>
        <input
          v-model="password"
          id="password"
          type="password"
          autocomplete="current-password"
          required
          placeholder="Enter your password"
          class="w-full px-4 py-2 border border-gray-300 rounded-md"
        />
      </div>
      <div class="flex items-center mb-4">
        <input
          v-model="remember"
          id="remember"
          type="checkbox"
          class="mr-2 border border-gray-300 rounded"
        />
        <label for="remember">Remember me</label>
      </div>
      <button
        type="submit"
        class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 rounded-md"
      >
        Sign In
      </button>
      <div class="mt-4 flex flex-col sm:flex-row sm:justify-between">
        <a href="#" class="text-blue-500 hover:text-blue-900 underline">Create an Account</a>
        <a href="#" class="text-blue-500 hover:text-blue-900 underline">Forgot Password?</a>
      </div>
    </form>

    <ToastView />
  </div>
</template>

<script>
import userAPI from '@/api/user'
import ToastView from '@/components/ToastView.vue'
import { getErrorToast } from '@/utilities'

export default {
  data() {
    return {
      username: '',
      password: '',
      remember: false
    }
  },
  methods: {
    login() {
      userAPI.loginUser(
        this.username,
        this.password,
        this.remember,
        () => {
          const path = new URLSearchParams(window.location.search).get('path')
          if (path) {
            document.location.replace(path)
          } else {
            document.location.replace('/')
          }
        },
        (error) => {
          this.$store.dispatch('createToast', getErrorToast(error))
        }
      )
    }
  },
  components: { ToastView }
}
</script>
