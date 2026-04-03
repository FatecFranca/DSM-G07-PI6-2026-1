<template>
  <transition name="fade">
    <div
      id="toast-warning"
      class="fixed right-5 top-20 z-50 flex items-center w-full max-w-xs p-4 text-gray-500 bg-white rounded-lg shadow"
      role="alert"
      v-if="isVisible"
    >
      <div
        class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-orange-500 bg-orange-100 rounded-lg"
      >
        <svg
          class="w-5 h-5"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-4a1 1 0 0 1-2 0V6a1 1 0 0 1 2 0v5Z"
          />
        </svg>
        <span class="sr-only">Warning icon</span>
      </div>
      <div class="ms-3 text-sm font-normal">{{ message }}</div>
      <button
        type="button"
        class="ms-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8"
        data-dismiss-target="#toast-warning"
        aria-label="Close"
        @click="hideToast"
      >
        <span class="sr-only">Close</span>
        <svg
          class="w-3 h-3"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 14 14"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
          />
        </svg>
      </button>
    </div>
  </transition>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'ToastWarningComponent',
  props: {
    message: {
      type: String,
      required: true
    }
  },
  setup() {
    const isVisible = ref(false)

    const showToast = () => {
      isVisible.value = true
    }
    const hideToast = () => {
      isVisible.value = false
    }

    return {
      isVisible,
      hideToast,
      showToast
    }
  }
})
</script>

<style scoped lang="scss">
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}
</style>
