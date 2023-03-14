<template>
<transition name="fade" appear>
    <navbar></navbar>
</transition>
<i-layout>
    <i-layout vertical class="py-2 pl-2 min-h-screen">
        <i-sidebar @contextmenu="onContextMenu($event)" class="z-50">
            <i-nav vertical >
                <i-nav-item @click="setlayoutcontent('home')">
                    <p class="pointer-events-none">Home</p>
                </i-nav-item>

                <i-collapsible v-if="user.userdata.role == 'admin'" v-model="open">
                    <i-collapsible-item name="Networks" title="Networks">
                        <i-nav-item v-for="network in layouts" :key="network.id" @click="setlayoutcontent(network)">
                          <p class="pointer-events-none text-blue-400">{{ network.id }}</p>
                          <p class="pointer-events-none text-sm text-gray-400">{{ network.config.name }}</p>
                          <p class="pointer-events-none text-sm">{{ network["config"]["ipAssignmentPools"][0] ? getCIDRAddress(network.config.ipAssignmentPools[0].ipRangeStart, network.config.ipAssignmentPools[0].ipRangeEnd) : "" }}</p>
                        </i-nav-item>
                    </i-collapsible-item>
                </i-collapsible>

                <i-nav-item v-if="user.userdata.role == 'admin'" @click="createNetwork">
                  <p class="text-amber-400 pointer-events-none">Create a Network...</p>
                </i-nav-item>
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
            <NetworkSettings v-if="renderComponent" class="p-2" :network="layoutcontent" @delete="deletefromchild" />
        </i-layout-content>
    </i-layout>
</i-layout>

<transition name="slide-fade" appear>
  <logo/>
</transition>


<transition name="slide-fade" appear>
  <i-alert class="w-1/2 absolute inset-x-1/4 top-2" dismissible color="danger" v-if=visibleAlert>
    <template #icon>
        <i-icon name="ink-danger" />
    </template>
    <p>Fehler, beim Speichern des Layouts</p>
  </i-alert>
</transition>


<transition name="slide-fade" appear>
  <i-alert class="w-1/2 absolute inset-x-1/4 top-2" dismissible color="success" v-if=visibleSuccess>
    <template #icon>
        <i-icon name="ink-check" />
    </template>
    <p>Neues Layout wurde Gespeichert</p>
  </i-alert>
</transition>


<context-menu v-model:show="show" :options="optionsComopnent">
    <context-menu-item label="Add Network" @click="createNetwork" />
    <context-menu-item label="Delete Network" @click="deleteNetwork" />
  </context-menu>


</template>

<script setup>
import { ref, onMounted, nextTick } from "vue"
import logo from "@/components/LogoComponet.vue"
import navbar from "@/components/NavBar.vue"
import NetworkSettings from "@/components/NetworkSettings/NetworkSettings.vue"
import { zeroapi } from "@/service/zeroapi.js"
import { UserStore } from "@/stores/user.js"
import { generateNetworkConfig } from "@/components/utils/NetworkConfig"
import { getCIDRAddress } from "@/components/utils/IP";

const user = UserStore()
const layoutcontent = ref("home")
const layouts = ref()
const visibleAlert = ref(false)
const visibleSuccess = ref(false)
const renderComponent = ref(true);
const open = ref()
const show = ref(false)
const aktuell_event = ref()

const optionsComopnent = ref({
        iconFontClass: 'iconfont',
        customClass: "class-a",
        zIndex: 999,
        minWidth: 230,
        x: 500,
        y: 200
      })

      
const forceRerender = async () => {
  // Remove MyComponent from the DOM
  renderComponent.value = false;
	// Wait for the change to get flushed to the DOM
	await nextTick();
	// Add the component back in
  renderComponent.value = true;
};

async function deletefromchild(nwid){
  const req = await zeroapi.delete("network/" + nwid);
    console.log("Action:", req);
    getUserLayouts()
    if (layoutcontent.value.id == nwid){
      layoutcontent.value = "home"
    }
}

async function createNetwork(){
    const network = await zeroapi.post("network", generateNetworkConfig());
    console.log(network);
    getUserLayouts()
  }

const deleteNetwork = async () => {
    const req = await zeroapi.delete("network/" + aktuell_event.value.target.children[0].innerText.trim());
    console.log("Action:", req);
    getUserLayouts()
    if (layoutcontent.value.id == aktuell_event.value.target.children[0].innerText.trim()){
      layoutcontent.value = "home"
    }
  };

function onContextMenu(e) {
      e.preventDefault();
      aktuell_event.value = e
      //Set the mouse position
      optionsComopnent.value.x = e.x;
      optionsComopnent.value.y = e.y;
      //Show menu
      show.value = true;
    }


onMounted(getUserLayouts)

function getUserLayouts(){
  zeroapi.get("network")
  .then((response) => {
    if (response.data.success == 200){
      layouts.value = response.data.data
    }    
  }).catch(function (error) {
    console.log(error)
  })}

function setlayoutcontent(content){
    layoutcontent.value = content
    forceRerender()
}

</script>

