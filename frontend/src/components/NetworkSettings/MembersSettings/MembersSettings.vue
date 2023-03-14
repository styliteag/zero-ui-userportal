<template>
    <i-collapsible-item name="Member settings" title="Member settings" class="z-[999]">
        <div class="grid grid-cols-1 gap-y-6" v-if="loaded">
            <div class="place-self-center flex gap-x-6">
                <i-tooltip>
                    <button @click="fetchData" ><i-icon name="ink-info" class="_color:warning" /></button>
                    <template #body>Reload Members</template>
                </i-tooltip>
                <i-tooltip>
                    <button @click="copyToClipboard()" ><svg-icon class="_color:warning" :fa-icon="faCopy" size="16"></svg-icon></button>
                    <template #body>Copy Network ID</template>
                </i-tooltip>
            </div>

            <div v-if="members.length != 0">
                <i-input type="text" placeholder="Search..." v-model="searchQuery" class="static mb-3"></i-input>
                <i-table color="dark" class="pt-2 ">
                    <thead >
                    <tr>
                        <th class="rounded-tl-lg">#</th>
                        <th>Authorized</th>
                        <th>Address</th>
                        <th>Name / Description</th>
                        <th>Managed IPs</th>
                        <th>Time to Live</th>
                        <th>Peer status</th>
                        <th>Physical IP / Latency</th>
                        <th class="rounded-tr-lg"></th>
                    </tr>
                    </thead>
                    <tbody v-for="member, index in filterdMembers" :key="index">
                    <tr>
                        <th class="_vertical-align:middle" scope="row"><DeleteMember :member=member @deletemember='sendDeleteReq(member)'/></th>
                        <td class="_vertical-align:middle"><i-checkbox class="pl-8" color="light" size="lg" v-model="member.config.authorized" @update:modelValue='sendReq(member)'/></td>
                        <td class="_vertical-align:middle"><p>{{ member.config.address }}</p></td>
                        <td class="flex flex-col">
                            <i-input v-model="member.name" placeholder="Name" @update:modelValue='sendReq(member)'/>
                            <i-input v-model="member.description" placeholder="Description" @update:modelValue='sendReq(member)'/>
                        </td>
                        <td class="w-48"><ManagedIP :member=member @change='sendReq(member)'/></td>
                        <td class="_vertical-align:middle"><p>{{ member.timetolive }}</p></td>
                        <td class="_vertical-align:middle">
                            <div v-if="member.online === 0">
                                <p class="text-red-700 text-xl font-bold">OFFLINE</p>
                            </div>
                            <div v-else-if="member.online === 1">
                                <p class="text-green-500 text-sm">ONLINE (v{{ member.config.vMajor }}.{{ member.config.vMinor }}.{{ member.config.vRev }})</p>
                            </div>
                            <div v-else>
                                <p class="text-orange-500 text-sm">RELAYED (v{{ member.config.vMajor }}.{{ member.config.vMinor }}.{{ member.config.vRev }})</p>
                            </div>
                        </td>
                        <td class="_vertical-align:middle">
                            <p v-if="member.physicalAddress">{{member.physicalAddress}} / {{member.physicalPort}}
                            <br />
                            {{member.latency}} ms
                            </p>
                        </td>
                        <td class="_vertical-align:middle">
                            <TagMember :member=member :network=network @change='sendReq(member)'/>
                        </td>
                    </tr>
                    </tbody>
                </i-table>
            </div>
            <div v-else class="text-center align-middle">
                <p class="text-4xl">No devices have joined this network. Use the app on your devices to join {{ network.id }}.</p>
            </div>
        </div>
        <i-loader v-else color="primary" />
    </i-collapsible-item>
</template>
<script setup>
import { ref, defineEmits, defineProps, nextTick, onMounted, watch,  onUnmounted } from "vue";
import { zeroapi } from "@/service/zeroapi.js"

import { faCopy } from "@fortawesome/free-solid-svg-icons";

import ManagedIP from "./components/ManagedIP.vue"
import DeleteMember from "./components/DeleteMember.vue";
import TagMember from "./components/TagMember.vue"

const renderComponent = ref(true)
/* eslint-disable */
const network = ref(props.network)
const members = ref(0)
const searchQuery = ref("")
const filterdMembers = ref()
const loaded = ref(false)

const emit = defineEmits(["sendrequest"])

const props = defineProps({
    network : Object,
})

const getmembersIntervall = setInterval(function(){fetchData()}, 10000)
onMounted(fetchData)
onMounted(function(){getmembersIntervall})
onUnmounted(function(){clearInterval(getmembersIntervall)})

watch(searchQuery, async () => {
    filterdMembers.value = members.value.filter((member) => (member.config.id.toLowerCase().indexOf(searchQuery.value.toLowerCase()) != -1))
})


function copyToClipboard(){
  let textToCopy = network.value.id;

  // text area method
  let textArea = document.createElement("textarea");
  textArea.value = textToCopy;
  textArea.style.position = "fixed";
  textArea.style.left = "-999999px";
  textArea.style.top = "-999999px";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  return new Promise((res, rej) => {
    document.execCommand("copy") ? res() : rej();
    textArea.remove();
  });
}

async function fetchData(){
    try {
      const req = await zeroapi.get("network/" + network.value["config"]["id"] + "/member");
      members.value = req.data.data
      filterdMembers.value = req.data.data
      forceRerender()
      loaded.value = true
    } catch (err) {
      console.error(err);
    }
}

async function sendDeleteReq(member){
    try {
      await zeroapi.delete("network/" + network.value["config"]["id"] + "/member/" + member["config"]["id"]);
      forceRerender()
      fetchData()
    } catch (err) {
      console.error(err);
    }
}

async function sendReq(member){
    try {
        console.log(member.config)
      await zeroapi.post("network/" + network.value["config"]["id"] + "/member/" + member["config"]["id"], member);
      forceRerender()
    } catch (err) {
      console.error(err);
    }
}

/* eslint-disable */
const forceRerender = async () => {
  // Remove MyComponent from the DOM
  renderComponent.value = false;
	// Wait for the change to get flushed to the DOM
	await nextTick();
	// Add the component back in
  renderComponent.value = true;
};
</script>
