<template>
    <div class="bg-[url('@/assets/images/background/bg3.jpg')] -z-10 fixed w-full h-full bg-cover bg-no-repeat bg-center"></div>
    <div id="welcome-page" class="flex items-center justify-center">
      <div class="text-left  bg-white backdrop-filter border-8 px-10 py-8 mt-8 rounded-3xl">
        <div class="text-center text-notsodark-900">
          <transition name="fade" :duration="700" appear>
            <div class="flex justify-center" style="transition-delay: 0.3s">
              <img :src="require('@/assets/images/logo/bottom_brand.svg')" class="w-32"/>
            </div>
          </transition>
          <transition name="fade" :duration="700" appear>
            <h2 class="text-4xl mb-2 font-bold text-center " style="transition-delay: 0.6s">
              Welcome to Blodåre Tre IpsecViewer
            </h2>
          </transition>
          <transition name="fade" :duration="1500" appear>
            <h2 class="text-3xl mb-5 text-center" style="transition-delay: 0.9s">
              Let's Start!
            </h2>
          </transition>
          <transition name="fade" :duration="1600" appear>
            <router-link to="/login">
            <i-button color="primary"  class="mt-2 font-bold rounded-full" style="transition-delay: 1.4s">
                Go →
            </i-button>
            </router-link>
          </transition>
        </div>
      </div>

    </div>
  </template>
<script setup>

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
</style>