<template>
<i-layout>
    <i-layout-header class="text-center">
        <p class="text-4xl">{{ network.id }}</p>
        <p class="text-2xl italic">{{ network.config.name }}</p>
    </i-layout-header>

    <i-layout-content>
        <i-collapsible v-model="open">
            <GeneralSettings   :network="network" @sendrequest="sendReq" />
            <MembersSettings   :network="network" @sendrequest="sendReq" />
            <NetworkRulesVue   :network="network" @sendrequest="sendReqwithAlert" />
            <NetworkManagement :network="network" @sendrequest="emit('delete', network.id)"/>
        </i-collapsible>
    </i-layout-content>

<i-alert color="success" v-show="success" class="left-1/2 transform -translate-x-1/2 absolute">
    <template #icon>
        <i-icon name="ink-check" />
    </template>
    <p>Deine Daten wurden an den Zerotier Controller Übermittelt</p>
</i-alert>

<i-alert color="danger" v-show="failure" class="left-1/2 transform -translate-x-1/2 absolute">
    <template #icon>
        <i-icon name="ink-warning" />
    </template>
    <p>Fehler Bitte Überprüfe deinen Zerotier Controller</p>
</i-alert>

</i-layout>




</template>

<script setup>
import { defineProps, ref, nextTick, defineEmits } from 'vue';
import { zeroapi } from "@/service/zeroapi.js"

import GeneralSettings from "./GeneralSettings/GeneralSettings.vue"
import MembersSettings from "./MembersSettings/MembersSettings.vue"
import NetworkRulesVue from './NetworkRules/NetworkRules.vue';
import NetworkManagement from './NetworkManagement/NetworkManagement.vue'


const network = ref(props.network)
const open = ref()
const renderComponent = ref(true);
const success = ref(false)
const failure = ref(false)


const emit = defineEmits(["delete"])
const props = defineProps({
    network : Object,
})

const forceRerender = async () => {
  // Remove MyComponent from the DOM
  renderComponent.value = false;
	// Wait for the change to get flushed to the DOM
	await nextTick();
	// Add the component back in
  renderComponent.value = true;
};

async function sendReq(){
    try {
      await zeroapi.post("network/" + network.value["config"]["id"], network.value);
      forceRerender()
    } catch (err) {
      console.error(err);
      failure.value = true
      setTimeout(function(){failure.value = false}, 7000);
    }
}

async function sendReqwithAlert(){
    try {
      await zeroapi.post("network/" + network.value["config"]["id"], network.value);
      success.value = true
      setTimeout(function(){success.value = false}, 7000);
      forceRerender()
    } catch (err) {
      console.error(err);
      failure.value = true
      setTimeout(function(){failure.value = false}, 7000);
    }
}

</script>