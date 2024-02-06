import { defineStore } from 'pinia'

export const useToastStore = defineStore({
  id: 'toast',
  state: () => ({
    ms: 0,
    message: '',
    classes: '',
    isVisible: false
  }),
  actions: {
    showToast(ms, message, classes) {
      this.ms = parseInt(ms)
      this.message = message
      this.classes = classes
      this.isVisible = true

      // Animation

      setTimeout(() => {
        this.classes += ' -translate-y-28'
      }, 10)

      setTimeout(() => {
        this.classes = this.classes.replace('-translate-y-28', '')
      }, this.ms - 500)

      // Hide toast notification

      setTimeout(() => {
        this.isVisible = false
      }, this.ms)
    }
  }
})
