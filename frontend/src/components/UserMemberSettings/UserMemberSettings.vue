<template>
<i-layout>
    <i-layout-header class="text-center">
        <p class="text-4xl">{{ props.networkname }}</p>
    </i-layout-header>

    <i-layout-content class="grid grid-cols-2 gap-4 pt-8">
        <MemberVue v-for="member in network" :key="member" :member="member" @authorize="authMember" @deauthorize="deauthMember" />
    </i-layout-content>

<i-alert color="success" v-show="success" class="left-1/2 transform -translate-x-1/2 absolute">
    <template #icon>
        <i-icon name="ink-check" />
    </template>
    <p>Deine Daten wurden an den Zerotier Controller Übermittelt</p>
</i-alert>
</i-layout>




</template>

<script setup>
import { defineProps, ref, defineEmits } from 'vue';
import MemberVue from "./components/MemberVue.vue"

const network = ref(props.network)
const success = ref(false)

/* eslint-disable */
const emit = defineEmits(["auth", "deauth"])
const props = defineProps({
    network : Object,
    networkname : String
})

function deauthMember(mid){
    emit("deauth", mid)
}

function authMember(mid, reason, time){
    emit("auth", props.networkname, mid, reason, time)
}

</script>