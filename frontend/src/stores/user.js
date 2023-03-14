import { defineStore } from "pinia";
import { ref, computed } from "vue"
 /* eslint-disable */

export const UserStore = defineStore('user', () => {
  const isAuth = ref(false)
  const userdata = ref({username : "demo", role: "demo", token: "demo", usericon: "default-avatar.svg"})

  const isLoggedIn = computed(() => isAuth.value)

  function authorize() {
    isAuth.value = true
  }

  function deauthorize() {
    isAuth.value = false
  }

  return { isAuth, userdata, isLoggedIn, authorize, deauthorize}
})
