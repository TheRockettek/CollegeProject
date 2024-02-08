<template>
  <div class="fixed top-6 right-6 space-y-3 z-50">
    <transition-group
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="translate-x-1 opacity-0"
      enter-to-class="translate-x-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-x-0 opacity-100"
      leave-to-class="translate-x-1 opacity-0"
    >
      <div v-for="toast in $store.getters.getToasts" v-bind:key="toast.id">
        <div
          id="toast-default"
          class="flex items-center w-full max-w-xs p-4 text-gray-500 border border-gray-300 bg-white dark:bg-secondary-dark dark:text-white rounded-lg shadow-sm"
          role="alert"
        >
          <svg v-if="toast.success" :class="[toast.class || 'bg-blue-100 text-blue-500', 'p-2 rounded-lg w-4 h-4']" fill="currentColor" viewBox="0 0 384 512"><path d="M326.6 166.6L349.3 144 304 98.7l-22.6 22.6L192 210.7l-89.4-89.4L80 98.7 34.7 144l22.6 22.6L146.7 256 57.4 345.4 34.7 368 80 413.3l22.6-22.6L192 301.3l89.4 89.4L304 413.3 349.3 368l-22.6-22.6L237.3 256l89.4-89.4z"/></svg>
          <svg v-else :class="[toast.class || 'bg-blue-100 text-blue-500', 'p-2 rounded-lg w-4 h-4']" fill="currentColor" viewBox="0 0 448 512"><path d="M447.9 142.5l-23.2 22L181 395.3l-22 20.8-22-20.8L23.2 287.6 0 265.6l44-46.5 23.2 22L159 328 380.7 118l23.2-22 44 46.5z"/></svg>
          <div class="mx-5 text-sm font-normal flex-1 capitalize">
            {{ toast.title }}
          </div>
          <button
            type="button"
            class="-mx-1.5 bg-white dark:bg-secondary-light text-gray-500 dark:text-white dark:hover:text-white hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 dark:focus:ring-secondary-light p-1.5 hover:bg-gray-100 dark:hover:bg-primary inline-flex h-8 w-8"
            data-dismiss-target="#toast-default"
            @click="hideToast(toast.id)"
            aria-label="Close"
          >
            <span class="sr-only">Close</span>
            <svg class="icon w-4 h-4" fill="currentColor" viewBox="0 0 384 512">
              <path
                d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"
              />
            </svg>
          </button>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script>
export default {
  methods: {
    hideToast(toastID) {
      this.$store.dispatch('removeToast', toastID)
    }
  }
}
</script>
