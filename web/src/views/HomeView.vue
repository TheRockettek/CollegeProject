<template>
  <div class="min-h-full">
    <HeadingView />
    <div class="py-10 mx-auto max-w-7xl px-8">
      <header class="mb-4">
        <nav class="flex mb-2" aria-label="Breadcrumb">
          <ol role="list" class="flex items-center space-x-2">
            <li><span class="text-sm font-medium text-gray-400">Home</span></li>
          </ol>
        </nav>
        <div
          class="w-full flex flex-col sm:flex-row sm:justify-between items-stretch sm:items-center"
        >
          <h1 class="text-3xl font-bold leading-tight tracking-tight text-gray-900">All Quizzes</h1>
          <router-link
            v-if="$store.getters.getCurrentUser?.role == 'editor'"
            to="/quiz/create"
            type="button"
            class="rounded-md bg-primary-500 hover:bg-primary-700 text-center px-3 py-2 text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500"
          >
            Create New Quiz
          </router-link>
          <button
            v-else
            role="button"
            disabled
            class="rounded-md px-3 py-2 text-sm font-semibold text-gray-300 bg-gray-100 hover:bg-gray-100 cursor-default shadow-sm"
          >
            Create New Quiz
          </button>
        </div>
      </header>
      <main>
        <div
          class="mb-4 p-4 bg-gray-200 border border-gray-300 rounded-md grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2"
        >
          <div class="relative">
            <div
              class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500"
            >
              <svg class="icon w-4 h-4" fill="currentColor" viewBox="0 0 512 512">
                <path
                  d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z"
                />
              </svg>
            </div>
            <input
              v-model="query"
              @change="fetchQuizzes"
              name="search"
              id="search"
              class="block w-full rounded-md border border-gray-300 py-1.5 pl-10 text-gray-900focus:ring-2 focus:ring-inset focus:ring-primary-500 sm:text-sm sm:leading-6"
              placeholder="Search..."
            />
          </div>

          <RadioGroup
            v-if="$store.getters.getCurrentUser?.role == 'editor'"
            :modelValue="status"
            @update:modelValue="
              (value) => {
                this.status = value
                fetchQuizzes()
              }
            "
            class="border border-gray-300 bg-white rounded-md w-full md:max-w-md"
          >
            <div class="grid grid-cols-1 gap-1 sm:grid-cols-3 p-1">
              <RadioGroupOption
                as="template"
                v-for="option in statusOptions"
                :key="option.name"
                :value="option.value"
                v-slot="{ active, checked }"
              >
                <div
                  :class="[
                    active ? 'ring-2 ring-primary-500 ring-offset-2' : '',
                    checked
                      ? 'bg-primary-500 text-white hover:bg-primary-700'
                      : 'text-gray-900 hover:bg-gray-50',
                    'flex items-center justify-center rounded py-1 px-3 text-sm sm:flex-1 cursor-pointer focus:outline-none'
                  ]"
                >
                  <RadioGroupLabel as="span">{{ option.name }}</RadioGroupLabel>
                </div>
              </RadioGroupOption>
            </div>
          </RadioGroup>
        </div>

        <div class="inline-block min-w-full align-middle rounded-md overflow-hidden bg-gray-50">
          <table class="min-w-full border-separate border-spacing-0 overflow-x-auto">
            <thead class="bg-gray-200 border border-gray-300">
              <tr>
                <th
                  scope="col"
                  class="sticky top-0 z-10 border-b border-gray-300 py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 backdrop-blur backdrop-filter sm:pl-6 lg:pl-8"
                >
                  Quiz Name
                </th>
                <th
                  scope="col"
                  class="sticky top-0 z-10 hidden border-b border-gray-300 px-3 py-3.5 text-left text-sm font-semibold text-gray-900 backdrop-blur backdrop-filter sm:table-cell"
                >
                  Question Count
                </th>
                <th
                  scope="col"
                  class="sticky top-0 z-10 hidden border-b border-gray-300 px-3 py-3.5 text-left text-sm font-semibold text-gray-900 backdrop-blur backdrop-filter lg:table-cell"
                >
                  Status
                </th>
                <th
                  scope="col"
                  class="sticky top-0 z-10 border-b border-gray-300 px-3 py-3.5 text-left text-sm font-semibold text-gray-900 backdrop-blur backdrop-filter"
                >
                  Last Updated
                </th>
                <th
                  scope="col"
                  class="sticky top-0 z-10 border-b border-gray-300 py-3.5 pl-3 pr-4 backdrop-blur backdrop-filter sm:pr-6 lg:pr-8"
                >
                  <span class="sr-only">Edit</span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="quiz in this.quizzes" :key="quiz.id">
                <td
                  class="whitespace-nowrap border-b border-gray-200 py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6 lg:pl-8"
                >
                  {{ quiz.name }}
                </td>
                <td
                  class="whitespace-nowrap border-b border-gray-200 hidden px-3 py-4 text-sm text-gray-900 sm:table-cell"
                >
                  {{ quiz.question_count }}
                </td>
                <td
                  class="whitespace-nowrap border-b border-gray-200 hidden px-3 py-4 text-sm text-gray-900 lg:table-cell"
                >
                  {{ quiz.status }}
                </td>
                <td
                  class="whitespace-nowrap border-b border-gray-200 px-3 py-4 text-sm text-gray-900"
                >
                  {{ getRelativeTimeFromISO(quiz.updated_at) }} by
                  <b>{{ quiz.updated_by?.name }}</b>
                </td>
                <td
                  class="relative whitespace-nowrap border-b border-gray-200 py-4 pr-4 pl-3 text-right text-sm font-medium sm:pr-8 lg:pr-8"
                >
                  <router-link
                    :to="'/quiz/' + quiz.id"
                    class="text-primary-500 hover:text-primary-700 underline"
                  >
                    <span v-if="$store.getters.getCurrentUser?.role == 'editor'">Edit</span>
                    <span v-else>View</span>
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="my-4 text-center" v-if="isDataError">
            <p>There was an error fetching quizzes. Please try again.</p>
            <button @click="fetchQuizzes" class="text-primary-500 hover:text-primary-700 underline">
              Retry
            </button>
          </div>
          <div class="my-4 text-center" v-else-if="quizzes.length === 0">No quizzes found</div>

          <nav
            class="flex items-center justify-between bg-white-50 px-4 py-2"
            aria-label="Pagination"
          >
            <div class="hidden sm:block">
              <p class="text-sm text-gray-700">
                Showing
                <span class="font-medium">{{ offset }}</span>
                to
                <span class="font-medium">{{ offset + quizzes.length }}</span>
                of
                <span class="font-medium">{{ count }}</span>
                results
              </p>
            </div>
            <div class="flex flex-1 justify-between sm:justify-end">
              <button
                @click="setOffset(offset - limit)"
                :class="[
                  offset > 0
                    ? 'text-gray-900 border border-gray-300 bg-white hover:bg-gray-50'
                    : 'text-gray-300 bg-gray-100 hover:bg-gray-100 cursor-default',
                  'relative inline-flex items-center rounded-md px-3 py-1 text-sm font-semibold focus-visible:outline-offset-0'
                ]"
              >
                Previous
              </button>
              <button
                @click="setOffset(offset + limit)"
                :class="[
                  offset < count - limit
                    ? 'text-gray-900 border border-gray-300 bg-white hover:bg-gray-50'
                    : 'text-gray-300 bg-gray-100 hover:bg-gray-100 cursor-default',
                  'relative ml-3 inline-flex items-center rounded-md px-3 py-1 text-sm font-semibold focus-visible:outline-offset-0'
                ]"
              >
                Next
              </button>
            </div>
          </nav>
        </div>
        <div class="my-4 text-center" v-if="!isDataFetched">
          <svg
            class="icon animate-spin w-8 h-8 text-gray-300"
            fill="currentColor"
            viewBox="0 0 512 512"
          >
            <path
              d="M477.7 384c21.8-37.7 34.3-81.4 34.3-128C512 114.6 397.4 0 256 0V64c106 0 192 86 192 192c0 35-9.4 67.8-25.7 96l55.4 32z"
            />
          </svg>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import HeadingView from '@/components/HeadingView.vue'
import quizAPI from '@/api/quiz.js'
import { getRelativeTimeFromISO } from '@/utilities'
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from '@headlessui/vue'

export default {
  components: {
    HeadingView,
    RadioGroup,
    RadioGroupLabel,
    RadioGroupOption
  },
  data() {
    return {
      quizzes: [],
      count: 0,
      query: '',
      limit: 10,
      offset: 0,
      status: '',
      isDataFetched: false,
      isDataError: false,

      statusOptions: [
        { name: 'All', value: '' },
        { name: 'Published', value: 'published' },
        { name: 'Draft', value: 'draft' }
        // { name: "Archived", value: "archived" },
      ],

      getRelativeTimeFromISO
    }
  },
  mounted() {
    this.fetchQuizzes()
  },
  methods: {
    setOffset(newOffset) {
      if (newOffset < 0 || newOffset > this.count - this.limit) {
        return
      }

      this.offset = newOffset
      this.fetchQuizzes()
    },
    fetchQuizzes() {
      this.isDataError = false
      this.isDataFetched = false
      quizAPI.getQuizzes(
        this.query,
        this.limit,
        this.offset,
        this.status,
        ({ quizzes, count }) => {
          this.quizzes = quizzes
          this.count = count
          this.isDataFetched = true
        },
        (error) => {
          console.error('Failed to fetch quizzes:', error)
          this.isDataError = true
          this.isDataFetched = true
        }
      )
    }
  }
}
</script>
