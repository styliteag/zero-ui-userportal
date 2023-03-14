<template>
<div class="bg-dark px-2 pt-1 -z-10 static w-full h-full bg-cover bg-no-repeat bg-center">
  <div class="relative bg-notsodark-900 rounded-lg border-2 h-20 border-notsodark-500 w-full grid grid-cols-3 gap-4 drop-shadow-x items-center justify-center py-2">
    <img class="h-16 pl-8 hover:cursor-pointer" :src="require(`@/assets/images/logo/zerotiericon.png`)" @click="router.push('/home')"/>
    <div class="h-fit text-center text-2xl md:text-3xl col-start-2">
          <p class="text-white">{{$route.name[0].toUpperCase() + $route.name.substring(1)}}</p>
      </div>
      <div class="col-start-3 place-self-end self-center mr-8 font-bold">
        <i-dropdown>
          <i-button class="place-end  overflow-hidden" circle size="lg"><img :src="loadImage(user.userdata.usericon)" class="h-full"/></i-button>
          <template #body>
              <i-dropdown-item :to="{ name: 'home' }">Home</i-dropdown-item>
              <i-dropdown-item :to="{ name: 'settings' }">Settings</i-dropdown-item>
              <i-dropdown-item>About</i-dropdown-item>
              <i-dropdown-divider />
              <i-dropdown-item :to="{ name: 'login' }" @click="user.deauthorize"><p class="text-red-600">Logout</p></i-dropdown-item>
          </template>
        </i-dropdown>
      </div>
  </div>
</div>
</template>

<script setup>
import { UserStore } from "@/stores/user.js"
import router from '@/router'


const user = UserStore()

function loadImage(filename){
    let img;
    try {
        img = require(`@/assets/images/account/${filename}`)
    } catch (error) {
	try {
          if (filename.includes("http")){
              img = filename
          }
          else{
              img = require(`@/assets/images/account/default-avatar.svg`)
          }
	} catch (error) {
            img = require(`@/assets/images/account/default-avatar.svg`)
	}
    }
    return img
}

</script>

