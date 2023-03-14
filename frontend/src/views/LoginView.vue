<template>
<div class="bg-dark -z-10 fixed pt-1 px-2 w-full h-full bg-cover bg-no-repeat bg-center text-center">
  <div class="relative bg-notsodark-900 rounded-lg overflow-hidden border-2 h-20 border-notsodark-500 w-full grid grid-cols-3 gap-4 drop-shadow-x items-center justify-center py-2">  
      <img class="place-start h-16 pl-4" :src="require(`@/assets/images/logo/zerotier.png`)" />
      <div class="text-center h-fit text-2xl md:text-3xl col-start-2">
          <p class="text-white">Login Page</p>
      </div>
      <div class="col-start-3 place-self-end pr-4 self-center">
          <i-button color="info" @click="visibleModal = true">
              <p class="text-black font-bold"> Login </p>
          </i-button>
      </div>
  </div>
  <p class="text-2xl pt-32">ZeroVUI - ZeroTier Controller Web VUI - is a web user interface for a self-hosted ZeroTier network controller.</p>
</div>

<i-modal v-model="visibleModal">
    <template #header>
        <p class="font-bold text-2xl"> Login </p>
    </template>
    <i-form @submit="onSubmit">
          <i-form-group>
              <i-form-label>Username</i-form-label>
              <i-input v-model="username" placeholder="username" />
          </i-form-group>

          <i-form-group>
              <i-form-label>Password</i-form-label>
              <i-input v-model="password" type="password" placeholder="password" />
          </i-form-group>

          <i-form-group class="flex gap-x-4 justify-center relative">
            <i-button type="submit" color="success">
              Submit
            </i-button>
          </i-form-group>
    </i-form>
</i-modal>

<transition name="slide-fade" appear>
  <i-alert class="w-1/2 absolute inset-x-1/4 top-2" dismissible color="danger" v-if=visibleAlert>
    <template #icon>
        <i-icon name="ink-danger" />
    </template>
    <p>Fehler, Bitte Überprüfe deine Zugangsdaten</p>
  </i-alert>
</transition>

<transition name="slide-fade" appear>
  <logo/>
</transition>
</template>



<script setup>
import { ref } from "vue"
import { zeroapi } from "@/service/zeroapi.js"
import router from '@/router'
import { UserStore } from "@/stores/user.js"

import logo from "@/components/LogoComponet.vue"


const visibleModal = ref(false)
const visibleAlert = ref(false)
const password = ref()
const username = ref()
const user = UserStore()

function onSubmit(){
  visibleModal.value = false
  visibleAlert.value = false
  zeroapi.post("/auth/login", {"username" : username.value, "password" : password.value})
  .then((response) => {
    if (response.data.success == 200){
      user.authorize()
      user.userdata = response.data.data
      if(user.userdata.role != "admin"){
        console.log("Welcome "+ user.userdata.username)
        router.push({ name: 'userhome', params: { userId: user.userdata.username } })
      }
      else{
        router.push({ name: 'home', params: { userId: user.userdata.username } })
      }
      
    }
    else{

      visibleAlert.value = true
      setTimeout(function(){visibleAlert.value = false}, 7000);
    }
    
  }).catch(function (error) {
    console.log(error)
    visibleAlert.value = true
      setTimeout(function(){visibleAlert.value = false}, 7000);
  })
  
}

</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>
