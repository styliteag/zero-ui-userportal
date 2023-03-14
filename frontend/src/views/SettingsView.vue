<template>
    <transition name="fade" appear>
        <navbar></navbar>
    </transition>
    <i-layout>
        <i-layout vertical class="py-2 pl-2 min-h-screen">
            <i-sidebar>
                <i-nav vertical>
                    <i-nav-item v-if="self_user.userdata.role == 'admin'" @click="setlayoutcontent('addusersettings')">
                        <p class="pointer-events-none">Add User</p>
                    </i-nav-item>

                    <i-nav-item @click="setlayoutcontent('changeusersettings')">
                        <p class="pointer-events-none">User Settings</p>
                    </i-nav-item>
    
                    <i-nav-item v-if="self_user.userdata.role == 'admin'" @click="setlayoutcontent('delusersettings')">
                      <p class="pointer-events-none">Delete User</p>
                    </i-nav-item>
                    <i-nav-item v-if="self_user.userdata.role == 'admin'" @click="setlayoutcontent('membersettings')">
                      <p class="pointer-events-none">Member Managment</p>
                    </i-nav-item>
                </i-nav>
            </i-sidebar>
            <i-layout-content v-if="layoutcontent == 'addusersettings' && self_user.userdata.role == 'admin'" class="flex flex-col h-full mx-2 py-4 border-2 border-notsodark-500 rounded-lg text-center items-center">
                <p class="text-4xl pb-10">Add User</p>
                <i-form @submit="Submit">
                    <i-form-group>
                        <i-form-label>Username</i-form-label>
                        <i-input v-model="selectedUser.username" placeholder="Type something.." />
                    </i-form-group>

                    <i-form-group>
                        <i-form-label>Password</i-form-label>
                        <i-input v-model="selectedUser.password" placeholder="Type something.." />
                    </i-form-group>

                    <i-form-group>
                        <i-form-label>User Role</i-form-label>
                        <i-radio-group v-model="selectedUser.role">
                            <i-radio value="demo">demo</i-radio>
                            <i-radio value="user">user</i-radio>
                            <i-radio value="admin">admin</i-radio>
                        </i-radio-group>
                    </i-form-group>

                    <i-form-group>
                        <i-form-label>User Icon</i-form-label>
                        <i-input v-model="selectedUser.usericon" placeholder="Type something.." >
                            <template #prepend>
                                <i-button class="place-end  overflow-hidden" disabled circle size="lg"><img :src="loadImage(selectedUser.usericon)" class="h-full"/></i-button>
                            </template>
                        </i-input>
                    </i-form-group>

                    <i-form-group>
                        <i-button type="submit" :loading="loading">
                            Submit
                        </i-button>
                    </i-form-group>
                </i-form>
            </i-layout-content>

            <i-layout-content v-if="layoutcontent == 'changeusersettings'" class="flex flex-col h-full mx-2 py-4 border-2 border-notsodark-500 rounded-lg text-center items-center">
                <p class="text-4xl pb-10">Change User Settings</p>
                <i-form @submit="onSubmit" :disabled="self_user.userdata.role == 'demo'">
                    <i-form-group>
                        <i-form-label>Username</i-form-label>
                        <i-select v-if="self_user.userdata.role == 'admin'" class="pt-2" placeholder="Choose something.." v-model="selectedUser.username" @search="getUsersInformation">
                            <i-select-option v-for="user in users" :key="user" :value=user :label=user />
                        </i-select>
                        <p v-else class="text-xl">{{ self_user.userdata.username }}</p>
                    </i-form-group>

                    <i-form-group v-if="self_user.userdata.role != 'admin'">
                        <i-form-label>Altes Password</i-form-label>
                        <i-input v-model="selectedUser.password" placeholder="Type something.." />
                    </i-form-group>

                    <i-form-group>
                        <i-form-label>Neues Password</i-form-label>
                        <i-input v-model="new_password" placeholder="Type something.." />
                    </i-form-group>

                    <i-form-group>
                        <i-form-label>User Role</i-form-label>
                        <i-radio-group v-model="selectedUser.role">
                            <i-radio value="demo">demo</i-radio>
                            <i-radio value="user">user</i-radio>
                            <i-radio v-show="self_user.userdata.role == 'admin'" value="admin">admin</i-radio>
                        </i-radio-group>
                    </i-form-group>

                    <i-form-group>
                        <i-form-label>User Icon</i-form-label>
                        <i-input v-model="selectedUser.usericon" placeholder="Type something..">
                            <template #prepend>
                                <i-button class="place-end  overflow-hidden" disabled circle size="lg"><img :src="loadImage(selectedUser.usericon)" class="h-full"/></i-button>
                            </template>
                        </i-input>
                    </i-form-group>

                    <i-form-group>
                        <i-button type="submit" :loading="loading">
                            Submit
                        </i-button>
                    </i-form-group>
                </i-form>
            </i-layout-content>

            <i-layout-content v-if="layoutcontent == 'delusersettings' && self_user.userdata.role == 'admin'" class="flex flex-col h-full mx-2 py-4 border-2 border-notsodark-500 rounded-lg text-center items-center">
                <p class="text-4xl pb-10">Delete User Settings</p>
                <i-form @submit="DelSubmit" v-if="renderComponent">
                    <i-form-group>
                        <i-form-label>Username</i-form-label>
                        <i-select class="pt-2" placeholder="Choose something.." v-model="selectedUser.username" @search="getUsersInformation">
                            <i-select-option v-for="user in users" :key="user" :value=user :label=user />
                        </i-select>
                    </i-form-group>

                    <i-form-group>
                        <i-button type="submit" :loading="loading">
                            Submit
                        </i-button>
                    </i-form-group>
                </i-form>
            </i-layout-content>

            <i-layout-content v-if="layoutcontent == 'membersettings' && self_user.userdata.role == 'admin'" class="flex flex-col h-full mx-2 py-4 border-2 border-notsodark-500 rounded-lg text-center items-center">
                <p class="text-4xl pb-10">Member Managment</p>
                <i-form @submit="SubmitMembers" v-if="renderComponent">
                    <i-form-group>
                        <i-form-label class="pt-4">Network</i-form-label>
                        <i-select class="pt-2" placeholder="Choose something.." v-model="network.id" @search="getMemberInformation">
                            <i-select-option v-for="network in networks" :key="network.id" :value=network.id :label=network.id />
                        </i-select>
                        <i-form-label class="pt-4">Username</i-form-label>
                        <i-select class="pt-2" placeholder="Choose something.." v-model="selectedUser.username" @search="getUsersMemberInformation">
                            <i-select-option v-for="user in users" :key="user" :value=user :label=user />
                        </i-select>
                    </i-form-group>

                    <div v-if="selectedUser.username != ''" class="pt-7 pb-6">
                        <i-checkbox-group v-model="rightside" v-if="Object.keys(leftside).length != 0">
                            <i-checkbox v-for="left in leftside" :key="left.config.id" :value="left">{{ left.name || left.config.id }}</i-checkbox>
                        </i-checkbox-group>
                        <p v-else class="text-4xl py-4">No Members available</p>
                    </div>
                    <i-form-group>
                        <i-button type="submit" :loading="loading">
                            Submit
                        </i-button>
                    </i-form-group>
                </i-form>
            </i-layout-content>
        </i-layout>
    </i-layout>
    
    <transition name="slide-fade" appear>
      <logo/>
    </transition>

    <i-alert color="danger" v-if="visibleAlert">
        <template #icon>
            <i-icon name="ink-danger" />
        </template>
        <p>Oh snap! Change a few things up and try submitting again.</p>
    </i-alert>

    <transition name="slide-fade" appear>
        <i-alert class="w-1/2 absolute inset-x-1/4 top-2" dismissible color="success" v-if=visibleSuccess>
            <template #icon>
                <i-icon name="ink-check" />
            </template>
            <p>Anfrage wurde erfolgreich verarbeitet</p>
        </i-alert>
    </transition>

</template>

<script setup>
/* eslint-disable */
import { ref, onMounted, nextTick } from "vue"
import logo from "@/components/LogoComponet.vue"
import navbar from "@/components/NavBar.vue"
import { UserStore } from "@/stores/user.js"
import { zeroapi } from "@/service/zeroapi.js"
import router from '@/router'


const self_user = UserStore()
const users = ref()
const selectedUser = ref({"username" : "", "password" : "", "role" : "", "usericon" : ""})
const layoutcontent = ref("homesettings")
const visibleSuccess = ref(false)
const visibleAlert = ref(false)
const renderComponent = ref(true) 
const loading = ref(false)
const new_password = ref()
const networks = ref()
const network = ref({"id" : ""})
const rightside = ref([])
const uservalue = ref()
const leftside = ref({})

            
onMounted(getUsers)
onMounted(getUserLayouts)
onMounted(usermember)

const forceRerender = async () => {
  // Remove MyComponent from the DOM
  renderComponent.value = false;
	// Wait for the change to get flushed to the DOM
	await nextTick();
	// Add the component back in
  renderComponent.value = true;
};

function usermember(){
    if(self_user.userdata.role != "admin"){
        selectedUser.value = self_user.userdata
    }
}

function getUserLayouts(){
  zeroapi.get("network")
  .then((response) => {
    if (response.data.success == 200){
        networks.value = response.data.data
    }    
  }).catch(function (error) {
    console.log(error)
  })}

function loadImage(filename){
    let img;
    try {
        img = require(`@/assets/images/account/${filename}`)
    } catch (error) {
        if (filename.includes("http")){
            img = filename
        }
        else{
            img = require(`@/assets/images/account/default-avatar.svg`)
        }
    }
    return img
}
            
function setlayoutcontent(content){
    layoutcontent.value = content
}

function getUsers(){
    zeroapi.get("user-managment")
  .then((response) => {
    if (response.data.success == 200){
        users.value = response.data.data
    }    
  })}

function getMemberInformation(){
    zeroapi.get("network/" + network.value.id + "/member")
  .then((response) => {
    if (response.data.success == 200){
        leftside.value = response.data.data
    }    
  })}

function getUsersMemberInformation(){
    zeroapi.get("user-managment/member/" + selectedUser.value.username)
  .then((response) => {
    if (response.data.success == 200){
        uservalue.value = response.data.data
    }    
    isAlreadyInList()
  })}

function isAlreadyInList(){
    for(let index in uservalue.value){

        for(let left in leftside.value){
            for(let index_index in uservalue.value[index]){
                if(leftside.value[left].config.address == uservalue.value[index][index_index].address){
                    rightside.value.push(leftside.value[left]);
                }
            }
            
        }
    }
}




  

function getUsersInformation(){
    zeroapi.get("user-managment/user/" + selectedUser.value.username)
  .then((response) => {
    if (response.data.success == 200){
        console.log(response.data)
        selectedUser.value = response.data.data
    }    
  })}

function onSubmit(){
  loading.value = true
  zeroapi.post("user-managment/modify/" + self_user.userdata.role, {"username" : selectedUser.value.username, "password" : new_password.value, "old_password" : selectedUser.value.password, "usericon": selectedUser.value.usericon, "role": selectedUser.value.role})
  .then((response) => {
    if (response.data.success == 200){
        visibleSuccess.value = true
        setTimeout(function(){visibleSuccess.value = false}, 7000);
        loading.value = false
    }
    else{

      visibleAlert.value = true
      setTimeout(function(){visibleAlert.value = false}, 7000);
    }
    
  }).catch(function (error) {
    console.log(error)
  })
  
}

function Submit(){
  loading.value = true
  zeroapi.post("user-managment/add/" + selectedUser.value.username, {"username" : selectedUser.value.username, "password" : selectedUser.value.password, "usericon": selectedUser.value.usericon, "role": selectedUser.value.role})
  .then((response) => {
    if (response.data.success == 200){
        visibleSuccess.value = true
        setTimeout(function(){visibleSuccess.value = false}, 7000);
        loading.value = false
        selectedUser.value = {"username" : "", "password" : "", "role" : "", "usericon" : ""}
        getUsers()
    }
    else{

      visibleAlert.value = true
      setTimeout(function(){visibleAlert.value = false}, 7000);
    }
    
  }).catch(function (error) {
    console.log(error)
  })
  
}

function SubmitMembers(){
  loading.value = true
  zeroapi.post("user-managment/member/" + selectedUser.value.username, {"right" : rightside.value})
  .then((response) => {
    if (response.data.success == 200){
        visibleSuccess.value = true
        setTimeout(function(){visibleSuccess.value = false}, 7000);
        loading.value = false
        getUsers()
        rightside.value = []
        selectedUser.value = {"username" : "", "password" : "", "role" : "", "usericon" : ""}
        network.value.id = {"id" : ""}
        forceRerender()
    }
    else{

      visibleAlert.value = true
      setTimeout(function(){visibleAlert.value = false}, 7000);
    }
    
  }).catch(function (error) {
    console.log(error)
  })
  
}

function DelSubmit(){
  loading.value = true
  zeroapi.post("user-managment/del/" + selectedUser.value.username)
  .then((response) => {
    if (response.data.success == 200){
        visibleSuccess.value = true
        setTimeout(function(){visibleSuccess.value = false}, 7000);
        loading.value = false
        selectedUser.value = {"username" : "", "password" : "", "role" : "", "usericon" : ""}
        forceRerender()
        getUsers()
        
    }
    else{

      visibleAlert.value = true
      setTimeout(function(){visibleAlert.value = false}, 7000);
    }
    
  }).catch(function (error) {
    console.log(error)
  })
  
}



</script>

<style>
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
