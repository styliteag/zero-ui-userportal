<template>
    <div class="pt-2">
        <i-tooltip  placement="left">
        <button @click="visible = true" ><svg-icon class="_color:warning" :fa-icon="faWrench" size="16"></svg-icon></button>
        <template #body>Member {{ member.config.address }} Settings</template>
    </i-tooltip>
    </div>

<i-modal v-model="visible" color="" transition="fade-in-transition" class="z-[999] rounded-lg">
    <template #header>
        <p>Member {{ member.config.address }} Settings</p>
    </template>
    <div>
        <i-checkbox v-model="member.config.activeBridge" color="light" size="md" @change="emit('change')"><p class="text-white">Allow Ethernet Bridging</p></i-checkbox>
        <i-checkbox v-model="member.config.noAutoAssignIps" color="light" size="md" @change="emit('change')"><p class="text-white">Do Not Auto-Assign IPs</p></i-checkbox>
    </div>
    <div class="flex flex-col pt-6 justify-center">
        <p class="text-xl">Capabilities</p>
            <div v-if="Object.entries(network.capabilitiesByName || []).length != 0">
                <i-checkbox-group v-model="member.config.capabilities" @update:modelValue=onCheckboxChange color="light" class="flex py-6 gap-y-2">
                    <i-checkbox  v-for="entry in Object.entries(network.capabilitiesByName)" :key="entry[0]" :value="entry[1]" color="light" size="md"><p class="text-white">{{ entry[0] }}</p></i-checkbox>
                </i-checkbox-group>
            </div>
            <p v-else class="py-6">No capabilities defined</p>

        <p class="text-xl">Tags</p>
            <div v-if="Object.entries(network.tagsByName || []).length != 0" class="flex flex-wrap gap-4 pt-4 pb-4">
                <div v-for="tag in Object.entries(network.tagsByName)" :key="tag[0]">
                    <div v-if=renderComponent>
                        <TagItem v-if="!isTagPresent(tag[1])" :tag="tag[1]" :tagname="tag[0]" :member=member :network=network @change=onTagChange />
                        <TagItemPresent v-else :tag="tag[1]" :tagname="tag[0]" :member=member @change=onTagChange />
                    </div>
                </div>
            </div>
            <p v-else>No tags defined</p>
        <i-button color="primary" @click="visible = false">
            Exit
        </i-button>
    </div>

</i-modal>
</template>
        
<script setup>
import { defineProps, ref, defineEmits, nextTick } from 'vue';
import { faWrench } from "@fortawesome/free-solid-svg-icons";
import { zeroapi } from "@/service/zeroapi.js"
import TagItem from './components/TagItem.vue';
import TagItemPresent from './components/TagItemPresent.vue'
//
// eslint-disable-next-line
const member = ref(props.member)
const network = ref(props.network)
const visible = ref(false)
const renderComponent = ref(true)


const props = defineProps({
    member : Object,
    network: Object
})
// eslint-disable-next-line
const emit = defineEmits(['change'])

async function sendReq () {
    try {
      await zeroapi.post("network/" + network.value["config"]["id"] + "/member/" + member.value["config"]["id"], member.value);
    } catch (err) {
      console.error(err);
    }
}

function isTagPresent (tagitem) {
    for (const tag in member.value.config.tags){
        if (tagitem.id == member.value.config.tags[tag][0]){
            return true
        }
    }
}

function onCheckboxChange () {
    sendReq()
}

function onTagChange () {
    sendReq()
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