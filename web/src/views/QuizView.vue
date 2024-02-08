<template>
  <div class="min-h-full" :class="[this.selectedIndex != null ? 'cursor-move' : '']">
    <HeadingView />
    <div class="py-10 mx-auto max-w-7xl px-8">
      <header class="mb-4">
        <nav class="flex mb-2" aria-label="Breadcrumb">
          <ol role="list" class="flex items-center space-x-2">
            <li><a href="/" class="text-sm font-medium text-gray-700 underline">Home</a></li>
            <li class="text-gray-300">⟩</li>
            <li>
              <span class="text-sm font-medium text-gray-400">{{ quizName }}</span>
            </li>
          </ol>
        </nav>
        <h1 class="text-3xl font-bold leading-tight tracking-tight text-gray-900">
          {{ quizName }}
        </h1>
      </header>
      <form @submit.prevent="saveQuiz">
        <main>
          <div
            class="mb-4 p-4 bg-gray-200 border border-gray-300 rounded-md grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2"
            v-if="$store.getters.getCurrentUser?.role == 'editor'"
          >
            <div>
              <label for="quizname" class="block font-bold">Quiz Name</label>
              <input
                v-model="quiz.name"
                id="quizname"
                type="text"
                required
                placeholder="Enter the quiz name"
                class="w-full px-4 py-2 border border-gray-300 rounded-md"
                @input="onValueUpdate"
              />
            </div>
            <div>
              <label for="status" class="block font-bold">Status</label>
              <select
                v-model="quiz.status"
                id="status"
                class="w-full px-4 py-2 border border-gray-300 rounded-md"
                required
                @change="onValueUpdate"
              >
                <option v-for="option in statusOptions" :value="option.value" :key="option.value">
                  {{ option.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="mb-4">
            <div
              v-for="(question, index) in quiz.questions"
              :key="question"
              class="flex"
              v-on:mousemove="this.mouseMoveHandler(index)"
              :class="[this.selectedIndex != null ? 'select-none' : '']"
            >
              <span class="w-full max-w-7 mr-2">
                {{ index + 1 }}.
                <div
                  v-if="$store.getters.getCurrentUser?.role == 'editor'"
                  class="mt-2 cursor-move"
                  v-on:mousedown="this.mouseDownHandler(index)"
                  :class="[this.selectedIndex == index ? 'text-primary-500' : '']"
                >
                  <svg class="icon w-5 h-5" fill="currentColor" viewBox="0 0 320 512">
                    <path
                      d="M40 352l48 0c22.1 0 40 17.9 40 40l0 48c0 22.1-17.9 40-40 40l-48 0c-22.1 0-40-17.9-40-40l0-48c0-22.1 17.9-40 40-40zm192 0l48 0c22.1 0 40 17.9 40 40l0 48c0 22.1-17.9 40-40 40l-48 0c-22.1 0-40-17.9-40-40l0-48c0-22.1 17.9-40 40-40zM40 320c-22.1 0-40-17.9-40-40l0-48c0-22.1 17.9-40 40-40l48 0c22.1 0 40 17.9 40 40l0 48c0 22.1-17.9 40-40 40l-48 0zM232 192l48 0c22.1 0 40 17.9 40 40l0 48c0 22.1-17.9 40-40 40l-48 0c-22.1 0-40-17.9-40-40l0-48c0-22.1 17.9-40 40-40zM40 160c-22.1 0-40-17.9-40-40L0 72C0 49.9 17.9 32 40 32l48 0c22.1 0 40 17.9 40 40l0 48c0 22.1-17.9 40-40 40l-48 0zM232 32l48 0c22.1 0 40 17.9 40 40l0 48c0 22.1-17.9 40-40 40l-48 0c-22.1 0-40-17.9-40-40l0-48c0-22.1 17.9-40 40-40z"
                    />
                  </svg>
                </div>
              </span>
              <div class="mb-2 bg-gray-200 border border-gray-300 rounded-md w-full">
                <div v-if="question._showAnswers" class="p-4">
                  <div v-if="$store.getters.getCurrentUser?.role == 'editor'">
                    <input
                      v-model="question.name"
                      id="quizname"
                      type="text"
                      required
                      placeholder="Enter the quiz name"
                      class="w-full px-4 py-2 border border-gray-300 rounded-md mb-4"
                      @input="onValueUpdate"
                    />
                    <fieldset
                      v-for="answer in question.answers"
                      :key="answer.id"
                      class="flex align-middle items-center mb-2"
                    >
                      <div class="min-w-8">
                        <input
                          type="checkbox"
                          :id="answer.id"
                          class="mr-2 border border-gray-300 rounded"
                          v-bind:value="answer.is_correct"
                          v-on:input="answer.is_correct = $event.target.checked"
                          :checked="answer.is_correct ? 1 : 0"
                          @input="onValueUpdate"
                        />
                      </div>
                      <input
                        @input="onAnswerChange(question)"
                        v-model="answer.name"
                        id="answer"
                        type="text"
                        required
                        placeholder="Enter an answer"
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                      />
                    </fieldset>
                    <div class="flex align-middle items-center mb-2 ml-8">
                      <input
                        @change="onNewAnswer(question)"
                        v-model="question._answer"
                        id="quizname"
                        type="text"
                        placeholder="Enter new answer"
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                      />
                    </div>
                  </div>
                  <div v-else>
                    <span class="text-xl font-bold leading-tight tracking-tight text-gray-900">{{
                      question.name
                    }}</span>
                    <ol class="space-y-1 mt-4">
                      <li
                        v-for="answer in question.answers"
                        :key="answer.id"
                        class="flex align-middle items-center mb-2"
                      >
                        <div class="min-w-8">
                          <input
                            type="radio"
                            class="mr-2 border-gray-300"
                            :checked="answer.is_correct ? 1 : 0"
                            disabled
                          />
                        </div>
                        <span class="w-full">
                          {{ answer.name }}
                        </span>
                      </li>
                    </ol>
                  </div>
                </div>
                <div v-else class="m-4">
                  <span class="text-xl font-bold leading-tight tracking-tight text-gray-900">{{
                    question.name
                  }}</span>
                  <ol class="space-y-1 mt-4">
                    <li
                      v-for="answer in question.answers"
                      :key="answer.id"
                      class="flex align-middle items-center mb-2"
                    >
                      <div class="min-w-8">
                        <input type="radio" class="mr-2 border-gray-300" disabled />
                      </div>
                      {{ answer.name }}
                    </li>
                  </ol>
                </div>
                <div
                  class="p-4 border-t border-gray-300 text-gray-500"
                  v-if="
                    $store.getters.getCurrentUser?.role == 'editor' ||
                    $store.getters.getCurrentUser?.role == 'viewer'
                  "
                >
                  <button
                    v-if="$store.getters.getCurrentUser?.role == 'editor'"
                    @click="copyQuestion(quiz, index)"
                    type="button"
                    class="hover:text-gray-900 mr-4"
                  >
                    <svg class="icon w-6 h-6" fill="currentColor" viewBox="0 0 448 512">
                      <path
                        d="M208 0H332.1c12.7 0 24.9 5.1 33.9 14.1l67.9 67.9c9 9 14.1 21.2 14.1 33.9V336c0 26.5-21.5 48-48 48H208c-26.5 0-48-21.5-48-48V48c0-26.5 21.5-48 48-48zM48 128h80v64H64V448H256V416h64v48c0 26.5-21.5 48-48 48H48c-26.5 0-48-21.5-48-48V176c0-26.5 21.5-48 48-48z"
                      />
                    </svg>
                  </button>
                  <button
                    v-if="$store.getters.getCurrentUser?.role == 'editor'"
                    @click="removeQuestion(quiz, index)"
                    type="button"
                    class="hover:text-gray-900 pr-4 border-r border-gray-300 mr-4"
                  >
                    <svg class="icon w-6 h-6" fill="currentColor" viewBox="0 0 448 512">
                      <path
                        d="M144 0L128 32H0V96H448V32H320L304 0H144zM416 128H32L56 512H392l24-384z"
                      />
                    </svg>
                  </button>
                  <button
                    v-if="question._showAnswers"
                    @click="toggleAnswers(question)"
                    type="button"
                    class="hover:text-gray-900"
                  >
                    <svg class="icon w-6 h-6 mr-1" fill="currentColor" viewBox="0 0 640 512">
                      <path
                        d="M38.8 5.1C28.4-3.1 13.3-1.2 5.1 9.2S-1.2 34.7 9.2 42.9l592 464c10.4 8.2 25.5 6.3 33.7-4.1s6.3-25.5-4.1-33.7L525.6 386.7c39.6-40.6 66.4-86.1 79.9-118.4c3.3-7.9 3.3-16.7 0-24.6c-14.9-35.7-46.2-87.7-93-131.1C465.5 68.8 400.8 32 320 32c-68.2 0-125 26.3-169.3 60.8L38.8 5.1zM223.1 149.5C248.6 126.2 282.7 112 320 112c79.5 0 144 64.5 144 144c0 24.9-6.3 48.3-17.4 68.7L408 294.5c8.4-19.3 10.6-41.4 4.8-63.3c-11.1-41.5-47.8-69.4-88.6-71.1c-5.8-.2-9.2 6.1-7.4 11.7c2.1 6.4 3.3 13.2 3.3 20.3c0 10.2-2.4 19.8-6.6 28.3l-90.3-70.8zM373 389.9c-16.4 6.5-34.3 10.1-53 10.1c-79.5 0-144-64.5-144-144c0-6.9 .5-13.6 1.4-20.2L83.1 161.5C60.3 191.2 44 220.8 34.5 243.7c-3.3 7.9-3.3 16.7 0 24.6c14.9 35.7 46.2 87.7 93 131.1C174.5 443.2 239.2 480 320 480c47.8 0 89.9-12.9 126.2-32.5L373 389.9z"
                      />
                    </svg>
                    Hide Answers
                  </button>
                  <button
                    v-else
                    @click="toggleAnswers(question)"
                    type="button"
                    class="hover:text-gray-900"
                  >
                    <svg class="icon w-6 h-6 mr-1" fill="currentColor" viewBox="0 0 576 512">
                      <path
                        d="M288 32c-80.8 0-145.5 36.8-192.6 80.6C48.6 156 17.3 208 2.5 243.7c-3.3 7.9-3.3 16.7 0 24.6C17.3 304 48.6 356 95.4 399.4C142.5 443.2 207.2 480 288 480s145.5-36.8 192.6-80.6c46.8-43.5 78.1-95.4 93-131.1c3.3-7.9 3.3-16.7 0-24.6c-14.9-35.7-46.2-87.7-93-131.1C433.5 68.8 368.8 32 288 32zM144 256a144 144 0 1 1 288 0 144 144 0 1 1 -288 0zm144-64c0 35.3-28.7 64-64 64c-7.1 0-13.9-1.2-20.3-3.3c-5.5-1.8-11.9 1.6-11.7 7.4c.3 6.9 1.3 13.8 3.2 20.7c13.7 51.2 66.4 81.6 117.6 67.9s81.6-66.4 67.9-117.6c-11.1-41.5-47.8-69.4-88.6-71.1c-5.8-.2-9.2 6.1-7.4 11.7c2.1 6.4 3.3 13.2 3.3 20.3z"
                      />
                    </svg>
                    <span v-if="$store.getters.getCurrentUser?.role == 'editor'">Edit Answers</span>
                    <span v-else>Show Answers</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="mb-4 text-center" v-if="$store.getters.getCurrentUser?.role == 'editor'">
            <button
              type="button"
              @click="addQuestion"
              class="px-4 py-2 w-full md:w-auto bg-primary-500 hover:bg-blue-700 text-white rounded-md"
            >
              Add Question
            </button>
          </div>

          <div class="flex justify-between" v-if="$store.getters.getCurrentUser?.role == 'editor'">
            <div>
              <button
                type="button"
                v-if="quiz.id"
                @click="deleteQuiz"
                class="px-4 py-2 border border-gray-300 hover:bg-gray-200 rounded-md"
              >
                Delete
              </button>
            </div>
            <div>
              <button
                type="button"
                @click="cancel"
                class="px-4 py-2 mr-2 bg-white hover:bg-gray-200 rounded-md"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-2 mr-2 bg-primary-500 hover:bg-blue-700 text-white rounded-md"
              >
                Save
              </button>
            </div>
          </div>
          <div v-if="quiz.updated_at" class="mt-2 text-right text-gray-900">
            Last updated {{ getRelativeTimeFromISO(quiz.updated_at) }} by
            <b>{{ quiz.updated_by?.name }}</b>
          </div>
        </main>
      </form>
    </div>

    <ConfirmLeave :unsavedChanges="unsavedChanges" />
  </div>
</template>

<script>
import HeadingView from '@/components/HeadingView.vue'
import ConfirmLeave from '@/components/ConfirmLeave.vue'
import quizAPI from '@/api/quiz.js'
import { getRelativeTimeFromISO, getErrorToast, getSuccessToast } from '@/utilities'

export default {
  components: {
    HeadingView,
    ConfirmLeave
  },
  data() {
    return {
      unsavedChanges: false,
      selectedIndex: null,

      quiz: {},
      quizName: '',
      isDataFetched: false,
      isDataError: false,

      statusOptions: [
        { name: 'Published', value: 'published' },
        { name: 'Draft', value: 'draft' },
        { name: 'Archived', value: 'archived' }
      ],

      getRelativeTimeFromISO
    }
  },
  beforeUnmount() {
    window.removeEventListener('mouseup', this.mouseUpHandler)
  },
  mounted() {
    window.addEventListener('mouseup', this.mouseUpHandler)
    if (this.$route.params.id == 'create') {
      this.isDataFetched = true
      this.quizName = 'New Quiz'
      this.quiz = {
        name: '',
        status: 'draft',
        questions: [{ name: '', order: 1, answers: [] }]
      }

      return
    }

    this.fetchQuiz()
  },
  methods: {
    onValueUpdate() {
      this.unsavedChanges = true
    },
    fetchQuiz() {
      this.isDataError = false
      this.isDataFetched = false
      quizAPI.getQuizById(
        this.$route.params.id,
        (quiz) => {
          this.quiz = quiz
          this.quizName = quiz?.name

          this.quiz.questions.forEach((question) => {
            question._showAnswers = false
            question._answer = ''
          })
        },
        (error) => {
          this.isDataError = true
          console.error(error)
        }
      )
    },
    addQuestion() {
      this.quiz.questions.push({
        name: '',
        order: this.quiz.questions.length + 1,
        answers: [],
        _showAnswers: true,
        _answer: ''
      })
    },
    cancel() {
      this.$router.go(-1)
    },
    onNewAnswer(question) {
      if (question._answer.trim() === '') {
        return
      }

      question.answers.push({
        name: question._answer,
        order: this.quiz.questions.length + 1,
        is_correct: false
      })
      question._answer = ''
      this.onValueUpdate()
    },
    onAnswerChange(question) {
      question.answers = question.answers.filter((answer) => answer.name.trim() !== '')
      this.onValueUpdate()
    },
    copyQuestion(quiz, index) {
      const question = quiz.questions[index]
      quiz.questions.push({
        name: question.name,
        order: quiz.questions.length + 1,
        answers: question.answers.map((answer) => ({ ...answer })),
        _showAnswers: question._showAnswers
      })
      this.onValueUpdate()
    },
    toggleAnswers(question) {
      question._showAnswers = !question._showAnswers
    },
    removeQuestion(quiz, index) {
      quiz.questions.splice(index, 1)
      this.onValueUpdate()
    },
    validateQuiz() {
      if (this.quiz.status === '') {
        this.$store.dispatch('createToast', getErrorToast('Status is required'))
        return false
      }

      if (this.quiz.name.trim() === '') {
        this.$store.dispatch('createToast', getErrorToast('Quiz name is required'))
        return false
      }

      for (const [index, question] of this.quiz.questions.entries()) {
        if (question.name.trim() === '') {
          this.$store.dispatch(
            'createToast',
            getErrorToast(`Question ${index + 1}: Name is required`)
          )
          return false
        }

        if (question.answers.length < 2) {
          this.$store.dispatch(
            'createToast',
            getErrorToast(`Question ${index + 1}: At least two answers are required`)
          )
          return false
        }

        if (!this.hasCorrectAnswer(question)) {
          this.$store.dispatch(
            'createToast',
            getErrorToast(`Question ${index + 1}: At least one correct answer is required`)
          )
          return false
        }

        for (const [aindex, answer] of question.answers.entries()) {
          if (answer.name.trim() === '') {
            this.$store.dispatch(
              'createToast',
              getErrorToast(`Question ${index + 1} Answer ${aindex + 1}: Name is required`)
            )
            return false
          }
        }
      }

      return true
    },
    hasCorrectAnswer(question) {
      return question.answers.some((answer) => answer.is_correct)
    },
    mouseDownHandler(index) {
      this.selectedIndex = index
    },
    mouseUpHandler() {
      this.selectedIndex = null
    },
    mouseMoveHandler(index) {
      if (this.selectedIndex != null && this.selectedIndex != index) {
        this.moveRule(index, this.selectedIndex)
        this.selectedIndex = index
      }
    },
    moveRule(index, newIndex) {
      if (index >= 0 && index <= this.quiz.questions.length - 1) {
        var temp = this.quiz.questions[index]
        this.quiz.questions[index] = this.quiz.questions[newIndex]
        this.quiz.questions[newIndex] = temp
        this.onValueUpdate()
      }
    },
    deleteQuiz() {
      if (confirm('Are you sure you want to delete this quiz?')) {
        quizAPI.deleteQuiz(
          this.quiz.id,
          () => {
            this.$store.dispatch('createToast', getSuccessToast('Quiz deleted'))
            this.$router.go(-1)
          },
          (error) => {
            this.$store.dispatch('createToast', getErrorToast(error))
          }
        )
      }
    },
    saveQuiz() {
      if (!this.validateQuiz()) {
        return
      }

      if (this.$route.params.id == 'create') {
        quizAPI.createQuiz(
          this.quiz,
          () => {
            this.$store.dispatch('createToast', getSuccessToast('Quiz created'))
            this.$router.go(-1)
          },
          (error) => {
            this.$store.dispatch('createToast', getErrorToast(error))
          }
        )
      } else {
        quizAPI.updateQuiz(
          this.$route.params.id,
          this.quiz,
          () => {
            this.$store.dispatch('createToast', getSuccessToast('Quiz saved'))
            this.$router.go(-1)
          },
          (error) => {
            this.$store.dispatch('createToast', getErrorToast(error))
          }
        )
      }
    }
  }
}
</script>
