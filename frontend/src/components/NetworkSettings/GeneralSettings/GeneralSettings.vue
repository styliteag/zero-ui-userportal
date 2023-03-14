<template>
    <i-collapsible-item name="General settings" title="General settings">
        <div class="grid grid-cols-1 gap-y-6">
            <div>
                <p class="text-3xl">Network ID</p>
                <p>{{ network.id }}</p>
                <div class="pt-2">
                    <i-input v-model="network.config.name" @change='emit("sendrequest")' clearable placeholder="Type something.." />
                    <i-textarea v-model="network.description" @change='emit("sendrequest")' clearable placeholder="Type something.." />
                </div>
            </div>
            <div>
                <p class="text-3xl">Access Control</p>
                <div class="flex pt-2">
                    <i-toggle v-model="network.config.private" size="lg" @change='emit("sendrequest")'></i-toggle>
                    <p v-if="network.config.private == true">Public</p>
                    <p v-else-if="network.config.private == false">Private</p>
                </div>
            </div>
            <div v-if="renderComponent">
                <ManagedRoutes :routes="network.config.routes" @change='emit("sendrequest")' />
            </div>
            <div>
                <IPv4AutoAssign :ipAssignmentPools="network.config.ipAssignmentPools" @change='emit("sendrequest")' @custom="setDefaultRoute" />
            </div>
            <div>
                <p class="pb-2">Multicast Recipient Limit</p>
                <i-number-input v-model="network.config.multicastLimit" @update:modelValue='emit("sendrequest")' :min="1" :max="255" placeholder="Enter a number.." />
            </div>
            <div>
                <i-checkbox v-model="network.config.enableBroadcast" @update:modelValue='emit("sendrequest")' size="lg">Enable Broadcast</i-checkbox>
            </div>
            <div>
                <p class="pb-2">Maximum Transmission Unit</p>
                <i-number-input v-model="network.config.mtu" @update:modelValue='emit("sendrequest")' :min="1" placeholder="Enter a number.." />            </div>
        </div>    
    </i-collapsible-item>
</template>
<script setup>
import { ref, defineEmits, defineProps, nextTick } from "vue";
import ManagedRoutes from "./components/ManagedRoutes";
import IPv4AutoAssign from "./components/IPv4AutoAssign";

const renderComponent = ref(true)
const network = ref(props.network)

const emit = defineEmits(["sendrequest"])

const props = defineProps({
    network : Object,
})

function setDefaultRoute(cidr){
    network.value.config.routes = cidr
    forceRerender()
}

const forceRerender = async () => {
  // Remove MyComponent from the DOM
  renderComponent.value = false;
	// Wait for the change to get flushed to the DOM
	await nextTick();
	// Add the component back in
  renderComponent.value = true;
};
</script>