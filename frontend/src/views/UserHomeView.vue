<template>
<transition name="fade" appear>
    <navbar></navbar>
</transition>
<i-layout>
    <i-layout vertical class="py-2 pl-2 min-h-screen">
        <i-sidebar @contextmenu="onContextMenu($event)" class="z-50">
            <i-nav vertical >
                <i-nav-item @click="setlayoutcontent('home')">
                    <p class="pointer-events-none">User Home</p>
                </i-nav-item>

                <i-collapsible v-model="open">
                    <i-collapsible-item name="Networks" title="Networks" v-if="renderComponent">
                        <i-nav-item v-for="networkname in Object.keys(layouts)" :key="networkname" @click="setlayoutcontent(networkname, layouts[networkname])">
                          <p class="pointer-events-none text-blue-400">{{ networkname }}</p>
                        </i-nav-item>
                    </i-collapsible-item>
                </i-collapsible>
            </i-nav>
        </i-sidebar>

        <i-layout-content v-if="layoutcontent == 'home'" class="flex flex-col h-full mx-2 border-2 border-notsodark-500 rounded-lg text-center items-center">
            <p class="text-3xl">Herzlich Willkommen</p>
            <div class="flex text-3xl gap-2 mb-1">
              <p class="underline">{{ user.userdata.username }}</p>
              <p>deine Rolle ist</p>
              <p class="underline">{{ user.userdata.role }}</p>
            </div>
        </i-layout-content>

        <i-layout-content name="layoutmulti" v-if="layoutcontent != 'home'"  class="h-sceen w-screen border-2 border-notsodark-500 rounded-lg relative mx-2">
            <UserMemberSettings v-if="renderComponent" class="p-2" :network="layoutcontent" :networkname="layoutcontentname" @auth="authMember" @deauth="deauthMember" />
        </i-layout-content>
    </i-layout>
</i-layout>

<transition name="slide-fade" appear>
  <logo/>
</transition>


</template>

<script setup>
import { ref, onMounted, nextTick } from "vue"
import logo from "@/components/LogoComponet.vue"
import navbar from "@/components/NavBar.vue"
import UserMemberSettings from "@/components/UserMemberSettings/UserMemberSettings.vue"
import { zeroapi } from "@/service/zeroapi.js"
import { UserStore } from "@/stores/user.js"

const user = UserStore()
const layoutcontent = ref("home")
const layoutcontentname = ref("")
const layouts = ref({})
const renderComponent = ref(true);
const open = ref()

      
const forceRerender = async () => {
  // Remove MyComponent from the DOM
  renderComponent.value = false;
	// Wait for the change to get flushed to the DOM
	await nextTick();
	// Add the component back in
  renderComponent.value = true;
};


onMounted(getUserLayouts)

function getUserLayouts(){
  zeroapi.get("user-managment/member/" + user.userdata.username)
  .then((response) => {
    if (response.data.success == 200){
      layouts.value = response.data.data
    }    
  }).catch(function (error) {
    console.log(error)
  })
  forceRerender()
}

async function deauthMember(mid){
    await zeroapi.post("network/" + layoutcontentname.value + "/member/" + mid, layoutcontent.value);
  }


async function authMember(nwid, mid, reason, time){
    await zeroapi.post("user-managment/member/" + user.userdata.username + "/reason", {"nwid" : nwid, "mid" : mid, "reason": reason.value, "duration": time.value});
    await zeroapi.post("network/" + layoutcontentname.value + "/member/" + mid, layoutcontent.value);
    getUserLayouts()
    forceRerender()
  }

function setlayoutcontent(name, content){
    layoutcontentname.value = name
    layoutcontent.value = content
    forceRerender()
}
</script>

