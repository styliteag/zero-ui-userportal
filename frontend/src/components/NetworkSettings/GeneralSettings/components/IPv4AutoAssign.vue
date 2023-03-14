<template>
    <p>IPv4 Auto-Assign</p>
    <div class="flex flex-wrap gap-3 justify-center pt-2">
        <div v-for="address, index in addressPool" :key="index" >
            <i-button color="primary" class="w-80" @click=setDefaultPool(index)>{{ address.name }}</i-button>
        </div>
    </div>
    <p class="pt-2">Auto-Assign Pools</p>
    <i-table color="dark" class="pt-2">
        <thead>
        <tr>
            <th>#</th>
            <th>Start</th>
            <th>End</th>
        </tr>
        </thead>
        <tbody v-for="ipAssignment, index in ipAssignmentPools" :key="index">
        <tr>
            <th scope="row"><button><i-icon @click="removePoolReq(index)" name="ink-times" class="text-red-900 mt-1" /></button></th>
            <td>{{ipAssignment.ipRangeStart}}</td>
            <td>{{ipAssignment.ipRangeEnd}}</td>
        </tr>
        </tbody>
    </i-table>
    <p class="pt-2">Add IPv4 Pool</p>
    <div class="pt-2">
        <i-row >
            <i-column xs="4"><i-input v-model="start" placeholder="Start" /></i-column>
            <i-column xs="4"><i-input v-model="end" placeholder="End" /></i-column>
            <i-column class="self-center -ml-4"><button><i-icon name="ink-plus" @click="addPoolReq(start, end)" class="_color:success" /></button></i-column>
        </i-row>
    </div>

</template>
        
<script setup>
import { defineProps, ref } from 'vue';
/* eslint-disable */
import { getCIDRAddress, validateIP, normilizeIP } from "@/components/utils/IP";
import { addressPool } from "@/components/utils/NetworkConfig";
    
const ipAssignmentPools = ref(props.ipAssignmentPools)
const start = ref()
const end = ref()

      
const props = defineProps({
    ipAssignmentPools : Object,
    })
    
const emit = defineEmits(['change', 'custom'])

function setDefaultPool(index){
    addPoolReq(addressPool[index]["start"], addressPool[index]["end"], true);

    emit("custom", [{"target" : getCIDRAddress(
          addressPool[index]["start"],
          addressPool[index]["end"]
        )}]);
  };

function removePoolReq(index){
    ipAssignmentPools.value.splice(index, 1);

    emit("change");
  };

function addPoolReq(localStart, localEnd, reset = false){
    let data = {};
    if (validateIP(localStart) && validateIP(localEnd)) {
      data["ipRangeStart"] = normilizeIP(localStart);
      data["ipRangeEnd"] = normilizeIP(localEnd);
    } else {
      return;
    }

    ipAssignmentPools.value.push(data);
    emit("change");
  };
    

     
</script>