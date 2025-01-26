import bootstrap from 'bootstrap/dist/js/bootstrap.bundle'
import { defineNuxtPlugin } from 'nuxt/app'

export default defineNuxtPlugin(nuxtApp => {
  nuxtApp.provide('bootstrap', bootstrap)
})
